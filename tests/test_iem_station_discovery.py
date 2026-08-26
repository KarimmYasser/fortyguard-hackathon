from __future__ import annotations

import httpx
import pytest

from src.api.iem_ground_truth_client import AsyncIEMGroundTruthClient


@pytest.mark.asyncio
async def test_nearest_station_discovery_uses_catalog_geometry():
    payload = {"features": [
        {"id": "FAR", "geometry": {"coordinates": [-110.0, 35.0]}, "properties": {"sid": "FAR"}},
        {"id": "KPHX", "geometry": {"coordinates": [-112.01, 33.43]}, "properties": {"sid": "KPHX", "sname": "Phoenix"}},
    ]}
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json=payload))
    async with httpx.AsyncClient(transport=transport) as http:
        result = await AsyncIEMGroundTruthClient(http_client=http).discover_nearest_station(33.4484, -112.074)
    assert result["station"] == "PHX"
    assert result["name"] == "Phoenix"
    assert result["distance_to_aoi_km"] < 10


@pytest.mark.asyncio
async def test_station_selection_prioritizes_coverage_then_distance(monkeypatch):
    client = AsyncIEMGroundTruthClient()
    async def candidates(*_args, **_kwargs):
        return [
            {"station": "NEAR", "distance_to_aoi_km": 1.0},
            {"station": "FULL", "distance_to_aoi_km": 5.0},
        ]
    async def fetch(station, *_args):
        count = 1 if station == "NEAR" else 3
        return {"data_source": "ground_truth_live", "series": [
            {"timestamp": str(i), "temperature_2m_c": 30} for i in range(count)
        ], "provenance": {"station": station}}
    monkeypatch.setattr(client, "discover_candidate_stations", candidates)
    monkeypatch.setattr(client, "fetch_hourly", fetch)
    selected, payload = await client.select_station(0, 0, "2023-01-01", "2023-01-01")
    assert selected["station"] == "FULL"
    assert payload["provenance"]["station_selection"][0]["station"] == "FULL"
