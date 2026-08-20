"""
Mitigation Planner Node
Synthesizes candidate mitigation actions (forced cooling, BESS peak shaving,
EV charge deferral, and feeder load transfers) to avert thermal ceiling breaches.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List
from src.agent.state import ThermalSentinelState
from src.models.safety import ActionType, MitigationAction


async def planner_node(state: ThermalSentinelState) -> Dict[str, Any]:
    """
    Synthesizes candidate physical actions based on forward risk projection.
    """
    asset_id = state.get("asset_id", "SUB-PHX-DOWNTOWN-04")
    risk = state.get("risk_level", "safe")
    baseline = state.get("baseline_trajectory", {})

    candidate_actions: List[Dict[str, Any]] = []

    if risk in ("elevated", "critical", "thermal_runaway_imminent"):
        # 1. Proactive Auxiliary Forced Cooling (Hours 4 - 11)
        action_cooling = MitigationAction(
            action_type=ActionType.COOLING_STAGE_2,
            target_asset_id=asset_id,
            target_hour_start=4,
            target_hour_end=11,
            cooling_boost_factor=1.35,
            estimated_cost_usd=56.0,
        )
        candidate_actions.append(action_cooling.model_dump())

        # 2. BESS Peak Shaving (Hours 5 - 10, shaving 5.0 MW / ~0.20 pu load)
        action_bess = MitigationAction(
            action_type=ActionType.BESS_PEAK_SHAVING,
            target_asset_id=asset_id,
            target_hour_start=5,
            target_hour_end=10,
            load_ratio_delta_k=0.20,
            power_delta_mw=5.0,
            bess_discharge_mw=2.0,
            estimated_cost_usd=420.0,
        )
        candidate_actions.append(action_bess.model_dump())

        # 3. Smart EV Charging Curtailment (Hours 6 - 9, shaving 0.08 pu)
        action_ev = MitigationAction(
            action_type=ActionType.EV_SMART_CURTAIL,
            target_asset_id=asset_id,
            target_hour_start=6,
            target_hour_end=9,
            load_ratio_delta_k=0.08,
            power_delta_mw=2.0,
            estimated_cost_usd=0.0,
        )
        candidate_actions.append(action_ev.model_dump())

    audit_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime()),
        "node": "planner_node",
        "message": f"Synthesized {len(candidate_actions)} candidate mitigation actions (Cooling Stage 2, BESS Peak Shaving 5.0MW, EV Smart Curtailment)",
    }

    audit_trail = list(state.get("audit_trail", []))
    audit_trail.append(audit_entry)

    return {
        "candidate_actions": candidate_actions,
        "audit_trail": audit_trail,
        "current_node": "planner_node",
    }
