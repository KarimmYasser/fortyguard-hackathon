"""
Phoenix July 2023 Heatwave Historical Replay Engine
Provides benchmark simulation comparing Baseline Controller (Airport weather + Static Rating)
versus Thermal Sentinel Grid (FortyGuard 2-meter Microclimate + IEEE/IEC Physics + CBF-QP Safety Gate).
"""

from __future__ import annotations

from typing import Any, Dict, List
from src.api.fortyguard_client import load_phoenix_fixture
from src.physics.transformer_thermal import TransformerThermalEngine
from src.physics.soil_cable import SoilCableEngine
from src.physics.urban_canyon import UrbanCanyonEngine
from src.physics.virtual_moisture import VirtualMoistureEngine
from src.physics.economic_model import EconomicEngine
from src.safety.cbf_gate import CBFSafetyGate
from src.models.safety import ActionType, MitigationAction


class PhoenixHeatwaveReplayEngine:
    """
    Replay benchmark generator for Phoenix July 24–26, 2023 episode.
    """

    def __init__(self) -> None:
        self.fixture = load_phoenix_fixture()
        self.thermal_engine = TransformerThermalEngine()
        self.soil_engine = SoilCableEngine()
        self.canyon_engine = UrbanCanyonEngine()
        self.moisture_engine = VirtualMoistureEngine()
        self.economic_engine = EconomicEngine()
        self.safety_gate = CBFSafetyGate()

    def generate_replay_dataset(self) -> Dict[str, Any]:
        """
        Generates full synchronized side-by-side replay dataset.
        """
        meta = self.fixture.get("scenario_metadata", {})
        forecast = self.fixture.get("hourly_forecast_12h", [])
        tiles = self.fixture.get("heatmap_geojson_tiles", {})

        canyon_res = self.canyon_engine.calculate_cooling_derate_factor(
            fortyguard_2m_ambient_c=47.6, reference_wind_speed_m_s=3.0
        )
        eta_cool = canyon_res.get("cooling_derate_eta_cool", 0.68)

        # 1. Baseline Simulation (Using Airport Weather + Static Rating without Mitigation)
        baseline_load = [h.get("baseline_load_ratio_k", 1.0) for h in forecast]
        baseline_traj = self.thermal_engine.simulate_trajectory(
            asset_id="SUB-PHX-DOWNTOWN-04",
            hourly_forecast=forecast,
            load_k_series=baseline_load,
            cooling_derate=eta_cool,
            forced_cooling_active=False,
        )

        # 2. Mitigated Simulation (With FortyGuard early warning + Stage 2 cooling + BESS)
        mitigated_load = list(baseline_load)
        # Apply BESS peak shaving from hour 5 to 10 (-0.22 pu)
        for h in range(5, 10):
            mitigated_load[h] = max(mitigated_load[h] - 0.22, 0.35)
        # Apply EV charging curtailment from hour 6 to 9 (-0.08 pu)
        for h in range(6, 9):
            mitigated_load[h] = max(mitigated_load[h] - 0.08, 0.35)

        mitigated_traj = self.thermal_engine.simulate_trajectory(
            asset_id="SUB-PHX-DOWNTOWN-04",
            hourly_forecast=forecast,
            load_k_series=mitigated_load,
            cooling_derate=eta_cool * 1.35,  # Forced cooling engaged
            forced_cooling_active=True,
        )

        # 3. Synchronized Timeline Alignment
        timeline_steps: List[Dict[str, Any]] = []
        bess_soc = 85.0

        for i in range(len(forecast)):
            b_step = baseline_traj.steps[i]
            m_step = mitigated_traj.steps[i]
            fc = forecast[i]

            # BESS discharge tracking
            if 5 <= i < 10:
                bess_soc -= 7.0  # 7% discharge per peak hour

            timeline_steps.append({
                "hour_index": i,
                "timestamp": fc.get("timestamp"),
                "time_label": fc.get("time_label"),
                
                # Chart 1: Boundary Ambient Comparison
                "airport_reference_temp_c": fc.get("airport_reference_temp_c"),
                "fortyguard_2m_ambient_c": fc.get("fortyguard_2m_ambient_c"),
                "microclimate_delta_c": fc.get("microclimate_delta_c"),
                "solar_irradiance_w_m2": fc.get("solar_irradiance_w_m2"),
                
                # Chart 2: Internal Physical State (Baseline vs Mitigated)
                "baseline_top_oil_c": b_step.t_top_oil_c,
                "baseline_hot_spot_c": b_step.t_hot_spot_c,
                "mitigated_top_oil_c": m_step.t_top_oil_c,
                "mitigated_hot_spot_c": m_step.t_hot_spot_c,
                "top_oil_ceiling_c": 110.0,
                "hot_spot_ceiling_c": 140.0,

                # Chart 3: Aging Acceleration, Loading & BESS
                "baseline_aging_factor_v": b_step.aging_acceleration_factor_v,
                "mitigated_aging_factor_v": m_step.aging_acceleration_factor_v,
                "baseline_cumulative_aging_hours": b_step.cumulative_loss_of_life_hours,
                "mitigated_cumulative_aging_hours": m_step.cumulative_loss_of_life_hours,
                "baseline_load_k": b_step.load_ratio_k,
                "mitigated_load_k": m_step.load_ratio_k,
                "bess_soc_pct": round(bess_soc, 1),
            })

        # 4. Safety Gate Preflight
        candidate_actions = [
            MitigationAction(
                action_type=ActionType.COOLING_STAGE_2,
                target_asset_id="SUB-PHX-DOWNTOWN-04",
                target_hour_start=4,
                target_hour_end=11,
                cooling_boost_factor=1.35,
            ),
            MitigationAction(
                action_type=ActionType.BESS_PEAK_SHAVING,
                target_asset_id="SUB-PHX-DOWNTOWN-04",
                target_hour_start=5,
                target_hour_end=10,
                load_ratio_delta_k=0.22,
                power_delta_mw=5.5,
                bess_discharge_mw=2.0,
            ),
            MitigationAction(
                action_type=ActionType.EV_SMART_CURTAIL,
                target_asset_id="SUB-PHX-DOWNTOWN-04",
                target_hour_start=6,
                target_hour_end=9,
                load_ratio_delta_k=0.08,
            ),
        ]

        safety_verdict = self.safety_gate.preflight_check(
            asset_id="SUB-PHX-DOWNTOWN-04",
            hourly_forecast=forecast,
            candidate_actions=candidate_actions,
            cooling_derate=eta_cool,
            bess_initial_soc_pct=85.0,
            bess_capacity_mwh=25.0,
        )

        # 5. Economic Avoided Loss ROI
        economic_eval = self.economic_engine.evaluate_net_avoided_loss(
            baseline_peak_hot_spot_c=baseline_traj.peak_hot_spot_c,
            mitigated_peak_hot_spot_c=mitigated_traj.peak_hot_spot_c,
            baseline_loss_of_life_hours=baseline_traj.total_loss_of_life_hours,
            mitigated_loss_of_life_hours=mitigated_traj.total_loss_of_life_hours,
            persistence_hours=meta.get("persistence_metrics", {}).get("persistence_hours_p40", 7.17),
            thermal_soak_index=meta.get("persistence_metrics", {}).get("thermal_soak_index_tsi", 4.12),
            bess_discharged_mwh=10.0,
            cooling_runtime_hours=7.0,
        )

        # 6. Underground Soil & Virtual Moisture States
        soil_eval = self.soil_engine.evaluate_compound_site_margin(
            consecutive_heatwave_days=24,
            initial_moisture=0.18,
            cable_load_k=1.18,
            transformer_top_oil_c=mitigated_traj.peak_top_oil_c,
            transformer_hot_spot_c=mitigated_traj.peak_hot_spot_c,
        )
        moisture_eval = self.moisture_engine.step_moisture_migration(
            paper_moisture_pct=2.5,
            oil_moisture_ppm=16.0,
            t_hot_spot_c=mitigated_traj.peak_hot_spot_c,
            t_oil_c=mitigated_traj.peak_top_oil_c,
            dt_hours=1.0,
        )

        return {
            "scenario_metadata": meta,
            "timeline_steps": timeline_steps,
            "baseline_summary": {
                "peak_top_oil_c": baseline_traj.peak_top_oil_c,
                "peak_hot_spot_c": baseline_traj.peak_hot_spot_c,
                "peak_aging_acceleration_v": baseline_traj.peak_aging_acceleration_v,
                "total_loss_of_life_hours": baseline_traj.total_loss_of_life_hours,
                "breached_emergency_ceiling": baseline_traj.breached_hot_spot_ceiling,
            },
            "mitigated_summary": {
                "peak_top_oil_c": mitigated_traj.peak_top_oil_c,
                "peak_hot_spot_c": mitigated_traj.peak_hot_spot_c,
                "peak_aging_acceleration_v": mitigated_traj.peak_aging_acceleration_v,
                "total_loss_of_life_hours": mitigated_traj.total_loss_of_life_hours,
                "breached_emergency_ceiling": mitigated_traj.breached_hot_spot_ceiling,
                "avoided_loss_of_life_hours": round(baseline_traj.total_loss_of_life_hours - mitigated_traj.total_loss_of_life_hours, 1),
            },
            "safety_gate_verdict": safety_verdict.model_dump(),
            "economic_evaluation": economic_eval,
            "soil_cable_state": soil_eval,
            "virtual_moisture_state": moisture_eval,
            "urban_canyon_state": canyon_res,
            "heatmap_geojson_tiles": tiles,
        }
