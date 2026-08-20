import pytest
from fastapi.testclient import TestClient
from src.server.main import app
from src.replay.phoenix_heatwave_replay import PhoenixHeatwaveReplayEngine


def test_phoenix_replay_engine():
    engine = PhoenixHeatwaveReplayEngine()
    data = engine.generate_replay_dataset()

    assert "scenario_metadata" in data
    assert "timeline_steps" in data
    assert len(data["timeline_steps"]) == 12

    baseline = data["baseline_summary"]
    mitigated = data["mitigated_summary"]

    assert baseline["peak_hot_spot_c"] > 140.0
    assert baseline["breached_emergency_ceiling"] is True

    assert mitigated["peak_hot_spot_c"] < 140.0
    assert mitigated["breached_emergency_ceiling"] is False
    assert mitigated["avoided_loss_of_life_hours"] > 50.0

    assert data["safety_gate_verdict"]["status"] == "ACCEPT"
    assert data["economic_evaluation"]["net_avoided_loss_usd"] > 150000.0


def test_fastapi_endpoints():
    client = TestClient(app)

    # Health check
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

    # Assets list
    res_assets = client.get("/api/v1/assets")
    assert res_assets.status_code == 200
    assert len(res_assets.json()) >= 3

    # Historical replay
    res_replay = client.get("/api/v1/replay/phoenix-2023")
    assert res_replay.status_code == 200
    assert "timeline_steps" in res_replay.json()

    # Economic ROI
    res_eco = client.get("/api/v1/dispatch/economic-roi")
    assert res_eco.status_code == 200
    assert res_eco.json()["net_avoided_loss_usd"] > 100000.0

    # Scan endpoint
    res_scan = client.post(
        "/api/v1/scan",
        json={"city": "Phoenix, AZ", "latitude": 33.4484, "longitude": -112.0740},
    )
    assert res_scan.status_code == 200
    assert res_scan.json()["status"] == "success"

    # API Usage endpoint
    res_usage = client.get("/api/v1/scan/usage")
    assert res_usage.status_code == 200
    assert "status" in res_usage.json()

