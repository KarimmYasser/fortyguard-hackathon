"""
72-Hour Multi-Day Compounding Heatwave Simulation Engine
Simulates the historic Phoenix July 24-26, 2023 3-day extreme heatwave episode.
Models continuous overnight heat traps, cumulative thermal soak,
and non-linear IEC 60287 soil moisture dryout across 72 hours.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from src.models.thermal import TransformerThermalParams
from src.physics.transformer_thermal import TransformerThermalEngine
from src.physics.soil_cable import SoilCableEngine, SoilCableParameters
from src.physics.urban_canyon import UrbanCanyonEngine
from src.physics.virtual_moisture import VirtualMoistureEngine
from src.physics.economic_model import EconomicEngine
from src.safety.cbf_gate import CBFSafetyGate, ActionType, MitigationAction


class DaySummary(BaseModel):
    """Summary metrics for each 24-hour day of the heatwave."""
    day_number: int
    date: str
    peak_ambient_2m_c: float
    coolest_tile_at_peak_c: float
    intra_aoi_spread_c: float
    end_of_day_soil_resistivity_rho: float
    cable_conductor_peak_c: float
    baseline_peak_hot_spot_c: float
    mitigated_peak_hot_spot_c: float
    baseline_loss_of_life_hours: float
    mitigated_loss_of_life_hours: float


class MultiDaySimulationResult(BaseModel):
    """Result of the full 72-hour multi-day compounding simulation."""
    scenario_name: str
    total_hours: int
    days_summary: List[DaySummary]
    timeline_72h: List[Dict[str, Any]]
    total_baseline_loss_of_life_hours: float
    total_mitigated_loss_of_life_hours: float
    total_avoided_loss_of_life_hours: float
    cumulative_net_avoided_loss_usd: float
    compounding_soil_dryout_factor: float
    scenario_metadata: Dict[str, Any]


class MultiDayHeatwaveEngine:
    """
    Executes continuous multi-day (72-hour) physical simulation with compounding soil dryout.
    """

    def __init__(self, tx_params: Optional[TransformerThermalParams] = None) -> None:
        self.tx_params = tx_params or TransformerThermalParams(rated_mva=25.0)
        self.thermal_engine = TransformerThermalEngine(self.tx_params)
        self.soil_engine = SoilCableEngine()
        self.canyon_engine = UrbanCanyonEngine()
        self.moisture_engine = VirtualMoistureEngine()
        self.economic_engine = EconomicEngine()
        self.safety_gate = CBFSafetyGate(thermal_params=self.tx_params)

    FIXTURE_PATH = (
        Path(__file__).resolve().parents[1]
        / "api"
        / "fixtures"
        / "phoenix_heatwave_2023_72h.json"
    )

    @staticmethod
    def _modelled_load_ratio(hour: int) -> float:
        """Grid load assumption; FortyGuard supplies weather, not SCADA."""
        if 0 <= hour < 7:
            return 0.65
        if 7 <= hour < 12:
            return 0.95
        if 12 <= hour < 17:
            return 1.18
        if 17 <= hour < 22:
            return 1.05
        return 0.75

    def _load_capture(self) -> Dict[str, Any]:
        """Load and strictly validate the frozen live FortyGuard capture."""
        if not self.FIXTURE_PATH.exists():
            raise FileNotFoundError(
                f"72h live capture missing: {self.FIXTURE_PATH}. "
                "Run scripts/regenerate_phoenix_72h_fixture.py."
            )
        capture = json.loads(self.FIXTURE_PATH.read_text(encoding="utf-8"))
        rows = capture.get("hourly_profile_72h") or []
        if len(rows) != 72:
            raise ValueError(f"72h live capture has {len(rows)} rows; expected exactly 72")
        expected = list(range(72))
        actual = [row.get("global_hour") for row in rows]
        if actual != expected:
            raise ValueError("72h live capture hours are missing, duplicated, or out of order")
        if any(not str(row.get("data_source", "")).startswith("fortyguard_live") for row in rows):
            raise ValueError("72h capture contains a row without live FortyGuard provenance")
        return capture

    def generate_72h_boundary_forcing(self) -> List[Dict[str, Any]]:
        """Return measured 24×3 boundary forcing plus an explicit load model."""
        capture = self._load_capture()
        return [
            {
                **row,
                "baseline_load_k": self._modelled_load_ratio(int(row["hour_of_day"])),
            }
            for row in capture["hourly_profile_72h"]
        ]

    def run_72h_simulation(self) -> MultiDaySimulationResult:
        """
        Runs the full 72-hour continuous multi-physics simulation.
        """
        forcing_steps = self.generate_72h_boundary_forcing()

        curr_theta_o_base = 25.0
        curr_theta_w_base = 12.0
        curr_theta_o_mit = 25.0
        curr_theta_w_mit = 12.0

        timeline_72h = []
        days_summary = []

        total_base_life = 0.0
        total_mit_life = 0.0

        soil_moisture = 0.18
        initial_soil_resistivity = self.soil_engine.calculate_soil_thermal_resistivity(soil_moisture)
        final_soil_resistivity = initial_soil_resistivity
        bess_soc = 85.0

        # Derive the canyon boundary from the measured hottest hour instead of
        # importing constants from the separate July 19 benchmark. Wind remains
        # an explicit model assumption because FortyGuard exposes no wind field.
        hottest_boundary = max(forcing_steps, key=lambda row: row["fortyguard_2m_ambient_c"])
        canyon_res = self.canyon_engine.calculate_cooling_derate_factor(
            fortyguard_2m_ambient_c=hottest_boundary["fortyguard_2m_ambient_c"],
            reference_wind_speed_m_s=2.8,
            solar_irradiance_w_m2=hottest_boundary["solar_irradiance_w_m2"],
        )
        eta_cool = canyon_res["cooling_derate_eta_cool"]

        day_base_life = 0.0
        day_mit_life = 0.0
        day_peak_2m = 0.0
        day_coolest_at_peak = 0.0
        day_spread_at_peak = 0.0
        day_peak_base_hs = 0.0
        day_peak_mit_hs = 0.0
        day_peak_cable_tc = 0.0

        for step in forcing_steps:
            gh = step["global_hour"]
            h_day = step["hour_of_day"]
            day_num = step["day_index"]
            t_2m = step["fortyguard_2m_ambient_c"]
            coolest_tile = step["coolest_tile_2m_c"]
            solar = step["solar_irradiance_w_m2"]
            base_k = step["baseline_load_k"]

            # Spread is spatial and must be taken from the same hour as the
            # daily AOI peak, never by subtracting extrema from different hours.
            if t_2m > day_peak_2m:
                day_peak_2m = t_2m
                day_coolest_at_peak = coolest_tile
                day_spread_at_peak = step["intra_aoi_spread_c"]

            # IEC 60287 Compounding Evaporative Soil Moisture Loss
            # Rate increases in afternoon heat and compounds across Day 1 -> 2 -> 3
            evap_rate = 0.0020 * (t_2m / 40.0)
            soil_moisture = max(0.035, soil_moisture - evap_rate)

            rho_soil = self.soil_engine.calculate_soil_thermal_resistivity(soil_moisture)
            final_soil_resistivity = rho_soil
            cable_tc = self.soil_engine.calculate_cable_temperature(
                current_ampacity_ratio=base_k,
                rho_soil=rho_soil,
                ambient_soil_temp_c=32.0 + day_num * 1.2,
            )
            day_peak_cable_tc = max(day_peak_cable_tc, cable_tc)

            # Baseline Step (uncontrolled)
            curr_theta_o_base, curr_theta_w_base, t_eff_base, t_o_base, t_hs_base = self.thermal_engine.step_discrete(
                theta_o_prev=curr_theta_o_base,
                theta_w_prev=curr_theta_w_base,
                t_ambient_2m=t_2m,
                solar_irradiance_w_m2=solar,
                load_k=base_k,
                dt_hours=1.0,
                cooling_derate=eta_cool,
            )
            v_base = self.thermal_engine.arrhenius_aging_factor(t_hs_base)
            day_base_life += v_base
            total_base_life += v_base
            day_peak_base_hs = max(day_peak_base_hs, t_hs_base)

            # Mitigated Step (Thermal Sentinel with BESS + Forced Cooling)
            mit_k = base_k
            forced_cooling = False
            if 6 <= h_day <= 18:
                forced_cooling = True

            if 12 <= h_day <= 17:
                mit_k = max(0.65, base_k - 0.20)
                bess_soc = max(30.0, bess_soc - 7.5)
            elif 0 <= h_day < 6:
                bess_soc = min(85.0, bess_soc + 8.0)

            effective_cooling = eta_cool * (1.35 if forced_cooling else 1.0)
            curr_theta_o_mit, curr_theta_w_mit, t_eff_mit, t_o_mit, t_hs_mit = self.thermal_engine.step_discrete(
                theta_o_prev=curr_theta_o_mit,
                theta_w_prev=curr_theta_w_mit,
                t_ambient_2m=t_2m,
                solar_irradiance_w_m2=solar,
                load_k=mit_k,
                dt_hours=1.0,
                cooling_derate=effective_cooling,
            )
            v_mit = self.thermal_engine.arrhenius_aging_factor(t_hs_mit)
            day_mit_life += v_mit
            total_mit_life += v_mit
            day_peak_mit_hs = max(day_peak_mit_hs, t_hs_mit)

            timeline_72h.append({
                "global_hour": gh,
                "day_number": day_num,
                "date": step["date"],
                "hour_of_day": h_day,
                "time_label": f"D{day_num} {step['time_label']}",
                "fortyguard_2m_ambient_c": t_2m,
                "coolest_tile_2m_c": coolest_tile,
                "tile_peak_2m_c": step["tile_peak_2m_c"],
                "intra_aoi_spread_c": step["intra_aoi_spread_c"],
                "relative_humidity_pct": step["relative_humidity_pct"],
                "wet_bulb_temp_c": step["wet_bulb_temp_c"],
                "cloud_cover_pct": step["cloud_cover_pct"],
                "solar_irradiance_w_m2": solar,
                "boundary_data_source": step["data_source"],
                "baseline_load_k": base_k,
                "soil_resistivity_rho": round(rho_soil, 3),
                "soil_moisture_volumetric": round(soil_moisture, 3),
                "cable_conductor_temp_c": round(cable_tc, 1),
                "baseline_top_oil_c": round(t_o_base, 1),
                "baseline_hot_spot_c": round(t_hs_base, 1),
                "baseline_aging_v": round(v_base, 2),
                "mitigated_top_oil_c": round(t_o_mit, 1),
                "mitigated_hot_spot_c": round(t_hs_mit, 1),
                "mitigated_aging_v": round(v_mit, 2),
                "bess_soc_pct": round(bess_soc, 1),
            })

            if h_day == 23:
                days_summary.append(DaySummary(
                    day_number=day_num,
                    date=step["date"],
                    peak_ambient_2m_c=round(day_peak_2m, 2),
                    coolest_tile_at_peak_c=round(day_coolest_at_peak, 2),
                    intra_aoi_spread_c=round(day_spread_at_peak, 2),
                    end_of_day_soil_resistivity_rho=round(rho_soil, 2),
                    cable_conductor_peak_c=round(day_peak_cable_tc, 1),
                    baseline_peak_hot_spot_c=round(day_peak_base_hs, 1),
                    mitigated_peak_hot_spot_c=round(day_peak_mit_hs, 1),
                    baseline_loss_of_life_hours=round(day_base_life, 1),
                    mitigated_loss_of_life_hours=round(day_mit_life, 1),
                ))
                day_base_life = 0.0
                day_mit_life = 0.0
                day_peak_2m = 0.0
                day_coolest_at_peak = 0.0
                day_spread_at_peak = 0.0
                day_peak_base_hs = 0.0
                day_peak_mit_hs = 0.0
                day_peak_cable_tc = 0.0

        avoided_life_hours = total_base_life - total_mit_life
        c_consequence = self.economic_engine.calculate_outage_consequence_cost()
        cum_avoided_loss = (0.98 - 0.01) * c_consequence + (avoided_life_hours * 1.944) - (3 * 469.0)

        return MultiDaySimulationResult(
            scenario_name="Phoenix July 24-26, 2023 FortyGuard 72-Hour Live Capture Replay",
            total_hours=72,
            days_summary=days_summary,
            timeline_72h=timeline_72h,
            total_baseline_loss_of_life_hours=round(total_base_life, 1),
            total_mitigated_loss_of_life_hours=round(total_mit_life, 1),
            total_avoided_loss_of_life_hours=round(avoided_life_hours, 1),
            cumulative_net_avoided_loss_usd=round(cum_avoided_loss, 2),
            compounding_soil_dryout_factor=round(
                final_soil_resistivity / initial_soil_resistivity, 2
            ),
            scenario_metadata=self._load_capture()["scenario_metadata"],
        )
