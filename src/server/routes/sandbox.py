"""
FastAPI Route for Live What-If Stress Studio (Interactive Physics Sandbox)
Allows judges & operators to dynamically modulate boundary conditions, multi-day persistence,
BESS capacity, and asset ratings, recalculating IEEE C57.91 & CBF-QP trajectories in real-time.
"""

from __future__ import annotations

from typing import Dict, Any, List
from fastapi import APIRouter
from pydantic import BaseModel, Field

from src.models.thermal import TransformerThermalParams
from src.physics.transformer_thermal import TransformerThermalEngine
from src.physics.soil_cable import SoilCableEngine
from src.physics.urban_canyon import UrbanCanyonEngine, UrbanCanyonParameters
from src.physics.virtual_moisture import VirtualMoistureEngine
from src.physics.economic_model import EconomicEngine
from src.safety.cbf_gate import CBFSafetyGate, ActionType, MitigationAction
from src.db.database import db_manager
from src.db.models import SimulationRunRecord

router = APIRouter(prefix="/sandbox", tags=["What-If Stress Studio"])



class SandboxSimulationRequest(BaseModel):
    """Dynamic inputs for the what-if sandbox simulation."""
    intra_aoi_spread_c: float = Field(default=4.5, ge=0.0, le=8.0, description="FortyGuard 2m delta above airport (°C)")
    heatwave_day: int = Field(default=24, ge=1, le=31, description="Compounding heatwave day (soil dryout progression)")
    transformer_mva: float = Field(default=25.0, ge=10.0, le=100.0, description="Transformer nameplate rating (MVA)")
    bess_capacity_mwh: float = Field(default=25.0, ge=0.0, le=100.0, description="Available utility BESS capacity (MWh)")
    canyon_aspect_ratio: float = Field(default=1.85, ge=0.2, le=4.0, description="Building canyon height-to-width ratio (H/W)")
    forced_cooling_enabled: bool = Field(default=True, description="Whether active auxiliary cooling pumps are available")


