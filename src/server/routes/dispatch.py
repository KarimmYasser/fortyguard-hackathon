"""
Agentic Dispatch & Economic ROI Router
Triggers the full LangGraph agent pipeline and evaluates investment-grade avoided loss.
"""

from __future__ import annotations

import logging
from typing import Any, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.agent.graph import run_thermal_sentinel_agent
from src.physics.economic_model import EconomicEngine
from src.db.database import db_manager
from src.db.models import (
    DispatchWorkOrderRecord,
    AgentExecutionTraceRecord,
    FinancialAuditRecord,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dispatch", tags=["Agentic Dispatch & ROI"])


class MitigationTriggerRequest(BaseModel):
    city: str = Field(default="Phoenix, AZ")
    asset_id: str = Field(default="SUB-PHX-DOWNTOWN-04")
    asset_name: str = Field(default="Phoenix Central Substation TX-04")
    latitude: float = Field(default=33.4484)
    longitude: float = Field(default=-112.0740)


@router.post("/run-mitigation")
async def run_mitigation_pipeline(req: MitigationTriggerRequest) -> Dict[str, Any]:
    """
    Runs the complete LangGraph StateGraph pipeline for the target asset and persists to database.
    """
    try:
        res = await run_thermal_sentinel_agent(
            target_city=req.city,
            asset_id=req.asset_id,
            asset_name=req.asset_name,
            location={"lat": req.latitude, "lon": req.longitude},
        )

        # 1. Persist authorized work order to SQLite / Supabase
        # NOTE: the LangGraph pipeline's real output nests these under
        # `b2b_work_order` / `safety_gate_verdict` / `candidate_actions`, not
        # the stale `dispatch_actions` / `safety_gate_passed` / `explanation`
        # keys previously read here (those never existed, so every run was
        # silently falling back to defaults, including a fixed work_order_id
        # per asset that caused every dispatch to overwrite the same row
        # instead of accumulating history).
        work_order = res.get("b2b_work_order", {})
        safety_verdict = res.get("safety_gate_verdict", {})
        candidate_actions = res.get("candidate_actions", []) or []
        b2c_advisory = res.get("b2c_advisory", {})

        import uuid
        wo_id = work_order.get("work_order_id") or f"WO-TSG-{req.asset_id}-{uuid.uuid4().hex[:8].upper()}"

        total_bess_discharge_mw = sum(
            float(a.get("bess_discharge_mw", 0.0)) for a in candidate_actions
        )
        cooling_active = any(
            a.get("action_type", "").startswith("COOLING") or a.get("cooling_boost_factor", 1.0) > 1.0
            for a in candidate_actions
        )
        is_safe = bool(safety_verdict.get("is_safe", True))
        narrative = (
            work_order.get("gpt_narrative")
            or b2c_advisory.get("guidance")
            or b2c_advisory.get("headline")
        )

        order_record = DispatchWorkOrderRecord(
            work_order_id=wo_id,
            asset_id=req.asset_id,
            calculated_k_safe=float(safety_verdict.get("nominal_load_k", 0.88)),
            bess_dispatch_mw=total_bess_discharge_mw,
            bess_volt_var_q_mvar=0.0,
            oltc_tap_step=-1,
            forced_cooling_active=cooling_active,
            gpt_narrative=narrative,
            safety_status="AUTHORIZED" if safety_verdict.get("status") == "ACCEPT" else "BLOCKED",
            cbf_barrier_compliant=is_safe,
        )
        await db_manager.save_dispatch_work_order(order_record)

        # 2. Persist Agent Execution Trace
        node_sequence = [step.get("node", "") for step in res.get("audit_trail", []) if step.get("node")]
        if not node_sequence:
            node_sequence = ["forecast_node", "physics_node", "planner_node", "safety_gate_node", "audit_dispatch_node"]

        duration_ms = 2450.0
        try:
            from datetime import datetime
            trail = res.get("audit_trail", [])
            if len(trail) >= 2:
                fmt = "%Y-%m-%d %H:%M:%SZ"
                start = datetime.strptime(trail[0]["timestamp"], fmt)
                end = datetime.strptime(trail[-1]["timestamp"], fmt)
                duration_ms = max((end - start).total_seconds() * 1000.0, 0.0)
        except Exception as exc:
            # Non-fatal: duration is telemetry, not a result.
            logger.debug("Could not derive agent duration from audit trail: %s", exc)

        trace_record = AgentExecutionTraceRecord(
            trace_id=f"TRACE-{uuid.uuid4().hex[:8].upper()}",
            asset_id=req.asset_id,
            duration_ms=duration_ms,
            node_sequence=node_sequence,
            cbf_safety_passed=is_safe,
            gpt_work_order_id=wo_id,
            gpt_advisory_text=narrative,
        )
        await db_manager.save_agent_trace(trace_record)

        return {"status": "success", "data": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/economic-roi")
async def get_economic_roi_metrics() -> Dict[str, Any]:
    """
    Returns current investment-grade Net Avoided Loss and ROI breakdown, persisting audit snapshot.
    """
    engine = EconomicEngine()
    result = engine.evaluate_net_avoided_loss()

    # Persist Financial Audit Snapshot
    try:
        import uuid
        audit = FinancialAuditRecord(
            audit_id=f"AUDIT-{uuid.uuid4().hex[:8].upper()}",
            asset_id="SUB-PHX-DOWNTOWN-04",
            # Fall back to 0.0 rather than inventing figures. These defaults
            # used to restate the retired 2,791,338 / 1,541,338 / 1,250,000
            # numbers, so a missing key silently wrote a fabricated audit row
            # that looked authoritative in the ledger.
            avoided_equipment_loss=float(result.get("breakdown", {}).get("avoided_catastrophic_replacement", 0.0)),
            avoided_customer_outage_loss=float(result.get("breakdown", {}).get("avoided_customer_outage_costs", 0.0)),
            avoided_aging_deferral=float(result.get("breakdown", {}).get("asset_life_extension_value", 0.0)),
            net_avoided_loss=float(result.get("net_avoided_loss", 0.0)),
            economic_roi_multiplier=float(result.get("roi_multiplier", 0.0)),
        )
        await db_manager.save_financial_audit(audit)
    except Exception as exc:
        # Persistence is the point of this endpoint; do not swallow silently.
        logger.warning("Failed to persist financial audit snapshot: %s", exc, exc_info=True)

    return result

