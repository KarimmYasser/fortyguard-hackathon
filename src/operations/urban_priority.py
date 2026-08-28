"""
Urban Cooling Priority Engine (Mike Stelfox 5-Layer Multiplicative Model)
Translates FortyGuard 2m microclimate intelligence, urban morphology, human exposure,
demographic vulnerability, and plantable ground opportunity into actionable cooling prioritization.

Implements the Multiplicative Risk & Opportunity Doctrine:
    Priority = Thermal Hazard (Layer 1) * Morphological Causes (Layer 2)
             * Human/Asset Exposure (Layer 3) * Social Vulnerability (Layer 4)
             * Actionable Opportunity (Layer 5)
"""

from __future__ import annotations

import math
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class UrbanParcel(BaseModel):
    """Represents an urban parcel, school campus, transit corridor, or infrastructure zone."""
    parcel_id: str = Field(..., description="Unique parcel identifier")
    name: str = Field(..., description="Human-readable zone name (e.g., 'Walker Jones Education Campus')")
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    area_sq_meters: float = Field(default=10000.0, description="Total parcel area in m^2")
    land_use: str = Field(default="mixed_urban", description="Land use type (e.g. 'school_campus', 'transit_hub', 'vacant_parking_lot')")

    # Layer 1: Thermal Conditions (FortyGuard 2m intelligence)
    fortyguard_2m_ambient_c: float = Field(default=41.5, description="FortyGuard 2m ambient air temperature (°C)")
    persistence_hours_p_theta: float = Field(default=6.0, description="Continuous hours above threshold (P_theta)")
    exceedance_degree_hours: float = Field(default=24.0, description="Cumulative degree-hours above baseline (°C·h)")

    # Layer 2: Underlying Physical Causes (Morphology & Land Cover)
    impervious_surface_ratio: float = Field(default=0.75, ge=0.0, le=1.0, description="Fraction of impervious asphalt/concrete")
    tree_canopy_ratio: float = Field(default=0.08, ge=0.0, le=1.0, description="Existing tree canopy fraction")
    surface_albedo: float = Field(default=0.18, ge=0.0, le=1.0, description="Pavement and facade reflectance")
    canyon_height_to_width_hw: float = Field(default=1.5, ge=0.0, description="Street canyon aspect ratio (H/W)")

    # Layer 3: Human & Critical Asset Exposure
    pedestrian_daily_traffic: int = Field(default=500, description="Estimated daily pedestrian foot traffic")
    transit_bus_stops_count: int = Field(default=3, description="Bus stops within 150m walking radius")
    vulnerable_occupants_count: int = Field(default=200, description="Students, seniors, or outdoor workers present")
    critical_grid_assets_count: int = Field(default=1, description="Transformers, switchgear, or BESS units present")

    # Layer 4: Social & Demographic Vulnerability
    asthma_prevalence_percent: float = Field(default=12.0, ge=0.0, le=100.0, description="Local pediatric/adult asthma rate (%)")
    poverty_rate_percent: float = Field(default=20.0, ge=0.0, le=100.0, description="Census tract poverty rate (%)")
    overnight_residential_soak: bool = Field(default=True, description="True if residents sleep on-site during overnight heatwave")
    cdc_social_vulnerability_index_svi: float = Field(default=0.70, ge=0.0, le=1.0, description="CDC Social Vulnerability Index (0-1)")

    # Layer 5: Actionable Opportunity & Feasibility
    plantable_ground_ratio: float = Field(default=0.20, ge=0.0, le=1.0, description="Fraction of parcel viable for tree/vegetation planting")
    public_right_of_way: bool = Field(default=True, description="True if municipal public land or easement (no private variance needed)")
    estimated_cooling_cost_per_sqm: float = Field(default=45.0, description="Cost ($/m^2) for canopy, shade sails, or cool pavements")


class PriorityScoreBreakdown(BaseModel):
    """Detailed mathematical breakdown of the 5-layer multiplicative scoring."""
    hazard_index_l1: float = Field(..., description="Normalized thermal hazard (0.0 to 1.0)")
    morphology_modifier_l2: float = Field(..., description="Morphological heat trapping multiplier (0.5 to 1.8)")
    exposure_index_l3: float = Field(..., description="Human and grid exposure factor (0.05 to 2.5)")
    vulnerability_multiplier_l4: float = Field(..., description="Social & demographic vulnerability multiplier (0.5 to 2.0)")
    opportunity_factor_l5: float = Field(..., description="Plantable feasibility factor (0.05 to 1.0)")
    raw_multiplicative_product: float = Field(..., description="H * M * E * V * O")
    final_priority_score: float = Field(..., description="Normalized 0 to 100 priority score")
    priority_tier: str = Field(..., description="'critical', 'high', 'moderate', or 'low'")
    recommended_interventions: List[str] = Field(..., description="Specific engineering and urban design actions")


