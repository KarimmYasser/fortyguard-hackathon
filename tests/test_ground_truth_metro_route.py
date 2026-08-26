from fastapi.testclient import TestClient

from src.server.main import app


def test_frozen_multi_station_route_is_deterministic_and_zero_credit():
    response = TestClient(app).get("/api/v1/validation/metro/phoenix")
    assert response.status_code == 200
    body = response.json()
    assert body["data_source"] == "ground_truth_replay"
    assert body["station_count"] == 3
    assert set(body["stations"]) == {"PHX", "DVT", "IWA"}
    assert body["credits_spent"] == 0
    assert body["metro_summary"]["station_peak_spread_c"] > 0
    assert "not parcel-level" in body["metro_summary"]["interpretation"]


def test_metro_route_refuses_cross_city_baseline_mismatch():
    response = TestClient(app).get("/api/v1/validation/metro/houston")
    assert response.status_code == 409
    assert "no co-located FortyGuard baseline" in response.json()["detail"]
