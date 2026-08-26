"""
Safety Gate and Control Barrier Function Data Models
Pydantic schemas for deterministic safety checking, constraint certificates,
and projected safe operating parameters (K_safe).
"""

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class SafetyStatus(str, Enum):
    ACCEPT = "ACCEPT"    # Plan passes all physical constraints
    MODIFY = "MODIFY"    # Plan requires projection onto safe envelope K_safe
    REJECT = "REJECT"    # Plan violates unrecoverable constraints (e.g. N-1 critical failure)


class ActionType(str, Enum):
    COOLING_STAGE_1 = "COOLING_STAGE_1"        # Low-speed auxiliary cooling fans
    COOLING_STAGE_2 = "COOLING_STAGE_2"        # Forced oil pumps & high-speed fans
    BESS_PEAK_SHAVING = "BESS_PEAK_SHAVING"    # Discharge BESS to absorb transformer load
    EV_SMART_CURTAIL = "EV_SMART_CURTAIL"      # Defer/throttle EV charging cluster
    LOAD_TRANSFER_N1 = "LOAD_TRANSFER_N1"      # Transfer non-critical feeder load to adjacent substation
    DEMAND_RESPONSE = "DEMAND_RESPONSE"        # Commercial HVAC setpoint modulation


class MitigationAction(BaseModel):
    action_type: ActionType
    target_asset_id: str
    target_hour_start: int
    target_hour_end: int
    power_delta_mw: float = Field(default=0.0, description="Load reduction in MW")
    load_ratio_delta_k: float = Field(default=0.0, description="Per-unit load reduction")
    cooling_boost_factor: float = Field(default=1.0, description="Enhancement to convective cooling")
    bess_discharge_mw: float = Field(default=0.0)
    estimated_cost_usd: float = Field(default=0.0)


class SafetyGateVerdict(BaseModel):
    """Complete model preflight verdict from the non-LLM trajectory gate."""
    status: SafetyStatus
    is_safe: bool
    hot_spot_compliant: bool
    top_oil_compliant: bool
    voltage_compliant: bool
    n_minus_one_compliant: bool
    bess_reserve_compliant: bool

    projected_peak_hot_spot_c: float
    projected_peak_top_oil_c: float
    voltage_pu_min: float
    voltage_pu_max: float
    bess_min_soc_pct: float

    nominal_load_k: float
    safe_max_load_k: float = Field(
        ...,
        description="Projected maximum permissible load ratio under configured model constraints"
    )
    violations: List[str] = Field(default_factory=list)
    mitigation_adjustments: List[str] = Field(default_factory=list)
    barrier_slack_delta: float = 0.0
    audit_timestamp: str = ""
