"""
Spatial Scan Router
Handles geospatial microclimate bounding box and parcel scanning via FortyGuard API.
"""

from __future__ import annotations

import hashlib
import json
import logging

from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.api.fortyguard_client import AsyncFortyGuardClient

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/scan", tags=["Geospatial Scan"])


class ScanRequest(BaseModel):
    city: str = Field(default="Phoenix, AZ")
    latitude: float = Field(default=33.4484)
    longitude: float = Field(default=-112.0740)
    polygon_aoi: Optional[Dict[str, Any]] = None
    start_date: str = Field(default="2023-07-19")
    analytic_type: str = Field(default="tcm", description="tcm | exceedance | persistence")
    threshold_c: Optional[float] = Field(default=40.0)


def _parcel_id_for_scan(req: ScanRequest, analysis_date: str) -> str:
    """Stable identity for one logical scan request.

    FortyGuard's component responses are cached separately in api_call_cache.
    The parcel store is an index of logical scans, so replaying identical inputs
    must upsert the same parcel rather than append a random duplicate row.
    """
    identity = {
        "city": req.city.strip(),
        "latitude": req.latitude,
        "longitude": req.longitude,
        "polygon_aoi": req.polygon_aoi,
        "analysis_date": analysis_date,
        "analytic_type": req.analytic_type,
        "threshold_c": req.threshold_c,
    }
    digest = hashlib.sha256(
        json.dumps(identity, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:12].upper()
    city_prefix = "".join(ch for ch in req.city.upper() if ch.isalnum())[:3] or "AOI"
    return f"PARCEL-{city_prefix}-{digest}"


@router.get("/usage")
async def get_api_usage() -> Dict[str, Any]:
    """
    Returns real-time FortyGuard API credit consumption, subscription status, and limits.
    """
    client = AsyncFortyGuardClient()
    try:
        if not client.api_key:
            return {
                "status": "mock",
                "api_key_configured": False,
                "credit_summary": {
                    "total_available_credits": 2000000,
                    "cycle_credits_used": 0,
                    "cycle_remaining_credits": 2000000,
                    "cycle_usage_percentage": 0.0,
                },
                "plan_details": {
                    "plan_type": "Hackathon Demo",
                    "active": True,
                },
            }
        usage = await client.fetch_api_key_usage()
        return {
            "status": "live",
            "api_key_configured": True,
            "data": usage,
        }
    except Exception as e:
        return {
            "status": "offline_fallback",
            "api_key_configured": bool(client.api_key),
            "error": str(e),
            "credit_summary": {
                "total_available_credits": 2000000,
                "cycle_credits_used": 0,
                "cycle_remaining_credits": 2000000,
                "cycle_usage_percentage": 0.0,
            },
            "plan_details": {
                "plan_type": "Hackathon",
                "active": True,
            },
        }


from src.api.fortyguard_client import AsyncFortyGuardClient
from src.db.database import db_manager
from src.db.models import MicroclimateParcelRecord


@router.get("/parcels")
async def list_scanned_parcels(limit: int = 50) -> Dict[str, Any]:
    """Read back stored scans so a scan result can be located after the fact."""
    rows = await db_manager.get_microclimate_parcels(limit=limit)
    return {"status": "success", "table": "microclimate_parcel_store", "count": len(rows), "parcels": rows}


@router.post("")
async def execute_spatial_scan(req: ScanRequest) -> Dict[str, Any]:
    """
    Execute a 2-metre thermal scan over the requested point or polygon.

    Returns a normalised `metrics` block whose 2m air temperature comes from the
    heatmap `tcm` analytic. env_params is *not* a source of air temperature: it
    echoes back whatever `temperature` you send, and its `heat_index_celsius`
    is not on the Celsius scale despite the name (Houston returns 99.1 there
    against a 39.8 apparent temperature). Reading that field as "2m Ambient"
    was showing a Fahrenheit-scaled heat index as if it were air temperature.
    """
    client = AsyncFortyGuardClient()
    try:
        if req.polygon_aoi:
            res = await client.create_heatmap(
                polygon_aoi=req.polygon_aoi,
                start_date=req.start_date,
                analytic_type=req.analytic_type,
                threshold=req.threshold_c,
                direction="above" if req.analytic_type in ("exceedance", "persistence") else None,
            )
        else:
            res = await client.environmental_parameters(
                latitude=req.latitude,
                longitude=req.longitude,
                temperature=req.threshold_c or 35.0,
                start_date=req.start_date,
                filter_type=3,
            )

        # Real 2m curve for THIS location and date, from tcm.
        forecast = await client.get_12h_forecast(
            latitude=req.latitude,
            longitude=req.longitude,
            start_time=req.start_date,
        )

        # Forward the date. Without it this defaulted to the pinned Phoenix
        # benchmark date, so a Houston 2025 scan came back stamped 2023-07-19.
        persistence = await client.get_persistence_and_exceedance(
            latitude=req.latitude,
            longitude=req.longitude,
            threshold_c=req.threshold_c or 40.0,
            start_date=req.start_date,
            hourly_forecast=forecast or None,
        )

        temps = [h["fortyguard_2m_ambient_c"] for h in forecast
                 if h.get("fortyguard_2m_ambient_c") is not None] if forecast else []
        coolest = [h["coolest_tile_2m_c"] for h in forecast
                   if h.get("coolest_tile_2m_c") is not None] if forecast else []
        peak_idx = temps.index(max(temps)) if temps else None
        peak_hour = forecast[peak_idx] if peak_idx is not None else {}

        metrics = {
            "peak_2m_ambient_c": round(max(temps), 2) if temps else None,
            "mean_2m_ambient_c": round(sum(temps) / len(temps), 2) if temps else None,
            "coolest_tile_2m_c": round(min(coolest), 2) if coolest else None,
            "intra_aoi_spread_c": peak_hour.get("intra_aoi_spread_c"),
            "solar_irradiance_w_m2": peak_hour.get("solar_irradiance_w_m2"),
            "wet_bulb_temp_c": peak_hour.get("wet_bulb_temp_c"),
            "relative_humidity_pct": peak_hour.get("relative_humidity_pct"),
            "persistence_hours_p40": persistence.get("persistence_hours_p40"),
            "exceedance_degree_hours_h40": persistence.get("exceedance_degree_hours_h40"),
            "thermal_soak_index_tsi": persistence.get("thermal_soak_index_tsi"),
            "analysis_date": persistence.get("analysis_date") or req.start_date,
            "data_source": (forecast[0].get("data_source") if forecast else None)
                           or persistence.get("data_source"),
            "n_hours": len(temps),
        }

        parcel_id = None
        try:
            # Persist what was actually measured. This used to write
            # surface_temp_c=58.2 / convective_temp_2m_c=42.74 /
            # asphalt_heat_trap_delta=1.1 for every scan regardless of city,
            # so a Houston scan was stored as Phoenix constants.
            if metrics["peak_2m_ambient_c"] is not None:
                parcel_id = _parcel_id_for_scan(req, metrics["analysis_date"])
                # City and analysis date ride inside the GeoJSON properties.
                # They are needed to re-run a stored scan, and the parcel table
                # has no column for either - properties is a first-class GeoJSON
                # member, so this needs no migration of the live Supabase table.
                geometry = req.polygon_aoi or {
                    "type": "Point",
                    "coordinates": [req.longitude, req.latitude],
                }
                parcel_rec = MicroclimateParcelRecord(
                    parcel_id=parcel_id,
                    polygon_geojson={
                        **geometry,
                        "properties": {
                            **(geometry.get("properties") or {}),
                            "city": req.city,
                            "analysis_date": metrics["analysis_date"],
                            "latitude": req.latitude,
                            "longitude": req.longitude,
                            "peak_2m_ambient_c": metrics["peak_2m_ambient_c"],
                            "persistence_hours_p40": metrics["persistence_hours_p40"],
                            "data_source": metrics["data_source"],
                        },
                    },
                    # No surface-skin analytic is requested here, so report the
                    # measured air temperature rather than inventing a skin temp.
                    surface_temp_c=metrics["peak_2m_ambient_c"],
                    convective_temp_2m_c=metrics["peak_2m_ambient_c"],
                    asphalt_heat_trap_delta=metrics["intra_aoi_spread_c"] or 0.0,
                )
                await db_manager.save_microclimate_parcel(parcel_rec)
            else:
                logger.warning("Scan for %s produced no 2m series; nothing persisted.", req.city)
        except Exception as exc:
            logger.warning("Failed to persist microclimate parcel: %s", exc, exc_info=True)

        return {
            "status": "success",
            "city": req.city,
            "coordinates": {"lat": req.latitude, "lon": req.longitude},
            "metrics": metrics,
            "parcel_id": parcel_id,
            "hourly_2m_profile": forecast,
            "scan_data": res,
            "persistence_layer": persistence,
        }
    except Exception as e:
        logger.warning("Spatial scan failed for %s: %s", req.city, e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
