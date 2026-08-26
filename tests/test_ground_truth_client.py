from __future__ import annotations

from unittest.mock import AsyncMock

import httpx
import pytest

from src.api.ground_truth_client import AsyncGroundTruthClient, GroundTruthError
from src.data_science.ground_truth_validation import (
    GroundTruthValidationError,
    compute_error_metrics,
    validate_fortyguard_curve,
)


class MemoryCache:
    def __init__(self):
        self.rows = {}
        self.saved = []

    @staticmethod
    def generate_query_hash(endpoint, params):
        return f"{endpoint}:{params['latitude']}:{params['start_date']}:{params['end_date']}"

    async def get_cached_api_call(self, key):
        return self.rows.get(key)

    async def save_cached_api_call(self, record):
        self.saved.append(record)
        self.rows[record.query_hash] = record.response_payload


def open_meteo_payload():
    return {
        "hourly": {
            "time": ["2023-07-19T06:00", "2023-07-19T07:00"],
            "temperature_2m": [35.0, 37.0],
            "relative_humidity_2m": [20, 18],
            "wind_speed_10m": [2.0, 2.5],
            "shortwave_radiation_instant": [100.0, 300.0],
            "surface_temperature": [39.0, 42.0],
        }
    }


@pytest.mark.asyncio
async def test_live_fetch_is_normalized_cached_and_zero_credit():
    cache = MemoryCache()
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json=open_meteo_payload()))
    async with httpx.AsyncClient(transport=transport) as http:
        client = AsyncGroundTruthClient(http_client=http, cache=cache)
        result = await client.fetch_hourly(33.4484, -112.074, "2023-07-19", "2023-07-19")

    assert result["data_source"] == "ground_truth_live"
    assert result["series"][0]["timestamp"] == "2023-07-19T06:00:00Z"
    assert result["series"][0]["solar_ghi_w_m2"] == 100.0
    assert result["provenance"]["evidence_class"].startswith("gridded")
    assert result["provenance"]["model_pinned"] is True
    assert "grid_metadata" in result["provenance"]
    assert len(cache.saved) == 1
    assert cache.saved[0].credits_spent == 0.0


@pytest.mark.asyncio
async def test_cache_hit_never_calls_network_or_credit_ledger():
    cache = MemoryCache()
    seed_client = AsyncGroundTruthClient(cache=cache)
    params = seed_client._params(33.4484, -112.074, "2023-07-19", "2023-07-19")
    key = cache.generate_query_hash("open-meteo:/v1/archive", params)
    cache.rows[key] = seed_client._normalize(open_meteo_payload(), params, key)
    http = AsyncMock()
    client = AsyncGroundTruthClient(http_client=http, cache=cache)

    result = await client.fetch_hourly(33.4484, -112.074, "2023-07-19", "2023-07-19")

    assert result["data_source"] == "ground_truth_cached"
    assert result["provenance"]["credits_spent"] == 0.0
    http.get.assert_not_awaited()
    assert cache.saved == []


@pytest.mark.asyncio
async def test_bad_upstream_shape_fails_closed():
    cache = MemoryCache()
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json={"hourly": {"time": []}}))
    async with httpx.AsyncClient(transport=transport) as http:
        with pytest.raises(GroundTruthError, match="invalid temperature_2m"):
            await AsyncGroundTruthClient(http_client=http, cache=cache).fetch_hourly(
                33.4484, -112.074, "2023-07-19", "2023-07-19"
            )
    assert cache.saved == []


def test_offset_aware_timestamp_is_canonicalized_for_utc_join():
    baseline = [{"timestamp": "2023-07-19T06:00:00-07:00", "fortyguard_2m_ambient_c": 36.1}]
    truth = [{"timestamp": "2023-07-19T13:00:00Z", "temperature_2m_c": 35.0}]
    metrics = compute_error_metrics(baseline, truth)
    assert metrics["paired_series"][0]["timestamp"] == "2023-07-19T13:00:00Z"
    assert metrics["paired_series"][0]["delta_t_c"] == 1.1


def test_metrics_align_by_timestamp_and_compute_expected_errors():
    baseline = [
        {"timestamp": "b", "fortyguard_2m_ambient_c": 5.0},
        {"timestamp": "a", "fortyguard_2m_ambient_c": 2.0},
        {"timestamp": "missing", "fortyguard_2m_ambient_c": 100.0},
    ]
    truth = [
        {"timestamp": "a", "temperature_2m_c": 1.0},
        {"timestamp": "b", "temperature_2m_c": 3.0},
    ]
    metrics = compute_error_metrics(baseline, truth, minimum_pairs=2)
    assert metrics["mae"] == 1.5
    assert metrics["rmse"] == pytest.approx((5 / 2) ** 0.5, abs=1e-4)
    assert metrics["peak_delta"] == 2.0
    assert metrics["n_pairs"] == 2
    assert metrics["spearman_r"] == 1.0
    assert metrics["heat_exposure"]["40"]["baseline"]["exceedance_hours"] == 0


def test_gridded_evidence_is_not_misclassified_as_in_situ():
    baseline = [{"timestamp": "t", "fortyguard_2m_ambient_c": 30}]
    truth = {
        "data_source": "ground_truth_live", "provider": "open_meteo_historical_archive",
        "provenance": {"evidence_class": "gridded meteorological benchmark (not an in-situ sensor)"},
        "series": [{"timestamp": "t", "temperature_2m_c": 29}],
    }
    assert validate_fortyguard_curve(baseline, truth)["evidence_tier"] == "C_gridded"


def test_validation_rejects_unlabelled_evidence():
    with pytest.raises(GroundTruthValidationError, match="untrusted"):
        validate_fortyguard_curve([], {"data_source": "unknown", "series": []})