class UrbanPriorityResult(BaseModel):
    """Result payload for an urban parcel evaluation."""
    parcel_id: str
    name: str
    land_use: str
    priority_score: float
    priority_tier: str
    rank: int = 1
    breakdown: PriorityScoreBreakdown
    paradox_context: str
    actionable_cooling_area_sqm: float
    estimated_intervention_budget_usd: float


class UrbanPriorityEngine:
    """
    Evaluates urban parcels and infrastructure zones using Mike Stelfox's 5-Layer Multiplicative Model.
    """

    def __init__(
        self,
        baseline_temp_c: float = 35.0,
        extreme_temp_c: float = 45.0,
    ) -> None:
        self.baseline_temp_c = baseline_temp_c
        self.extreme_temp_c = extreme_temp_c

    def evaluate_parcel(self, parcel: UrbanParcel) -> UrbanPriorityResult:
        """Computes the 5-layer priority score and recommendation portfolio for a single parcel."""
        # Layer 1: Thermal Hazard Index (0.0 - 1.0)
        temp_delta = max(0.0, parcel.fortyguard_2m_ambient_c - self.baseline_temp_c)
        temp_range = max(1.0, self.extreme_temp_c - self.baseline_temp_c)
        normalized_temp = min(1.0, temp_delta / temp_range)
        normalized_persistence = min(1.0, parcel.persistence_hours_p_theta / 12.0)
        normalized_exceedance = min(1.0, parcel.exceedance_degree_hours / 48.0)

        hazard_l1 = (
            0.40 * normalized_temp
            + 0.35 * normalized_persistence
            + 0.25 * normalized_exceedance
        )
        hazard_l1 = max(0.05, min(1.0, hazard_l1))

        # Layer 2: Morphology & Land Cover Modifier (0.5 - 1.8)
        # Impervious asphalt increases heat trapping; tree canopy mitigates it.
        canyon_factor = min(0.3, 0.1 * parcel.canyon_height_to_width_hw)
        albedo_penalty = max(0.0, (0.35 - parcel.surface_albedo) * 0.5)
        canopy_benefit = parcel.tree_canopy_ratio * 0.6
        morphology_l2 = 1.0 + (parcel.impervious_surface_ratio * 0.4) - canopy_benefit + albedo_penalty + canyon_factor
        morphology_l2 = max(0.5, min(1.8, morphology_l2))

        # Layer 3: Exposure Index (0.05 - 2.5)
        # Combines pedestrian foot traffic, school/elderly occupants, bus stops, and grid assets
        ped_score = min(0.8, parcel.pedestrian_daily_traffic / 1000.0)
        occupant_score = min(1.0, parcel.vulnerable_occupants_count / 300.0)
        bus_stop_score = min(0.5, parcel.transit_bus_stops_count * 0.12)
        grid_score = min(0.4, parcel.critical_grid_assets_count * 0.20)
        
        exposure_l3 = ped_score + occupant_score + bus_stop_score + grid_score
        exposure_l3 = max(0.05, min(2.5, exposure_l3))

        # Layer 4: Social & Demographic Vulnerability Multiplier (0.5 - 2.0)
        svi_component = parcel.cdc_social_vulnerability_index_svi * 0.5
        asthma_component = min(0.3, (parcel.asthma_prevalence_percent / 25.0) * 0.3)
        poverty_component = min(0.2, (parcel.poverty_rate_percent / 40.0) * 0.2)
        overnight_component = 0.20 if parcel.overnight_residential_soak else 0.0

        vulnerability_l4 = 0.8 + svi_component + asthma_component + poverty_component + overnight_component
        vulnerability_l4 = max(0.5, min(2.0, vulnerability_l4))

        # Layer 5: Actionable Opportunity Factor (0.05 - 1.0)
        plantable_score = min(0.6, (parcel.plantable_ground_ratio / 0.30) * 0.6)
        row_score = 0.40 if parcel.public_right_of_way else 0.15
        opportunity_l5 = plantable_score + row_score
        opportunity_l5 = max(0.05, min(1.0, opportunity_l5))

        # Multiplicative Synthesis
        raw_product = hazard_l1 * morphology_l2 * exposure_l3 * vulnerability_l4 * opportunity_l5
        # Scaling constant mapped to 0-100 scale
        scaled_score = round(min(100.0, raw_product * 45.0), 1)

        if scaled_score >= 70.0:
            tier = "critical"
        elif scaled_score >= 45.0:
            tier = "high"
        elif scaled_score >= 25.0:
            tier = "moderate"
        else:
            tier = "low"

        # Actionable Interventions Strategy
        interventions = self._derive_interventions(parcel, tier)

        # Contextual explanation of the "Empty Parking Lot vs School" paradox
        paradox_note = self._generate_paradox_context(parcel, hazard_l1, exposure_l3, scaled_score)

        actionable_area = round(parcel.area_sq_meters * parcel.plantable_ground_ratio, 1)
        budget = round(actionable_area * parcel.estimated_cooling_cost_per_sqm, 2)

        breakdown = PriorityScoreBreakdown(
            hazard_index_l1=round(hazard_l1, 3),
            morphology_modifier_l2=round(morphology_l2, 3),
            exposure_index_l3=round(exposure_l3, 3),
            vulnerability_multiplier_l4=round(vulnerability_l4, 3),
            opportunity_factor_l5=round(opportunity_l5, 3),
            raw_multiplicative_product=round(raw_product, 4),
            final_priority_score=scaled_score,
            priority_tier=tier,
            recommended_interventions=interventions,
        )

        return UrbanPriorityResult(
            parcel_id=parcel.parcel_id,
            name=parcel.name,
            land_use=parcel.land_use,
            priority_score=scaled_score,
            priority_tier=tier,
            rank=1,
            breakdown=breakdown,
            paradox_context=paradox_note,
            actionable_cooling_area_sqm=actionable_area,
            estimated_intervention_budget_usd=budget,
        )

    def rank_parcels(self, parcels: List[UrbanParcel]) -> List[UrbanPriorityResult]:
        """Evaluates and ranks a portfolio of urban parcels by final priority score."""
        results = [self.evaluate_parcel(p) for p in parcels]
        results.sort(key=lambda r: -r.priority_score)
        for idx, item in enumerate(results, start=1):
            item.rank = idx
        return results

    def _derive_interventions(self, parcel: UrbanParcel, tier: str) -> List[str]:
        actions: List[str] = []
        if parcel.tree_canopy_ratio < 0.15 and parcel.plantable_ground_ratio > 0.10:
            actions.append(f"Targeted tree canopy expansion on {round(parcel.area_sq_meters * parcel.plantable_ground_ratio):,} m² plantable ground")
        if parcel.transit_bus_stops_count > 0:
            actions.append(f"Deploy active transit shelter shade canopies across {parcel.transit_bus_stops_count} bus stops within 150m")
        if parcel.surface_albedo < 0.25 and parcel.impervious_surface_ratio > 0.60:
            actions.append("High-albedo cool pavement coating retrofit (albedo 0.15 -> 0.45)")
        if parcel.critical_grid_assets_count > 0:
            actions.append("Substation & electrical asset micro-misting and solar fin radiation shielding")
        if parcel.vulnerable_occupants_count > 100:
            actions.append(f"Protected pedestrian cooling corridor connecting school/residential facilities ({parcel.vulnerable_occupants_count} occupants)")
        if not actions:
            actions.append("Routine microclimate monitoring and passive vegetation preservation")
        return actions

    def _generate_paradox_context(self, parcel: UrbanParcel, hazard: float, exposure: float, score: float) -> str:
        if exposure > 0.8 and score >= 50.0:
            return (
                f"High-Impact Priority: Despite convective air hazard {parcel.fortyguard_2m_ambient_c}°C, "
                f"dense human exposure ({parcel.vulnerable_occupants_count} occupants, {parcel.transit_bus_stops_count} bus stops) "
                f"and {round(parcel.plantable_ground_ratio * 100)}% plantable feasibility make this an optimal intervention parcel."
            )
        elif exposure < 0.2 and parcel.fortyguard_2m_ambient_c > 42.0:
            return (
                f"Empty Hotspot Filtered: High surface temperature ({parcel.fortyguard_2m_ambient_c}°C) "
                f"de-prioritized due to near-zero human occupancy and lack of public right-of-way."
            )
        else:
            return f"Standard urban parcel with balanced exposure and thermal conditions (Priority Score: {score}/100)."
