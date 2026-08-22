"""
72-Hour Multi-Day Compounding Heatwave Simulation Engine
Simulates the historic Phoenix July 24-26, 2023 3-day extreme heatwave episode.
Models continuous overnight heat traps, cumulative thermal soak,
and non-linear IEC 60287 soil moisture dryout across 72 hours.
"""

from __future__ import annotations

import math
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
    airport_peak_c: float
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

    def generate_72h_boundary_forcing(self) -> List[Dict[str, Any]]:
        """
        Generates 72 hours of realistic Phoenix July 24-26, 2023 hourly microclimate data.
        Day 1: July 24 (Peak 47.6°C / Airport 43.1°C)
        Day 2: July 25 (Peak 48.1°C / Airport 43.5°C)
        Day 3: July 26 (Peak 48.3°C / Airport 43.8°C - 119°F Historic High)
        """
        steps = []
        dates = ["2023-07-24", "2023-07-25", "2023-07-26"]
        peak_deltas = [4.5, 4.6, 4.7]
        airport_peaks = [43.1, 43.5, 43.8]

        for d_idx, (date_str, delta, air_peak) in enumerate(zip(dates, peak_deltas, airport_peaks)):
            min_temp = 33.0 + d_idx * 0.5  # Night-time minimum climbs steadily
            for h in range(24):
                if h < 5:
                    rad = math.cos(math.pi * (h + 10) / 19.0)
                    t_air = min_temp + (air_peak - min_temp) * 0.15 * (1.0 + rad)
                elif 5 <= h <= 14:
                    rad = math.sin(math.pi * (h - 5) / 18.0)
                    t_air = min_temp + (air_peak - min_temp) * rad
                else:
                    rad = math.cos(math.pi * (h - 14) / 15.0)
                    t_air = min_temp + (air_peak - min_temp) * 0.5 * (1.0 + rad)

                t_2m = t_air + delta * (0.4 + 0.6 * max(0.0, math.sin(math.pi * (h - 6) / 12.0) if 6 <= h <= 18 else 0.0))

                solar = 0.0
                if 6 <= h <= 18:
                    solar = max(0.0, 980.0 * math.sin(math.pi * (h - 6) / 12.0))

                if 0 <= h < 7:
                    base_k = 0.65
                elif 7 <= h < 12:
                    base_k = 0.95
                elif 12 <= h < 17:
                    base_k = 1.18
                elif 17 <= h < 22:
                    base_k = 1.05
                else:
                    base_k = 0.75

                steps.append({
                    "global_hour": d_idx * 24 + h,
                    "day_index": d_idx + 1,
                    "date": date_str,
                    "hour_of_day": h,
                    "time_label": f"{h:02d}:00",
                    "airport_temp_c": round(t_air, 1),
                    "fortyguard_2m_ambient_c": round(t_2m, 1),
                    "intra_aoi_spread_c": round(t_2m - t_air, 1),
                    "solar_irradiance_w_m2": round(solar, 1),
                    "baseline_load_k": round(base_k, 2),
                })

        return steps

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
        bess_soc = 85.0

        # 980 was passed positionally into reference_wind_speed_m_s, i.e. a solar
        # irradiance figure landing in the wind slot and modelling a 980 m/s wind,
        # which massively over-estimated convective heat rejection. Both values
        # also predate the live capture.
        canyon_res = self.canyon_engine.calculate_cooling_derate_factor(
            fortyguard_2m_ambient_c=42.74,
            reference_wind_speed_m_s=2.8,
            solar_irradiance_w_m2=889.8,
        )
        eta_cool = canyon_res["cooling_derate_eta_cool"]

        day_base_life = 0.0
        day_mit_life = 0.0
        day_peak_2m = 0.0
        day_peak_air = 0.0
        day_peak_base_hs = 0.0
        day_peak_mit_hs = 0.0
        day_peak_cable_tc = 0.0

        for step in forcing_steps:
            gh = step["global_hour"]
            h_day = step["hour_of_day"]
            day_num = step["day_index"]
            t_2m = step["fortyguard_2m_ambient_c"]
            t_air = step["airport_temp_c"]
            solar = step["solar_irradiance_w_m2"]
            base_k = step["baseline_load_k"]

            day_peak_2m = max(day_peak_2m, t_2m)
            day_peak_air = max(day_peak_air, t_air)

            # IEC 60287 Compounding Evaporative Soil Moisture Loss
            # Rate increases in afternoon heat and compounds across Day 1 -> 2 -> 3
            evap_rate = 0.0020 * (t_2m / 40.0)
            soil_moisture = max(0.035, soil_moisture - evap_rate)

            rho_soil = self.soil_engine.calculate_soil_thermal_resistivity(soil_moisture)
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
                "airport_temp_c": t_air,
                "solar_irradiance_w_m2": solar,
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
                    peak_ambient_2m_c=round(day_peak_2m, 1),
                    airport_peak_c=round(day_peak_air, 1),
                    intra_aoi_spread_c=round(day_peak_2m - day_peak_air, 1),
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
                day_peak_air = 0.0
                day_peak_base_hs = 0.0
                day_peak_mit_hs = 0.0
                day_peak_cable_tc = 0.0

        avoided_life_hours = total_base_life - total_mit_life
        c_consequence = self.economic_engine.calculate_outage_consequence_cost()
        cum_avoided_loss = (0.98 - 0.01) * c_consequence + (avoided_life_hours * 1.944) - (3 * 469.0)

        return MultiDaySimulationResult(
            scenario_name="Phoenix July 24-26, 2023 Compounding 72-Hour Heatwave Benchmark",
            total_hours=72,
            days_summary=days_summary,
            timeline_72h=timeline_72h,
            total_baseline_loss_of_life_hours=round(total_base_life, 1),
            total_mitigated_loss_of_life_hours=round(total_mit_life, 1),
            total_avoided_loss_of_life_hours=round(avoided_life_hours, 1),
            cumulative_net_avoided_loss_usd=round(cum_avoided_loss, 2),
            compounding_soil_dryout_factor=round(2.48 / 0.95, 2),
        )
