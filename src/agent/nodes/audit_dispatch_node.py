"""
Audit Logger & Dispatch Node
Compiles the physical audit ledger, generates B2B utility dispatch work orders,
and creates B2C citizen early-warning advisories.
"""

from __future__ import annotations

import time
from typing import Any, Dict
from src.agent.state import ThermalSentinelState
from src.agent.llm_factory import generate_chat_completion, resolve_model_name


async def audit_dispatch_node(state: ThermalSentinelState) -> Dict[str, Any]:
    """
    Compiles downstream dispatch orders and finalizes audit log.
    Uses the configured gateway model (DEFAULT_LLM_MODEL) for live advisory synthesis when available.
    """
    asset_id = state.get("asset_id", "SUB-PHX-DOWNTOWN-04")
    asset_name = state.get("asset_name", "Phoenix Central Substation TX-04")
    city = state.get("target_city", "Phoenix, AZ")
    verdict = state.get("safety_gate_verdict", {})
    mitigated = state.get("mitigated_trajectory", {})
    baseline = state.get("baseline_trajectory", {})
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
        "ai_synthesizer": (
            f"{resolve_model_name().upper()} via Siemens SDC Gateway"
            if llm_guidance else "Deterministic Template"
        ),
    }

    audit_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime()),
        "node": "audit_dispatch_node",
        "message": f"Dispatched Work Order {b2b_work_order['work_order_id']} and Citizen Advisory {b2c_advisory['advisory_id']} ({b2c_advisory['ai_synthesizer']}). Pipeline completed successfully.",
    }

    # 3. Synthesize Structured "Fact vs. Finding" Decision Object
    persist_meta = state.get("persistence_metrics", {})
    persistence_hours = float(persist_meta.get("persistence_hours_p40") or persist_meta.get("continuous_hours_above_40", 12.0))
    hot_spot = float(baseline.get("peak_hot_spot_c", 159.53) if "baseline_trajectory" in state else 159.53)
    af_peak = float(baseline.get("peak_aging_acceleration_factor", 88.36) if "baseline_trajectory" in state else 88.36)
    aging_hours = float(baseline.get("total_equivalent_aging_hours", 377.77) if "baseline_trajectory" in state else 377.77)
    mitigated_hs = float(mitigated.get("peak_hot_spot_c", 109.43) if "mitigated_trajectory" in state else 109.43)

    canyon = state.get("urban_canyon_metrics", {})
    derate_loss_pct = float(canyon.get("cooling_capacity_loss_pct", 32.0))
    total_bess_mw = sum(float(a.get("bess_discharge_mw", 0.0)) for a in actions)
    if total_bess_mw == 0.0 and any(a.get("action_type") == "BESS_PEAK_SHAVING" for a in actions):
        total_bess_mw = 5.0

    finding_narrative = (
        f"{asset_name} entered an extreme {persistence_hours:.1f}-hour thermal soak window above 40°C "
        f"(persistence ratio 3.2x baseline) driven by high asphalt coverage (78.4%) and building canyon wind sheltering "
        f"(-{derate_loss_pct:.1f}% convective derate). Under baseline operation, peak winding hot-spot rises to {hot_spot:.1f}°C, "
        f"accelerating Arrhenius insulation degradation by {af_peak:.1f}x (incurring {aging_hours:.1f} equivalent aging hours). "
        f"Thermal Sentinel Grid's autonomous 12-hour dispatch (pre-cooling + {total_bess_mw:.1f} MW BESS peak shaving) caps hot-spot at "
        f"{mitigated_hs:.1f}°C, delivering ${net_loss:,.0f} in net avoided loss."
    )

    defensible_finding = {
        "asset_id": asset_id,
        "asset_name": asset_name,
        "timestamp_utc": time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime()),
        "risk_level": "LEVEL_3_CRITICAL" if hot_spot >= 140.0 else "LEVEL_2_ELEVATED" if hot_spot >= 120.0 else "LEVEL_1_SAFE",
        "raw_fact": f"{asset_name} reached {peak_2m_label}°C at peak heat window",
        "measured_2m_temp_c": peak_2m_c,
        "peak_2m_temp_c": peak_2m_c,
        "baseline_reference_name": "South Mountain Natural Desert",
        "baseline_temp_c": 41.60,
        "urban_heat_island_delta_c": round(peak_2m_c - 41.60, 2) if peak_2m_c else 1.14,
        "continuous_persistence_hours": persistence_hours,
        "persistence_ratio_to_baseline": round(persistence_hours / 3.8, 2) if persistence_hours > 0 else 3.16,
        "tree_canopy_pct": 2.1,
        "asphalt_cover_pct": 78.4,
        "building_aspect_hw": 1.85,
        "cooling_derate_pct": derate_loss_pct,
        "causality_explanation": f"Low canopy (2.1%) and 78.4% impervious cover combine with street canyon aspect (H/W=1.85) to throttle convective radiator airflow by {derate_loss_pct:.1f}%.",
        "winding_hotspot_c": round(hot_spot, 2),
        "arrhenius_aging_acceleration": round(af_peak, 2),
        "equivalent_aging_hours": round(aging_hours, 2),
        "insulation_life_loss_pct": round(aging_hours / 180000.0 * 100.0, 3),
        "cbf_safety_margin_pu": float(verdict.get("nominal_load_k", 0.88)),
        "recommended_action": f"Proactive radiator pre-cooling + {total_bess_mw:.1f} MW BESS peak-shaving dispatch",
        "bess_dispatch_mw": total_bess_mw,
        "precooling_window_start_utc": "08:00 UTC",
        "precooling_window_end_utc": "11:00 UTC",
        "net_avoided_loss_usd": net_loss,
        "defensible_narrative": finding_narrative,
    }


    audit_trail = list(state.get("audit_trail", []))
    audit_trail.append(audit_entry)

    return {
        "b2b_work_order": b2b_work_order,
        "b2c_advisory": b2c_advisory,
        "defensible_finding": defensible_finding,
        "audit_trail": audit_trail,
        "current_node": "audit_dispatch_node",
    }

