"""Evidence-aware orchestration for external FortyGuard validation.

The pipeline prefers physical station observations and falls back to gridded
meteorology. Satellite skin temperature is intentionally outside this contract:
it must never be substituted for the 2 m air boundary used by the physics code.
"""

from __future__ import annotations

import hashlib
import json
import math
import statistics
from typing import Any, Mapping, Sequence

from src.api.ground_truth_client import AsyncGroundTruthClient
from src.api.iem_ground_truth_client import AsyncIEMGroundTruthClient
from src.db.models import ValidationRunRecord
from src.data_science.ground_truth_validation import (
    GroundTruthValidationError,
    validate_fortyguard_curve,
)


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two WGS84 coordinate pairs."""
    values = (lat1, lon1, lat2, lon2)
    if not all(math.isfinite(float(value)) for value in values):
        raise ValueError("coordinates must be finite")
    if not (-90 <= lat1 <= 90 and -90 <= lat2 <= 90 and -180 <= lon1 <= 180 and -180 <= lon2 <= 180):
        raise ValueError("coordinates are outside valid bounds")
    radius_km = 6371.0088
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    return radius_km * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def aggregate_station_reports(reports: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    """Summarize per-station validation without pretending stations are pixels."""
    usable = {
        station: report for station, report in reports.items()
        if isinstance((report.get("metrics") or {}).get("temperature_2m"), Mapping)
    }
    if not usable:
        raise GroundTruthValidationError("no usable station reports")
    temperature = {
        station: report["metrics"]["temperature_2m"] for station, report in usable.items()
    }
    return {
        "station_count": len(temperature),
        "stations": usable,
        "metro_summary": {
            "median_mae_c": round(statistics.median(row["mae"] for row in temperature.values()), 4),
            "median_rmse_c": round(statistics.median(row["rmse"] for row in temperature.values()), 4),
            "median_bias_c": round(statistics.median(row["mean_bias"] for row in temperature.values()), 4),
            "min_station_peak_c": round(min(row["ground_truth_peak"] for row in temperature.values()), 4),
            "max_station_peak_c": round(max(row["ground_truth_peak"] for row in temperature.values()), 4),
            "station_peak_spread_c": round(
                max(row["ground_truth_peak"] for row in temperature.values())
                - min(row["ground_truth_peak"] for row in temperature.values()), 4
            ),
            "minimum_coverage_pct": round(min(row["coverage_pct"] for row in temperature.values()), 2),
            "interpretation": "Sparse station envelope; not parcel-level validation.",
        },
    }


class GroundTruthValidationPipeline:
    """Select, annotate, and validate an hourly 2 m air reference series."""

    def __init__(
        self,
        *,
        iem_client: AsyncIEMGroundTruthClient | None = None,
        gridded_client: AsyncGroundTruthClient | None = None,
        database: Any = None,
    ) -> None:
        self.iem_client = iem_client or AsyncIEMGroundTruthClient()
        self.gridded_client = gridded_client or AsyncGroundTruthClient()
        self.database = database

    @staticmethod
    def _identity(value: Any) -> str:
        rendered = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
        return hashlib.sha256(rendered.encode("utf-8")).hexdigest()

    async def _persist(self, report: dict[str, Any], baseline: Sequence[Mapping[str, Any]], configuration: dict[str, Any]) -> None:
        if self.database is None:
            return
        reference_identity = self._identity({
            "provider": report.get("provider"), "provenance": report.get("provenance"),
            "metrics_window": report.get("metrics", {}).get("temperature_2m", {}).get("paired_series", []),
        })
        baseline_identity = self._identity(baseline)
        validation_id = self._identity({
            "baseline": baseline_identity, "reference": reference_identity, "configuration": configuration,
        })
        await self.database.save_validation_run(ValidationRunRecord(
            validation_id=validation_id,
            scenario_id=str(configuration.get("scenario_id", "ad_hoc")),
            provider=str(report.get("provider")),
            evidence_class=str((report.get("provenance") or {}).get("evidence_class", "unknown")),
            baseline_identity=baseline_identity,
            reference_identity=reference_identity,
            configuration=configuration,
            report=report,
        ))
        report["validation_id"] = validation_id

    @staticmethod
    def _annotate_station_distance(payload: Mapping[str, Any], latitude: float, longitude: float) -> dict[str, Any]:
        result = dict(payload)
        provenance = dict(result.get("provenance") or {})
        station_lat = provenance.get("station_latitude")
        station_lon = provenance.get("station_longitude")
        if station_lat is not None and station_lon is not None:
            provenance["distance_to_aoi_km"] = round(
                haversine_km(latitude, longitude, float(station_lat), float(station_lon)), 3
            )
        else:
            provenance["distance_to_aoi_km"] = None
        provenance["target_latitude"] = latitude
        provenance["target_longitude"] = longitude
        result["provenance"] = provenance
        return result

    async def validate_metro(
        self,
        baseline: Sequence[Mapping[str, Any]],
        *,
        metro: str,
        start_date: str,
        end_date: str,
        minimum_pairs: int = 6,
    ) -> dict[str, Any]:
        """Validate against each available physical station in a metro group."""
        payload = await self.iem_client.fetch_metro_stations(metro, start_date, end_date)
        reports, failures = {}, list(payload.get("failures", []))
        for station, station_payload in payload["stations"].items():
            try:
                reports[station] = validate_fortyguard_curve(
                    baseline, station_payload, minimum_pairs=minimum_pairs
                )
            except Exception as exc:
                failures.append({"station": station, "reason": str(exc)})
        result = aggregate_station_reports(reports)
        result.update({
            "metro": payload["metro"],
            "data_source": payload["data_source"],
            "credits_spent": 0.0,
            "failures": failures,
            "evidence_class": "multi-station in-situ envelope",
        })
        return result

    async def validate(
        self,
        baseline: Sequence[Mapping[str, Any]],
        *,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str,
        station: str | None,
        minimum_pairs: int = 6,
        source: str = "auto",
        scenario_id: str = "ad_hoc",
    ) -> dict[str, Any]:
        """Run validation, using gridded data only when station evidence fails.

        ``source`` may be ``auto``, ``iem``, or ``open-meteo``. Forced IEM
        requests fail closed rather than silently changing evidence class.
        """
        if source not in {"auto", "iem", "open-meteo"}:
            raise ValueError("source must be auto, iem, or open-meteo")

        failures: list[dict[str, str]] = []
        selected_station = station
        discovery: dict[str, Any] | None = None
        if source in {"auto", "iem"}:
            try:
                if not selected_station:
                    discovery, station_payload = await self.iem_client.select_station(
                        latitude, longitude, start_date, end_date
                    )
                    selected_station = str(discovery["station"])
                else:
                    station_payload = await self.iem_client.fetch_hourly(selected_station, start_date, end_date)
                station_payload = self._annotate_station_distance(station_payload, latitude, longitude)
                report = validate_fortyguard_curve(
                    baseline, station_payload, minimum_pairs=minimum_pairs
                )
                report["selection"] = {
                    "requested_source": source,
                    "selected_source": "iem",
                    "fallback_used": False,
                    "station_discovery": discovery,
                    "failures": failures,
                }
                await self._persist(report, baseline, {
                    "scenario_id": scenario_id, "source": source,
                    "station": selected_station, "latitude": latitude, "longitude": longitude,
                    "start_date": start_date, "end_date": end_date, "minimum_pairs": minimum_pairs,
                })
                return report
            except Exception as exc:
                if source == "iem":
                    raise
                failures.append({"source": "iem", "reason": str(exc)})

        try:
            gridded_payload = await self.gridded_client.fetch_hourly(
                latitude, longitude, start_date, end_date
            )
            report = validate_fortyguard_curve(
                baseline, gridded_payload, minimum_pairs=minimum_pairs
            )
        except Exception as exc:
            failures.append({"source": "open-meteo", "reason": str(exc)})
            raise GroundTruthValidationError(
                "no usable 2 m air-temperature reference: "
                + "; ".join(f"{row['source']}: {row['reason']}" for row in failures)
            ) from exc

        report["selection"] = {
            "requested_source": source,
            "selected_source": "open-meteo",
            "fallback_used": source == "auto",
            "failures": failures,
        }
        await self._persist(report, baseline, {
            "scenario_id": scenario_id, "source": source,
            "station": station, "latitude": latitude, "longitude": longitude,
            "start_date": start_date, "end_date": end_date, "minimum_pairs": minimum_pairs,
        })
        return report
