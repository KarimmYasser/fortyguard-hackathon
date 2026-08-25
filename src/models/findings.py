"""Defensible Finding Pydantic Schemas.

Implements the authoritative "Fact vs. Finding" decision framework from FortyGuard ML leadership (Session 07):
- Transforms raw static temperature measurements ("Substation reached 42.7°C") into defensible findings
  combining:
  1. Raw Fact (measurement, timestamp, location)
  2. Contextual Baseline Comparison (land-cover delta vs unbuilt natural desert, persistence multiplier)
  3. Morphological Causality (canopy deficit, asphalt concentration, building canyon aspect)
  4. Asset Degradation Impact (Arrhenius aging acceleration AF, hot spot rise, insulation life loss)
  5. Actionable Mitigation Finding (pre-cooling window, BESS dispatch MW, net avoided loss in USD)
"""

from __future__ import annotations

from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field
import uuid


class DefensibleFinding(BaseModel):
    """Pydantic model representing an auditable, comparative, and actionable decision finding."""
    id: str = Field(default_factory=lambda: f"FINDING_{uuid.uuid4().hex[:8].upper()}")
    asset_id: str
    asset_name: str
    timestamp_utc: str
    risk_level: Literal["LEVEL_1_SAFE", "LEVEL_2_ELEVATED", "LEVEL_3_CRITICAL"] = "LEVEL_1_SAFE"

    # 1. Raw Fact
    raw_fact: str = Field(..., description="Static measurement fact")
    measured_2m_temp_c: float
    peak_2m_temp_c: float

    # 2. Comparative Baseline
    baseline_reference_name: str = Field(default="South Mountain Natural Desert")
    baseline_temp_c: float = 41.60
    urban_heat_island_delta_c: float = Field(default=1.14, description="Measured urban land-cover delta (°C)")
    continuous_persistence_hours: float = Field(default=12.0, description="Continuous hours above 40°C (P40)")
    persistence_ratio_to_baseline: float = Field(default=3.16, description="Ratio of thermal soak duration vs baseline (e.g. 3.2x)")

    # 3. Morphological Causality
    tree_canopy_pct: float = Field(default=2.1, description="Tree canopy coverage in parcel (%)")
    asphalt_cover_pct: float = Field(default=78.4, description="Asphalt/impervious surface (%)")
    building_aspect_hw: float = Field(default=1.85, description="Urban canyon building H/W aspect ratio")
    cooling_derate_pct: float = Field(default=32.0, description="Radiator convective cooling derate from wind sheltering (%)")
    causality_explanation: str = Field(..., description="Causal attribution from land-cover and urban geometry")

    # 4. Physical Asset Degradation Impact
    winding_hotspot_c: float = Field(..., description="Peak winding hot-spot temperature (°C)")
    arrhenius_aging_acceleration: float = Field(..., description="Arrhenius loss-of-life acceleration factor AF")
    equivalent_aging_hours: float = Field(..., description="Equivalent aging hours incurred during heatwave")
    insulation_life_loss_pct: float = Field(..., description="Percentage of transformer insulation life consumed")
    cbf_safety_margin_pu: float = Field(default=0.98, description="Control Barrier Function safety margin (pu)")

    # 5. Autonomous Mitigation Action
    recommended_action: str = Field(..., description="Recommended control or dispatch action")
    bess_dispatch_mw: float = Field(default=0.0, description="Recommended BESS peak-shaving dispatch (MW)")
    precooling_window_start_utc: str = Field(default="08:00 UTC")
    precooling_window_end_utc: str = Field(default="11:00 UTC")
    net_avoided_loss_usd: float = Field(default=0.0, description="Net avoided financial loss via LBNL ICE framework ($)")
    defensible_narrative: str = Field(..., description="Synthesized executive finding narrative paragraph")


class FindingSynthesisReport(BaseModel):
    """Collection of findings across a monitored portfolio or single scan."""
    total_findings: int
    critical_findings_count: int
    elevated_findings_count: int
    safe_findings_count: int
    findings: List[DefensibleFinding]
    portfolio_summary: str
