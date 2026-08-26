import pytest
from fastapi.testclient import TestClient
from src.server.main import app
from src.replay.phoenix_heatwave_replay import PhoenixHeatwaveReplayEngine


def test_phoenix_replay_engine():
    engine = PhoenixHeatwaveReplayEngine()
    data = engine.generate_replay_dataset()

    assert "scenario_metadata" in data
    assert "provenance" in data
    assert "integrated_grid_evaluation" in data
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


def test_security_headers_and_cors_are_restrictive():
    client = TestClient(app)

    response = client.get(
        "/api/health",
        headers={"Origin": "https://www.thermal-sentinel-grid.live"},
    )
    assert response.headers["access-control-allow-origin"] == "https://www.thermal-sentinel-grid.live"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "strict-origin-when-cross-origin"

    untrusted = client.get(
        "/api/health",
        headers={"Origin": "https://attacker.example"},
    )
    assert "access-control-allow-origin" not in untrusted.headers


def test_vercel_serverless_path_normalizer():
    """Verify that api.index.app correctly handles /v1/... and /api/v1/... routes."""
    from api.index import app as vercel_app
    client = TestClient(vercel_app)

    # 1. Unstripped path
    res1 = client.get("/api/v1/replay/phoenix-2023")
    assert res1.status_code == 200
    assert "timeline_steps" in res1.json()

    # 2. Stripped path (/v1/...)
    res2 = client.get("/v1/replay/phoenix-2023")
    assert res2.status_code == 200
    assert "timeline_steps" in res2.json()

    # 3. Header-based rewrites (when Vercel passes /api/index.py with x-matched-path)
    res_hdr1 = client.get("/api/index.py", headers={"x-matched-path": "/api/v1/replay/phoenix-2023"})
    assert res_hdr1.status_code == 200
    assert "timeline_steps" in res_hdr1.json()

    res_hdr2 = client.get("/api/index.py", headers={"x-now-route-matches": "1=v1%2Freplay%2Fphoenix-2023"})
    assert res_hdr2.status_code == 200
    assert "timeline_steps" in res_hdr2.json()

    # 4. Health checks
    assert client.get("/health").status_code == 200
    assert client.get("/api").status_code == 200
    assert client.get("/api/health").status_code == 200
    assert client.get("/v1/health").status_code == 200

