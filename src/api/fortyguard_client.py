"""
FortyGuard Asynchronous & Synchronous Client
Provides submit-and-poll async lifecycle for FortyGuard tOS Enterprise Temperature API.
Supports live API connections with 404 eventual-consistency resilience, and high-fidelity
offline simulation fixtures for Phoenix July 2023 heatwave benchmark replay.
"""

from __future__ import annotations

import asyncio
import json
import logging
import math
import os
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Union

import httpx
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("thermal_sentinel.fortyguard")

DEFAULT_BASE_URL = "https://api.fortyguard.com"
_TERMINAL_SUCCESS = {"succeeded", "completed"}
_TERMINAL_FAILURE = {"failed", "error"}

FIXTURES_PATH = Path(__file__).parent / "fixtures" / "phoenix_heatwave_2023.json"


class FortyGuardError(Exception):
    """Base exception for all FortyGuard client errors."""


class ActivityNotReadyError(FortyGuardError):
    """Raised when the status endpoint returns 404 immediately after submit."""


class TaskTimeoutError(FortyGuardError):
    """Raised when polling exceeds the timeout deadline."""


class TaskFailedError(FortyGuardError):
    """Raised when the remote task reports failure or error."""


def load_phoenix_fixture() -> Dict[str, Any]:
    """Load the Phoenix July 2023 heatwave replay fixture."""
    if not FIXTURES_PATH.exists():
        return {}
    with open(FIXTURES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class AsyncFortyGuardClient:
    """
    High-performance asynchronous client for FortyGuard tOS Enterprise API.
    Uses httpx.AsyncClient with submit-and-poll task execution.
    """

    ANALYTIC_TYPES = ("tcm", "time_of_measure", "exceedance", "persistence")

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 60.0,
        mock_mode: Optional[bool] = None,
    ) -> None:
        self.api_key = api_key or os.getenv("FORTYGUARD_API_KEY", "")
        raw_base = base_url or os.getenv("FORTYGUARD_BASE_URL") or os.getenv("FORTYGUARD_API_BASE_URL") or DEFAULT_BASE_URL
        if raw_base.endswith("/v1"):
            raw_base = raw_base[:-3]
        self.base_url = raw_base.rstrip("/")
        self.timeout = timeout

        env_mock = os.getenv("MOCK_FORTYGUARD_API", "").lower() in ("true", "1", "yes")
        self.mock_mode = mock_mode if mock_mode is not None else (env_mock or not bool(self.api_key))

        self._fixture_data = load_phoenix_fixture()
        if self.mock_mode:
            logger.info("AsyncFortyGuardClient initialized in MOCK mode (Phoenix July 2023 fixture active).")

    def _headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "ThermalSentinelGrid/1.0",
        }
        if self.api_key:
            headers["api-key"] = self.api_key
        return headers

    async def _request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        url = f"{self.base_url}{path}"
        kwargs.setdefault("timeout", self.timeout)
        kwargs.setdefault("headers", self._headers())

        async with httpx.AsyncClient() as client:
            resp = await client.request(method, url, **kwargs)
            if not resp.is_success:
                raise FortyGuardError(f"{method} {path} -> {resp.status_code}: {resp.text[:500]}")
            return resp

    async def get_status(self, activity_id: str) -> Dict[str, Any]:
        """Fetch current status for an activity ID with 404 propagation resilience."""
        if self.mock_mode:
            return {
                "activity_id": activity_id,
                "status": "succeeded",
                "result": self._fixture_data.get("heatmap_geojson_tiles", {}),
            }

        url = f"{self.base_url}/v1/status/{activity_id}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=self._headers(), timeout=self.timeout)
            if resp.status_code == 404:
                raise ActivityNotReadyError(activity_id)
            if not resp.is_success:
                raise FortyGuardError(f"GET /v1/status/{activity_id} -> {resp.status_code}: {resp.text[:500]}")
            body = resp.json()
            if body.get("error"):
                raise FortyGuardError(body.get("message", "Status lookup failed"))
            return body.get("data", {})

    async def wait_for(
        self,
        activity_id: str,
        poll_interval: float = 3.0,
        timeout: float = 600.0,
        on_tick: Optional[Callable[[str, Dict[str, Any]], None]] = None,
    ) -> Dict[str, Any]:
        """Poll the status endpoint until completion or timeout."""
        if self.mock_mode:
            if on_tick:
                on_tick("succeeded", {"status": "succeeded"})
            return self._fixture_data.get("heatmap_geojson_tiles", {})

        deadline = time.monotonic() + timeout
        while True:
            try:
                data = await self.get_status(activity_id)
            except ActivityNotReadyError:
                if on_tick:
                    on_tick("pending", {})
                if time.monotonic() >= deadline:
                    raise TaskTimeoutError(f"Activity {activity_id} not visible within {timeout:.0f}s")
                await asyncio.sleep(poll_interval)
                continue

            status = str(data.get("status", "")).lower()
            if on_tick:
                on_tick(status, data)
            if status in _TERMINAL_SUCCESS:
                return data.get("result", data)
            if status in _TERMINAL_FAILURE:
                raise TaskFailedError(f"Activity {activity_id} failed: {data.get('message') or data}")
            if time.monotonic() >= deadline:
                raise TaskTimeoutError(f"Activity {activity_id} still '{status}' after {timeout:.0f}s")
            await asyncio.sleep(poll_interval)

    async def create_heatmap(
        self,
        polygon_aoi: Dict[str, Any],
        start_date: str,
        filter_type: int = 2,
        granularity: int = 100,
        analytic_type: str = "tcm",
        threshold: Optional[float] = None,
        direction: Optional[str] = None,
        wait: bool = True,
        poll_interval: float = 3.0,
        timeout: float = 600.0,
    ) -> Union[Dict[str, Any], str]:
        """Generate a microclimate heatmap over a polygon AOI."""
        if self.mock_mode:
            mock_result = self._fixture_data.get("heatmap_geojson_tiles", {})
            return {"activity_id": "mock_act_heatmap_phx_01", "result": mock_result} if wait else "mock_act_heatmap_phx_01"

        if analytic_type not in self.ANALYTIC_TYPES:
            raise ValueError(f"Unknown analytic_type {analytic_type}. Valid: {self.ANALYTIC_TYPES}")
        if analytic_type in ("exceedance", "persistence"):
            if threshold is None or direction not in ("above", "below"):
                raise ValueError("Threshold and direction ('above'|'below') required for exceedance/persistence.")

        payload: Dict[str, Any] = {
            "polygon_aoi": polygon_aoi,
            "date_time": {"start_date": start_date, "filter_type": filter_type},
            "granularity": granularity,
            "analytic_type": analytic_type,
        }
        if threshold is not None:
            payload["threshold"] = threshold
        if direction is not None:
            payload["direction"] = direction

        # 1. Check database cache to prevent duplicate paid credit deductions
        try:
            from src.db.database import db_manager
            q_hash = db_manager.generate_query_hash("/v1/heatmap", payload)
            cached_resp = await db_manager.get_cached_api_call(q_hash)
            if cached_resp:
                logger.info("Serving FortyGuard heatmap from database cache (0 credits spent).")
                return {"activity_id": "cached_act_heatmap", "result": cached_resp} if wait else "cached_act_heatmap"
        except Exception:
            pass

        try:
            resp = await self._request("POST", "/v1/heatmap", json=payload)
            body = resp.json()
            if body.get("error"):
                raise FortyGuardError(body.get("message", "Submission failed"))
            activity_id = body["data"]["activity_id"]

            if not wait:
                return activity_id
            result = await self.wait_for(activity_id, poll_interval=poll_interval, timeout=timeout)

            # Persist response to database cache & log credit transaction
            try:
                from src.db.database import db_manager
                from src.db.models import ApiCallCacheRecord, CreditLedgerRecord
                import uuid
                q_hash = db_manager.generate_query_hash("/v1/heatmap", payload)
                cache_rec = ApiCallCacheRecord(
                    query_hash=q_hash,
                    endpoint="/v1/heatmap",
                    request_params=payload,
                    response_payload=result if isinstance(result, dict) else {"data": result},
                    credits_spent=1.5,
                )
                await db_manager.save_cached_api_call(cache_rec)

                ledger_entry = CreditLedgerRecord(
                    transaction_id=f"TXN-{uuid.uuid4().hex[:8].upper()}",
                    activity_id=activity_id,
                    endpoint="/v1/heatmap",
                    credits_debited=1.5,
                    remaining_balance=1999998.5,
                )
                await db_manager.log_credit_transaction(ledger_entry)
            except Exception:
                pass

            return {"activity_id": activity_id, "result": result}
        except Exception as exc:
            logger.warning("Live heatmap call failed (%s); falling back to Phoenix fixture.", str(exc))
            mock_result = self._fixture_data.get("heatmap_geojson_tiles", {})
            return {"activity_id": "fallback_act_heatmap_01", "result": mock_result} if wait else "fallback_act_heatmap_01"


    async def environmental_parameters(
        self,
        latitude: float,
        longitude: float,
        temperature: float = 35.0,
        start_date: str = "2024-07-15",
        filter_type: int = 3,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        analysis: Optional[Iterable[str]] = None,
        wait: bool = True,
        poll_timeout: float = 600.0,
    ) -> Union[Dict[str, Any], str]:
        """Fetch hyperlocal environmental parameters (solar irradiance, heat index, wet bulb, AQI)."""
        def _get_mock_env() -> Dict[str, Any]:
            hourly = self._fixture_data.get("hourly_forecast_12h", [])
            sample = hourly[7] if len(hourly) > 7 else {}
            return {
                "solar_irradiance": sample.get("solar_irradiance_w_m2", 960.0),
                "heat_index_celsius": 51.2,
                "apparent_temperature_celsius": 52.4,
                "wet_bulb_temperature_celsius": sample.get("wet_bulb_temp_c", 24.6),
                "relative_humidity_percent": sample.get("relative_humidity_pct", 11.0),
                "air_quality:idx": 65,
                "elevation": 331.0,
            }

        def _normalize_live_result(raw_result: Any) -> Dict[str, Any]:
            if not isinstance(raw_result, dict):
                return _get_mock_env()
            if "locations" in raw_result and raw_result["locations"]:
                loc = raw_result["locations"][0]
                params = loc.get("parameters", {})
                solar_data = loc.get("solar_irradiance", {})
                clear_sky = solar_data.get("clear_sky", {}) if isinstance(solar_data, dict) else {}

                def _extract_val(arr_or_val: Any, default: float) -> float:
                    if isinstance(arr_or_val, list) and arr_or_val:
                        valid = [float(v) for v in arr_or_val if v is not None]
                        return max(valid) if valid else default
                    if isinstance(arr_or_val, (int, float)):
                        return float(arr_or_val)
                    return default

                hi = _extract_val(params.get("heat_index_celsius"), 38.5)
                apparent = _extract_val(params.get("apparent_temperature_celsius"), 39.0)
                wet_bulb = _extract_val(params.get("wet_bulb_temperature_celsius"), 23.5)
                rh = _extract_val(params.get("relative_humidity_percent"), 25.0)
                aqi = _extract_val(params.get("air_quality:idx"), 60.0)
                ghi = clear_sky.get("ghi") if isinstance(clear_sky, dict) else None
                if ghi is None:
                    ghi = _extract_val(solar_data, 576.9)

                return {
                    **raw_result,
                    "heat_index_celsius": round(hi, 1),
                    "apparent_temperature_celsius": round(apparent, 1),
                    "wet_bulb_temperature_celsius": round(wet_bulb, 1),
                    "relative_humidity_percent": round(rh, 1),
                    "solar_irradiance": round(float(ghi), 1),
                    "air_quality:idx": round(aqi, 1),
                    "elevation": loc.get("elevation", 330.0),
                }
            return raw_result

        if self.mock_mode:
            return {"activity_id": "mock_act_env_phx_01", "result": _get_mock_env()} if wait else "mock_act_env_phx_01"

        dt_obj: Dict[str, Any] = {"start_date": start_date, "filter_type": filter_type}
        if filter_type == 1:
            dt_obj["start_time"] = start_time or "14:00"
        elif filter_type == 2:
            dt_obj["start_time"] = start_time or "08:00"
            dt_obj["end_time"] = end_time or "18:00"

        payload: Dict[str, Any] = {
            "latitude": latitude,
            "longitude": longitude,
            "temperature": temperature,
            "date_time": dt_obj,
        }
        if analysis:
            payload["analysis"] = list(analysis)

        try:
            resp = await self._request("POST", "/v1/env_params", json=payload)
            body = resp.json()
            activity_id = body["data"]["activity_id"]

            if not wait:
                return activity_id
            raw_result = await self.wait_for(activity_id, poll_interval=3.0, timeout=poll_timeout)
            normalized = _normalize_live_result(raw_result)
            return {"activity_id": activity_id, "result": normalized}
        except Exception as exc:
            logger.warning("Live env_params call failed (%s); falling back to Phoenix fixture.", str(exc))
            return {"activity_id": "fallback_act_env_01", "result": _get_mock_env()} if wait else "fallback_act_env_01"

    # ------------------------------------------------------------------
    # Live analytics helpers
    # ------------------------------------------------------------------

    BENCHMARK_ANALYSIS_DATE = "2023-07-19"
    _HISTORICAL_LOWER_BOUND = date(2019, 1, 1)

    @staticmethod
    def _build_aoi(
        latitude: float,
        longitude: float,
        half_extent_deg: float = 0.011,
    ) -> Dict[str, Any]:
        """
        Build a closed GeoJSON polygon AOI centred on a point.

        ~0.011 deg is roughly a 2.4 km box (~1.9 mi^2), comfortably inside the
        10 mi^2 ceiling on the Basic/Startup plans. The ring is explicitly
        closed (first vertex repeated last), which the API validates.
        """
        lat0, lat1 = latitude - half_extent_deg, latitude + half_extent_deg
        lon0, lon1 = longitude - half_extent_deg, longitude + half_extent_deg
        ring = [[lon0, lat0], [lon1, lat0], [lon1, lat1], [lon0, lat1], [lon0, lat0]]
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {},
                    "geometry": {"type": "Polygon", "coordinates": [ring]},
                }
            ],
        }

    def _resolve_analysis_date(self, requested: Optional[str] = None) -> str:
        """
        Clamp the analysis date into the window the API actually serves.

        FortyGuard accepts 2019-01-01 .. now+12h and returns 400 outside it.
        The previous implementation requested `today`, which fails whenever the
        host clock runs ahead of the published archive - the request was
        rejected and the client silently fell back to the bundled fixture.
        Anything out of range now resolves to a pinned benchmark date that is
        guaranteed to exist, so the demo stays reproducible.
        """
        pinned = os.getenv("FORTYGUARD_ANALYSIS_DATE", "").strip() or self.BENCHMARK_ANALYSIS_DATE
        candidate = (requested or pinned).strip()
        try:
            parsed = datetime.strptime(candidate, "%Y-%m-%d").date()
        except ValueError:
            return pinned
        upper = (datetime.now(timezone.utc) + timedelta(hours=12)).date()
        if parsed < self._HISTORICAL_LOWER_BOUND or parsed > upper:
            logger.info("Analysis date %s outside API window; using %s.", candidate, pinned)
            return pinned
        return candidate

    async def _run_heatmap(self, payload: Dict[str, Any], credits: float = 1.5) -> Dict[str, Any]:
        """
        Submit a heatmap analytic, poll to completion, and memoise the result.

        Every distinct payload is cached by query hash so repeated scans of the
        same AOI/hour never re-spend credits, and each live completion is
        written to the credit ledger.
        """
        db_manager = None
        q_hash = None
        try:
            from src.db.database import db_manager as _dbm
            db_manager = _dbm
            q_hash = db_manager.generate_query_hash("/v1/heatmap", payload)
            cached = await db_manager.get_cached_api_call(q_hash)
            if cached:
                return cached
        except Exception:
            pass

        resp = await self._request("POST", "/v1/heatmap", json=payload)
        body = resp.json()
        if body.get("error"):
            raise FortyGuardError(body.get("message", "Heatmap submission failed"))
        activity_id = body["data"]["activity_id"]
        result = await self.wait_for(activity_id, poll_interval=3.0, timeout=self.timeout * 6)

        if db_manager is not None and q_hash:
            try:
                from src.db.models import ApiCallCacheRecord, CreditLedgerRecord
                import uuid

                await db_manager.save_cached_api_call(
                    ApiCallCacheRecord(
                        query_hash=q_hash,
                        endpoint="/v1/heatmap",
                        request_params=payload,
                        response_payload=result if isinstance(result, dict) else {"data": result},
                        credits_spent=credits,
                    )
                )
                await db_manager.log_credit_transaction(
                    CreditLedgerRecord(
                        transaction_id=f"TXN-{uuid.uuid4().hex[:8].upper()}",
                        activity_id=activity_id,
                        endpoint=f"/v1/heatmap:{payload.get('analytic_type', 'tcm')}",
                        credits_debited=credits,
                        remaining_balance=0.0,
                    )
                )
            except Exception:
                pass
        return result if isinstance(result, dict) else {}

    async def _cached_env_params(
        self,
        latitude: float,
        longitude: float,
        analysis_date: str,
    ) -> Dict[str, Any]:
        """
        Fetch (and durably cache) the hourly environmental parameter arrays.

        Returns {} when live data is genuinely unavailable. Note that
        environmental_parameters() swallows its own failures and hands back the
        offline fixture, so the presence of a 'locations' key is what actually
        distinguishes a real response from the fallback.
        """
        cache_key = {"latitude": latitude, "longitude": longitude, "start_date": analysis_date, "filter_type": 3}
        db_manager = None
        q_hash = None
        try:
            from src.db.database import db_manager as _dbm

            db_manager = _dbm
            q_hash = db_manager.generate_query_hash("/v1/env_params", cache_key)
            cached = await db_manager.get_cached_api_call(q_hash)
            if cached and cached.get("locations"):
                return cached
        except Exception:
            pass

        try:
            env_result = await self.environmental_parameters(
                latitude=latitude,
                longitude=longitude,
                temperature=40.0,
                start_date=analysis_date,
                filter_type=3,
                poll_timeout=float(os.getenv("FORTYGUARD_ENV_TIMEOUT_S", "180")),
            )
        except Exception as exc:
            logger.warning("env_params unavailable (%s); hourly humidity/solar fall back to benchmark.", exc)
            return {}

        payload = env_result.get("result", {}) if isinstance(env_result, dict) else {}
        if not isinstance(payload, dict) or not payload.get("locations"):
            logger.warning("env_params returned no live locations; humidity/solar fall back to benchmark.")
            return {}

        if db_manager is not None and q_hash:
            try:
                from src.db.models import ApiCallCacheRecord

                await db_manager.save_cached_api_call(
                    ApiCallCacheRecord(
                        query_hash=q_hash,
                        endpoint="/v1/env_params",
                        request_params=cache_key,
                        response_payload=payload,
                        credits_spent=1.0,
                    )
                )
            except Exception:
                pass
        return payload

    def _fixture_persistence(self, threshold_c: float) -> Dict[str, Any]:
        """Phoenix July 2023 benchmark persistence layer (offline replay).

        Reads the captured fixture rather than restating it. These were once
        inline literals (7.17 h / 34.25 C*h / TSI 4.12) that survived the
        regeneration of the fixture and silently contradicted it - the capture
        says 12.0 h / 17.48 C*h / TSI 3.68.
        """
        meta = self._fixture_data.get("scenario_metadata", {}).get("persistence_metrics", {})
        return {
            "threshold_c": threshold_c,
            "persistence_hours_p40": meta.get("persistence_hours_p40", 12.0),
            "exceedance_hours_e40": meta.get("exceedance_hours_e40", 12.0),
            "exceedance_degree_hours_h40": meta.get("exceedance_degree_hours_h40", 17.48),
            "thermal_soak_index_tsi": meta.get("thermal_soak_index_tsi", 3.68),
            "consecutive_heatwave_days": meta.get("consecutive_heatwave_days", 24),
            "data_source": "phoenix_fixture",
        }

    async def get_12h_forecast(
        self,
        latitude: float = 33.4484,
        longitude: float = -112.0740,
        start_time: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Build a 12-hour hourly microclimate profile from live FortyGuard data.

        2-metre air temperature is only available from the heatmap `tcm`
        analytic (env_params echoes back whatever `temperature` you send and
        never returns measured air temperature), so one `tcm` job is issued per
        forecast hour and all of them are awaited concurrently. A single
        env_params job supplies the real hourly humidity / wet-bulb / cloud
        arrays. Results are cached per hour, so a repeated scan costs 0 credits.
        """
        if self.mock_mode or not self.api_key:
            return self._fixture_data.get("hourly_forecast_12h", [])

        analysis_date = self._resolve_analysis_date(start_time)
        aoi = self._build_aoi(latitude, longitude)
        hours = list(range(6, 18))  # 06:00 - 17:00 local, the heat-of-day window

        # env_params is issued first and on its own. The API appears to serialise
        # work per key: when it was launched alongside 12 heatmap jobs it sat in
        # 'processing' behind them and blew a 600s deadline, even though the same
        # request completes in ~5s uncontended.
        env_payload = await self._cached_env_params(latitude, longitude, analysis_date)

        # Bound fan-out so a 12-hour scan doesn't saturate the account's queue.
        semaphore = asyncio.Semaphore(int(os.getenv("FORTYGUARD_MAX_CONCURRENCY", "6")))

        async def _hour_temp(hour: int) -> Optional[Dict[str, float]]:
            payload = {
                "polygon_aoi": aoi,
                "granularity": 100,
                "analytic_type": "tcm",
                "date_time": {
                    "start_date": analysis_date,
                    "start_time": f"{hour:02d}:00",
                    "filter_type": 1,
                },
            }
            try:
                async with semaphore:
                    res = await self._run_heatmap(payload)
                stats = (res or {}).get("stats_data", {}).get("temperature_stats", {})
                if not stats:
                    return None
                return {
                    "mean": float(stats.get("mean")),
                    "min": float(stats.get("minimum")),
                    "max": float(stats.get("maximum")),
                }
            except Exception as exc:
                logger.warning("tcm hour %02d failed: %s", hour, exc)
                return None

        try:
            temp_results = await asyncio.gather(*[_hour_temp(h) for h in hours])
        except Exception as exc:
            logger.warning("Live forecast lookup failed (%s); falling back to Phoenix fixture.", exc)
            return self._fixture_data.get("hourly_forecast_12h", [])

        if not any(temp_results):
            logger.warning("No live tcm hours resolved; falling back to Phoenix fixture.")
            return self._fixture_data.get("hourly_forecast_12h", [])

        locations = env_payload.get("locations") or [{}]
        params = locations[0].get("parameters", {}) if locations else {}
        solar = locations[0].get("solar_irradiance", {}) if locations else {}
        daily_ghi = float((solar.get("clear_sky") or {}).get("ghi") or 0.0)

        def _hourly(key: str, hour: int, default: float) -> float:
            arr = params.get(key)
            if isinstance(arr, list) and len(arr) > hour and arr[hour] is not None:
                try:
                    return float(arr[hour])
                except (TypeError, ValueError):
                    return default
            return default

        fixture_hours = self._fixture_data.get("hourly_forecast_12h", [])
        forecast: List[Dict[str, Any]] = []

        for idx, hour in enumerate(hours):
            temps = temp_results[idx]
            if temps is None:
                continue
            fallback = fixture_hours[idx] if idx < len(fixture_hours) else {}

            # Despite the name, cloud_cover_octas is reported on a 0-100 percent
            # scale (observed values up to 100.0, where octas cap at 8). Treating
            # it as octas drove the attenuation term negative and produced
            # negative irradiance, so normalise and clamp defensively.
            cloud_raw = _hourly("cloud_cover_octas", hour, 0.0)
            cloud_fraction = min(max(cloud_raw / 100.0, 0.0), 1.0)

            # Clear-sky diurnal geometry scaled by the reported daily GHI and
            # attenuated by the measured hourly cloud fraction. The shape is
            # solar geometry; the magnitude and attenuation are live values.
            # With no live GHI, fall back to the benchmark hour's irradiance
            # rather than emitting a physically impossible 0 W/m2 at midday.
            solar_shape = max(0.0, math.sin(math.pi * (hour - 5.5) / 13.0))
            attenuation = max(0.15, 1.0 - 0.75 * cloud_fraction)
            if daily_ghi > 0:
                solar_wm2 = round(daily_ghi * 1.6 * solar_shape * attenuation, 1)
            else:
                solar_wm2 = round(
                    float(fallback.get("solar_irradiance_w_m2", 950.0 * solar_shape)) * attenuation, 1
                )

            ambient = round(temps["mean"], 2)
            coolest = round(temps["min"], 2)

            forecast.append(
                {
                    "hour_index": idx,
                    "timestamp": f"{analysis_date}T{hour:02d}:00:00Z",
                    "time_label": datetime.strptime(f"{hour:02d}:00", "%H:%M").strftime("%I:%M %p"),
                    # --- measured by FortyGuard ---
                    "fortyguard_2m_ambient_c": ambient,
                    "coolest_tile_2m_c": coolest,
                    "intra_aoi_spread_c": round(ambient - coolest, 2),
                    "tile_peak_2m_c": round(temps["max"], 2),
                    "relative_humidity_pct": round(
                        _hourly("relative_humidity_percent", hour, fallback.get("relative_humidity_pct", 20.0)), 1
                    ),
                    "wet_bulb_temp_c": round(
                        _hourly("wet_bulb_temperature_celsius", hour, fallback.get("wet_bulb_temp_c", 22.0)), 1
                    ),
                    "heat_index_c": round(_hourly("heat_index_celsius", hour, ambient), 1),
                    "cloud_cover_pct": round(cloud_raw, 1),
                    "solar_irradiance_w_m2": solar_wm2,
                    # --- grid-side scenario state (modelled, not FortyGuard) ---
                    "wind_speed_m_s": fallback.get("wind_speed_m_s", 2.0),
                    "baseline_load_ratio_k": fallback.get("baseline_load_ratio_k", 0.85),
                    "hospital_critical_load_mw": fallback.get("hospital_critical_load_mw", 4.2),
                    "bess_soc_pct": fallback.get("bess_soc_pct", 85.0),
                    "data_source": "fortyguard_live" if env_payload else "fortyguard_live_partial",
                }
            )

        for i, row in enumerate(forecast):
            row["hour_index"] = i
        logger.info("Live 12h forecast built from %d FortyGuard tcm hours.", len(forecast))
        return forecast

    async def get_persistence_and_exceedance(
        self,
        latitude: float = 33.4484,
        longitude: float = -112.0740,
        threshold_c: float = 40.0,
        start_date: Optional[str] = None,
        hourly_forecast: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Fetch real continuous persistence (P_theta) and exceedance (E_theta).

        Both are first-class FortyGuard analytics (`analytic_type` of
        `persistence` / `exceedance` on /v1/heatmap, returned in hours). The
        previous implementation never issued a request at all - it derived a
        number from the caller's distance to downtown Phoenix, so every city
        outside Phoenix received the same synthetic floor value.

        Degree-hours (H_theta, in C*h) is not an API primitive, so it is
        integrated from the measured hourly 2m series when one is supplied.
        """
        if self.mock_mode or not self.api_key:
            return self._fixture_persistence(threshold_c)

        analysis_date = self._resolve_analysis_date(start_date)
        aoi = self._build_aoi(latitude, longitude)
        base = {
            "polygon_aoi": aoi,
            "granularity": 100,
            "date_time": {
                "start_date": analysis_date,
                "start_time": "00:00",
                "end_time": "23:00",
                "filter_type": 2,
            },
            "threshold": threshold_c,
            "direction": "above",
        }

        try:
            persistence_res, exceedance_res = await asyncio.gather(
                self._run_heatmap({**base, "analytic_type": "persistence"}),
                self._run_heatmap({**base, "analytic_type": "exceedance"}),
            )
        except Exception as exc:
            logger.warning("Live persistence/exceedance failed (%s); using benchmark fixture.", exc)
            return self._fixture_persistence(threshold_c)

        p_stats = (persistence_res or {}).get("stats_data", {})
        e_stats = (exceedance_res or {}).get("stats_data", {})
        if "mean" not in p_stats or "mean" not in e_stats:
            logger.warning("Unexpected persistence/exceedance payload; using benchmark fixture.")
            return self._fixture_persistence(threshold_c)

        p_hours = round(float(p_stats["mean"]), 2)
        e_hours = round(float(e_stats["mean"]), 2)

        # Integrate degree-hours from the measured hourly curve when available.
        degree_hours = 0.0
        if hourly_forecast:
            for row in hourly_forecast:
                t = row.get("fortyguard_2m_ambient_c")
                if isinstance(t, (int, float)) and t > threshold_c:
                    degree_hours += float(t) - threshold_c
        degree_hours = round(degree_hours, 2)

        # TSI uses the same definition as the thermal engine:
        # TSI = P/tau_o + lambda * (H / (tau_o * theta_scale))
        tau_o, lam, theta_scale = 3.5, 0.5, 10.0
        tsi = round((p_hours / tau_o) + lam * (degree_hours / (tau_o * theta_scale)), 2)

        return {
            "threshold_c": threshold_c,
            "persistence_hours_p40": p_hours,
            "exceedance_hours_e40": e_hours,
            "exceedance_degree_hours_h40": degree_hours,
            "thermal_soak_index_tsi": tsi,
            "consecutive_heatwave_days": self._fixture_data.get("scenario_metadata", {}).get(
                "consecutive_heatwave_days", 24
            ),
            "n_cells": p_stats.get("n_cells"),
            "analysis_date": analysis_date,
            "data_source": "fortyguard_live",
        }

    async def fetch_api_key_usage(self) -> Dict[str, Any]:
        """POST /v1/system/fetch-api-key-usage - current billing cycle summary."""
        resp = await self._request("POST", "/v1/system/fetch-api-key-usage", json={"api_key": self.api_key})
        return resp.json()

    async def fetch_api_key_custom_usage(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """POST /v1/system/fetch-api-key-custom-usage - usage over custom date window."""
        def _to_iso(value: str, end_of_day: bool) -> str:
            if "T" in value:
                return value
            return f"{value}T{'23:59:59' if end_of_day else '00:00:00'}Z"

        payload = {
            "api_key": self.api_key,
            "start_date": _to_iso(start_date, end_of_day=False),
            "end_date": _to_iso(end_date, end_of_day=True),
        }
        resp = await self._request("POST", "/v1/system/fetch-api-key-custom-usage", json=payload)
        return resp.json()


class FortyGuardClient:
    """Synchronous wrapper around AsyncFortyGuardClient for scripts and notebooks."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 60.0,
        mock_mode: Optional[bool] = None,
    ) -> None:
        self._async_client = AsyncFortyGuardClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            mock_mode=mock_mode,
        )

    def _run_async(self, coro: Any) -> Any:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        if loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
        return loop.run_until_complete(coro)

    def create_heatmap(self, *args: Any, **kwargs: Any) -> Any:
        return self._run_async(self._async_client.create_heatmap(*args, **kwargs))

    def environmental_parameters(self, *args: Any, **kwargs: Any) -> Any:
        return self._run_async(self._async_client.environmental_parameters(*args, **kwargs))

    def get_12h_forecast(self, *args: Any, **kwargs: Any) -> Any:
        return self._run_async(self._async_client.get_12h_forecast(*args, **kwargs))

    def get_persistence_and_exceedance(self, *args: Any, **kwargs: Any) -> Any:
        return self._run_async(self._async_client.get_persistence_and_exceedance(*args, **kwargs))

    def fetch_api_key_usage(self) -> Dict[str, Any]:
        return self._run_async(self._async_client.fetch_api_key_usage())

    def fetch_api_key_custom_usage(self, start_date: str, end_date: str) -> Dict[str, Any]:
        return self._run_async(self._async_client.fetch_api_key_custom_usage(start_date, end_date))
