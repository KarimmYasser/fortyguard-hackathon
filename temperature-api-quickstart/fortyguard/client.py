"""Python client for the FortyGuard tOS Enterprise API.

One method per endpoint. All analysis endpoints are async task-based —
the `_submit_and_wait` helper handles polling so notebook users don't have to.
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any, Iterable

import requests

from .exceptions import (
    ActivityNotReadyError,
    FortyGuardError,
    TaskFailedError,
    TaskTimeoutError,
)

DEFAULT_BASE_URL = "https://api.fortyguard.com"
_TERMINAL_SUCCESS = {"succeeded", "completed"}
_TERMINAL_FAILURE = {"failed", "error"}


class FortyGuardClient:
    """Thin wrapper around the tOS Enterprise API.

    Parameters
    ----------
    api_key:
        FortyGuard API key. Falls back to the ``FORTYGUARD_API_KEY`` env var.
    base_url:
        API root. Falls back to ``FORTYGUARD_BASE_URL`` then the prod default.
    timeout:
        Per-request HTTP timeout in seconds.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 60.0,
    ) -> None:
        self.api_key = api_key or os.getenv("FORTYGUARD_API_KEY")
        if not self.api_key:
            raise FortyGuardError(
                "No API key provided. Pass api_key=... or set FORTYGUARD_API_KEY in your .env file."
            )
        self.base_url = (base_url or os.getenv("FORTYGUARD_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(
            {"api-key": self.api_key, "Content-Type": "application/json"}
        )

    # ------------------------------------------------------------------ core

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = f"{self.base_url}{path}"
        kwargs.setdefault("timeout", self.timeout)
        resp = self._session.request(method, url, **kwargs)
        if not resp.ok:
            raise FortyGuardError(
                f"{method} {path} -> {resp.status_code}: {resp.text[:500]}"
            )
        return resp

    def _submit(self, path: str, payload: dict) -> str:
        body = self._request("POST", path, json=payload).json()
        if body.get("error"):
            raise FortyGuardError(body.get("message", "Submission failed"))
        try:
            return body["data"]["activity_id"]
        except KeyError as exc:
            raise FortyGuardError(f"Unexpected response shape: {body}") from exc

    def get_status(self, activity_id: str) -> dict:
        """Return the raw status-endpoint JSON for an activity.

        Right after submission the status endpoint can briefly return 404 while
        the activity propagates. That is surfaced as ``ActivityNotReadyError`` so
        callers (``wait_for``) can retry instead of failing.
        """
        resp = self._session.get(
            f"{self.base_url}/v1/status/{activity_id}", timeout=self.timeout
        )
        if resp.status_code == 404:
            raise ActivityNotReadyError(activity_id)
        if not resp.ok:
            raise FortyGuardError(
                f"GET /v1/status/{activity_id} -> {resp.status_code}: {resp.text[:500]}"
            )
        body = resp.json()
        if body.get("error"):
            raise FortyGuardError(body.get("message", "Status lookup failed"))
        return body["data"]

    def wait_for(
        self,
        activity_id: str,
        poll_interval: float = 3.0,
        timeout: float = 600.0,
        on_tick: callable | None = None,
    ) -> dict:
        """Poll the status endpoint until the task terminates.

        Returns the ``result`` payload on success. Raises on failure or timeout.
        """
        deadline = time.monotonic() + timeout
        while True:
            try:
                data = self.get_status(activity_id)
            except ActivityNotReadyError:
                # Not queryable yet (eventual consistency right after submit).
                # Keep polling until the deadline instead of failing on the race.
                if on_tick:
                    on_tick("pending", {})
                if time.monotonic() >= deadline:
                    raise TaskTimeoutError(
                        f"Activity {activity_id} never became visible within {timeout:.0f}s"
                    )
                time.sleep(poll_interval)
                continue
            status = str(data.get("status", "")).lower()
            if on_tick:
                on_tick(status, data)
            if status in _TERMINAL_SUCCESS:
                return data.get("result", data)
            if status in _TERMINAL_FAILURE:
                raise TaskFailedError(
                    f"Activity {activity_id} failed: {data.get('message') or data}"
                )
            if time.monotonic() >= deadline:
                raise TaskTimeoutError(
                    f"Activity {activity_id} still '{status}' after {timeout:.0f}s"
                )
            time.sleep(poll_interval)

    def _submit_and_wait(
        self,
        path: str,
        payload: dict,
        *,
        poll_interval: float,
        timeout: float,
        verbose: bool,
    ) -> dict:
        activity_id = self._submit(path, payload)
        if verbose:
            print(f"Submitted -> activity_id={activity_id}")

        def _tick(status: str, _data: dict) -> None:
            if verbose:
                print(f"  status: {status}")

        result = self.wait_for(
            activity_id,
            poll_interval=poll_interval,
            timeout=timeout,
            on_tick=_tick if verbose else None,
        )
        if verbose:
            print("Done.")
        return {"activity_id": activity_id, "result": result}

    # ---------------------------------------------------------- analysis API

    #: Analysis heatmap types selectable via ``analytic_type``. ``tcm`` is the
    #: default snapshot; the other three are the analysis heatmaps that reuse the
    #: same task, each stored as its own record.
    ANALYTIC_TYPES: tuple[str, ...] = (
        "tcm", "time_of_measure", "exceedance", "persistence",
    )

    def create_heatmap(
        self,
        polygon_aoi: dict,
        start_date: str,
        filter_type: int,
        granularity: int = 100,
        start_time: str | None = None,
        end_time: str | None = None,
        end_date: str | None = None,
        analytic_type: str = "tcm",
        threshold: float | None = None,
        direction: str | None = None,
        *,
        wait: bool = True,
        poll_interval: float = 3.0,
        timeout: float = 600.0,
        verbose: bool = True,
    ) -> dict | str:
        """POST /v1/heatmap — generate a thermal map over a polygon AOI.

        ``filter_type``: 1=single hour, 2=range of hours, 3=single day,
        4=range of days (pass ``end_date``).
        ``granularity``: spatial resolution in meters (60, 80, or 100).

        Analysis heatmaps (``analytic_type``, default ``"tcm"``):

        * ``tcm`` — snapshot temperature (the classic heatmap), tiles in °F.
        * ``time_of_measure`` — UTC hour-of-day (0-23) of each cell's peak.
        * ``exceedance`` — count of hours each cell spends past ``threshold``
          (a count of hours, not degree-hours).
        * ``persistence`` — longest continuous run of such hours.

        ``threshold`` (**°C**, default 30 on the API side — note the contrast
        with the °F tile readings) and ``direction`` (``"above"``/``"below"``)
        are required for ``exceedance`` and ``persistence``, ignored otherwise.

        The three analysis types return a different schema from ``tcm``: each
        tile carries ``properties.value`` (interpret via ``stats_data.units``,
        currently ``"hour"``) rather than the ``tcm`` temperature fields, and
        ``stats_data`` carries ``analytic_type``/``units``/``n_cells``/
        ``min``/``max``/``mean``.
        """
        if analytic_type not in self.ANALYTIC_TYPES:
            raise ValueError(
                f"Unknown analytic_type {analytic_type!r}. "
                f"Valid options: {self.ANALYTIC_TYPES}"
            )
        if analytic_type in ("exceedance", "persistence"):
            if threshold is None:
                raise ValueError(
                    f"analytic_type={analytic_type!r} requires a threshold (°C)."
                )
            if direction not in ("above", "below"):
                raise ValueError(
                    f"analytic_type={analytic_type!r} requires direction "
                    f"'above' or 'below'."
                )

        date_time: dict[str, Any] = {"start_date": start_date, "filter_type": filter_type}
        if start_time is not None:
            date_time["start_time"] = start_time
        if end_time is not None:
            date_time["end_time"] = end_time
        if end_date is not None:
            date_time["end_date"] = end_date

        payload: dict[str, Any] = {
            "polygon_aoi": polygon_aoi,
            "date_time": date_time,
            "granularity": granularity,
            "analytic_type": analytic_type,
        }
        if threshold is not None:
            payload["threshold"] = threshold
        if direction is not None:
            payload["direction"] = direction

        if not wait:
            return self._submit("/v1/heatmap", payload)
        return self._submit_and_wait(
            "/v1/heatmap", payload,
            poll_interval=poll_interval, timeout=timeout, verbose=verbose,
        )

    def satellite_segmentation(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        filter_type: int,
        granularity: int = 100,
        start_time: str | None = None,
        end_time: str | None = None,
        end_date: str | None = None,
        *,
        wait: bool = True,
        poll_interval: float = 3.0,
        timeout: float = 600.0,
        verbose: bool = True,
    ) -> dict | str:
        """POST /v1/satellite — land-cover segmentation of a satellite tile (Premium)."""
        date_time: dict[str, Any] = {"start_date": start_date, "filter_type": filter_type}
        if start_time is not None:
            date_time["start_time"] = start_time
        if end_time is not None:
            date_time["end_time"] = end_time
        if end_date is not None:
            date_time["end_date"] = end_date

        payload = {
            "sat": {"latitude": latitude, "longitude": longitude},
            "date_time": date_time,
            "granularity": granularity,
        }
        if not wait:
            return self._submit("/v1/satellite", payload)
        return self._submit_and_wait(
            "/v1/satellite", payload,
            poll_interval=poll_interval, timeout=timeout, verbose=verbose,
        )

    def street_view_segmentation(
        self,
        latitude: float,
        longitude: float,
        vertical_angle: float = 0.0,
        horizontal_angle: float = 0.0,
        back_view: bool = False,
        *,
        wait: bool = True,
        poll_interval: float = 3.0,
        timeout: float = 600.0,
        verbose: bool = True,
    ) -> dict | str:
        """POST /v1/streetview — segmentation of a ground-level street view (Premium)."""
        payload = {
            "latitude": latitude,
            "longitude": longitude,
            "vertical_angle": vertical_angle,
            "horizontal_angle": horizontal_angle,
            "back_view": back_view,
        }
        if not wait:
            return self._submit("/v1/streetview", payload)
        return self._submit_and_wait(
            "/v1/streetview", payload,
            poll_interval=poll_interval, timeout=timeout, verbose=verbose,
        )

    #: Parameter names the env_params endpoint accepts/returns (the exact strings
    #: the API emits). Pass a subset via ``analysis=`` to restrict the response.
    _ENV_PARAMS_ANALYSES: tuple[str, ...] = (
        "heat_index_celsius", "apparent_temperature_celsius", "wet_bulb_temperature_celsius",
        "relative_humidity_percent", "precipitation_mm", "cloud_cover_octas",
        "air_quality:idx", "air_quality_no2:idx", "air_quality_o3:idx",
        "air_quality_pm2p5:idx", "air_quality_pm10:idx", "air_quality_so2:idx",
        "aqi_us_co", "methane_ppb", "co2_ppm", "elevation", "solar_irradiance",
    )

    def environmental_parameters(
        self,
        latitude: float,
        longitude: float,
        temperature: float,
        start_date: str,
        filter_type: int,
        start_time: str | None = None,
        end_time: str | None = None,
        end_date: str | None = None,
        analysis: Iterable[str] | None = None,
        *,
        wait: bool = True,
        poll_interval: float = 3.0,
        timeout: float = 600.0,
        verbose: bool = True,
    ) -> dict | str:
        """POST /v1/env_params — heat index, AQI, solar irradiance, and more.

        ``analysis`` optionally restricts the response to a subset of
        ``_ENV_PARAMS_ANALYSES`` (the exact parameter names the API emits). Omit it
        (default ``None``) to get the endpoint's full default set of parameters.
        """
        if analysis is not None:
            analysis = list(analysis)
            unknown = set(analysis) - set(self._ENV_PARAMS_ANALYSES)
            if unknown:
                raise ValueError(
                    f"Unknown env-params analysis {unknown}. "
                    f"Valid options: {self._ENV_PARAMS_ANALYSES}"
                )
        date_time: dict[str, Any] = {"start_date": start_date, "filter_type": filter_type}
        if start_time is not None:
            date_time["start_time"] = start_time
        if end_time is not None:
            date_time["end_time"] = end_time
        if end_date is not None:
            date_time["end_date"] = end_date

        payload: dict[str, Any] = {
            "latitude": latitude,
            "longitude": longitude,
            "temperature": temperature,
            "date_time": date_time,
        }
        if analysis is not None:
            payload["analysis"] = analysis
        if not wait:
            return self._submit("/v1/env_params", payload)
        return self._submit_and_wait(
            "/v1/env_params", payload,
            poll_interval=poll_interval, timeout=timeout, verbose=verbose,
        )

    # ---------------------------------------------------- heat intelligence

    _HEAT_INTEL_ANALYSES: tuple[str, ...] = (
        "geographic", "environmental", "urban", "events", "anthropogenic",
    )

    def heat_intelligence(
        self,
        latitude: float,
        longitude: float,
        temperature: float,
        date: str,
        analysis: Iterable[str] = ("environmental",),
        output_path: str | Path | None = None,
        *,
        poll_interval: float = 5.0,
        timeout: float = 900.0,
        verbose: bool = True,
    ) -> Path:
        """POST /v1/heat_intelligence — generate a heat-intelligence report.

        Waits for completion, then downloads the generated PDF. On completion the
        status response returns the standard JSON envelope with a short-lived
        ``result.download_link`` (a pre-signed blob URL to the report PDF). Older
        API versions streamed the PDF body from the status endpoint directly; that
        is still handled for backward compatibility. The file is written to
        ``output_path`` (default: ``./outputs/heat_intelligence_<activity_id>.pdf``).
        """
        analysis_list = list(analysis)
        unknown = set(analysis_list) - set(self._HEAT_INTEL_ANALYSES)
        if unknown:
            raise ValueError(
                f"Unknown analysis types {unknown}. "
                f"Valid options: {self._HEAT_INTEL_ANALYSES}"
            )
        payload = {
            "latitude": latitude,
            "longitude": longitude,
            "temperature": temperature,
            "date": date,
            "analysis": analysis_list,
        }
        activity_id = self._submit("/v1/heat_intelligence", payload)
        if verbose:
            print(f"Submitted -> activity_id={activity_id}")

        deadline = time.monotonic() + timeout
        url = f"{self.base_url}/v1/status/{activity_id}"
        while True:
            resp = self._session.get(url, stream=True, timeout=self.timeout)
            if resp.status_code == 404:
                # Not queryable yet (eventual consistency right after submit) — retry.
                resp.close()
                if verbose:
                    print("  status: pending")
                if time.monotonic() >= deadline:
                    raise TaskTimeoutError(
                        f"Activity {activity_id} never became visible within {timeout:.0f}s"
                    )
                time.sleep(poll_interval)
                continue
            if not resp.ok:
                raise FortyGuardError(
                    f"GET /v1/status/{activity_id} -> {resp.status_code}: {resp.text[:500]}"
                )
            content_type = resp.headers.get("Content-Type", "")
            # Legacy API: the status endpoint streamed the PDF body directly.
            if "application/pdf" in content_type or "octet-stream" in content_type:
                target = Path(output_path) if output_path else (
                    Path("outputs") / f"heat_intelligence_{activity_id}.pdf"
                )
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open("wb") as fh:
                    for chunk in resp.iter_content(chunk_size=65536):
                        if chunk:
                            fh.write(chunk)
                if verbose:
                    print(f"Saved report to {target}")
                return target

            body = resp.json()
            resp.close()
            if body.get("error"):
                raise FortyGuardError(body.get("message", "Status lookup failed"))
            data = body.get("data", {})
            status = str(data.get("status", "")).lower()
            if verbose:
                print(f"  status: {status}")
            # Current API: status returns JSON with a pre-signed download link.
            if status in _TERMINAL_SUCCESS:
                download_link = (data.get("result") or {}).get("download_link")
                if not download_link:
                    raise FortyGuardError(
                        f"Activity {activity_id} completed but the status response "
                        f"contained no report download_link"
                    )
                target = Path(output_path) if output_path else (
                    Path("outputs") / f"heat_intelligence_{activity_id}.pdf"
                )
                target.parent.mkdir(parents=True, exist_ok=True)
                # Pre-signed blob URL — fetch directly, no API auth headers needed.
                with requests.get(download_link, stream=True, timeout=self.timeout) as dl:
                    if not dl.ok:
                        raise FortyGuardError(
                            f"Downloading report -> {dl.status_code}: {dl.text[:200]}"
                        )
                    with target.open("wb") as fh:
                        for chunk in dl.iter_content(chunk_size=65536):
                            if chunk:
                                fh.write(chunk)
                if verbose:
                    print(f"Saved report to {target}")
                return target
            if status in _TERMINAL_FAILURE:
                raise TaskFailedError(f"Activity {activity_id} failed")
            if time.monotonic() >= deadline:
                raise TaskTimeoutError(
                    f"Activity {activity_id} still '{status}' after {timeout:.0f}s"
                )
            time.sleep(poll_interval)

    # ------------------------------------------------------------- credits

    def fetch_api_key_usage(self) -> dict:
        """POST /v1/system/fetch-api-key-usage — current billing cycle summary."""
        body = self._request(
            "POST",
            "/v1/system/fetch-api-key-usage",
            json={"api_key": self.api_key},
        ).json()
        return body

    def fetch_api_key_custom_usage(self, start_date: str, end_date: str) -> dict:
        """POST /v1/system/fetch-api-key-custom-usage — usage over a custom range.

        ``start_date``/``end_date`` accept ``YYYY-MM-DD`` (we format to ISO)
        or already-ISO strings (passed through).
        """
        def _to_iso(value: str, end_of_day: bool) -> str:
            if "T" in value:
                return value
            return f"{value}T{'23:59:59' if end_of_day else '00:00:00'}Z"

        body = self._request(
            "POST",
            "/v1/system/fetch-api-key-custom-usage",
            json={
                "api_key": self.api_key,
                "start_date": _to_iso(start_date, end_of_day=False),
                "end_date": _to_iso(end_date, end_of_day=True),
            },
        ).json()
        return body
