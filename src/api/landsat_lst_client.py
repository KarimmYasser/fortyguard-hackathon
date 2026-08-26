"""Landsat Collection 2 surface-temperature context via STAC.

This adapter is deliberately separate from 2 m air validation. It returns
``surface_temperature_c`` products only and refuses to expose an ambient-air
field. Raster reading is optional so the core server remains lightweight.
"""

from __future__ import annotations

import asyncio
import math
from typing import Any, Mapping, Sequence

import httpx
import numpy as np

from src.api.rate_limit import provider_limiter
from src.api.retry import RETRYABLE_STATUS, sleep_before_retry

DEFAULT_STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"
COLLECTION = "landsat-c2-l2"
LANDSAT_LIMITER = provider_limiter("planetary-computer", max_concurrency=2, min_interval_s=0.15)


class LandsatLSTError(RuntimeError):
    pass


def landsat_clear_mask(qa_pixel: np.ndarray) -> np.ndarray:
    """Valid ST pixels: not fill, dilated cloud, cirrus, cloud, or shadow."""
    qa = np.asarray(qa_pixel, dtype=np.uint16)
    invalid_bits = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4)
    return (qa & invalid_bits) == 0


def calibrate_surface_temperature(
    digital_numbers: np.ndarray,
    qa_pixel: np.ndarray,
    *,
    scale: float = 0.00341802,
    offset_kelvin: float = 149.0,
    already_scaled: bool = False,
) -> np.ndarray:
    """Apply C2 L2 calibration exactly once and mask invalid pixels."""
    values = np.asarray(digital_numbers, dtype=float)
    celsius = values - 273.15 if already_scaled else values * scale + offset_kelvin - 273.15
    return np.where(landsat_clear_mask(qa_pixel) & np.isfinite(celsius), celsius, np.nan)


def spatial_surface_context_metrics(
    fortyguard_air_c: Sequence[float], landsat_surface_c: Sequence[float]
) -> dict[str, Any]:
    """Compare co-located spatial ranks while preserving air/LST semantics."""
    air, surface = np.asarray(fortyguard_air_c, dtype=float), np.asarray(landsat_surface_c, dtype=float)
    valid = np.isfinite(air) & np.isfinite(surface)
    air, surface = air[valid], surface[valid]
    if air.size < 2:
        raise LandsatLSTError("at least two co-located valid air/LST samples are required")
    air_rank = np.argsort(np.argsort(air)).astype(float)
    surface_rank = np.argsort(np.argsort(surface)).astype(float)
    rank_r = float(np.corrcoef(air_rank, surface_rank)[0, 1])
    threshold_air, threshold_surface = np.percentile(air, 75), np.percentile(surface, 75)
    hot_air, hot_surface = air >= threshold_air, surface >= threshold_surface
    union = int(np.logical_or(hot_air, hot_surface).sum())
    return {
        "n_colocated": int(air.size),
        "spearman_rank_r": round(rank_r, 4),
        "upper_quartile_hot_zone_iou": round(float(np.logical_and(hot_air, hot_surface).sum()) / max(union, 1), 4),
        "mean_surface_minus_air_c": round(float(np.mean(surface - air)), 4),
        "interpretation": "Spatial context only; the surface-minus-air gradient is not forecast error.",
    }


def summarize_surface_temperature(values: np.ndarray) -> dict[str, Any]:
    finite = np.asarray(values, dtype=float)
    valid = finite[np.isfinite(finite)]
    if not valid.size:
        raise LandsatLSTError("surface-temperature raster has no valid clear pixels")
    return {
        "valid_pixel_count": int(valid.size),
        "mean_surface_temperature_c": round(float(np.mean(valid)), 4),
        "min_surface_temperature_c": round(float(np.min(valid)), 4),
        "max_surface_temperature_c": round(float(np.max(valid)), 4),
        "p90_surface_temperature_c": round(float(np.percentile(valid, 90)), 4),
    }


