"""
FastAPI Routes for AC Distribution Feeder Power Flow & Grid Network
"""

from __future__ import annotations

from typing import Dict, Any, Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field

from src.physics.power_flow import DistributionPowerFlowEngine

router = APIRouter(prefix="/api/v1/power-flow", tags=["AC Power Flow Network"])


class PowerFlowSolveRequest(BaseModel):
    """Parameters for AC power flow solve request."""
    substation_slack_v_pu: float = Field(default=1.03, ge=0.90, le=1.10)
    tx_load_multiplier_k: float = Field(default=1.18, ge=0.30, le=1.80)
    bess_discharge_mw: float = Field(default=0.0, ge=0.0, le=25.0)
    bess_volt_var_q_mvar: float = Field(default=0.0, ge=0.0, le=15.0)
    oltc_tap_position: int = Field(default=4, ge=-16, le=16)
    soil_resistivity_rho: float = Field(default=1.0, ge=0.5, le=3.0)


@router.post("/solve")
async def solve_feeder_power_flow(req: PowerFlowSolveRequest) -> Dict[str, Any]:
    """
    Solves AC power flow on the 4-bus distribution feeder under dynamic loading and BESS dispatch.
    """
    engine = DistributionPowerFlowEngine(oltc_tap=req.oltc_tap_position)
    solution = engine.solve_power_flow(
        substation_slack_v_pu=req.substation_slack_v_pu,
        tx_load_multiplier_k=req.tx_load_multiplier_k,
        bess_discharge_mw=req.bess_discharge_mw,
        bess_volt_var_q_mvar=req.bess_volt_var_q_mvar,
        soil_resistivity_rho=req.soil_resistivity_rho,
    )
    return solution.model_dump()


@router.get("/feeder-solution")
async def get_default_feeder_solution() -> Dict[str, Any]:
    """
    Returns the nominal AC power flow solution for the Phoenix Central Substation & Hospital Feeder.
    """
    engine = DistributionPowerFlowEngine(oltc_tap=4)
    solution = engine.solve_power_flow()
    return solution.model_dump()
