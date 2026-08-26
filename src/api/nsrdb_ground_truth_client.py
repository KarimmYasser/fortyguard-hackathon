"""NLR NSRDB GOES Aggregated PSM v4 solar benchmark adapter."""

from __future__ import annotations

import copy
import csv
import io
import logging
import math
import os
from datetime import date, datetime, timedelta, timezone
from typing import Any, Mapping, Optional

import httpx

from src.api.retry import RETRYABLE_STATUS, sleep_before_retry

# NREL was renamed NLR in 2025. PSM v3.2.2 was superseded by the GOES
# Aggregated PSM v4 product; this is the current documented CONUS endpoint.
DEFAULT_NSRDB_URL = (
    "https://developer.nlr.gov/api/nsrdb/v2/solar/"
    "nsrdb-GOES-aggregated-v4-0-0-download.csv"
)
logger = logging.getLogger("thermal_sentinel.ground_truth.nsrdb")


class NSRDBGroundTruthError(RuntimeError):
    pass


def _number(value: Any) -> Optional[float]:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


class AsyncNSRDBGroundTruthClient:
    """Fetch hourly PSM data, with explicit modeled-solar provenance."""

    def __init__(self, *, api_key: str | None = None, email: str | None = None,
                 base_url: str = DEFAULT_NSRDB_URL, timeout: float = 60.0,
                 max_retries: int = 2, http_client=None, cache=None) -> None:
        self.api_key = api_key or os.getenv("NREL_API_KEY")
        self.email = email or os.getenv("NREL_EMAIL")
        self.base_url, self.timeout, self.max_retries = base_url, timeout, max_retries
        self.http_client, self.cache = http_client, cache

    def _cache(self):
        if self.cache is not None:
            return self.cache
        from src.db.database import db_manager
        return db_manager

    def _params(self, latitude: float, longitude: float, year: int) -> dict[str, Any]:
        if not self.api_key or not self.email:
            raise NSRDBGroundTruthError("NREL_API_KEY and NREL_EMAIL are required")
        if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
            raise ValueError("latitude/longitude are outside valid bounds")
        return {
            "api_key": self.api_key, "email": self.email,
            "wkt": f"POINT({longitude:.6f} {latitude:.6f})", "names": str(year),
            "interval": "60", "utc": "true", "leap_day": "true",
            "attributes": "ghi,dni,dhi,air_temperature,relative_humidity,wind_speed,surface_albedo,surface_pressure",
        }

    @staticmethod
    def _safe_cache_params(params: Mapping[str, Any]) -> dict[str, Any]:
        return {key: value for key, value in params.items() if key not in {"api_key", "email"}}

    async def _text(self, params: Mapping[str, Any]) -> str:
        for attempt in range(self.max_retries + 1):
            try:
                if self.http_client is not None:
                    response = await self.http_client.get(
                        self.base_url, params=params, timeout=self.timeout, follow_redirects=True
                    )
                else:
                    async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                        response = await client.get(self.base_url, params=params)
                if response.status_code in RETRYABLE_STATUS and attempt < self.max_retries:
                    await sleep_before_retry(attempt, response.headers)
                    continue
                if response.status_code == 404:
                    raise NSRDBGroundTruthError(
                        "NSRDB returned 404. Verify that your NLR developer key is active "
                        "and authorized for the GOES Aggregated PSM v4 download API; use --source open-meteo "
                        "for the no-key modeled fallback."
                    )
                response.raise_for_status()
                return response.text
            except NSRDBGroundTruthError:
                raise
            except httpx.ConnectError as exc:
                raise NSRDBGroundTruthError(
                    f"cannot resolve or connect to NSRDB host {self.base_url!r}; "
                    "check DNS/network access or use --source open-meteo"
                ) from exc
            except httpx.HTTPError as exc:
                if attempt < self.max_retries:
                    await sleep_before_retry(attempt)
                    continue
                # Do not stringify httpx request errors: their URLs include the
                # API key and email query parameters.
                raise NSRDBGroundTruthError(
                    f"NSRDB request failed ({type(exc).__name__}); use --source open-meteo "
                    "if the credentialed service is unavailable"
                ) from exc
        raise NSRDBGroundTruthError("NSRDB request failed")  # pragma: no cover

    @staticmethod
    def _normalize(text: str, start: date, end: date, cache_key: str) -> dict[str, Any]:
        lines = text.splitlines()
        header = next((i for i, line in enumerate(lines) if line.startswith("Year,")), None)
        if header is None:
            raise NSRDBGroundTruthError("NSRDB CSV is missing its Year header")
        series = []
        for row in csv.DictReader(io.StringIO("\n".join(lines[header:]))):
            try:
                stamp = datetime(int(row["Year"]), int(row["Month"]), int(row["Day"]),
                                 int(row["Hour"]), int(row.get("Minute", 0)), tzinfo=timezone.utc)
            except (KeyError, TypeError, ValueError):
                continue
            if not start <= stamp.date() <= end:
                continue
            # Hourly PSM v4 records are timestamped at interval midpoint (:30).
            # Align to the nearest UTC hour, matching the FortyGuard hourly key.
            if stamp.minute >= 30:
                stamp += timedelta(hours=1)
            stamp = stamp.replace(minute=0, second=0, microsecond=0)
            series.append({
                "timestamp": stamp.isoformat().replace("+00:00", "Z"),
                "temperature_2m_c": _number(row.get("Temperature") or row.get("Air Temperature")),
                "relative_humidity_2m_pct": _number(row.get("Relative Humidity")),
                "wind_speed_10m_m_s": _number(row.get("Wind Speed")),
                "solar_ghi_w_m2": _number(row.get("GHI")),
                "solar_dni_w_m2": _number(row.get("DNI")),
                "solar_dhi_w_m2": _number(row.get("DHI")),
                # GOES Aggregated PSM v4 does not publish skin temperature.
                "surface_temperature_c": None,
                "surface_albedo": _number(row.get("Surface Albedo")),
                "surface_pressure": _number(row.get("Pressure") or row.get("Surface Pressure")),
            })
        if not series:
            raise NSRDBGroundTruthError("NSRDB response has no rows in the requested date window")
        return {
            "provider": "nlr_nsrdb_goes_aggregated_v4", "data_source": "ground_truth_live", "series": series,
            "provenance": {
                "data_source": "ground_truth_live", "provider": "NLR NSRDB GOES Aggregated PSM v4",
                "evidence_class": "satellite physical-model solar benchmark (not in-situ)",
                "product": "nsrdb-GOES-aggregated-v4-0-0",
                "unavailable_fields": ["surface_temperature_c"],
                "timezone": "UTC",
                "hourly_alignment": "PSM v4 :30 interval midpoints rounded to nearest UTC hour",
                "cache_key": cache_key, "credits_spent": 0.0,
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
            },
        }

    async def fetch_hourly(self, latitude: float, longitude: float, start_date: str,
                           end_date: str, *, force_refresh: bool = False) -> dict[str, Any]:
        start, end = date.fromisoformat(start_date), date.fromisoformat(end_date)
        if start > end or start.year != end.year:
            raise ValueError("NSRDB requests must be ordered and within one calendar year")
        params = self._params(latitude, longitude, start.year)
        safe = self._safe_cache_params(params) | {
            "start_date": start_date, "end_date": end_date, "parser_version": 2,
        }
        cache = self._cache()
        key = cache.generate_query_hash(
            "nlr:/api/nsrdb/v2/solar/nsrdb-GOES-aggregated-v4-0-0-download.csv", safe
        )
        if not force_refresh:
            cached = await cache.get_cached_api_call(key)
            # Read the pre-parser-version cache identity during migration. New
            # writes always use parser_version=2, so stale formats age out.
            if not isinstance(cached, dict):
                legacy_safe = {k: v for k, v in safe.items() if k != "parser_version"}
                legacy_key = cache.generate_query_hash(
                    "nlr:/api/nsrdb/v2/solar/nsrdb-GOES-aggregated-v4-0-0-download.csv",
                    legacy_safe,
                )
                cached = await cache.get_cached_api_call(legacy_key)
            if isinstance(cached, dict) and isinstance(cached.get("series"), list):
                result = copy.deepcopy(cached)
                result["data_source"] = result["provenance"]["data_source"] = "ground_truth_cached"
                result["provenance"]["credits_spent"] = 0.0
                return result
        result = self._normalize(await self._text(params), start, end, key)
        try:
            from src.db.models import ApiCallCacheRecord
            await cache.save_cached_api_call(ApiCallCacheRecord(
                query_hash=key,
                endpoint="nlr:/api/nsrdb/v2/solar/nsrdb-GOES-aggregated-v4-0-0-download.csv",
                request_params=safe, response_payload=result, credits_spent=0.0,
            ))
        except Exception as exc:
            logger.warning("Failed to persist NSRDB benchmark %s: %s", key, exc)
        return result
