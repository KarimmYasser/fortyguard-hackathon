import pytest
from src.safety.cbf_gate import CBFSafetyGate
from src.models.safety import SafetyStatus, ActionType, MitigationAction
from src.api.fortyguard_client import load_phoenix_fixture


def test_safety_gate_baseline_violation():
    fixture = load_phoenix_fixture()
    forecast = fixture["hourly_forecast_12h"]

    gate = CBFSafetyGate()
    # Baseline without mitigation has heavy loading and high ambient
    verdict = gate.preflight_check(
        asset_id="SUB-PHX-DOWNTOWN-04",
        hourly_forecast=forecast,
        candidate_actions=[],  # No mitigation
        cooling_derate=0.68,   # Urban canyon throttling
    )

    assert verdict.status in (SafetyStatus.MODIFY, SafetyStatus.REJECT)
    assert verdict.is_safe is False
    assert len(verdict.violations) > 0
    assert verdict.safe_max_load_k < verdict.nominal_load_k


def test_safety_gate_mitigation_pass():
    fixture = load_phoenix_fixture()
    forecast = fixture["hourly_forecast_12h"]

    gate = CBFSafetyGate()
    # Apply complete mitigation package
    actions = [
        MitigationAction(
            action_type=ActionType.COOLING_STAGE_2,
            target_asset_id="SUB-PHX-DOWNTOWN-04",
            target_hour_start=4,
            target_hour_end=11,
            cooling_boost_factor=1.35,
        ),
        MitigationAction(
            action_type=ActionType.BESS_PEAK_SHAVING,
            target_asset_id="SUB-PHX-DOWNTOWN-04",
            target_hour_start=5,
            target_hour_end=10,
            load_ratio_delta_k=0.25,
            power_delta_mw=5.0,
            bess_discharge_mw=2.0,
        ),
        MitigationAction(
            action_type=ActionType.EV_SMART_CURTAIL,
            target_asset_id="SUB-PHX-DOWNTOWN-04",
            target_hour_start=6,
            target_hour_end=9,
            load_ratio_delta_k=0.10,
        ),
    ]

    verdict = gate.preflight_check(
        asset_id="SUB-PHX-DOWNTOWN-04",
        hourly_forecast=forecast,
        candidate_actions=actions,
        cooling_derate=0.68,
        bess_initial_soc_pct=85.0,
        bess_capacity_mwh=25.0,
    )

    assert verdict.status == SafetyStatus.ACCEPT
    assert verdict.is_safe is True
    assert verdict.hot_spot_compliant is True
    assert verdict.projected_peak_hot_spot_c < 140.0
    assert verdict.bess_reserve_compliant is True
