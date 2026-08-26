"""Iowa Environmental Mesonet ASOS in-situ ground-truth adapter.

IEM republishes physical ASOS/AWOS observations without authentication.  This
is the primary zero-key evidence source for FortyGuard 2 m air-temperature
validation. Standard ASOS stations do not measure GHI or skin temperature;
those fields must remain absent rather than being filled from a model.
"""

from __future__ import annotations

import asyncio
import copy
import csv
import io
import logging
import math
from datetime import date, datetime, timezone
from typing import Any, Dict, Mapping, Optional

import httpx

from src.api.retry import RETRYABLE_STATUS, sleep_before_retry

logger = logging.getLogger("thermal_sentinel.ground_truth.iem")

DEFAULT_IEM_URL = "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py"
DEFAULT_IEM_STATIONS_URL = "https://mesonet.agron.iastate.edu/geojson/network/ASOS.geojson"
METRO_STATIONS = {
    "phoenix": ("PHX", "KPHX"),
    "houston": ("IAH", "KIAH"),
    "las_vegas": ("LAS", "KLAS"),
    "san_jose": ("SJC", "KSJC"),
}
METRO_STATION_GROUPS = {
    "phoenix": ("PHX", "DVT", "IWA"),
    "houston": ("IAH", "HOU", "SGR"),
    "las_vegas": ("LAS", "VGT", "HND"),
    "san_jose": ("SJC", "RHV", "NUQ"),
}


class IEMGroundTruthError(RuntimeError):
    """Raised when IEM observations cannot be safely consumed."""


def _number(value: Any) -> Optional[float]:
    if value is None or str(value).strip().lower() in {"", "m", "null", "none", "nan"}:
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def _timestamp(value: str) -> datetime:
    text = value.strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _nearest_hour(value: datetime) -> str:
    """Map METAR observations (commonly at :51/:53) to the nearest UTC hour."""
    if value.minute >= 30:
        from datetime import timedelta
        value += timedelta(hours=1)
    return value.replace(minute=0, second=0, microsecond=0).isoformat().replace("+00:00", "Z")


