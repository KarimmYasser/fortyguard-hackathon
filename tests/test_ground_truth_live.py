"""Opt-in upstream schema smoke tests: RUN_LIVE_GROUND_TRUTH_TESTS=1 pytest -m live."""

from __future__ import annotations

import os

import pytest

from src.api.ground_truth_client import AsyncGroundTruthClient
from src.api.iem_ground_truth_client import AsyncIEMGroundTruthClient
from src.api.landsat_lst_client import AsyncLandsatLSTClient

pytestmark = [
    pytest.mark.live,
    pytest.mark.skipif(
        os.getenv("RUN_LIVE_GROUND_TRUTH_TESTS") != "1",
        reason="live public API tests are opt-in",
    ),
]


@pytest.mark.asyncio
async def test_live_iem_schema():
    result = await AsyncIEMGroundTruthClient().fetch_hourly(
        "PHX", "2023-07-19", "2023-07-19", force_refresh=True
    )
    assert result["series"]
    assert result["provenance"]["evidence_class"] == "in-situ station observation"


@pytest.mark.asyncio
async def test_live_open_meteo_schema():
    result = await AsyncGroundTruthClient().fetch_hourly(
        33.4484, -112.074, "2023-07-19", "2023-07-19", force_refresh=True
    )
    assert len(result["series"]) == 24
    assert "gridded" in result["provenance"]["evidence_class"]


@pytest.mark.asyncio
async def test_live_landsat_search_and_cog_summary():
    client = AsyncLandsatLSTClient()
    bbox = [-112.08, 33.447, -112.068, 33.45]
    result = await client.search(bbox, "2023-07-01/2023-07-31", cloud_cover_lt=30, limit=3)
    assert result["observations"]
    summary = await client.summarize_scene(result["observations"][0], bbox)
    assert summary["summary"]["valid_pixel_count"] > 0
    assert summary["variable"] == "surface_temperature_c"
