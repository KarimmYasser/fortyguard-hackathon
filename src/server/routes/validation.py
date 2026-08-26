"""External ground-truth validation routes."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from src.api.fortyguard_client import load_phoenix_fixture
from src.api.landsat_lst_client import AsyncLandsatLSTClient, spatial_surface_context_metrics
from src.data_science.ground_truth_pipeline import (
    GroundTruthValidationPipeline,
    aggregate_station_reports,
)
from src.data_science.ground_truth_validation import (
    validate_fortyguard_curve,
)
from src.db.database import db_manager

router = APIRouter(prefix="/validation", tags=["External Validation"])
FIXTURES = Path(__file__).parents[2] / "api" / "fixtures"


class FieldSensorPayload(BaseModel):
    sensor_id: str = Field(min_length=1, max_length=128)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    height_m: float = Field(ge=1.25, le=2.25)
    calibration_reference: str = Field(min_length=1)
    calibration_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    series: list[dict]


class FieldSensorValidationRequest(BaseModel):
    scenario_id: str = Field(min_length=1, max_length=128)
    minimum_pairs: int = Field(default=6, ge=1, le=744)
    baseline: list[dict]
    sensor: FieldSensorPayload


@router.post("/field-sensor")
async def validate_field_sensor(request: FieldSensorValidationRequest):
    """Validate against calibrated, co-located 1.25–2.25 m field observations."""
    if not request.baseline or not request.sensor.series:
        raise HTTPException(status_code=422, detail="baseline and sensor series are required")
    payload = {
        "provider": "field_sensor",
        "data_source": "ground_truth_live",
        "series": request.sensor.series,
        "provenance": {
            "evidence_class": "co-located calibrated field sensor",
            "sensor_id": request.sensor.sensor_id,
            "station_latitude": request.sensor.latitude,
            "station_longitude": request.sensor.longitude,
            "measurement_height_m": request.sensor.height_m,
            "calibration_reference": request.sensor.calibration_reference,
            "calibration_date": request.sensor.calibration_date,
            "credits_spent": 0.0,
        },
    }
    try:
        report = validate_fortyguard_curve(
            request.baseline, payload, minimum_pairs=request.minimum_pairs
        )
        report["selection"] = {
            "requested_source": "field_sensor", "selected_source": "field_sensor",
            "fallback_used": False, "failures": [],
        }
        pipeline = GroundTruthValidationPipeline(database=db_manager)
        await pipeline._persist(report, request.baseline, {
            "scenario_id": request.scenario_id, "source": "field_sensor",
            "sensor_id": request.sensor.sensor_id, "minimum_pairs": request.minimum_pairs,
        })
        return report
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"field-sensor validation failed: {exc}") from exc


class ValidationRequest(BaseModel):
    """General validation request for an existing FortyGuard hourly capture."""
    scenario_id: str = Field(min_length=1, max_length=128)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    start_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    end_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    station: str | None = Field(default=None, min_length=3, max_length=8)
    source: Literal["auto", "iem", "open-meteo"] = "auto"
    minimum_pairs: int = Field(default=6, ge=1, le=744)
    baseline: list[dict]


@router.post("/air-temperature")
async def validate_air_temperature(request: ValidationRequest):
    """Validate any supplied FortyGuard 2 m hourly capture with typed evidence."""
    if not request.baseline:
        raise HTTPException(status_code=422, detail="baseline must contain hourly observations")
    try:
        return await GroundTruthValidationPipeline(database=db_manager).validate(
            request.baseline,
            latitude=request.latitude, longitude=request.longitude,
            start_date=request.start_date, end_date=request.end_date,
            station=request.station, minimum_pairs=request.minimum_pairs,
            source=request.source, scenario_id=request.scenario_id,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"external validation failed: {exc}") from exc


@router.get("/surface-context/landsat")
async def landsat_surface_context(
    min_lon: float = Query(ge=-180, le=180),
    min_lat: float = Query(ge=-90, le=90),
    max_lon: float = Query(ge=-180, le=180),
    max_lat: float = Query(ge=-90, le=90),
    datetime_range: str = Query(pattern=r"^\d{4}-\d{2}-\d{2}/\d{4}-\d{2}-\d{2}$"),
    cloud_cover_lt: float = Query(default=20, ge=0, le=100),
    summarize_first: bool = Query(default=False),
):
    """Discover Landsat LST scenes as surface context, never ambient air."""
    if min_lon >= max_lon or min_lat >= max_lat:
        raise HTTPException(status_code=422, detail="bbox minimums must be below maximums")
    try:
        client = AsyncLandsatLSTClient()
        result = await client.search(
            [min_lon, min_lat, max_lon, max_lat], datetime_range,
            cloud_cover_lt=cloud_cover_lt,
        )
        if summarize_first and result["observations"]:
            observation = result["observations"][0]
            result["first_scene_summary"] = await client.summarize_scene(
                observation, [min_lon, min_lat, max_lon, max_lat]
            )
            fixture_tiles = load_phoenix_fixture().get("heatmap_geojson_tiles", {}).get("features", [])
            phoenix_overlap = min_lon < -112.068 and max_lon > -112.080 and min_lat < 33.450 and max_lat > 33.447
            if fixture_tiles and phoenix_overlap:
                samples = await client.sample_polygons(observation, fixture_tiles)
                pairs = [row for row in samples if row.get("fortyguard_2m_air_c") is not None]
                if len(pairs) >= 2:
                    result["spatial_context"] = {
                        "samples": samples,
                        "metrics": spatial_surface_context_metrics(
                            [row["fortyguard_2m_air_c"] for row in pairs],
                            [row["mean_surface_temperature_c"] for row in pairs],
                        ),
                        "warning": "Fixture tile geometry is used only when the requested AOI overlaps Phoenix; LST remains surface context.",
                    }
        return result
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Landsat context search failed: {exc}") from exc


@router.get("/metro/{metro}")
async def validate_metro_stations(
    metro: Literal["phoenix", "houston", "las_vegas", "san_jose"],
    source: Literal["replay", "live"] = Query(default="replay"),
    minimum_pairs: int = Query(default=6, ge=1, le=24),
):
    """Compare the Phoenix benchmark against a sparse metro station envelope.

    Only Phoenix currently has a matching FortyGuard baseline; other metro
    names are reserved until a FortyGuard capture for the same place/time is
    supplied, preventing cross-city comparisons.
    """
    if metro != "phoenix":
        raise HTTPException(
            status_code=409,
            detail=f"no co-located FortyGuard baseline is available for {metro}",
        )
    fixture = load_phoenix_fixture()
    try:
        if source == "replay":
            reports = {}
            for station in ("phx", "dvt", "iwa"):
                payload = json.loads(
                    (FIXTURES / f"phx_{station}_2023_07_19.json").read_text(encoding="utf-8")
                )
                reports[station.upper()] = validate_fortyguard_curve(
                    fixture["hourly_forecast_12h"],
                    payload,
                    minimum_pairs=minimum_pairs,
                )
            result = aggregate_station_reports(reports)
            result.update({
                "metro": "phoenix", "data_source": "ground_truth_replay",
                "credits_spent": 0.0, "failures": [],
                "evidence_class": "frozen multi-station in-situ envelope",
            })
            return result
        return await GroundTruthValidationPipeline().validate_metro(
            fixture["hourly_forecast_12h"], metro=metro,
            start_date="2023-07-19", end_date="2023-07-19",
            minimum_pairs=minimum_pairs,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"metro validation failed: {exc}") from exc


@router.get("/phoenix-2023")
async def validate_phoenix_benchmark(
    source: Literal["auto", "iem", "open-meteo"] = Query(default="auto"),
    station: str | None = Query(default=None, min_length=3, max_length=8),
    minimum_pairs: int = Query(default=6, ge=1, le=24),
):
    """Compare the frozen FortyGuard Phoenix curve with hourly 2 m air data.

    IEM/ASOS is preferred because it is a physical observation. Open-Meteo is
    an explicitly labelled gridded fallback. This endpoint never treats
    satellite land-surface temperature as ambient air.
    """
    fixture = load_phoenix_fixture()
    metadata = fixture["scenario_metadata"]
    location = metadata["location"]
    try:
        return await GroundTruthValidationPipeline(database=db_manager).validate(
            fixture["hourly_forecast_12h"],
            latitude=float(location["latitude"]),
            longitude=float(location["longitude"]),
            start_date="2023-07-19",
            end_date="2023-07-19",
            station=station,
            minimum_pairs=minimum_pairs,
            source=source,
            scenario_id="phoenix_heatwave_july_2023",
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"external validation failed: {exc}") from exc
