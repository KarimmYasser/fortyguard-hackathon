from __future__ import annotations

from unittest.mock import AsyncMock

import httpx
import pytest

from src.api.iem_ground_truth_client import AsyncIEMGroundTruthClient, IEMGroundTruthError
from src.data_science.ground_truth_validation import validate_fortyguard_curve


class MemoryCache:
    def __init__(self):
        self.rows = {}
        self.saved = []

    @staticmethod
    def generate_query_hash(endpoint, params):
        return f"{endpoint}:{params['station']}:{params['year1']}:{params['day1']}"

    async def get_cached_api_call(self, key):
        return self.rows.get(key)

    async def save_cached_api_call(self, record):
        self.saved.append(record)
        self.rows[record.query_hash] = record.response_payload


IEM_CSV = """# IEM generated data
station,valid,lon,lat,tmpf,relh,sknt,drct
PHX,2023-07-19 05:51,-112.01,33.43,96.8,21,4,90
PHX,2023-07-19 06:10,-112.01,33.43,98.6,20,6,100
PHX,2023-07-19 06:51,-112.01,33.43,100.4,19,8,110
"""


@pytest.mark.asyncio
async def test_iem_normalizes_physical_station_data_to_hourly_utc():
    cache = MemoryCache()
    transport = httpx.MockTransport(lambda request: httpx.Response(200, text=IEM_CSV))
    async with httpx.AsyncClient(transport=transport) as http:
        result = await AsyncIEMGroundTruthClient(http_client=http, cache=cache).fetch_hourly(
            "KPHX", "2023-07-19", "2023-07-19"
        )

    assert result["provider"] == "iem_asos"
    assert result["provenance"]["evidence_class"] == "in-situ station observation"
    assert result["provenance"]["station"] == "PHX"
    assert result["provenance"]["station_latitude"] == 33.43
    assert result["provenance"]["station_longitude"] == -112.01
    assert result["series"][0]["timestamp"] == "2023-07-19T06:00:00Z"
    assert result["series"][0]["temperature_2m_c"] == 36.5  # average 36C and 37C
    assert result["series"][0]["wind_speed_10m_m_s"] == pytest.approx(2.5722, abs=1e-4)
    assert result["series"][0]["solar_ghi_w_m2"] is None
    assert cache.saved[0].credits_spent == 0.0


@pytest.mark.asyncio
async def test_iem_cache_replay_is_zero_credit_and_network_free():
    cache = MemoryCache()
    seed = AsyncIEMGroundTruthClient(cache=cache)
    params = seed._params("PHX", "2023-07-19", "2023-07-19")
    cache_params = dict(params)
    cache_params["data"] = list(params["data"])
    key = cache.generate_query_hash("iem:/cgi-bin/request/asos.py", cache_params)
    cache.rows[key] = seed._normalize(IEM_CSV, params, key)
    http = AsyncMock()

    result = await AsyncIEMGroundTruthClient(http_client=http, cache=cache).fetch_hourly(
        "PHX", "2023-07-19", "2023-07-19"
    )

    assert result["data_source"] == "ground_truth_cached"
    assert result["provenance"]["credits_spent"] == 0.0
    http.get.assert_not_awaited()


@pytest.mark.asyncio
async def test_iem_rejects_html_or_empty_responses():
    cache = MemoryCache()
    transport = httpx.MockTransport(lambda request: httpx.Response(200, text="<html>error</html>"))
    async with httpx.AsyncClient(transport=transport) as http:
        with pytest.raises(IEMGroundTruthError, match="missing a CSV header"):
            await AsyncIEMGroundTruthClient(http_client=http, cache=cache).fetch_hourly(
                "PHX", "2023-07-19", "2023-07-19"
            )


def test_iem_temperature_validation_does_not_invent_solar_metrics():
    baseline = [
        {
            "timestamp": "2023-07-19T06:00:00Z",
            "fortyguard_2m_ambient_c": 37.0,
            "solar_irradiance_w_m2": 100.0,
        }
    ]
    truth = AsyncIEMGroundTruthClient._normalize(
        IEM_CSV,
        AsyncIEMGroundTruthClient._params("PHX", "2023-07-19", "2023-07-19"),
        "key",
    )
    report = validate_fortyguard_curve(baseline, truth)
    assert set(report["metrics"]) == {"temperature_2m"}
