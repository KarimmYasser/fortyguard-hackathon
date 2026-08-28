"""
Unit tests for Mike Stelfox 5-Layer Multiplicative Urban Priority Engine.
"""

import pytest
from src.operations.urban_priority import (
    UrbanParcel,
    UrbanPriorityEngine,
    UrbanPriorityResult,
)


def test_walker_jones_vs_empty_parking_lot_paradox():
    """
    Validates Mike Stelfox's core thesis:
    An educational campus with vulnerable students and bus stops (Walker Jones) must
    rank significantly higher in intervention priority than an uninhabited vacant asphalt
    parking lot, even if the parking lot has higher raw temperature.
    """
    engine = UrbanPriorityEngine(baseline_temp_c=35.0, extreme_temp_c=45.0)

    # 1. Walker Jones Education Campus (Real DC Case Study from Session 13)
    walker_jones = UrbanParcel(
        parcel_id="DC_WALKER_JONES_01",
        name="Walker Jones Education Campus",
        latitude=38.9032,
        longitude=-77.0162,
        area_sq_meters=44.0 * 4046.86,  # ~44 acres in m2
        land_use="school_campus",
        fortyguard_2m_ambient_c=40.8,
        persistence_hours_p_theta=7.5,
        exceedance_degree_hours=32.0,
        impervious_surface_ratio=0.79,
        tree_canopy_ratio=0.08,
        surface_albedo=0.18,
        canyon_height_to_width_hw=1.4,
        pedestrian_daily_traffic=1200,
        transit_bus_stops_count=5,
        vulnerable_occupants_count=418,  # 418 students
        critical_grid_assets_count=2,
        asthma_prevalence_percent=18.5,
        poverty_rate_percent=31.0,
        overnight_residential_soak=True,
        cdc_social_vulnerability_index_svi=0.88,
        plantable_ground_ratio=0.20,
        public_right_of_way=True,
    )

    # 2. Empty Industrial Asphalt Parking Lot (Hotter, but zero people)
    empty_parking_lot = UrbanParcel(
        parcel_id="DC_VACANT_ASPHALT_02",
        name="Vacant Industrial Storage Yard",
        latitude=38.9180,
        longitude=-76.9950,
        area_sq_meters=20000.0,
        land_use="vacant_parking_lot",
        fortyguard_2m_ambient_c=44.2,  # 3.4°C hotter raw temperature!
        persistence_hours_p_theta=9.0,
        exceedance_degree_hours=42.0,
        impervious_surface_ratio=0.98,
        tree_canopy_ratio=0.01,
        surface_albedo=0.12,
        canyon_height_to_width_hw=0.2,
        pedestrian_daily_traffic=10,  # Empty
        transit_bus_stops_count=0,
        vulnerable_occupants_count=0,  # Zero students/seniors
        critical_grid_assets_count=0,
        asthma_prevalence_percent=5.0,
        poverty_rate_percent=5.0,
        overnight_residential_soak=False,
        cdc_social_vulnerability_index_svi=0.20,
        plantable_ground_ratio=0.02,
        public_right_of_way=False,
    )

    result_school = engine.evaluate_parcel(walker_jones)
    result_parking = engine.evaluate_parcel(empty_parking_lot)

    # Walker Jones must have a substantially higher priority score despite lower raw temperature
    assert result_school.priority_score > result_parking.priority_score
    assert result_school.priority_tier in ("critical", "high")
    assert result_parking.priority_tier in ("moderate", "low")

    # Verify exposure & vulnerability factors
    assert result_school.breakdown.exposure_index_l3 > result_parking.breakdown.exposure_index_l3 * 3.0
    assert result_school.breakdown.opportunity_factor_l5 > result_parking.breakdown.opportunity_factor_l5

    # Check that actionable interventions include tree canopy & bus stop shading
    assert any("tree canopy expansion" in act.lower() for act in result_school.breakdown.recommended_interventions)
    assert any("bus stop" in act.lower() for act in result_school.breakdown.recommended_interventions)


def test_portfolio_ranking_and_budget_calculation():
    """Tests multi-parcel ranking and financial budget estimation."""
    engine = UrbanPriorityEngine()

    parcels = [
        UrbanParcel(
            parcel_id="P1",
            name="Downtown Commercial Plaza",
            latitude=38.90,
            longitude=-77.03,
            area_sq_meters=15000.0,
            pedestrian_daily_traffic=3000,
            vulnerable_occupants_count=50,
            plantable_ground_ratio=0.10,
        ),
        UrbanParcel(
            parcel_id="P2",
            name="Public Senior Housing Complex",
            latitude=38.89,
            longitude=-77.01,
            area_sq_meters=25000.0,
            pedestrian_daily_traffic=600,
            vulnerable_occupants_count=350,
            plantable_ground_ratio=0.25,
            asthma_prevalence_percent=22.0,
            cdc_social_vulnerability_index_svi=0.92,
        ),
        UrbanParcel(
            parcel_id="P3",
            name="Abandoned Rail Corridor",
            latitude=38.92,
            longitude=-76.98,
            area_sq_meters=50000.0,
            pedestrian_daily_traffic=5,
            vulnerable_occupants_count=0,
            plantable_ground_ratio=0.50,
            public_right_of_way=False,
        ),
    ]

    ranked = engine.rank_parcels(parcels)
    assert len(ranked) == 3
    assert ranked[0].rank == 1
    assert ranked[1].rank == 2
    assert ranked[2].rank == 3
    assert ranked[0].priority_score >= ranked[1].priority_score >= ranked[2].priority_score

    # Check budget math
    for item in ranked:
        assert item.estimated_intervention_budget_usd > 0.0
        assert item.actionable_cooling_area_sqm > 0.0


def test_edge_case_zero_opportunity():
    """Ensures parcels with zero plantable opportunity are properly penalized in feasibility."""
    engine = UrbanPriorityEngine()
    parcel = UrbanParcel(
        parcel_id="P_ZERO_OPP",
        name="Fully Paved Private Rooftop",
        latitude=38.90,
        longitude=-77.00,
        plantable_ground_ratio=0.0,
        public_right_of_way=False,
    )
    result = engine.evaluate_parcel(parcel)
    assert result.breakdown.opportunity_factor_l5 <= 0.20
    assert result.actionable_cooling_area_sqm == 0.0
    assert result.estimated_intervention_budget_usd == 0.0
