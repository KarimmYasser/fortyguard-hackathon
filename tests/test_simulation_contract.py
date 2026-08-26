"""Cross-engine invariants and provenance contract regression tests."""

from fastapi.testclient import TestClient

from src.api.fortyguard_client import load_phoenix_fixture
from src.physics.bess_electro_thermal import BESSElectroThermalEngine
from src.physics.soil_cable import SoilCableEngine
from src.physics.transformer_thermal import TransformerThermalEngine
from src.replay.phoenix_heatwave_replay import PhoenixHeatwaveReplayEngine
from src.server.main import app


def test_replay_has_explicit_evidence_contract():
    data = PhoenixHeatwaveReplayEngine().generate_replay_dataset()
    provenance = data["provenance"]
    kinds = {row["field"]: row["kind"] for row in provenance["evidence"]}
    assert provenance["operating_mode"] == "demo"
    assert provenance["validation_status"] == "environment_only"
    assert kinds["fortyguard_2m_ambient_c"] == "measured"
    assert kinds["grid_load_and_topology"] == "assumed"
    assert kinds["equipment_and_grid_trajectories"] == "simulated"
    assert kinds["economic_and_failure_risk"] == "unvalidated"
    assert "integrated_grid_evaluation" in data
    assert "sensitivity_analysis" in data
    bounds = data["sensitivity_analysis"]["peak_hot_spot_c"]
    assert bounds["low"] < bounds["high"]


def test_forced_cooling_is_applied_once_and_reduces_temperature():
    fixture = load_phoenix_fixture()
    forecast = fixture["hourly_forecast_12h"]
    loads = [h["baseline_load_ratio_k"] for h in forecast]
    engine = TransformerThermalEngine()
    passive = engine.simulate_trajectory("TX", forecast, loads, cooling_derate=0.68)
    active = engine.simulate_trajectory(
        "TX", forecast, loads, cooling_derate=0.68, forced_cooling_active=True
    )
    explicit_once = engine.simulate_trajectory("TX", forecast, loads, cooling_derate=0.68 * 1.35)
    assert active.peak_hot_spot_c < passive.peak_hot_spot_c
    assert active.peak_hot_spot_c == explicit_once.peak_hot_spot_c


def test_higher_load_does_not_reduce_transformer_hotspot():
    fixture = load_phoenix_fixture()
    forecast = fixture["hourly_forecast_12h"]
    engine = TransformerThermalEngine()
    low = engine.simulate_trajectory("TX", forecast, [0.7] * len(forecast))
    high = engine.simulate_trajectory("TX", forecast, [1.2] * len(forecast))
    assert high.peak_hot_spot_c > low.peak_hot_spot_c


def test_drier_soil_does_not_improve_cable_ampacity():
    engine = SoilCableEngine()
    wet = engine.calculate_soil_thermal_resistivity(0.20)
    dry = engine.calculate_soil_thermal_resistivity(0.04)
    assert dry > wet
    assert engine.compute_cable_ampacity_derate(dry) < engine.compute_cable_ampacity_derate(wet)


def test_bess_soc_conserves_discharged_energy_within_floor():
    engine = BESSElectroThermalEngine()
    result = engine.simulate_dispatch_trajectory([30.0, 30.0], [2.5, 2.5], initial_soc=0.8)
    # 5 MWh discharged from a 25 MWh pack: 80% -> 60%.
    assert result[-1].state_of_charge_pct == 60.0


def test_replay_integrates_advanced_engines_on_same_timeline():
    data = PhoenixHeatwaveReplayEngine().generate_replay_dataset()
    integrated = data["integrated_grid_evaluation"]
    assert integrated["timeline_hours"] == len(data["timeline_steps"])
    assert integrated["reliability"]["baseline"]["system_cascading_risk_pct"] >= integrated["reliability"]["mitigated"]["system_cascading_risk_pct"]
    assert integrated["power_flow_peak_hour"]["mitigated"]["total_grid_losses_kw"] <= integrated["power_flow_peak_hour"]["baseline"]["total_grid_losses_kw"]


def test_advanced_physics_endpoints_persist_without_stale_attribute_errors(monkeypatch):
    from src.server.routes import advanced_physics

    async def no_op(*args, **kwargs):
        return None

    monkeypatch.setattr(advanced_physics.db_manager, "log_dlr_telemetry", no_op)
    monkeypatch.setattr(advanced_physics.db_manager, "save_cascading_risk_snapshot", no_op)
    client = TestClient(app)
    assert client.post("/api/v1/physics/dlr-solve", json={}).status_code == 200
    baseline = client.get("/api/v1/physics/cascading-hazard").json()
    mitigated = client.get("/api/v1/physics/cascading-hazard?is_mitigated=true").json()
    assert baseline["system_cascading_risk_pct"] >= mitigated["system_cascading_risk_pct"]
