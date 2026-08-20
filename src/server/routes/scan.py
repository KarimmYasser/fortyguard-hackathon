"""
Spatial Scan Router
Handles geospatial microclimate bounding box and parcel scanning via FortyGuard API.
"""

from __future__ import annotations

from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.api.fortyguard_client import AsyncFortyGuardClient

router = APIRouter(prefix="/scan", tags=["Geospatial Scan"])


class ScanRequest(BaseModel):
    city: str = Field(default="Phoenix, AZ")
    latitude: float = Field(default=33.4484)
    longitude: float = Field(default=-112.0740)
    polygon_aoi: Optional[Dict[str, Any]] = None
    start_date: str = Field(default="2023-07-24")
    analytic_type: str = Field(default="tcm", description="tcm | exceedance | persistence")
    threshold_c: Optional[float] = Field(default=40.0)


@router.post("")
async def execute_spatial_scan(req: ScanRequest) -> Dict[str, Any]:
    """
    Executes a high-resolution 2-meter thermal scan over target coordinates or polygon.
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
            # Point parcel environmental lookup
            res = await client.environmental_parameters(
                latitude=req.latitude,
                longitude=req.longitude,
                temperature=47.6,
                start_date=req.start_date,
            )

        persistence = await client.get_persistence_and_exceedance(
            latitude=req.latitude,
            longitude=req.longitude,
            threshold_c=req.threshold_c or 40.0,
        )

        return {
            "status": "success",
            "city": req.city,
            "coordinates": {"lat": req.latitude, "lon": req.longitude},
            "scan_data": res,
            "persistence_layer": persistence,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
