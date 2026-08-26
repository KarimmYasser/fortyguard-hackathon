#!/usr/bin/env python3
"""Fetch public ground truth and drive the IEEE C57.91 transformer solver.

The script normalizes Synoptic, NSRDB, Landsat/Planetary Computer, ECOSTRESS,
EIA, and CAISO responses into a small, auditable JSON report. Missing API keys
or unavailable services can be replaced by deterministic *labelled* mock data
for offline development; pass ``--strict`` to prohibit that fallback.

Satellite LST is retained as surface context only. Balancing-authority demand is
retained as regional context and converted to a *modelled load shape*; it is
never represented as feeder, substation, or transformer telemetry.

Examples:
  python scripts/fetch_ground_truth_comparison.py --start 2024-07-01 --end 2024-07-02
  SYNOPTIC_API_KEY=... EIA_API_KEY=... NREL_API_KEY=... NREL_EMAIL=... \
    python scripts/fetch_ground_truth_comparison.py --strict --output data/ground_truth.json
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import os
import sys
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping

import httpx
from dotenv import load_dotenv

# Permit direct execution as ``python scripts/...py`` from any working directory.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

from src.physics.transformer_thermal import TransformerThermalEngine

SYNOPTIC_URL = "https://api.synopticdata.com/v2/stations/timeseries"
# NREL was renamed NLR in 2025. The legacy developer.nrel.gov hostname no
# longer resolves consistently; this is the current GOES Aggregated PSM v4 URL.
NSRDB_URL = "https://developer.nlr.gov/api/nsrdb/v2/solar/nsrdb-GOES-aggregated-v4-0-0-download.csv"
PLANETARY_URL = "https://planetarycomputer.microsoft.com/api/stac/v1/search"
CMR_STAC_URL = "https://cmr.earthdata.nasa.gov/stac/LPCLOUD/search"
EIA_URL = "https://api.eia.gov/v2/electricity/rto/region-data/data/"
CAISO_URL = "http://oasis.caiso.com/oasisapi/SingleZip"


class GroundTruthFetchError(RuntimeError):
    """An upstream response could not be fetched or safely parsed."""


def _number(value: Any, *, field: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise GroundTruthFetchError(f"{field} is not numeric: {value!r}") from exc
    if not math.isfinite(result):
        raise GroundTruthFetchError(f"{field} is not finite")
    return result


def _utc_hour(value: str) -> str:
    text = value.strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).replace(minute=0, second=0, microsecond=0).isoformat().replace("+00:00", "Z")


def _compact_utc(value: str, *, end: bool = False) -> str:
    parsed = datetime.fromisoformat(value)
    if end and len(value) == 10:
        parsed += timedelta(days=1)
    return parsed.strftime("%Y%m%d%H%M")


def _iso_range(start: str, end: str) -> str:
    return f"{start[:10]}T00:00:00Z/{end[:10]}T23:59:59Z"


def parse_synoptic(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    stations = payload.get("STATION")
    if not isinstance(stations, list):
        summary = payload.get("SUMMARY") if isinstance(payload.get("SUMMARY"), Mapping) else {}
        message = summary.get("RESPONSE_MESSAGE") or "response is missing STATION"
        code = summary.get("RESPONSE_CODE")
        raise GroundTruthFetchError(f"Synoptic API rejected the query (code {code}): {message}")
    for station in stations:
        obs = station.get("OBSERVATIONS", {})
        times = obs.get("date_time")
        if not isinstance(times, list):
            continue
        temp_key = next((k for k in obs if k.startswith("air_temp_set_")), None)
        solar_key = next((k for k in obs if k.startswith("solar_radiation_set_")), None)
        humidity_key = next((k for k in obs if k.startswith("relative_humidity_set_")), None)
        if temp_key is None or len(obs[temp_key]) != len(times):
            continue
        for i, stamp in enumerate(times):
            rows.append({
                "timestamp": _utc_hour(str(stamp)),
                "station_id": station.get("STID"),
                "station_name": station.get("NAME"),
                "temperature_2m_c": _number(obs[temp_key][i], field="air_temp"),
                "solar_ghi_w_m2": _number(obs[solar_key][i], field="solar_radiation") if solar_key and obs[solar_key][i] is not None else None,
                "relative_humidity_pct": _number(obs[humidity_key][i], field="relative_humidity") if humidity_key and obs[humidity_key][i] is not None else None,
            })
    if not rows:
        raise GroundTruthFetchError("Synoptic response contains no usable air-temperature observations")
    return rows


def parse_nsrdb_csv(
    text: str,
    *,
    start_date: str | None = None,
    end_date: str | None = None,
) -> list[dict[str, Any]]:
    lines = text.splitlines()
    header_index = next((i for i, line in enumerate(lines) if line.startswith("Year,")), None)
    if header_index is None:
        raise GroundTruthFetchError("NSRDB CSV is missing its Year header")
    rows = []
    for record in csv.DictReader(lines[header_index:]):
        stamp = datetime(
            int(record["Year"]), int(record["Month"]), int(record["Day"]),
            int(record["Hour"]), int(record.get("Minute", 0)), tzinfo=timezone.utc,
        )
        if start_date and stamp.date() < datetime.fromisoformat(start_date[:10]).date():
            continue
        if end_date and stamp.date() > datetime.fromisoformat(end_date[:10]).date():
            continue
        temperature = record.get("Temperature") or record.get("Air Temperature")
        rows.append({
            "timestamp": stamp.isoformat().replace("+00:00", "Z"),
            "temperature_2m_c": _number(temperature, field="Temperature"),
            "solar_ghi_w_m2": _number(record["GHI"], field="GHI"),
            "solar_dni_w_m2": _number(record["DNI"], field="DNI") if record.get("DNI") else None,
            "solar_dhi_w_m2": _number(record["DHI"], field="DHI") if record.get("DHI") else None,
        })
    if not rows:
        raise GroundTruthFetchError("NSRDB CSV contains no data rows")
    return rows


def parse_stac(payload: Mapping[str, Any], *, thermal_key: str) -> list[dict[str, Any]]:
    features = payload.get("features")
    if not isinstance(features, list):
        raise GroundTruthFetchError("STAC response is missing features")
    rows = []
    for item in features:
        assets = item.get("assets", {})
        asset = assets.get(thermal_key)
        if asset is None and thermal_key == "LST":
            asset = next((v for k, v in assets.items() if "lst" in k.lower()), None)
        if not isinstance(asset, Mapping) or not asset.get("href"):
            continue
        props = item.get("properties", {})
        rows.append({
            "scene_id": item.get("id"),
            "timestamp": props.get("datetime") or props.get("start_datetime"),
            "cloud_cover_pct": props.get("eo:cloud_cover"),
            "thermal_asset_url": asset["href"],
        })
    return rows


def parse_eia(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    records = payload.get("response", {}).get("data") if isinstance(payload.get("response"), Mapping) else None
    if not isinstance(records, list):
        raise GroundTruthFetchError("EIA response is missing response.data")
    parsed = []
    for record in records:
        units = str(record.get("value-units", "megawatthours"))
        # EIA-930 hourly demand is hourly energy in MWh. Its one-hour average
        # power is numerically MW, but preserve both names instead of silently
        # relabelling the upstream unit.
        value = _number(record["value"], field="EIA value")
        parsed.append({
            "timestamp": _utc_hour(str(record["period"])),
            "load_mwh": value,
            "average_load_mw": value if units.lower() in {"megawatthours", "mwh"} else None,
            "load_mw": value,  # compatibility alias consumed by build_thermal_comparison
            "balancing_authority": record.get("respondent") or record.get("subba"),
            "units": units,
            "interval_hours": 1,
        })
    return parsed


def parse_caiso_zip(content: bytes) -> list[dict[str, Any]]:
    try:
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            csv_name = next(name for name in archive.namelist() if name.lower().endswith(".csv"))
            text = archive.read(csv_name).decode("utf-8-sig")
    except (zipfile.BadZipFile, StopIteration, UnicodeDecodeError) as exc:
        raise GroundTruthFetchError("CAISO response is not a ZIP containing CSV") from exc
    rows = []
    for record in csv.DictReader(io.StringIO(text)):
        if record.get("LOAD_TYPE") and "Actual" not in record["LOAD_TYPE"]:
            continue
        stamp = record.get("INTERVALSTARTTIME_GMT") or record.get("OPR_DT")
        if stamp and record.get("MW") not in (None, ""):
            rows.append({
                "timestamp": _utc_hour(stamp),
                "load_mw": _number(record["MW"], field="CAISO MW"),
                "area": record.get("TAC_AREA_NAME") or record.get("TAC_ZONE_NAME"),
            })
    return rows


def mock_weather(start: str, hours: int = 24) -> list[dict[str, Any]]:
    base = datetime.fromisoformat(start[:10]).replace(tzinfo=timezone.utc)
    return [{
        "timestamp": (base + timedelta(hours=i)).isoformat().replace("+00:00", "Z"),
        "temperature_2m_c": round(31 + 10 * max(0.0, math.sin(math.pi * (i - 6) / 18)), 2),
        "solar_ghi_w_m2": round(900 * max(0.0, math.sin(math.pi * (i - 6) / 12)), 2),
    } for i in range(hours)]


def mock_load(start: str, hours: int = 24) -> list[dict[str, Any]]:
    base = datetime.fromisoformat(start[:10]).replace(tzinfo=timezone.utc)
    return [{
        "timestamp": (base + timedelta(hours=i)).isoformat().replace("+00:00", "Z"),
        "load_mw": round(16 + 6 * max(0.0, math.sin(math.pi * (i - 8) / 14)), 3),
    } for i in range(hours)]


class GroundTruthFetcher:
    def __init__(
        self,
        client: httpx.Client | None = None,
        *,
        timeout: float = 45.0,
        allow_mock: bool = True,
        offline: bool = False,
    ) -> None:
        self.client = client or httpx.Client(timeout=timeout, follow_redirects=True)
        self._owns_client = client is None
        self.allow_mock = allow_mock
        self.offline = offline

    def close(self) -> None:
        if self._owns_client:
            self.client.close()

    def _run(
        self,
        provider: str,
        operation: Callable[[], Any],
        fallback: Callable[[], Any],
        *,
        allow_empty: bool = False,
    ) -> dict[str, Any]:
        if self.offline:
            return {
                "provider": provider,
                "data_source": "mock_fallback",
                "records": fallback(),
                "error": "offline mode requested; no network request attempted",
            }
        try:
            records = operation()
            if not records and not allow_empty:
                raise GroundTruthFetchError(f"{provider} returned no records for the requested window")
            return {
                "provider": provider,
                "data_source": "live" if records else "live_no_records",
                "records": records,
                "error": None,
            }
        except Exception as exc:
            # Provider exceptions can include a URL with query credentials.
            # Every credentialed operation below converts those to safe errors.
            message = (
                str(exc)
                if isinstance(exc, GroundTruthFetchError)
                else f"{provider} request failed ({type(exc).__name__})"
            )
            if not self.allow_mock:
                return {"provider": provider, "data_source": "unavailable", "records": [], "error": message}
            return {"provider": provider, "data_source": "mock_fallback", "records": fallback(), "error": message}

    def synoptic(self, lat: float, lon: float, start: str, end: str, token: str | None) -> dict[str, Any]:
        def fetch() -> Any:
            if not token:
                raise GroundTruthFetchError("SYNOPTIC_API_KEY is not set")
            response = self.client.get(SYNOPTIC_URL, params={
                "token": token, "radius": f"{lat},{lon},15", "start": _compact_utc(start),
                "end": _compact_utc(end, end=True), "vars": "air_temp,solar_radiation,relative_humidity",
                "obtimezone": "UTC", "units": "metric", "output": "json",
            })
            try:
                response.raise_for_status()
            except httpx.HTTPError as exc:
                raise GroundTruthFetchError(f"Synoptic HTTP failure ({response.status_code})") from exc
            return parse_synoptic(response.json())
        return self._run("synoptic", fetch, lambda: mock_weather(start))

    def nsrdb(self, lat: float, lon: float, start: str, end: str, api_key: str | None, email: str | None) -> dict[str, Any]:
        def fetch() -> Any:
            if not api_key or not email:
                raise GroundTruthFetchError("NREL_API_KEY and NREL_EMAIL are required")
            response = self.client.get(NSRDB_URL, params={
                "api_key": api_key, "email": email, "wkt": f"POINT({lon} {lat})",
                "names": start[:4], "interval": "60",
                "attributes": "ghi,dni,dhi,air_temperature,surface_albedo,dew_point",
                "utc": "true", "leap_day": "true",
            })
            try:
                response.raise_for_status()
            except httpx.HTTPError as exc:
                raise GroundTruthFetchError(f"NLR NSRDB HTTP failure ({response.status_code})") from exc
            return parse_nsrdb_csv(response.text, start_date=start, end_date=end)
        return self._run("nrel_nsrdb", fetch, lambda: mock_weather(start))

    def planetary(self, lat: float, lon: float, start: str, end: str) -> dict[str, Any]:
        bbox = [lon - 0.05, lat - 0.05, lon + 0.05, lat + 0.05]
        def fetch() -> Any:
            response = self.client.post(PLANETARY_URL, json={"collections": ["landsat-c2-l2"], "bbox": bbox, "datetime": _iso_range(start, end), "query": {"eo:cloud_cover": {"lt": 15}}, "limit": 5})
            response.raise_for_status()
            return parse_stac(response.json(), thermal_key="lwir11")
        return self._run("planetary_computer_landsat", fetch, list, allow_empty=True)

    def ecostress(self, lat: float, lon: float, start: str, end: str) -> dict[str, Any]:
        bbox = [lon - 0.05, lat - 0.05, lon + 0.05, lat + 0.05]
        def fetch() -> Any:
            response = self.client.post(CMR_STAC_URL, json={"collections": ["ECO2LSTE.002"], "bbox": bbox, "datetime": _iso_range(start, end), "limit": 5})
            response.raise_for_status()
            return parse_stac(response.json(), thermal_key="LST")
        return self._run("nasa_ecostress", fetch, list, allow_empty=True)

    def eia(self, start: str, end: str, api_key: str | None, respondent: str = "CISO") -> dict[str, Any]:
        def fetch() -> Any:
            if not api_key:
                raise GroundTruthFetchError("EIA_API_KEY is not set")
            response = self.client.get(EIA_URL, params={
                "api_key": api_key, "frequency": "hourly", "data[0]": "value",
                "facets[respondent][]": respondent, "facets[type][]": "D",
                "start": f"{start[:10]}T00", "end": f"{end[:10]}T23",
                "sort[0][column]": "period", "sort[0][direction]": "asc", "offset": 0, "length": 5000,
            })
            try:
                response.raise_for_status()
            except httpx.HTTPError as exc:
                raise GroundTruthFetchError(f"EIA HTTP failure ({response.status_code})") from exc
            return parse_eia(response.json())
        return self._run("eia_rto", fetch, lambda: mock_load(start))

    def caiso(self, start: str, end: str) -> dict[str, Any]:
        def oasis_time(value: str, add_day: bool = False) -> str:
            dt = datetime.fromisoformat(value[:10]) + (timedelta(days=1) if add_day else timedelta())
            return dt.strftime("%Y%m%dT00:00-0000")
        def fetch() -> Any:
            response = self.client.get(CAISO_URL, params={
                "queryname": "SLD_FCST", "market_run_id": "ACTUAL", "resultformat": "6", "version": "1",
                "startdatetime": oasis_time(start), "enddatetime": oasis_time(end, True),
            })
            try:
                response.raise_for_status()
            except httpx.HTTPError as exc:
                raise GroundTruthFetchError(f"CAISO HTTP failure ({response.status_code})") from exc
            return parse_caiso_zip(response.content)
        return self._run("caiso_oasis", fetch, lambda: mock_load(start))


def build_thermal_comparison(
    weather: Iterable[Mapping[str, Any]],
    load: Iterable[Mapping[str, Any]],
    *,
    transformer_rating_mw: float = 25.0,
    load_evidence_class: str = "regional_balancing_authority",
    regional_peak_load_ratio: float = 1.0,
) -> dict[str, Any]:
    """Align inputs and run the production IEEE solver without evidence leakage.

    ``asset_scada`` load is interpreted as transformer MW and divided by the
    nameplate rating. Regional BA/ISO demand has no transformer-level magnitude,
    so only its normalized temporal shape is used and its peak is explicitly
    mapped to ``regional_peak_load_ratio`` per unit.
    """
    if transformer_rating_mw <= 0:
        raise ValueError("transformer_rating_mw must be positive")
    if load_evidence_class not in {"asset_scada", "regional_balancing_authority", "modelled"}:
        raise ValueError("load_evidence_class must be asset_scada, regional_balancing_authority, or modelled")
    if regional_peak_load_ratio <= 0:
        raise ValueError("regional_peak_load_ratio must be positive")
    weather_by_hour = {_utc_hour(str(r["timestamp"])): r for r in weather}
    load_by_hour = {_utc_hour(str(r["timestamp"])): r for r in load}
    timestamps = sorted(weather_by_hour.keys() & load_by_hour.keys())
    if not timestamps:
        raise GroundTruthFetchError("weather and load series have no overlapping UTC hours")

    aligned_load_mw = [
        max(0.0, _number(load_by_hour[stamp]["load_mw"], field="load_mw"))
        for stamp in timestamps
    ]
    if load_evidence_class == "asset_scada":
        load_k = [value / transformer_rating_mw for value in aligned_load_mw]
        mapping = "asset MW / transformer nameplate MW"
    else:
        peak = max(aligned_load_mw)
        if peak <= 0:
            raise GroundTruthFetchError("regional/modelled load has no positive values")
        load_k = [value / peak * regional_peak_load_ratio for value in aligned_load_mw]
        mapping = (
            "normalized regional/modelled temporal shape; peak explicitly mapped "
            f"to {regional_peak_load_ratio:.3f} pu"
        )

    forecast = []
    for stamp in timestamps:
        w = weather_by_hour[stamp]
        forecast.append({
            "timestamp": stamp,
            "fortyguard_2m_ambient_c": _number(w["temperature_2m_c"], field="temperature_2m_c"),
            "solar_irradiance_w_m2": _number(w.get("solar_ghi_w_m2") or 0.0, field="solar_ghi_w_m2"),
        })

    trajectory = TransformerThermalEngine().simulate_trajectory("ground-truth-comparison", forecast, load_k)
    return {
        "aligned_hours": len(timestamps),
        "transformer_rating_mw": transformer_rating_mw,
        "load_evidence_class": load_evidence_class,
        "load_mapping": mapping,
        "regional_peak_load_ratio": regional_peak_load_ratio if load_evidence_class != "asset_scada" else None,
        "load_ratio_k": [round(v, 6) for v in load_k],
        "peak_top_oil_c": trajectory.peak_top_oil_c,
        "peak_hot_spot_c": trajectory.peak_hot_spot_c,
        "total_loss_of_life_hours": trajectory.total_loss_of_life_hours,
        "steps": [step.model_dump() for step in trajectory.steps],
        "solver": "src.physics.transformer_thermal.TransformerThermalEngine (IEEE C57.91 / IEC 60076-7)",
        "evidence_boundary": (
            "Wholesale BA demand is contextual/model input, not feeder telemetry; "
            "transformer loading is a scenario mapping unless asset SCADA is supplied."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--latitude", type=float, default=34.0522)
    parser.add_argument("--longitude", type=float, default=-118.2437)
    parser.add_argument("--start", default="2024-07-01")
    parser.add_argument("--end", default="2024-07-02")
    parser.add_argument("--transformer-rating-mw", type=float, default=25.0)
    parser.add_argument("--regional-peak-load-ratio", type=float, default=1.0, help="scenario pu peak assigned to normalized EIA/CAISO shape")
    parser.add_argument("--strict", action="store_true", help="fail instead of using labelled deterministic mock fallbacks")
    parser.add_argument("--offline", action="store_true", help="make no network calls and emit labelled deterministic mock data")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if datetime.fromisoformat(args.start[:10]) > datetime.fromisoformat(args.end[:10]):
        parser.error("--start must be on or before --end")

    if args.strict and args.offline:
        parser.error("--strict and --offline are mutually exclusive")

    fetcher = GroundTruthFetcher(allow_mock=not args.strict, offline=args.offline)
    try:
        sources = {
            "synoptic": fetcher.synoptic(args.latitude, args.longitude, args.start, args.end, os.getenv("SYNOPTIC_TOKEN") or os.getenv("SYNOPTIC_API_KEY")),
            "nsrdb": fetcher.nsrdb(args.latitude, args.longitude, args.start, args.end, os.getenv("NREL_API_KEY"), os.getenv("NREL_EMAIL")),
            "landsat": fetcher.planetary(args.latitude, args.longitude, args.start, args.end),
            "ecostress": fetcher.ecostress(args.latitude, args.longitude, args.start, args.end),
            "eia": fetcher.eia(args.start, args.end, os.getenv("EIA_API_KEY")),
            "caiso": fetcher.caiso(args.start, args.end),
        }
    finally:
        fetcher.close()

    def choose_source(names: tuple[str, ...]) -> dict[str, Any]:
        candidates = [sources[name] for name in names if sources[name]["records"]]
        if not candidates:
            raise GroundTruthFetchError(f"no records available from {', '.join(names)}")
        return next((row for row in candidates if row["data_source"] == "live"), candidates[0])

    weather = choose_source(("synoptic", "nsrdb"))
    load = choose_source(("eia", "caiso"))
    temperature_validation_eligible = weather["provider"] == "synoptic" and weather["data_source"] == "live"
    solar_validation_eligible = weather["provider"] == "nrel_nsrdb" and weather["data_source"] == "live"
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "query": {"latitude": args.latitude, "longitude": args.longitude, "start": args.start, "end": args.end},
        "sources": sources,
        "evidence_status": {
            "validation_eligible": temperature_validation_eligible,
            "temperature_validation_eligible": temperature_validation_eligible,
            "solar_validation_eligible": solar_validation_eligible,
            "temperature_evidence": (
                "in-situ station observation"
                if temperature_validation_eligible
                else "satellite physical-model meteorology" if weather["provider"] == "nrel_nsrdb" and weather["data_source"] == "live"
                else "mock"
            ),
            "satellite_role": "surface context only; never substituted for 2 m air",
            "grid_role": "regional temporal context; not feeder/substation/transformer telemetry",
        },
        "comparison_inputs": {"weather": weather["provider"], "load": load["provider"]},
        "thermal_comparison": build_thermal_comparison(
            weather["records"], load["records"],
            transformer_rating_mw=args.transformer_rating_mw,
            load_evidence_class="regional_balancing_authority" if load["data_source"] == "live" else "modelled",
            regional_peak_load_ratio=args.regional_peak_load_ratio,
        ),
    }
    rendered = json.dumps(report, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
