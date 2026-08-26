from fastapi.testclient import TestClient

from src.server.main import app


def test_ground_truth_comparison_replay_exposes_chart_and_uhi_metrics():
    response = TestClient(app).get("/api/v1/benchmark/ground-truth-comparison")
    assert response.status_code == 200
    body = response.json()
    metrics = body["metrics"]["temperature_2m"]

    assert body["data_source"] == "ground_truth_replay"
    assert body["provenance"]["evidence_class"] == "in-situ station observation"
    assert body["comparison"]["formula"] == "ΔT = T_FortyGuard_2m - T_Station_Ground_Truth"
    assert metrics["n_pairs"] == 12
    assert len(metrics["paired_series"]) == 12
    # FortyGuard fixture labels are Phoenix local time; the endpoint converts
    # them to UTC before joining the UTC ASOS observations.
    assert metrics["paired_series"][0]["timestamp"] == "2023-07-19T13:00:00Z"
    assert metrics["paired_series"][0]["delta_t_c"] == -0.5667
    assert metrics["pearson_r"] > 0.9
    assert metrics["mean_delta_t_c"] < 0  # PHX was hotter; do not force an UHI story.
    assert metrics["urban_station_anomaly"]["observed"] is False
    assert metrics["urban_heat_island"]["verified"] is False
    assert metrics["urban_heat_island"]["status"] == "not_established_by_station_comparison"
    assert "canonicalized to UTC" in body["comparison"]["time_alignment"]["conversion"]
