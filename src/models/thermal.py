"""
Thermal and Physical State Data Models
Pydantic schemas for IEEE C57.91 / IEC 60076-7 thermal state estimation,
environmental boundary conditions, and insulation degradation metrics.
"""

from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class TransformerThermalParams(BaseModel):
    """IEEE C57.91 / IEC 60076-7 Rated Transformer Parameters."""
    tau_o: float = Field(default=2.5, description="Top-oil thermal time constant (hours)")
    tau_w: float = Field(default=0.1, description="Winding hot-spot thermal time constant (hours, ~6 min)")
    delta_theta_or: float = Field(default=50.0, description="Rated-load top-oil rise above ambient (°C)")
    delta_theta_wr: float = Field(default=25.0, description="Rated-load winding gradient over top oil (°C)")
    R: float = Field(default=5.0, description="Ratio of load loss to no-load loss at rated load")
    n: float = Field(default=0.8, description="Top-oil cooling exponent (0.8 for ONAN)")
    m: float = Field(default=0.8, description="Winding cooling exponent (0.8 for ONAN)")
    
    # Solar parameters
    alpha_abs: float = Field(default=0.80, description="Surface solar absorptivity")
    A_proj: float = Field(default=2.5, description="Projected solar exposure area (m^2)")
    A_surf: float = Field(default=45.0, description="Total tank & radiator fin convective surface area (m^2)")
    F_view: float = Field(default=0.60, description="Sky/solar view factor")
    h_eff: float = Field(default=12.0, description="Convective heat transfer coefficient (W/m^2·K)")

    # Safety limits
    t_o_max_c: float = Field(default=110.0, description="Maximum continuous top-oil limit (°C)")
    t_hs_max_c: float = Field(default=140.0, description="Emergency winding hot-spot limit (°C)")
    t_hs_warn_c: float = Field(default=120.0, description="Warning winding hot-spot threshold (°C)")


class ThermalStepState(BaseModel):
    """Single discrete-time physical state output."""
    timestamp: str
    hour_index: int
    t_ambient_2m_c: float
    t_solar_increment_c: float
    t_ambient_eff_c: float
    load_ratio_k: float
    theta_o_c: float
    theta_w_c: float
    t_top_oil_c: float
    t_hot_spot_c: float
    aging_acceleration_factor_v: float
    cumulative_loss_of_life_hours: float
    cooling_derate_eta: float = 1.0


class ThermalTrajectory(BaseModel):
    """Full 12-hour forward physical trajectory."""
    asset_id: str
    steps: List[ThermalStepState]
    peak_top_oil_c: float
    peak_hot_spot_c: float
    peak_aging_acceleration_v: float
    total_loss_of_life_hours: float
    thermal_soak_index_tsi: float
    top_oil_response_ratio: float
    winding_response_ratio: float
    breached_hot_spot_ceiling: bool
    breached_top_oil_ceiling: bool
