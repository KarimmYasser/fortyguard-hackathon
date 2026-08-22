import pytest
from fastapi.testclient import TestClient
from src.server.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_sandbox_simulate_default(client):
    payload = {
        "intra_aoi_spread_c": 4.5,
        "heatwave_day": 24,
        "transformer_mva": 25.0,
        "bess_capacity_mwh": 25.0,
        "canyon_aspect_ratio": 1.85,
        "forced_cooling_enabled": True,
    }
    response = client.post("/api/v1/sandbox/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["timeline_steps"]) == 12
    assert "baseline_summary" in data
    assert "mitigated_summary" in data
    assert "safety_gate_verdict" in data
    assert "economic_evaluation" in data
    assert data["economic_evaluation"]["net_avoided_loss_usd"] > 0


def test_sandbox_simulate_extreme_heat_zero_bess(client):
    payload = {
        "intra_aoi_spread_c": 6.0,
        "heatwave_day": 31,
        "transformer_mva": 35.0,
        "bess_capacity_mwh": 0.0,
        "canyon_aspect_ratio": 2.5,
        "forced_cooling_enabled": False,
    }
    response = client.post("/api/v1/sandbox/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    # Without BESS and forced cooling at +6C, hot-spot should be high
    assert data["baseline_summary"]["peak_hot_spot_c"] > 140.0
