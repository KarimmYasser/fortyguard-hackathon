"""
Pytest Suite for Advanced Mathematical Physics & Reliability Engines
Tests IEEE Std 738 DLR, BESS Electro-Thermal ODEs, Weibull Hazard, and Chance-Constrained OPF.
"""

import pytest
from src.physics.dynamic_line_rating import DynamicLineRatingEngine, ConductorSpecification
from src.physics.bess_electro_thermal import BESSElectroThermalEngine, BESSContainerSpecification
from src.physics.weibull_hazard import ArrheniusWeibullHazardEngine
from src.physics.chance_constrained_opf import ChanceConstrainedOPFEngine, CC_OPF_Request


def test_dynamic_line_rating_heat_balance():
    """Verifies IEEE 738 steady-state heat balance and ampacity solver."""
    engine = DynamicLineRatingEngine()
    sol = engine.evaluate_line(
        current_amps=800.0,
        t_ambient_c=45.0,
        wind_speed_m_per_s=1.5,
        wind_angle_deg=90.0,
        solar_irradiance_w_per_m2=950.0,
    )
    assert sol.conductor_temp_c > 45.0
    assert sol.max_dynamic_ampacity_amps > 500.0
    assert sol.ground_clearance_m > 0.0
    assert sol.catenary_sag_m > 3.0
    assert sol.status in ("SAFE", "WARNING_SAG", "THERMAL_OVERLOAD")


def test_dynamic_line_rating_wind_sensitivity():
    """Verifies that higher wind speed enhances convective cooling and raises dynamic ampacity."""
    engine = DynamicLineRatingEngine()
    sol_low_wind = engine.evaluate_line(current_amps=800.0, t_ambient_c=45.0, wind_speed_m_per_s=0.5)
    sol_high_wind = engine.evaluate_line(current_amps=800.0, t_ambient_c=45.0, wind_speed_m_per_s=4.0)

    assert sol_high_wind.max_dynamic_ampacity_amps > sol_low_wind.max_dynamic_ampacity_amps
    assert sol_high_wind.conductor_temp_c < sol_low_wind.conductor_temp_c


def test_bess_electro_thermal_ode_integration():
    """Verifies 2-state thermal ODE conservation and SEI degradation calculation."""
    engine = BESSElectroThermalEngine()
    ambients = [40.0, 44.0, 48.0, 46.0]
    dispatches = [4.0, 8.0, 6.0, 2.0]

    results = engine.simulate_dispatch_trajectory(
        ambient_temps_c=ambients,
        dispatch_powers_mw=dispatches,
        initial_soc=0.90,
        initial_core_temp_c=35.0,
    )
    assert len(results) == 4
    # Core temperature should rise under high dispatch and ambient heat
    assert results[1].core_temp_c > results[0].core_temp_c
    # SOH should slightly decrease monotonically
    assert results[-1].state_of_health_pct < 100.0
    assert results[-1].cumulative_capacity_loss_pct > 0.0
    assert results[-1].state_of_charge_pct < 90.0


def test_weibull_hazard_cascading_risk():
    """Verifies time-dependent Weibull hazard integration and cascading blackout risk."""
    engine = ArrheniusWeibullHazardEngine()
    unmitigated_report = engine.evaluate_grid_cascading_risk(
        transformer_temp_trajectory=[100.0, 120.0, 142.0, 150.0, 135.0],
        cable_temp_trajectory=[75.0, 88.0, 102.0, 108.0, 95.0],
        line_temp_trajectory=[60.0, 72.0, 85.0, 88.0, 75.0],
        is_mitigated=False,
    )
    mitigated_report = engine.evaluate_grid_cascading_risk(
        transformer_temp_trajectory=[95.0, 105.0, 120.0, 134.0, 125.0],
        cable_temp_trajectory=[68.0, 75.0, 82.0, 86.0, 80.0],
        line_temp_trajectory=[55.0, 62.0, 68.0, 72.0, 65.0],
        is_mitigated=True,
    )
    assert unmitigated_report.system_cascading_risk_pct > mitigated_report.system_cascading_risk_pct
    assert unmitigated_report.economic_loss_risk_usd >= mitigated_report.economic_loss_risk_usd
    assert len(unmitigated_report.assets) == 3


def test_chance_constrained_opf_solution():
    """Verifies Second-Order Cone chance-constrained power flow feasibility."""
    engine = ChanceConstrainedOPFEngine()
    req = CC_OPF_Request(
        base_ambient_temp_c=47.6,
        forecast_std_dev_c=1.85,
        confidence_level_pct=95.0,
        total_grid_load_mw=22.8,
        total_grid_load_mvar=6.8,
        bess_max_power_mw=8.0,
    )
    sol = engine.solve_cc_opf(req)
    assert sol.converged is True
    assert sol.quantile_z_score == 1.645
    assert sol.worst_case_ambient_temp_c > 47.6
    assert sol.optimal_bess_active_mw > 0.0
    assert len(sol.buses) == 4
    assert len(sol.branches) == 3
    assert sol.min_voltage_lower_bound_pu >= 0.90
