"""
FastAPI Routes for IEEE C57.91 Annex G Benchmarking & 72-Hour Compounding Replay
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, Literal
from fastapi import APIRouter, HTTPException, Query

from src.api.fortyguard_client import load_phoenix_fixture
from src.data_science.ground_truth_pipeline import GroundTruthValidationPipeline, haversine_km
from src.data_science.ground_truth_validation import (
    validate_fortyguard_curve,
)
from src.physics.ieee_annex_g_benchmark import IEEEAnnexGBenchmarkEngine
from src.physics.multi_day_heatwave import MultiDayHeatwaveEngine

router = APIRouter(tags=["Academic Standards & 72h Compounding"])
FIXTURES = Path(__file__).parents[2] / "api" / "fixtures"
GROUND_TRUTH_REPLAY = FIXTURES / "phx_phx_2023_07_19.json"


@router.get("/api/v1/benchmark/ground-truth-comparison")
async def get_ground_truth_comparison(
    source: Literal["replay", "auto", "iem", "open-meteo"] = Query(default="replay"),
    station: str = Query(default="PHX", min_length=3, max_length=8),
    minimum_pairs: int = Query(default=6, ge=1, le=24),
) -> Dict[str, Any]:
    """Compare FortyGuard urban 2 m telemetry with an independent station.

    The default frozen IEM/ASOS replay is deterministic for demos. ``iem`` and
    ``auto`` can refresh public observations; Open-Meteo is a labelled gridded
    fallback. This endpoint validates environmental temperature only: ISO LMP
    and feeder benchmarks are separate grid/electrical evidence domains.
    """
    fixture = load_phoenix_fixture()
    baseline = fixture["hourly_forecast_12h"]
    location = fixture["scenario_metadata"]["location"]
    try:
        if source == "replay":
            truth = json.loads(GROUND_TRUTH_REPLAY.read_text(encoding="utf-8"))
            truth["provenance"]["distance_to_aoi_km"] = round(
                haversine_km(
                    float(location["latitude"]), float(location["longitude"]),
                    float(truth["provenance"]["station_latitude"]),
                    float(truth["provenance"]["station_longitude"]),
                ), 3
            )
            report = validate_fortyguard_curve(baseline, truth, minimum_pairs=minimum_pairs)
            report["selection"] = {
                "requested_source": "replay", "selected_source": "iem_replay",
                "fallback_used": False, "failures": [],
            }
        else:
            report = await GroundTruthValidationPipeline().validate(
                baseline,
                latitude=float(location["latitude"]), longitude=float(location["longitude"]),
                start_date="2023-07-19", end_date="2023-07-19",
                station=station, minimum_pairs=minimum_pairs, source=source,
                scenario_id="phoenix_heatwave_july_2023",
            )
        report["comparison"] = {
            "formula": "ΔT = T_FortyGuard_2m - T_Station_Ground_Truth",
            "scope": "urban microclimate validation; no proprietary feeder telemetry claimed",
            "scenario": fixture["scenario_metadata"]["name"],
            "time_alignment": {
                "fortyguard_source_clock": "Phoenix local civil time (MST, UTC-07:00)",
                "station_clock": "UTC",
                "conversion": "Offset-aware FortyGuard timestamps canonicalized to UTC before exact-hour join",
                "verified_from": "FortyGuard env_params metadata.timezone_offset_hours",
            },
            "claim_guardrail": (
                "A single airport comparison can quantify agreement and an urban-station anomaly, "
                "but cannot by itself prove a causal urban heat-island effect."
            ),
            "grid_context": {
                "included": False,
                "reason": (
                    "Wholesale EIA/ISO demand and LMP are not temperature ground truth, and "
                    "public distribution-feeder SCADA is generally unavailable."
                ),
                "supported_offline_benchmarks": [
                    "IEEE distribution test feeders", "EPRI OpenDSS circuits", "NREL SMART-DS"
                ],
            },
        }
        return report
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"ground-truth comparison failed: {exc}") from exc


@router.get("/api/v1/benchmark/ieee-annex-g")
async def get_ieee_annex_g_validation() -> Dict[str, Any]:
    """
    Executes the official IEEE Std C57.91-2011 Annex G reference benchmark test suite.
    Demonstrates zero deviation from the published IEEE standard numerical tables.
    """
    engine = IEEEAnnexGBenchmarkEngine()
    return engine.run_all_benchmarks()


@router.get("/api/v1/replay/72h-compounding")
async def get_72h_compounding_replay() -> Dict[str, Any]:
    """
    Replays a frozen live FortyGuard capture containing every hour from
    July 24-26, 2023 through the continuous transformer / cable model. The
    environmental boundary is measured; load, soil evolution and mitigation
    remain explicitly modelled because FortyGuard exposes no grid telemetry.
    """
    engine = MultiDayHeatwaveEngine()
    result = engine.run_72h_simulation()
    return result.model_dump()