@router.post("/simulate")
async def run_sandbox_simulation(req: SandboxSimulationRequest) -> Dict[str, Any]:
    """
    Executes live multi-physics simulation and CBF-QP safety gate under customized parameters.
    """
    airport_temps = [34.2, 35.8, 38.1, 40.5, 42.0, 43.1, 42.8, 41.5, 40.2, 38.9, 37.4, 35.9]
    solar_fluxes = [280.0, 520.0, 750.0, 910.0, 980.0, 940.0, 810.0, 620.0, 410.0, 190.0, 50.0, 0.0]
    time_labels = [
        "06:00 AM", "07:00 AM", "08:00 AM", "09:00 AM",
        "10:00 AM", "11:00 AM", "12:00 PM", "01:00 PM",
        "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM",
    ]

    # 1. Physical parameters scaled to user MVA
    tx_params = TransformerThermalParams(
        rated_mva=req.transformer_mva,
        tau_o=2.8 * (req.transformer_mva / 25.0) ** 0.35,
        tau_w=0.10,
    )
    thermal_solver = TransformerThermalEngine(tx_params)
    soil_engine = SoilCableEngine()
    canyon_engine = UrbanCanyonEngine(
        UrbanCanyonParameters(height_to_width_ratio_hw=req.canyon_aspect_ratio)
    )
    moisture_engine = VirtualMoistureEngine()
    economic_engine = EconomicEngine()
    safety_gate = CBFSafetyGate(thermal_params=tx_params)

    # 2. Canyon Aerodynamics
    canyon_res = canyon_engine.calculate_cooling_derate_factor(
        fortyguard_2m_ambient_c=43.1 + req.intra_aoi_spread_c,
        solar_irradiance_w_m2=980.0,
    )
    eta_cool = canyon_res["cooling_derate_eta_cool"]

    # 3. Build Forecast Stream with user's microclimate delta
    forecast_dicts: List[Dict[str, Any]] = []
    for h, time_lbl, t_air, s_w in zip(range(6, 18), time_labels, airport_temps, solar_fluxes):
        t_2m = t_air + req.intra_aoi_spread_c
        forecast_dicts.append(
            {
                "hour_index": h,
                "time_label": time_lbl,
                "timestamp": f"2023-07-24T{h:02d}:00:00Z",
                "fortyguard_2m_ambient_c": t_2m,
                "solar_irradiance_w_m2": s_w,
            }
        )

    # 4. Baseline Simulation (nominal load 1.18 pu peak)
    base_loads = [0.85, 0.92, 1.02, 1.12, 1.18, 1.16, 1.10, 1.05, 0.98, 0.90, 0.82, 0.75]
    baseline_traj = thermal_solver.simulate_trajectory(
        asset_id="SUB-PHX-DOWNTOWN-04",
        hourly_forecast=forecast_dicts,
        load_k_series=base_loads,
        cooling_derate=eta_cool,
        forced_cooling_active=False,
    )

    # 5. Mitigated Actions & Load Profile
    mit_loads = list(base_loads)
    candidate_actions: List[MitigationAction] = []

    if req.forced_cooling_enabled:
        candidate_actions.append(
            MitigationAction(
                action_type=ActionType.COOLING_STAGE_2,
                target_asset_id="SUB-PHX-DOWNTOWN-04",
                target_hour_start=4,
                target_hour_end=11,
                cooling_boost_factor=1.35,
            )
        )

    if req.bess_capacity_mwh > 0.0:
        bess_shave_k = min(0.25, (req.bess_capacity_mwh / 25.0) * 0.22)
        candidate_actions.append(
            MitigationAction(
                action_type=ActionType.BESS_PEAK_SHAVING,
                target_asset_id="SUB-PHX-DOWNTOWN-04",
                target_hour_start=5,
                target_hour_end=10,
                load_ratio_delta_k=bess_shave_k,
                power_delta_mw=bess_shave_k * req.transformer_mva,
                bess_discharge_mw=min(5.0, req.bess_capacity_mwh / 4.0),
            )
        )
        for i in range(4, 10):
            mit_loads[i] = max(0.65, mit_loads[i] - bess_shave_k)

    mitigated_traj = thermal_solver.simulate_trajectory(
        asset_id="SUB-PHX-DOWNTOWN-04",
        hourly_forecast=forecast_dicts,
        load_k_series=mit_loads,
        cooling_derate=eta_cool,
        forced_cooling_active=req.forced_cooling_enabled,
    )

    # 6. Safety Gate Preflight
    safety_verdict = safety_gate.preflight_check(
        asset_id="SUB-PHX-DOWNTOWN-04",
        hourly_forecast=forecast_dicts,
        candidate_actions=candidate_actions,
        cooling_derate=eta_cool,
        bess_initial_soc_pct=85.0,
        bess_capacity_mwh=max(req.bess_capacity_mwh, 1.0),
        transformer_rating_mva=req.transformer_mva,
    )

    # 7. Soil Dryout & Virtual Moisture
    soil_eval = soil_engine.evaluate_compound_site_margin(
        consecutive_heatwave_days=req.heatwave_day,
        initial_moisture=0.18,
        cable_load_k=1.18,
        transformer_top_oil_c=mitigated_traj.peak_top_oil_c,
        transformer_hot_spot_c=mitigated_traj.peak_hot_spot_c,
    )
    moisture_eval = moisture_engine.step_moisture_migration(
        paper_moisture_pct=2.5,
        oil_moisture_ppm=16.0,
        t_hot_spot_c=mitigated_traj.peak_hot_spot_c,
        t_oil_c=mitigated_traj.peak_top_oil_c,
        dt_hours=1.0,
    )

    # 8. Avoided Loss Model
    bess_discharged_mwh = min(req.bess_capacity_mwh * 0.4, 12.5) if req.bess_capacity_mwh > 0 else 0.0
    economic_eval = economic_engine.evaluate_net_avoided_loss(
        baseline_peak_hot_spot_c=baseline_traj.peak_hot_spot_c,
        mitigated_peak_hot_spot_c=mitigated_traj.peak_hot_spot_c,
        baseline_loss_of_life_hours=baseline_traj.total_loss_of_life_hours,
        mitigated_loss_of_life_hours=mitigated_traj.total_loss_of_life_hours,
        persistence_hours=min(7.17 * (req.intra_aoi_spread_c / 4.5), 11.0),
        thermal_soak_index=min(4.12 * (req.intra_aoi_spread_c / 4.5), 8.0),
        bess_discharged_mwh=bess_discharged_mwh,
        cooling_runtime_hours=7.0 if req.forced_cooling_enabled else 0.0,
    )

    # 9. Timeline Steps
    timeline_steps = []
    bess_soc = 85.0
    for idx, (f_dict, b_step, m_step) in enumerate(
        zip(forecast_dicts, baseline_traj.steps, mitigated_traj.steps)
    ):
        if req.bess_capacity_mwh > 0 and 4 <= idx <= 9:
            bess_soc = max(30.0, bess_soc - (bess_discharged_mwh / req.bess_capacity_mwh * 100.0 / 6.0))

        timeline_steps.append(
            {
                "hour_index": idx,
                "timestamp": f_dict["timestamp"],
                "time_label": f_dict["time_label"],
                "coolest_tile_2m_c": airport_temps[idx],
                "fortyguard_2m_ambient_c": f_dict["fortyguard_2m_ambient_c"],
                "intra_aoi_spread_c": round(f_dict["fortyguard_2m_ambient_c"] - airport_temps[idx], 1),
                "solar_irradiance_w_m2": f_dict["solar_irradiance_w_m2"],
                "baseline_top_oil_c": b_step.t_top_oil_c,
                "baseline_hot_spot_c": b_step.t_hot_spot_c,
                "baseline_aging_factor_v": b_step.aging_acceleration_factor_v,
                "baseline_load_k": base_loads[idx],
                "mitigated_top_oil_c": m_step.t_top_oil_c,
                "mitigated_hot_spot_c": m_step.t_hot_spot_c,
                "mitigated_aging_factor_v": m_step.aging_acceleration_factor_v,
                "mitigated_load_k": mit_loads[idx],
                "bess_soc_pct": round(bess_soc, 1),
            }
        )

    # Asynchronously persist simulation run snapshot
    try:
        import uuid
        sim_id = f"SIM-{uuid.uuid4().hex[:8].upper()}"
        sim_record = SimulationRunRecord(
            simulation_id=sim_id,
            scenario_name=f"WhatIf Delta={req.intra_aoi_spread_c}C Day={req.heatwave_day}",
            delta_c=req.intra_aoi_spread_c,
            heatwave_day=req.heatwave_day,
            transformer_mva=req.transformer_mva,
            bess_mwh=req.bess_capacity_mwh,
            canyon_hw_ratio=req.canyon_aspect_ratio,
            cooling_fans_stage=2 if req.forced_cooling_enabled else 0,
            peak_hot_spot_c=baseline_traj.peak_hot_spot_c,
            hours_above_140c=sum(1.0 for s in baseline_traj.steps if s.t_hot_spot_c >= 140.0),
            net_avoided_loss=float(economic_eval.get("net_avoided_loss", 2791338.0)),
        )
        await db_manager.save_simulation_run(sim_record)
    except Exception:
        pass

    return {
        "status": "success",
        "inputs_applied": req.model_dump(),
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
            "avoided_loss_of_life_hours": round(
                baseline_traj.total_loss_of_life_hours - mitigated_traj.total_loss_of_life_hours, 1
            ),
        },
        "safety_gate_verdict": safety_verdict.model_dump(),
        "economic_evaluation": economic_eval,
        "soil_cable_state": soil_eval,
        "virtual_moisture_state": moisture_eval,
        "urban_canyon_state": canyon_res,
    }
