from __future__ import annotations

import pytest

from src.data_science.ground_truth_pipeline import (
    GroundTruthValidationPipeline,
    haversine_km,
)


BASELINE = [
    {"timestamp": "2023-07-19T06:00:00Z", "fortyguard_2m_ambient_c": 36.0},
    {"timestamp": "2023-07-19T07:00:00Z", "fortyguard_2m_ambient_c": 38.0},
]


def payload(provider: str, evidence_class: str):
    return {
        "provider": provider,
        "data_source": "ground_truth_live",
        "series": [
            {"timestamp": "2023-07-19T06:00:00Z", "temperature_2m_c": 35.0},
            {"timestamp": "2023-07-19T07:00:00Z", "temperature_2m_c": 37.0},
        ],
        "provenance": {
            "evidence_class": evidence_class,
            "station_latitude": 33.43,
            "station_longitude": -112.01,
        },
    }


class StubIEM:
    def __init__(self, result=None, error=None):
        self.result, self.error = result, error

    async def fetch_hourly(self, *_args):
        if self.error:
            raise self.error
        return self.result


class StubGrid:
    def __init__(self, result):
        self.result = result
        self.called = False

    async def fetch_hourly(self, *_args):
        self.called = True
        return self.result


def test_haversine_reports_station_separation():
    assert haversine_km(33.4484, -112.074, 33.43, -112.01) == pytest.approx(6.29, abs=0.1)


@pytest.mark.asyncio
async def test_pipeline_prefers_physical_station_and_records_distance():
    grid = StubGrid(payload("open_meteo", "gridded"))
    pipeline = GroundTruthValidationPipeline(
        iem_client=StubIEM(payload("iem_asos", "in-situ station observation")),
        gridded_client=grid,
    )
    report = await pipeline.validate(
        BASELINE,
        latitude=33.4484,
        longitude=-112.074,
        start_date="2023-07-19",
        end_date="2023-07-19",
        station="PHX",
        minimum_pairs=2,
    )
    assert report["selection"]["selected_source"] == "iem"
    assert report["selection"]["fallback_used"] is False
    assert report["provenance"]["distance_to_aoi_km"] > 0
    assert grid.called is False


@pytest.mark.asyncio
async def test_pipeline_falls_back_explicitly_to_gridded_air_data():
    pipeline = GroundTruthValidationPipeline(
        iem_client=StubIEM(error=RuntimeError("station unavailable")),
        gridded_client=StubGrid(payload("open_meteo", "gridded meteorological benchmark")),
    )
    report = await pipeline.validate(
        BASELINE,
        latitude=33.4484,
        longitude=-112.074,
        start_date="2023-07-19",
        end_date="2023-07-19",
        station="PHX",
        minimum_pairs=2,
    )
    assert report["selection"]["selected_source"] == "open-meteo"
    assert report["selection"]["fallback_used"] is True
    assert report["selection"]["failures"][0]["source"] == "iem"


@pytest.mark.asyncio
async def test_forced_iem_fails_closed_without_fallback():
    grid = StubGrid(payload("open_meteo", "gridded"))
    pipeline = GroundTruthValidationPipeline(
        iem_client=StubIEM(error=RuntimeError("station unavailable")),
        gridded_client=grid,
    )
    with pytest.raises(RuntimeError, match="station unavailable"):
        await pipeline.validate(
            BASELINE,
            latitude=33.4484,
            longitude=-112.074,
            start_date="2023-07-19",
            end_date="2023-07-19",
            station="PHX",
            minimum_pairs=2,
            source="iem",
        )
    assert grid.called is False
