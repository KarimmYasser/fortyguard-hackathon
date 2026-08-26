"""Open/free meteorological benchmark adapter.

Open-Meteo's Historical Archive is used because it is the only no-key source in
our evaluated set that provides a consistent temperature, humidity, wind,
solar, and surface-temperature series for every target metro.  It is an
ERA5/ERA5-Land-derived gridded benchmark, not an in-situ station observation;
that distinction is retained in every response's provenance.
"""

from __future__ import annotations

import asyncio
import copy
import logging
import math
from datetime import date, datetime, timezone
from typing import Any, Dict, Iterable, Mapping, Optional, Sequence

import httpx

from src.api.retry import RETRYABLE_STATUS, sleep_before_retry

logger = logging.getLogger("thermal_sentinel.ground_truth")

DEFAULT_BASE_URL = "https://archive-api.open-meteo.com/v1/archive"
HOURLY_VARIABLES = (
    "temperature_2m",
    "relative_humidity_2m",
    "wind_speed_10m",
    "shortwave_radiation_instant",
    "surface_temperature",
)
FIELD_MAP = {
    "temperature_2m": "temperature_2m_c",
    "relative_humidity_2m": "relative_humidity_2m_pct",
    "wind_speed_10m": "wind_speed_10m_m_s",
    "shortwave_radiation_instant": "solar_ghi_w_m2",
    "surface_temperature": "surface_temperature_c",
}
METRO_COORDINATES = {
    "phoenix": (33.4484, -112.0740),
    "houston": (29.7604, -95.3698),
    "san_jose": (37.3382, -121.8863),
}


class GroundTruthError(RuntimeError):
    """Raised when a benchmark response cannot be safely consumed."""


def _iso_hour(value: str) -> str:
    """Normalize an ISO timestamp to a UTC, hour-resolution cache/join key."""
    text = value.strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).replace(minute=0, second=0, microsecond=0).isoformat().replace("+00:00", "Z")


def _finite_number(value: Any) -> Optional[float]:
    if value is None or isinstance(value, bool):
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


