"""Commercial Early Adopter Archetypes & COCO Customer Discovery Framework.

Directly implements the Product-Market Fit validation strategy from Thamir (Session 08):
- Bridges FortyGuard microclimate intelligence to agile early adopters who feel immediate financial pain.
- Provides 4 pre-configured commercial archetypes (Solar Farm, Data Center, Hospital, Utility Substation).
- Implements the COCO Customer Discovery structure (Context, Outcomes, Constraints, Options)
  to generate auditable executive risk briefs and commercial pricing proposals.
"""

from __future__ import annotations

from typing import Dict, List, Literal, Optional, Any
from pydantic import BaseModel, Field


class CommercialArchetype(BaseModel):
    """Pydantic model representing a targeted commercial customer segment and its physical/economic parameters."""
    sector_id: Literal["SOLAR_FARM", "DATA_CENTER", "HOSPITAL_FEEDER", "UTILITY_SUBSTATION"]
    title: str
    icon: str
    badge_color: str
    target_buyer_title: str
    target_buyer_persona: str
    acute_pain_point: str

    # Physical Asset Nameplate & Boundary Limits
    nameplate_capacity_mva: float
    inverter_derating_temp_c: float
    critical_thermal_ceiling_c: float
    baseline_load_k: float
    bess_capacity_mwh: float
    voll_rate_per_kwh: float
    typical_capital_replacement_cost_usd: float
    cooling_derate_hw_ratio: float
    soil_resistivity_k_m_w: float

    # COCO Customer Discovery Framework (Session 08)
    coco_context: str = Field(..., description="1. Context: Macro operational environment & heat exposure")
    coco_outcomes: str = Field(..., description="2. Outcomes: Exact success metrics & key results")
    coco_constraints: str = Field(..., description="3. Constraints: Legacy manual workarounds & friction")
    coco_options: str = Field(..., description="4. Options: Willingness-to-pay & software-only implementation")

    # Commercial Valuation & ROI
    monthly_saas_tier_usd: float
    projected_avoided_loss_usd: float
    roi_multiplier: float