class AsyncIEMGroundTruthClient:
    """Async, durable-cache-first adapter for physical airport observations."""

    def __init__(
        self,
        *,
        base_url: str = DEFAULT_IEM_URL,
        timeout: float = 30.0,
        max_retries: int = 2,
        http_client: Optional[httpx.AsyncClient] = None,
        cache: Any = None,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max(0, max_retries)
        self._http_client = http_client
        self._cache = cache

    def _cache_backend(self) -> Any:
        if self._cache is not None:
            return self._cache
        from src.db.database import db_manager
        return db_manager

    @staticmethod
    def _params(station: str, start_date: str, end_date: str) -> Dict[str, Any]:
        try:
            start, end = date.fromisoformat(start_date), date.fromisoformat(end_date)
        except ValueError as exc:
            raise ValueError("dates must use YYYY-MM-DD") from exc
        if start > end:
            raise ValueError("start_date must be on or before end_date")
        # The established year/month/day form is supported by IEM's long-lived
        # download endpoint and avoids ambiguity in alternate sts/ets parsers.
        return {
            "station": station.upper().removeprefix("K"),
            "data": ["tmpf", "relh", "sknt", "drct"],
            "year1": start.year,
            "month1": start.month,
            "day1": start.day,
            "year2": end.year,
            "month2": end.month,
            "day2": end.day,
            "tz": "Etc/UTC",
            "format": "onlycomma",
            "latlon": "yes",
            "missing": "M",
            "trace": "T",
        }

    async def _request_text(self, params: Mapping[str, Any]) -> str:
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
                return response.text
            except httpx.HTTPError as exc:
                if attempt < self.max_retries:
                    await sleep_before_retry(attempt)
                    continue
                raise IEMGroundTruthError(f"IEM request failed: {exc}") from exc
        raise IEMGroundTruthError("IEM request failed")  # pragma: no cover

    @staticmethod
    def _normalize(text: str, params: Mapping[str, Any], cache_key: str) -> Dict[str, Any]:
        # IEM may prefix informational lines beginning with '#'.
        clean = "\n".join(line for line in text.splitlines() if line.strip() and not line.startswith("#"))
        reader = csv.DictReader(io.StringIO(clean))
        if not reader.fieldnames or "valid" not in reader.fieldnames:
            raise IEMGroundTruthError("IEM response is missing a CSV header or valid timestamp")

        buckets: Dict[str, list[Dict[str, Optional[float]]]] = {}
        station_coordinates: list[tuple[float, float]] = []
        for raw in reader:
            temp_c = _number(raw.get("tmpc"))
            if temp_c is None:
                temp_f = _number(raw.get("tmpf"))
                temp_c = None if temp_f is None else (temp_f - 32.0) * 5.0 / 9.0
            wind_m_s = _number(raw.get("sped"))
            if wind_m_s is None:
                knots = _number(raw.get("sknt"))
                wind_m_s = None if knots is None else knots * 0.514444
            try:
                stamp = _nearest_hour(_timestamp(str(raw.get("valid", ""))))
            except (TypeError, ValueError):
                continue
            latitude, longitude = _number(raw.get("lat")), _number(raw.get("lon"))
            if latitude is not None and longitude is not None:
                station_coordinates.append((latitude, longitude))
            buckets.setdefault(stamp, []).append(
                {
                    "temperature_2m_c": temp_c,
                    "relative_humidity_2m_pct": _number(raw.get("relh")),
                    "wind_speed_10m_m_s": wind_m_s,
                    "wind_direction_deg": _number(raw.get("drct")),
                }
            )

        def mean(rows: list[Dict[str, Optional[float]]], field: str) -> Optional[float]:
            values = [row[field] for row in rows if row[field] is not None]
            return None if not values else round(sum(values) / len(values), 4)

        series = [
            {
                "timestamp": stamp,
                "temperature_2m_c": mean(rows, "temperature_2m_c"),
                "relative_humidity_2m_pct": mean(rows, "relative_humidity_2m_pct"),
                "wind_speed_10m_m_s": mean(rows, "wind_speed_10m_m_s"),
                "wind_direction_deg": mean(rows, "wind_direction_deg"),
                "solar_ghi_w_m2": None,
                "surface_temperature_c": None,
            }
            for stamp, rows in sorted(buckets.items())
        ]
        if not series:
            raise IEMGroundTruthError("IEM response contains no parseable observations")

        station_latitude = (
            round(sum(point[0] for point in station_coordinates) / len(station_coordinates), 6)
            if station_coordinates else None
        )
        station_longitude = (
            round(sum(point[1] for point in station_coordinates) / len(station_coordinates), 6)
            if station_coordinates else None
        )
        return {
            "provider": "iem_asos",
            "data_source": "ground_truth_live",
            "series": series,
            "provenance": {
                "data_source": "ground_truth_live",
                "provider": "Iowa Environmental Mesonet ASOS archive",
                "upstream_network": "ASOS/AWOS/METAR physical station",
                "evidence_class": "in-situ station observation",
                "station": params["station"],
                "station_latitude": station_latitude,
                "station_longitude": station_longitude,
                "endpoint": DEFAULT_IEM_URL,
                "timezone": "UTC",
                "hourly_alignment": "METAR observations rounded to nearest UTC hour; multiple reports averaged",
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
                "cache_key": cache_key,
                "credits_spent": 0.0,
                "unavailable_fields": ["solar_ghi_w_m2", "surface_temperature_c"],
            },
        }

    @staticmethod
    def _as_cached(payload: Mapping[str, Any]) -> Dict[str, Any]:
        result = copy.deepcopy(dict(payload))
        result["data_source"] = "ground_truth_cached"
        result.setdefault("provenance", {})["data_source"] = "ground_truth_cached"
        result["provenance"]["credits_spent"] = 0.0
        return result

    async def discover_candidate_stations(self, latitude: float, longitude: float, *, limit: int = 5) -> list[Dict[str, Any]]:
        """Return nearest geolocated ASOS candidates for subsequent coverage ranking."""
        if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
            raise ValueError("latitude/longitude are outside valid bounds")
        try:
            if self._http_client is not None:
                response = await self._http_client.get(DEFAULT_IEM_STATIONS_URL, timeout=self.timeout)
            else:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.get(DEFAULT_IEM_STATIONS_URL)
            response.raise_for_status()
            features = response.json().get("features", [])
        except (httpx.HTTPError, ValueError, AttributeError) as exc:
            raise IEMGroundTruthError(f"IEM station discovery failed: {exc}") from exc

        def distance(feature: Mapping[str, Any]) -> float:
            coordinates = (feature.get("geometry") or {}).get("coordinates") or []
            if len(coordinates) < 2:
                return float("inf")
            lon2, lat2 = map(float, coordinates[:2])
            phi1, phi2 = math.radians(latitude), math.radians(lat2)
            dphi, dlambda = math.radians(lat2 - latitude), math.radians(lon2 - longitude)
            a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
            return 6371.0088 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        usable = [feature for feature in features if distance(feature) < float("inf")]
        if not usable:
            raise IEMGroundTruthError("IEM station catalog contains no geolocated stations")
        candidates = []
        for feature in sorted(usable, key=distance)[:max(1, limit)]:
            properties = feature.get("properties") or {}
            coordinates = feature["geometry"]["coordinates"]
            station = properties.get("sid") or properties.get("id") or feature.get("id")
            if station:
                candidates.append({
                    "station": str(station).upper().removeprefix("K"),
                    "name": properties.get("sname") or properties.get("name"),
                    "latitude": float(coordinates[1]), "longitude": float(coordinates[0]),
                    "distance_to_aoi_km": round(distance(feature), 3),
                    "catalog": DEFAULT_IEM_STATIONS_URL,
                })
        if not candidates:
            raise IEMGroundTruthError("nearest IEM stations have no identifiers")
        return candidates

    async def discover_nearest_station(self, latitude: float, longitude: float) -> Dict[str, Any]:
        return (await self.discover_candidate_stations(latitude, longitude, limit=1))[0]

    async def select_station(
        self, latitude: float, longitude: float, start_date: str, end_date: str,
        *, candidate_limit: int = 5,
    ) -> tuple[Dict[str, Any], Dict[str, Any]]:
        """Rank nearby candidates by valid hourly coverage, then distance."""
        candidates = await self.discover_candidate_stations(latitude, longitude, limit=candidate_limit)
        results = await asyncio.gather(
            *(self.fetch_hourly(row["station"], start_date, end_date) for row in candidates),
            return_exceptions=True,
        )
        ranked = []
        for candidate, result in zip(candidates, results):
            if isinstance(result, Exception):
                candidate = {**candidate, "valid_temperature_hours": 0, "error": str(result)}
            else:
                valid = sum(row.get("temperature_2m_c") is not None for row in result["series"])
                candidate = {**candidate, "valid_temperature_hours": valid, "payload": result}
            ranked.append(candidate)
        ranked.sort(key=lambda row: (-row["valid_temperature_hours"], row["distance_to_aoi_km"]))
        winner = ranked[0]
        if not winner["valid_temperature_hours"]:
            raise IEMGroundTruthError("nearby IEM candidates have no valid temperature coverage")
        payload = winner.pop("payload")
        return winner, {**payload, "provenance": {**payload["provenance"], "station_selection": ranked}}

    async def fetch_hourly(
        self,
        station: str,
        start_date: str,
        end_date: str,
        *,
        force_refresh: bool = False,
    ) -> Dict[str, Any]:
        params = self._params(station, start_date, end_date)
        cache = self._cache_backend()
        cache_params = dict(params)
        cache_params["data"] = list(params["data"])
        cache_key = cache.generate_query_hash("iem:/cgi-bin/request/asos.py", cache_params)
        if not force_refresh:
            try:
                cached = await cache.get_cached_api_call(cache_key)
                if isinstance(cached, dict) and isinstance(cached.get("series"), list):
                    return self._as_cached(cached)
            except Exception as exc:
                logger.warning("IEM cache lookup failed: %s", exc)

        result = self._normalize(await self._request_text(params), params, cache_key)
        try:
            from src.db.models import ApiCallCacheRecord
            await cache.save_cached_api_call(
                ApiCallCacheRecord(
                    query_hash=cache_key,
                    endpoint="iem:/cgi-bin/request/asos.py",
                    request_params=cache_params,
                    response_payload=result,
                    credits_spent=0.0,
                )
            )
        except Exception as exc:
            logger.warning("Failed to persist IEM ground truth %s: %s", cache_key, exc)
        return result

    async def fetch_metro(self, metro: str, start_date: str, end_date: str) -> Dict[str, Any]:
        key = metro.lower().replace(" ", "_")
        if key not in METRO_STATIONS:
            raise ValueError(f"unknown metro: {metro}")
        station, _icao = METRO_STATIONS[key]
        return await self.fetch_hourly(station, start_date, end_date)

    async def fetch_metro_stations(
        self, metro: str, start_date: str, end_date: str
    ) -> Dict[str, Any]:
        """Fetch a predefined metro station group concurrently, preserving failures."""
        key = metro.lower().replace(" ", "_")
        if key not in METRO_STATION_GROUPS:
            raise ValueError(f"unknown metro: {metro}")
        stations = METRO_STATION_GROUPS[key]
        results = await asyncio.gather(
            *(self.fetch_hourly(station, start_date, end_date) for station in stations),
            return_exceptions=True,
        )
        observations, failures = {}, []
        for station, result in zip(stations, results):
            if isinstance(result, Exception):
                failures.append({"station": station, "reason": str(result)})
            else:
                observations[station] = result
        if not observations:
            raise IEMGroundTruthError(
                f"no usable {key} stations: "
                + "; ".join(f"{row['station']}: {row['reason']}" for row in failures)
            )
        return {
            "metro": key,
            "requested_stations": list(stations),
            "stations": observations,
            "failures": failures,
            "data_source": (
                "ground_truth_cached"
                if all(row.get("data_source") == "ground_truth_cached" for row in observations.values())
                else "ground_truth_live"
            ),
            "credits_spent": 0.0,
        }
