from __future__ import annotations

import pytest

from src.api.iem_ground_truth_client import AsyncIEMGroundTruthClient
from src.data_science.ground_truth_pipeline import GroundTruthValidationPipeline


BASELINE = [
    {"timestamp": "2023-01-01T00:00:00Z", "fortyguard_2m_ambient_c": 10.0},
    {"timestamp": "2023-01-01T01:00:00Z", "fortyguard_2m_ambient_c": 12.0},
]


def payload(station, values):
    return {
        "provider": "iem_asos", "data_source": "ground_truth_cached",
        "series": [
            {"timestamp": "2023-01-01T00:00:00Z", "temperature_2m_c": values[0]},
            {"timestamp": "2023-01-01T01:00:00Z", "temperature_2m_c": values[1]},
        ],
        "provenance": {"station": station, "evidence_class": "in-situ station observation"},
    }


class StubIEM:
    async def fetch_metro_stations(self, *_args):
        return {
            "metro": "phoenix", "data_source": "ground_truth_cached", "credits_spent": 0,
            "stations": {"PHX": payload("PHX", [9, 11]), "DVT": payload("DVT", [8, 10])},
            "failures": [{"station": "IWA", "reason": "unavailable"}],
        }


@pytest.mark.asyncio
async def test_metro_report_preserves_per_station_metrics_and_spread():
    result = await GroundTruthValidationPipeline(iem_client=StubIEM()).validate_metro(
        BASELINE, metro="phoenix", start_date="2023-01-01", end_date="2023-01-01", minimum_pairs=2
    )
    assert result["station_count"] == 2
    assert result["metro_summary"]["median_mae_c"] == 1.5
    assert result["metro_summary"]["station_peak_spread_c"] == 1.0
    assert result["failures"][0]["station"] == "IWA"
    assert result["credits_spent"] == 0


def test_known_metro_groups_have_three_stations():
    from src.api.iem_ground_truth_client import METRO_STATION_GROUPS
    assert all(len(stations) == 3 for stations in METRO_STATION_GROUPS.values())
    assert set(METRO_STATION_GROUPS) == {"phoenix", "houston", "las_vegas", "san_jose"}
