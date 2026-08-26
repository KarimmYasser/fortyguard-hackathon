from fastapi.testclient import TestClient

from src.server.main import app


def test_general_validation_rejects_empty_baseline():
    response = TestClient(app).post("/api/v1/validation/air-temperature", json={
        "scenario_id": "test", "latitude": 33.4, "longitude": -112.0,
        "start_date": "2023-07-19", "end_date": "2023-07-19",
        "source": "auto", "minimum_pairs": 1, "baseline": [],
    })
    assert response.status_code == 422


def test_landsat_bbox_validation_fails_before_network():
    response = TestClient(app).get("/api/v1/validation/surface-context/landsat", params={
        "min_lon": 1, "min_lat": 1, "max_lon": 0, "max_lat": 0,
        "datetime_range": "2024-01-01/2024-01-31",
    })
    assert response.status_code == 422
