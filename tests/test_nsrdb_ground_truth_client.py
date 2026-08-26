from __future__ import annotations

from unittest.mock import AsyncMock

import httpx
import pytest

from src.api.nsrdb_ground_truth_client import AsyncNSRDBGroundTruthClient, NSRDBGroundTruthError


CSV = """Source,Location ID
NSRDB,1
Year,Month,Day,Hour,Minute,GHI,DNI,DHI,Temperature,Relative Humidity,Wind Speed,Surface Albedo,Pressure
2023,7,19,6,30,100,300,20,35,21,2.1,0.2,980
2023,7,19,7,30,250,500,30,37,19,2.4,0.2,979
"""


class Cache:
    def __init__(self): self.rows, self.saved = {}, []
    def generate_query_hash(self, endpoint, params):
        assert "api_key" not in params and "email" not in params
        return endpoint + str(sorted(params.items()))
    async def get_cached_api_call(self, key): return self.rows.get(key)
    async def save_cached_api_call(self, record):
        self.saved.append(record); self.rows[record.query_hash] = record.response_payload


def test_uses_current_nlr_hostname():
    assert AsyncNSRDBGroundTruthClient(api_key="x", email="x@y.z").base_url.startswith(
        "https://developer.nlr.gov/"
    )


def test_credentials_are_required():
    client = AsyncNSRDBGroundTruthClient(api_key="placeholder", email="x@y.z")
    client.api_key = client.email = None
    with pytest.raises(NSRDBGroundTruthError, match="NREL_API_KEY"):
        client._params(33, -112, 2023)


@pytest.mark.asyncio
async def test_nsrdb_normalization_and_secret_safe_cache():
    cache = Cache()
    transport = httpx.MockTransport(lambda request: httpx.Response(200, text=CSV))
    async with httpx.AsyncClient(transport=transport) as http:
        result = await AsyncNSRDBGroundTruthClient(
            api_key="secret", email="person@example.com", http_client=http, cache=cache
        ).fetch_hourly(33.4484, -112.074, "2023-07-19", "2023-07-19")
    assert result["series"][0]["timestamp"] == "2023-07-19T07:00:00Z"
    assert result["series"][0]["solar_ghi_w_m2"] == 100
    assert result["series"][0]["surface_temperature_c"] is None
    assert result["series"][0]["surface_albedo"] == 0.2
    assert result["provenance"]["evidence_class"].endswith("(not in-situ)")
    assert "secret" not in str(cache.saved[0].request_params)
    assert "person@example.com" not in str(cache.saved[0].request_params)
    assert cache.saved[0].credits_spent == 0


@pytest.mark.asyncio
async def test_nsrdb_404_has_actionable_fallback_message():
    transport = httpx.MockTransport(lambda request: httpx.Response(404, text="Not Found"))
    async with httpx.AsyncClient(transport=transport) as http:
        with pytest.raises(NSRDBGroundTruthError, match="use --source open-meteo"):
            await AsyncNSRDBGroundTruthClient(
                api_key="secret", email="x@y.z", http_client=http, cache=Cache(), max_retries=0
            ).fetch_hourly(33.4484, -112.074, "2023-07-19", "2023-07-19")


@pytest.mark.asyncio
async def test_nsrdb_cache_hit_is_network_free():
    cache = Cache()
    seed = AsyncNSRDBGroundTruthClient(api_key="secret", email="x@y.z", cache=cache)
    params = seed._params(33.4484, -112.074, 2023)
    safe = seed._safe_cache_params(params) | {
        "start_date": "2023-07-19", "end_date": "2023-07-19", "parser_version": 2,
    }
    key = cache.generate_query_hash(
        "nlr:/api/nsrdb/v2/solar/nsrdb-GOES-aggregated-v4-0-0-download.csv", safe
    )
    cache.rows[key] = seed._normalize(CSV, __import__("datetime").date(2023, 7, 19), __import__("datetime").date(2023, 7, 19), key)
    http = AsyncMock()
    result = await AsyncNSRDBGroundTruthClient(
        api_key="secret", email="x@y.z", http_client=http, cache=cache
    ).fetch_hourly(33.4484, -112.074, "2023-07-19", "2023-07-19")
    assert result["data_source"] == "ground_truth_cached"
    http.get.assert_not_awaited()