class AsyncLandsatLSTClient:
    def __init__(self, *, base_url: str = DEFAULT_STAC_URL, http_client=None, timeout: float = 30.0, max_retries: int = 2):
        self.base_url = base_url.rstrip("/")
        self.http_client = http_client
        self.timeout = timeout
        self.max_retries = max_retries

    async def _json(self, method: str, path: str, **kwargs) -> Mapping[str, Any]:
        for attempt in range(self.max_retries + 1):
            try:
                async with LANDSAT_LIMITER.slot():
                    if self.http_client is not None:
                        response = await self.http_client.request(method, f"{self.base_url}{path}", timeout=self.timeout, **kwargs)
                    else:
                        async with httpx.AsyncClient(timeout=self.timeout) as client:
                            response = await client.request(method, f"{self.base_url}{path}", **kwargs)
                if response.status_code in RETRYABLE_STATUS and attempt < self.max_retries:
                    await sleep_before_retry(attempt, response.headers)
                    continue
                response.raise_for_status()
                payload = response.json()
                if not isinstance(payload, Mapping):
                    raise LandsatLSTError("STAC returned a non-object payload")
                return payload
            except (httpx.HTTPError, ValueError) as exc:
                if attempt < self.max_retries:
                    await sleep_before_retry(attempt)
                    continue
                raise LandsatLSTError(f"STAC request failed: {exc}") from exc
        raise LandsatLSTError("STAC request failed")

    async def verify_collection(self) -> Mapping[str, Any]:
        payload = await self._json("GET", f"/collections/{COLLECTION}")
        if payload.get("id") != COLLECTION:
            raise LandsatLSTError(f"unexpected collection: {payload.get('id')!r}")
        return payload

    async def search(self, bbox: Sequence[float], datetime_range: str, *, cloud_cover_lt: float = 20.0, limit: int = 20) -> dict[str, Any]:
        if len(bbox) != 4 or not all(math.isfinite(float(value)) for value in bbox):
            raise ValueError("bbox must contain four finite WGS84 coordinates")
        await self.verify_collection()
        payload = await self._json("POST", "/search", json={
            "collections": [COLLECTION], "bbox": list(bbox), "datetime": datetime_range,
            "limit": limit, "query": {"eo:cloud_cover": {"lt": cloud_cover_lt}},
        })
        observations = []
        for item in payload.get("features", []):
            assets = item.get("assets") or {}
            thermal = assets.get("lwir11")
            qa = assets.get("qa_pixel")
            if not isinstance(thermal, Mapping) or not isinstance(qa, Mapping):
                continue
            raster_band = ((thermal.get("raster:bands") or [{}])[0])
            observations.append({
                "scene_id": item.get("id"),
                "acquired_at": (item.get("properties") or {}).get("datetime"),
                "sensor": "Landsat 8/9 TIRS",
                "product": COLLECTION,
                "variable": "surface_temperature_c",
                "evidence_class": "satellite surface temperature (not 2 m air)",
                "native_thermal_resolution_m": 100,
                "output_grid_resolution_m": 30,
                "scene_cloud_cover_pct": (item.get("properties") or {}).get("eo:cloud_cover"),
                "thermal_asset_href": thermal.get("href"),
                "qa_asset_href": qa.get("href"),
                "scale": raster_band.get("scale", 0.00341802),
                "offset_kelvin": raster_band.get("offset", 149.0),
                "requires_pixel_qa_mask": True,
                "signed_url_may_expire": True,
            })
        return {
            "provider": "microsoft_planetary_computer",
            "collection": COLLECTION,
            "evidence_class": "satellite surface temperature (context only)",
            "observations": observations,
        }

    @staticmethod
    def _sign(url: str) -> str:
        try:
            import planetary_computer
        except ImportError as exc:  # pragma: no cover - dependency guard
            raise LandsatLSTError("planetary-computer is required for asset signing") from exc
        return str(planetary_computer.sign_url(url))

    async def sample_polygons(
        self, observation: Mapping[str, Any], features: Sequence[Mapping[str, Any]]
    ) -> list[dict[str, Any]]:
        """Compute QA-masked mean LST for GeoJSON polygons on the thermal grid."""
        try:
            import rasterio
            from rasterio.features import geometry_mask, geometry_window
            from rasterio.vrt import WarpedVRT
            from rasterio.warp import transform_geom
        except ImportError as exc:  # pragma: no cover
            raise LandsatLSTError("rasterio is required for COG processing") from exc
        thermal_url, qa_url = self._sign(str(observation["thermal_asset_href"])), self._sign(str(observation["qa_asset_href"]))

        def read() -> list[dict[str, Any]]:
            rows = []
            with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR"):
                with rasterio.open(thermal_url) as thermal, rasterio.open(qa_url) as qa_source:
                    with WarpedVRT(
                        qa_source, crs=thermal.crs, transform=thermal.transform,
                        width=thermal.width, height=thermal.height,
                        resampling=rasterio.enums.Resampling.nearest,
                    ) as qa:
                        for feature in features:
                            geometry = feature.get("geometry") or feature
                            projected = transform_geom("EPSG:4326", thermal.crs, geometry)
                            window = geometry_window(thermal, [projected])
                            local_transform = rasterio.windows.transform(window, thermal.transform)
                            local_inside = geometry_mask(
                                [projected], out_shape=(int(window.height), int(window.width)),
                                transform=local_transform, invert=True,
                            )
                            dn, qa_values = thermal.read(1, window=window), qa.read(1, window=window)
                            values = calibrate_surface_temperature(
                                dn, qa_values, scale=float(observation.get("scale", 0.00341802)),
                                offset_kelvin=float(observation.get("offset_kelvin", 149.0)),
                            )
                            values[~local_inside] = np.nan
                            summary = summarize_surface_temperature(values)
                            rows.append({
                                "feature_id": (feature.get("properties") or {}).get("tile_id") or feature.get("id"),
                                "fortyguard_2m_air_c": (feature.get("properties") or {}).get("ambient_temp_c"),
                                **summary,
                            })
            return rows
        try:
            return await asyncio.to_thread(read)
        except Exception as exc:
            raise LandsatLSTError(f"failed to sample Landsat polygons: {exc}") from exc

    async def summarize_scene(self, observation: Mapping[str, Any], bbox: Sequence[float]) -> dict[str, Any]:
        """Read signed COG windows, clip to WGS84 AOI, QA-mask, and summarize."""
        try:
            import rasterio
            from rasterio.enums import Resampling
            from rasterio.warp import transform_bounds
            from rasterio.windows import from_bounds
        except ImportError as exc:  # pragma: no cover - dependency guard
            raise LandsatLSTError("rasterio is required for COG processing") from exc
        thermal_url = self._sign(str(observation["thermal_asset_href"]))
        qa_url = self._sign(str(observation["qa_asset_href"]))

        def read() -> tuple[np.ndarray, np.ndarray, int]:
            with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR"):
                with rasterio.open(thermal_url) as thermal:
                    bounds = transform_bounds("EPSG:4326", thermal.crs, *map(float, bbox), densify_pts=21)
                    window = from_bounds(*bounds, transform=thermal.transform).round_offsets().round_lengths()
                    window = window.intersection(rasterio.windows.Window(0, 0, thermal.width, thermal.height))
                    dn = thermal.read(1, window=window, masked=False)
                    total = int(dn.size)
                    with rasterio.open(qa_url) as qa:
                        qa_values = qa.read(
                            1, window=window, out_shape=dn.shape,
                            resampling=Resampling.nearest, masked=False,
                        )
            return dn, qa_values, total

        try:
            dn, qa, total_pixels = await asyncio.to_thread(read)
        except Exception as exc:
            raise LandsatLSTError(f"failed to read signed Landsat COG: {exc}") from exc
        calibrated = calibrate_surface_temperature(
            dn, qa, scale=float(observation.get("scale", 0.00341802)),
            offset_kelvin=float(observation.get("offset_kelvin", 149.0)),
        )
        summary = summarize_surface_temperature(calibrated)
        summary["valid_pixel_pct"] = round(100.0 * summary["valid_pixel_count"] / max(total_pixels, 1), 2)
        return {
            **{key: value for key, value in observation.items() if not key.endswith("_href")},
            "aoi_bbox_wgs84": list(map(float, bbox)),
            "summary": summary,
            "processing": "signed remote COG window; nearest-neighbor QA; C2 scale/offset; Celsius",
        }