# Catalog of the 4 standard commercial archetypes
COMMERCIAL_ARCHETYPES_CATALOG: Dict[str, CommercialArchetype] = {
    "SOLAR_FARM": CommercialArchetype(
        sector_id="SOLAR_FARM",
        title="Utility-Scale Solar & BESS Farm",
        icon="Sun",
        badge_color="#F59E0B",
        target_buyer_title="Solar Asset Operations & Yield Manager",
        target_buyer_persona="Independent Power Producer (IPP) operating 25-100 MW solar+storage assets in Sunbelt / MENA",
        acute_pain_point="Inverter thermal derating at 45°C ambient air, clipping peak midday generation export and losing $12k-$35k/day in feed-in revenue.",
        nameplate_capacity_mva=25.0,
        inverter_derating_temp_c=45.0,
        critical_thermal_ceiling_c=50.0,
        baseline_load_k=0.92,
        bess_capacity_mwh=10.0,
        voll_rate_per_kwh=4.50,
        typical_capital_replacement_cost_usd=850000.0,
        cooling_derate_hw_ratio=0.30,
        soil_resistivity_k_m_w=1.80,
        coco_context="Utility-scale PV strings and central inverters operating in unshaded 45°C+ desert boundary layers with intense solar irradiance (>950 W/m²).",
        coco_outcomes="Eliminate thermal clipping trips, maximize MWh export delivery during peak PPA pricing windows, and maintain BESS cells below 50°C thermal runaway ceiling.",
        coco_constraints="Current practice is reactive derating by inverter firmware, cutting power by 2.5% per °C above 45°C without predictive pre-cooling.",
        coco_options="Deploy Thermal Sentinel Grid API hooks on existing SCADA gateways to schedule morning BESS charge-cooling and dynamically tilt trackers during peak heat.",
        monthly_saas_tier_usd=1490.0,
        projected_avoided_loss_usd=485000.0,
        roi_multiplier=325.5,
    ),
    "DATA_CENTER": CommercialArchetype(
        sector_id="DATA_CENTER",
        title="High-Density AI Data Center Chiller Yard",
        icon="Server",
        badge_color="#8B5CF6",
        target_buyer_title="VP of Mission-Critical Facilities & Infrastructure",
        target_buyer_persona="Enterprise colocation and AI cloud data center operators running 50-100 kW per rack densities",
        acute_pain_point="Outdoor chiller yard convective aerodynamic throttling in dense urban heat islands, degrading PUE from 1.15 to >1.45 and risking compute thermal throttling.",
        nameplate_capacity_mva=75.0,
        inverter_derating_temp_c=46.0,
        critical_thermal_ceiling_c=52.0,
        baseline_load_k=0.85,
        bess_capacity_mwh=20.0,
        voll_rate_per_kwh=25.00,
        typical_capital_replacement_cost_usd=3200000.0,
        cooling_derate_hw_ratio=1.90,
        soil_resistivity_k_m_w=2.20,
        coco_context="Enclosed chiller yards and rooftop cooling towers trapped in deep urban street canyons with 32% convective airflow stagnation during 12-hour heatwaves.",
        coco_outcomes="Maintain PUE SLA < 1.20, prevent chiller stage-3 compressor trips, and avoid $2.5M in SLA outage penalties for tier-IV enterprise customers.",
        coco_constraints="Chiller plant controllers only respond to immediate outdoor wet-bulb sensors, unable to predict 12-hour canyon heat persistence.",
        coco_options="Thermal Sentinel Grid multi-agent orchestration of thermal ice-storage pre-cooling at 08:00 AM off-peak, shifting 8.5 MW cooling load ahead of peak heat.",
        monthly_saas_tier_usd=4950.0,
        projected_avoided_loss_usd=2150000.0,
        roi_multiplier=434.3,
    ),
    "HOSPITAL_FEEDER": CommercialArchetype(
        sector_id="HOSPITAL_FEEDER",
        title="Critical Healthcare Center Feeder",
        icon="Activity",
        badge_color="#EF4444",
        target_buyer_title="Director of Plant Operations & Healthcare Facilities",
        target_buyer_persona="Regional trauma medical centers and university teaching hospitals with strict Joint Commission power quality mandates",
        acute_pain_point="Substation feeder transformer overheating during summer heatwaves, causing voltage fluctuations and triggering emergency diesel generator transfer switches.",
        nameplate_capacity_mva=15.0,
        inverter_derating_temp_c=40.0,
        critical_thermal_ceiling_c=48.0,
        baseline_load_k=0.75,
        bess_capacity_mwh=8.0,
        voll_rate_per_kwh=50.00,
        typical_capital_replacement_cost_usd=1200000.0,
        cooling_derate_hw_ratio=1.10,
        soil_resistivity_k_m_w=1.60,
        coco_context="Dedicated 15 MVA hospital substation step-down transformers operating near emergency vehicle asphalt bays with constant 24/7 medical ICU load.",
        coco_outcomes="Zero voltage violations outside ANSI C84.1 Range A (0.95-1.05 pu), zero unforced diesel transfer switches, and 100% equipment life preservation.",
        coco_constraints="Hospital engineers cannot afford any risk of power interruption; switching solutions must be non-intrusive software with deterministic safety bounds.",
        coco_options="Thermal Sentinel Grid CBF-gated autonomous Volt/VAR tap regulation and 3.0 MW BESS peak injection during 13:00-17:00 thermal peaks.",
        monthly_saas_tier_usd=2490.0,
        projected_avoided_loss_usd=1820000.0,
        roi_multiplier=730.9,
    ),
    "UTILITY_SUBSTATION": CommercialArchetype(
        sector_id="UTILITY_SUBSTATION",
        title="Municipal Distribution Substation",
        icon="Zap",
        badge_color="#06B6D4",
        target_buyer_title="Substation Reliability & Asset Management Lead",
        target_buyer_persona="Investor-owned electric utilities (APS, ConEd, ERCOT, DEWA) managing 500+ distribution substations",
        acute_pain_point="Unmeasured 2-meter asphalt thermal soak accelerating Arrhenius transformer paper degradation by 88x and risking catastrophic $1.5M blowout fires.",
        nameplate_capacity_mva=50.0,
        inverter_derating_temp_c=42.0,
        critical_thermal_ceiling_c=55.0,
        baseline_load_k=1.00,
        bess_capacity_mwh=10.0,
        voll_rate_per_kwh=12.50,
        typical_capital_replacement_cost_usd=1500000.0,
        cooling_derate_hw_ratio=1.85,
        soil_resistivity_k_m_w=2.45,
        coco_context="Downtown Phoenix core substation surrounded by 78.4% asphalt cover, enduring 12 continuous hours above 40°C air temperature.",
        coco_outcomes="Avoid catastrophic $1.5M transformer replacement, prevent 180 MWh customer blackout ($2.25M VoLL consequence), and extend fleet operating life by 374+ equivalent hours.",
        coco_constraints="SCADA systems are reactive (alarming at 135°C when failure is locked in); airport weather stations 10 miles away miss street-level microclimate.",
        coco_options="Deploy Thermal Sentinel Grid across all high-risk urban substations with 12-hour proactive radiator pre-cooling and 5.0 MW BESS peak-shaving dispatch.",
        monthly_saas_tier_usd=3500.0,
        projected_avoided_loss_usd=2576849.0,
        roi_multiplier=736.2,
    ),
}


class COCOExecutiveBrief(BaseModel):
    """Structured COCO Customer Discovery & Commercial Proposal Brief."""
    brief_id: str
    target_sector: str
    title: str
    buyer_persona: str
    prepared_for: str
    generation_date_utc: str
    
    # 4 Pillars
    context_statement: str
    outcomes_statement: str
    constraints_statement: str
    options_statement: str
    
    # Quantitative Risk Assessment
    monitored_assets_count: int
    total_nameplate_mva: float
    peak_ambient_thermal_soak_hours: float
    max_winding_hotspot_unmitigated_c: float
    capped_winding_hotspot_mitigated_c: float
    insulation_aging_reduction_pct: float
    
    # Commercial Economics
    annual_saas_subscription_usd: float
    gross_avoided_outage_loss_usd: float
    net_customer_roi_multiplier: float
    payback_period_days: float
    executive_recommendation: str