class AsyncGroundTruthClient:
    """Async, durable-cache-first client for Open-Meteo historical data."""

    def __init__(
        self,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 2,
        http_client: Optional[httpx.AsyncClient] = None,
        cache: Any = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max(0, max_retries)
        self._http_client = http_client
        self._cache = cache

    @staticmethod
    def _validate_request(latitude: float, longitude: float, start_date: str, end_date: str) -> None:
        if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
            raise ValueError("latitude/longitude are outside valid bounds")
        try:
            start = date.fromisoformat(start_date)
            end = date.fromisoformat(end_date)
        except ValueError as exc:
            raise ValueError("dates must use YYYY-MM-DD") from exc
        if start > end:
            raise ValueError("start_date must be on or before end_date")

    def _params(self, latitude: float, longitude: float, start_date: str, end_date: str) -> Dict[str, Any]:
        return {
            "latitude": round(float(latitude), 6),
            "longitude": round(float(longitude), 6),
            "start_date": start_date,
            "end_date": end_date,
            "hourly": ",".join(HOURLY_VARIABLES),
            "timezone": "UTC",
            "wind_speed_unit": "ms",
            "models": "era5_land",
        }

    def _cache_backend(self) -> Any:
        if self._cache is not None:
            return self._cache
        from src.db.database import db_manager
        return db_manager

    async def _request_json(self, params: Mapping[str, Any]) -> Dict[str, Any]:
        for attempt in range(self.max_retries + 1):
            try:
                if self._http_client is not None:
                    response = await self._http_client.get(self.base_url, params=params, timeout=self.timeout)
                else:
                    async with httpx.AsyncClient(timeout=self.timeout) as client:
                        response = await client.get(self.base_url, params=params)
                if response.status_code in RETRYABLE_STATUS and attempt < self.max_retries:
                    await sleep_before_retry(attempt, response.headers)
                    continue
                response.raise_for_status()
                payload = response.json()
                if not isinstance(payload, dict) or payload.get("error"):
                    raise GroundTruthError(str(payload.get("reason", "invalid Open-Meteo response")))
                return payload
            except GroundTruthError:
                raise
            except (httpx.HTTPError, ValueError) as exc:
                if attempt < self.max_retries:
                    await sleep_before_retry(attempt)
                    continue
                raise GroundTruthError(f"Open-Meteo request failed: {exc}") from exc
        raise GroundTruthError("Open-Meteo request failed")  # pragma: no cover

    @staticmethod
    def _normalize(payload: Mapping[str, Any], params: Mapping[str, Any], cache_key: str) -> Dict[str, Any]:
        hourly = payload.get("hourly")
        if not isinstance(hourly, Mapping) or not isinstance(hourly.get("time"), list):
            raise GroundTruthError("Open-Meteo response is missing hourly.time")
        times = hourly["time"]
        arrays: Dict[str, Sequence[Any]] = {}
        for remote_name in HOURLY_VARIABLES:
            values = hourly.get(remote_name)
            if not isinstance(values, list) or len(values) != len(times):
                raise GroundTruthError(f"Open-Meteo response has an invalid {remote_name} array")
            arrays[remote_name] = values

        series = []
        for index, timestamp in enumerate(times):
            row: Dict[str, Any] = {"timestamp": _iso_hour(str(timestamp))}
            for remote_name, local_name in FIELD_MAP.items():
                row[local_name] = _finite_number(arrays[remote_name][index])
            series.append(row)

        now = datetime.now(timezone.utc).isoformat()
        return {
            "provider": "open_meteo_historical_archive",
            "data_source": "ground_truth_live",
            "series": series,
            "provenance": {
                "data_source": "ground_truth_live",
                "provider": "Open-Meteo Historical Weather API",
                "upstream_models": payload.get("model") or params.get("models", "era5_land"),
                "model_pinned": True,
                "grid_metadata": {
                    "response_latitude": _finite_number(payload.get("latitude")),
                    "response_longitude": _finite_number(payload.get("longitude")),
                    "elevation_m": _finite_number(payload.get("elevation")),
                    "utc_offset_seconds": _finite_number(payload.get("utc_offset_seconds")),
                },
                "evidence_class": "gridded meteorological benchmark (not an in-situ sensor)",
                "endpoint": DEFAULT_BASE_URL,
                "latitude": params["latitude"],
                "longitude": params["longitude"],
                "start_date": params["start_date"],
                "end_date": params["end_date"],
                "timezone": "UTC",
                "retrieved_at": now,
                "cache_key": cache_key,
                "credits_spent": 0.0,
            },
        }

    @staticmethod
    def _as_cached(payload: Mapping[str, Any]) -> Dict[str, Any]:
        result = copy.deepcopy(dict(payload))
        result["data_source"] = "ground_truth_cached"
        provenance = result.setdefault("provenance", {})
        provenance["data_source"] = "ground_truth_cached"
        provenance["credits_spent"] = 0.0
        return result

    async def fetch_hourly(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str,
        *,
        force_refresh: bool = False,
    ) -> Dict[str, Any]:
        """Fetch one UTC hourly series, using durable cache before the network.

        No credit-ledger entry is created: this upstream is free, and a replay
        must never be represented as a paid FortyGuard call.
        """
        self._validate_request(latitude, longitude, start_date, end_date)
        params = self._params(latitude, longitude, start_date, end_date)
        cache = self._cache_backend()
        cache_key = cache.generate_query_hash("open-meteo:/v1/archive", params)

        if not force_refresh:
            try:
                cached = await cache.get_cached_api_call(cache_key)
                if isinstance(cached, dict) and isinstance(cached.get("series"), list):
                    return self._as_cached(cached)
            except Exception as exc:  # cache outages must not mask a usable public API
                logger.warning("Ground-truth cache lookup failed: %s", exc)

        raw = await self._request_json(params)
        result = self._normalize(raw, params, cache_key)
        try:
            from src.db.models import ApiCallCacheRecord
            await cache.save_cached_api_call(
                ApiCallCacheRecord(
                    query_hash=cache_key,
                    endpoint="open-meteo:/v1/archive",
                    request_params=params,
                    response_payload=result,
                    credits_spent=0.0,
                )
            )
        except Exception as exc:  # successful evidence remains usable if persistence is down
            logger.warning("Failed to persist ground-truth response %s: %s", cache_key, exc)
        return result

    async def fetch_metros(
        self,
        metros: Iterable[str],
        start_date: str,
        end_date: str,
    ) -> Dict[str, Dict[str, Any]]:
        """Fetch known target metros concurrently."""
        names = [name.lower().replace(" ", "_") for name in metros]
        unknown = sorted(set(names) - METRO_COORDINATES.keys())
        if unknown:
            raise ValueError(f"unknown metros: {', '.join(unknown)}")
        results = await asyncio.gather(
            *(self.fetch_hourly(*METRO_COORDINATES[name], start_date, end_date) for name in names)
        )
        return dict(zip(names, results))
