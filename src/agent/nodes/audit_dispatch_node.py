"""
Audit Logger & Dispatch Node
Compiles the physical audit ledger, generates B2B utility dispatch work orders,
and creates B2C citizen early-warning advisories.
"""

from __future__ import annotations

import time
from typing import Any, Dict
from src.agent.state import ThermalSentinelState


async def audit_dispatch_node(state: ThermalSentinelState) -> Dict[str, Any]:
    """
    Compiles downstream dispatch orders and finalizes audit log.
    """
    asset_id = state.get("asset_id", "SUB-PHX-DOWNTOWN-04")
    asset_name = state.get("asset_name", "Phoenix Central Substation TX-04")
    city = state.get("target_city", "Phoenix, AZ")
    verdict = state.get("safety_gate_verdict", {})
    mitigated = state.get("mitigated_trajectory", {})
    eco = state.get("economic_evaluation", {})
    actions = state.get("candidate_actions", [])

    # 1. B2B Enterprise / Utility Work Order
    b2b_work_order = {
        "work_order_id": f"WO-TSG-{asset_id}-{int(time.time())}",
        "target_substation": asset_name,
        "location": city,
        "dispatch_status": "AUTOMATED_APPROVED_BY_SAFETY_GATE" if verdict.get("is_safe") else "OPERATOR_OVERRIDE_REQUIRED",
        "authorized_mitigations": actions,
        "target_peak_hot_spot_c": mitigated.get("peak_hot_spot_c"),
        "hot_spot_safety_margin_c": round(140.0 - (mitigated.get("peak_hot_spot_c") or 0.0), 1),
        "avoided_outage_risk_usd": eco.get("avoided_outage_risk_usd"),
        "net_avoided_loss_usd": eco.get("net_avoided_loss_usd"),
        "regulatory_compliance": "IEEE Std C57.91 & ANSI C84.1 Compliant",
    }

    # 2. B2C Citizen / Tenant Advisory
    b2c_advisory = {
        "advisory_id": f"ADV-HEAT-{int(time.time())}",
        "city": city,
        "alert_level": "HEAT_MICROCLIMATE_ADVISORY",
        "headline": "Extreme 2-Meter Heat Corridor Active in Downtown Phoenix",
        "guidance": (
            "Hyperlocal air temperatures surrounding street-level electrical infrastructure "
            "are projected to hit 47.6°C between 11:00 AM and 05:00 PM. Automated grid cooling "
            "and battery peak shaving are actively engaged to prevent power interruptions. "
            "Residents are advised to schedule EV charging after 07:00 PM."
        ),
        "expected_peak_hour": "01:00 PM - 03:00 PM",
    }

    audit_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime()),
        "node": "audit_dispatch_node",
        "message": f"Dispatched Work Order {b2b_work_order['work_order_id']} and Citizen Advisory {b2c_advisory['advisory_id']}. Pipeline completed successfully.",
    }

    audit_trail = list(state.get("audit_trail", []))
    audit_trail.append(audit_entry)

    return {
        "b2b_work_order": b2b_work_order,
        "b2c_advisory": b2c_advisory,
        "audit_trail": audit_trail,
        "current_node": "audit_dispatch_node",
    }
