"""
Safety Gate Node
Executes deterministic Control Barrier Function (CBF-QP) constraint checks,
performs K_safe projection if needed, and computes investment-grade Net Avoided Loss ROI.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List
from src.agent.state import ThermalSentinelState
from src.models.safety import MitigationAction, SafetyStatus
from src.physics.transformer_thermal import TransformerThermalEngine
from src.physics.economic_model import EconomicEngine
from src.safety.cbf_gate import CBFSafetyGate


async def safety_gate_node(state: ThermalSentinelState) -> Dict[str, Any]:
    """
    Validates candidate mitigation plan against hard physical boundaries.
    """
    asset_id = state.get("asset_id", "SUB-PHX-DOWNTOWN-04")
    forecast = state.get("fortyguard_forecast", [])
    raw_actions = state.get("candidate_actions", [])
    canyon = state.get("urban_canyon_metrics", {})
    baseline = state.get("baseline_trajectory", {})
    persist = state.get("persistence_metrics", {})

    eta_cool = canyon.get("cooling_derate_eta_cool", 0.68)
    gate = CBFSafetyGate()
    economic_engine = EconomicEngine()
    thermal_engine = TransformerThermalEngine()

    actions = [MitigationAction(**a) for a in raw_actions]

    # Deterministic Preflight Check
    verdict = gate.preflight_check(
        asset_id=asset_id,
        hourly_forecast=forecast,
        candidate_actions=actions,
        cooling_derate=eta_cool,
        bess_initial_soc_pct=85.0,
        bess_capacity_mwh=25.0,
    )
    # Flush before returning: on serverless the lambda freezes once the
    # response is sent, so a background task never completes.
    await gate.persist_pending_certificates()

    # Compute Mitigated Thermal Trajectory
    mitigated_load_curve = [h.get("baseline_load_ratio_k", 1.0) for h in forecast]
    forced_cooling = False
    for a in actions:
        if a.action_type.name.startswith("COOLING"):
            forced_cooling = True
        if a.load_ratio_delta_k > 0:
            start = max(a.target_hour_start, 0)
            end = min(a.target_hour_end, len(mitigated_load_curve))
            for h in range(start, end):
                mitigated_load_curve[h] = max(mitigated_load_curve[h] - a.load_ratio_delta_k, 0.35)

    mitigated_traj = thermal_engine.simulate_trajectory(
        asset_id=asset_id,
        hourly_forecast=forecast,
        load_k_series=mitigated_load_curve,
        cooling_derate=eta_cool * (1.35 if forced_cooling else 1.0),
        forced_cooling_active=forced_cooling,
    )

    # Economic ROI calculation
    eco_eval = economic_engine.evaluate_net_avoided_loss(
        baseline_peak_hot_spot_c=baseline.get("peak_hot_spot_c", 143.2),
        mitigated_peak_hot_spot_c=mitigated_traj.peak_hot_spot_c,
        baseline_loss_of_life_hours=baseline.get("total_loss_of_life_hours", 88.6),
        mitigated_loss_of_life_hours=mitigated_traj.total_loss_of_life_hours,
        persistence_hours=persist.get("persistence_hours_p40", 12.0),
        thermal_soak_index=persist.get("thermal_soak_index_tsi", 3.68),
        bess_discharged_mwh=10.0,
        cooling_runtime_hours=7.0,
    )

    audit_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime()),
        "node": "safety_gate_node",
        "message": f"Safety Gate Verdict: [{verdict.status.value}] - Projected Peak Hot-Spot: {mitigated_traj.peak_hot_spot_c}°C (Cap: 140°C), Net Avoided Loss: ${eco_eval['net_avoided_loss_usd']:,} (ROI: {eco_eval['roi_multiple']}x)",
    }

    audit_trail = list(state.get("audit_trail", []))
    audit_trail.append(audit_entry)

    return {
        "safety_gate_verdict": verdict.model_dump(),
        "mitigated_trajectory": mitigated_traj.model_dump(),
        "economic_evaluation": eco_eval,
        "audit_trail": audit_trail,
        "current_node": "safety_gate_node",
    }
