import pytest
from src.physics.power_flow import DistributionPowerFlowEngine


def test_power_flow_nominal_solution():
    engine = DistributionPowerFlowEngine(oltc_tap=4)  # +2.5% boost
    sol = engine.solve_power_flow(
        substation_slack_v_pu=1.03,
        tx_load_multiplier_k=1.0,
        bess_discharge_mw=0.0,
        bess_volt_var_q_mvar=0.0,
    )

    assert sol.converged is True
    assert len(sol.buses) == 4
    assert len(sol.branches) == 3
    assert sol.ansi_c84_envelope_compliant is True
    # Hospital bus voltage must be within ANSI C84.1 Range A (0.95 to 1.05)
    hospital_bus = next(b for b in sol.buses if b.bus_id == "BUS-04")
    assert 0.95 <= hospital_bus.voltage_magnitude_pu <= 1.05


def test_power_flow_volt_var_support():
    engine = DistributionPowerFlowEngine(oltc_tap=2)
    # Heavy load without BESS
    sol_base = engine.solve_power_flow(
        tx_load_multiplier_k=1.25,
        bess_discharge_mw=0.0,
        bess_volt_var_q_mvar=0.0,
    )

    # With BESS active (4 MW) and reactive Volt/VAR injection (2 MVAR)
    sol_mit = engine.solve_power_flow(
        tx_load_multiplier_k=1.25,
        bess_discharge_mw=4.0,
        bess_volt_var_q_mvar=2.0,
    )

    # Hospital voltage should improve under Volt/VAR support
    assert sol_mit.min_voltage_pu > sol_base.min_voltage_pu
    assert sol_mit.total_grid_losses_kw < sol_base.total_grid_losses_kw


def test_power_flow_oltc_optimization():
    engine = DistributionPowerFlowEngine()
    best_tap, sol = engine.optimize_oltc_tap_for_feeder(tx_load_multiplier_k=1.18)

    assert sol.converged is True
    assert sol.ansi_c84_envelope_compliant is True
