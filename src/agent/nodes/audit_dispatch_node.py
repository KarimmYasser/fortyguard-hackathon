"""
Audit Logger & Dispatch Node
Compiles the physical audit ledger, generates B2B utility dispatch work orders,
and creates B2C citizen early-warning advisories.
"""

from __future__ import annotations

import time
from typing import Any, Dict
from src.agent.state import ThermalSentinelState
from src.agent.llm_factory import generate_chat_completion


async def audit_dispatch_node(state: ThermalSentinelState) -> Dict[str, Any]:
    """
    Compiles downstream dispatch orders and finalizes audit log.
    Uses GPT-5.4 via Siemens SDC LLM Gateway for live advisory synthesis when available.
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

    # 2. Live LLM Synthesis for Citizen Advisory
    # Report the peak this run actually saw. This used to state a fixed 47.6 C
    # in both the fallback copy and the LLM prompt, so the public advisory and
    # the model's input disagreed with the dashboard on every run.
    peak_2m_c = max(
        (h.get("fortyguard_2m_ambient_c", 0.0) for h in state.get("fortyguard_forecast", [])),
        default=0.0,
    )
    peak_2m_label = f"{peak_2m_c:.1f}" if peak_2m_c else "extreme"
    net_loss = eco.get("net_avoided_loss_usd") or 0

    default_guidance = (
        f"Hyperlocal air temperatures surrounding street-level electrical infrastructure "
        f"are projected to hit {peak_2m_label}°C between 11:00 AM and 05:00 PM. Automated grid cooling "
        f"and battery peak shaving are actively engaged to prevent power interruptions. "
        f"Residents are advised to schedule EV charging after 07:00 PM."
    )

    llm_guidance = await generate_chat_completion(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an autonomous power grid resilience agent. "
                    "Write a concise, professional 2-sentence public advisory for residents "
                    "explaining that extreme microclimate heat is active, but autonomous BESS battery "
                    "peak shaving and transformer cooling have been dispatched to ensure uninterrupted power."
                ),
            },
            {
                "role": "user",
                "content": f"Location: {city}, Substation: {asset_name}, Projected 2m Heat: {peak_2m_label}°C, Avoided Loss: ${net_loss:,.0f}.",
            },
        ],
        max_completion_tokens=150,
        temperature=0.2,
    )

    b2c_advisory = {
        "advisory_id": f"ADV-HEAT-{int(time.time())}",
        "city": city,
        "alert_level": "HEAT_MICROCLIMATE_ADVISORY",
        "headline": f"Extreme 2-Meter Heat Corridor Active in {city}",
        "guidance": llm_guidance or default_guidance,
        "expected_peak_hour": "01:00 PM - 03:00 PM",
        "ai_synthesizer": "GPT-5.4 via Siemens SDC Gateway" if llm_guidance else "Deterministic Template",
    }

    audit_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime()),
        "node": "audit_dispatch_node",
        "message": f"Dispatched Work Order {b2b_work_order['work_order_id']} and Citizen Advisory {b2c_advisory['advisory_id']} ({b2c_advisory['ai_synthesizer']}). Pipeline completed successfully.",
    }

    audit_trail = list(state.get("audit_trail", []))
    audit_trail.append(audit_entry)

    return {
        "b2b_work_order": b2b_work_order,
        "b2c_advisory": b2c_advisory,
        "audit_trail": audit_trail,
        "current_node": "audit_dispatch_node",
    }
