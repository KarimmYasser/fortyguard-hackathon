"""
Agentic Dispatch & Economic ROI Router
Triggers the full LangGraph agent pipeline and evaluates investment-grade avoided loss.
"""

from __future__ import annotations

from typing import Any, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.agent.graph import run_thermal_sentinel_agent
from src.physics.economic_model import EconomicEngine

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
    Runs the complete LangGraph StateGraph pipeline for the target asset.
    """
    try:
        res = await run_thermal_sentinel_agent(
            target_city=req.city,
            asset_id=req.asset_id,
            asset_name=req.asset_name,
            location={"lat": req.latitude, "lon": req.longitude},
        )
        return {"status": "success", "data": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/economic-roi")
async def get_economic_roi_metrics() -> Dict[str, Any]:
    """
    Returns current investment-grade Net Avoided Loss and ROI breakdown.
    """
    engine = EconomicEngine()
    return engine.evaluate_net_avoided_loss()
