"""
Unit tests for Human Comfort & Mean Radiant Temperature (MRT) Physics Engine.
"""

import pytest
from src.physics.human_comfort import (
    HumanComfortEngine,
    MicroclimateInput,
    ComfortMetrics,
    ShadingInterventionComparison,
)


def test_mrt_and_utci_unshaded_sun_baseline():
    """
    Validates that in full summer direct sun (850 W/m^2 solar, 41.5°C air),
    radiant heat flux causes Mean Radiant Temperature (MRT) to spike 15-25°C above ambient air,
    driving UTCI into 'very_strong_heat_stress' or 'extreme_heat_stress'.
    """
    engine = HumanComfortEngine()
    baseline = MicroclimateInput(
        fortyguard_2m_ambient_c=41.5,
        relative_humidity_pct=25.0,
        wind_speed_2m_m_s=1.2,
        solar_irradiance_w_m2=850.0,
        surface_albedo=0.15,  # Dark asphalt
        tree_canopy_cover_pct=5.0,
        artificial_shade_fraction=0.0,
        canyon_height_to_width_hw=1.4,
    )

    metrics = engine.evaluate_comfort(baseline)

    # MRT should be substantially higher than 2m dry-bulb air temperature
    assert metrics.mean_radiant_temp_mrt_c > baseline.fortyguard_2m_ambient_c + 15.0
    assert metrics.utci_temp_c > 42.0
    assert metrics.utci_stress_category in ("extreme_heat_stress", "very_strong_heat_stress")
    assert metrics.max_safe_continuous_work_minutes <= 30
    assert metrics.estimated_wet_bulb_c > 20.0


def test_shading_intervention_physics_proof():
    """
    Validates Mike Stelfox's core thesis:
    Deploying shade canopies and tree canopies moves 2m air temp only marginally (-0.35°C),
    but slashes Mean Radiant Temperature by >12°C and UTCI by >4°C.
    """
    engine = HumanComfortEngine()
    baseline = MicroclimateInput(
        fortyguard_2m_ambient_c=42.0,
        relative_humidity_pct=20.0,
        wind_speed_2m_m_s=1.5,
        solar_irradiance_w_m2=900.0,
        surface_albedo=0.14,
        tree_canopy_cover_pct=8.0,
        artificial_shade_fraction=0.0,
    )

    comp = engine.simulate_cooling_intervention(
        baseline=baseline,
        added_canopy_pct=25.0,
        added_shade_fraction=0.55,
        cool_pavement_albedo=0.45,
    )

    # Air temperature change is modest
    assert abs(comp.delta_air_temp_c) < 1.0

    # MRT and UTCI reductions are substantial
    assert comp.intervened_mrt_c < comp.baseline_mrt_c - 12.0
    assert comp.intervened_utci_c < comp.baseline_utci_c - 4.0
    assert comp.radiant_flux_reduction_w_m2 > 300.0
    assert "Physical Proof" in comp.human_experience_finding


def test_nocturnal_baseline_no_solar():
    """Validates that at night (zero solar irradiance), MRT reflects nocturnal clear-sky radiative cooling."""
    engine = HumanComfortEngine()
    night_input = MicroclimateInput(
        fortyguard_2m_ambient_c=32.0,
        relative_humidity_pct=40.0,
        wind_speed_2m_m_s=2.0,
        solar_irradiance_w_m2=0.0,  # Night
        surface_albedo=0.15,
        tree_canopy_cover_pct=10.0,
    )

    metrics = engine.evaluate_comfort(night_input)
    # At night without solar radiation, MRT is governed purely by longwave ground and clear-sky radiation (~26-30°C)
    assert 24.0 <= metrics.mean_radiant_temp_mrt_c <= 32.0
    assert metrics.effective_solar_flux_absorbed_w_m2 == 0.0
    assert metrics.utci_stress_category == "comfortable"



def test_stull_wet_bulb_accuracy():
    """Validates psychrometric wet-bulb temperature against standard meteorological benchmarks."""
    engine = HumanComfortEngine()
    # At 40°C and 20% RH, wet-bulb is approximately 21.0 - 22.5°C
    tw = engine.calculate_stull_wet_bulb(temp_c=40.0, rh_pct=20.0)
    assert 20.0 <= tw <= 23.0
