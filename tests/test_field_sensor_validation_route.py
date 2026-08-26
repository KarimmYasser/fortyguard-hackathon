from fastapi.testclient import TestClient

from src.server.main import app


def test_field_sensor_validation_accepts_calibrated_colocated_data():
    baseline = [
        {"timestamp": f"2023-01-01T0{i}:00:00Z", "fortyguard_2m_ambient_c": 30 + i}
        for i in range(2)
    ]
    sensor = [
        {"timestamp": f"2023-01-01T0{i}:00:00Z", "temperature_2m_c": 29 + i}
        for i in range(2)
    ]
    response = TestClient(app).post("/api/v1/validation/field-sensor", json={
        "scenario_id": "field-test", "minimum_pairs": 2, "baseline": baseline,
        "sensor": {
            "sensor_id": "S-1", "latitude": 33.4, "longitude": -112.0,
            "height_m": 2.0, "calibration_reference": "NIST traceable certificate 123",
            "calibration_date": "2023-01-01", "series": sensor,
        },
    })
    assert response.status_code == 200
    body = response.json()
    assert body["evidence_tier"] == "A_colocated_field"
    assert body["validation_id"]
