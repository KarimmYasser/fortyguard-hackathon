"""
Asset Management Router
Manages registration and query of distribution transformers, substations, and BESS assets.
"""

from __future__ import annotations

from typing import Any, Dict, List
from fastapi import APIRouter
from src.models.asset import AssetType, InfrastructureAsset, MountingLocation

router = APIRouter(prefix="/assets", tags=["Asset Registry"])

# In-memory registry preloaded with Phoenix benchmark assets
ASSET_REGISTRY: Dict[str, InfrastructureAsset] = {
    "SUB-PHX-DOWNTOWN-04": InfrastructureAsset(
        id="SUB-PHX-DOWNTOWN-04",
        name="Phoenix Central Substation TX-04 (25 MVA)",
        asset_type=AssetType.TRANSFORMER_BOX,
        mounting_location=MountingLocation.GROUND_LEVEL,
        latitude=33.4484,
        longitude=-112.0740,
        max_safe_ambient_temp_c=40.0,
        critical_explosion_temp_c=50.0,
        current_load_percentage=85.0,
        owner_type="B2B",
        contact_email="ops-grid@phx-utility.com",
    ),
    "SUB-PHX-DOWNTOWN-05": InfrastructureAsset(
        id="SUB-PHX-DOWNTOWN-05",
        name="Phoenix Central Substation TX-05 (Parallel 25 MVA)",
        asset_type=AssetType.TRANSFORMER_BOX,
        mounting_location=MountingLocation.GROUND_LEVEL,
        latitude=33.4488,
        longitude=-112.0745,
        max_safe_ambient_temp_c=40.0,
        critical_explosion_temp_c=50.0,
        current_load_percentage=75.0,
        owner_type="B2B",
        contact_email="ops-grid@phx-utility.com",
    ),
    "BESS-PHX-CENTRAL-01": InfrastructureAsset(
        id="BESS-PHX-CENTRAL-01",
        name="Downtown Utility BESS (25 MWh / 5 MW)",
        asset_type=AssetType.BATTERY_STORAGE,
        mounting_location=MountingLocation.GROUND_LEVEL,
        latitude=33.4480,
        longitude=-112.0735,
        max_safe_ambient_temp_c=38.0,
        critical_explosion_temp_c=48.0,
        current_load_percentage=60.0,
        owner_type="B2B",
        contact_email="bess-ops@phx-utility.com",
    ),
}


from src.db.database import db_manager


@router.get("", response_model=List[InfrastructureAsset])
async def list_registered_assets() -> List[InfrastructureAsset]:
    """List all registered critical energy infrastructure assets from the database."""
    db_assets = await db_manager.get_grid_assets()
    if db_assets and len(db_assets) > 0:
        assets_list = []
        for a in db_assets:
            a_type = AssetType.TRANSFORMER_BOX
            if "BESS" in a.get("type", "") or "Storage" in a.get("type", ""):
                a_type = AssetType.BATTERY_STORAGE
            elif "Conductor" in a.get("type", "") or "Line" in a.get("type", ""):
                a_type = AssetType.ELECTRICAL_PANEL

            assets_list.append(
                InfrastructureAsset(
                    id=a.get("asset_id"),
                    name=a.get("name"),
                    asset_type=a_type,
                    mounting_location=MountingLocation.GROUND_LEVEL,
                    latitude=float(a.get("latitude")),
                    longitude=float(a.get("longitude")),
                    max_safe_ambient_temp_c=40.0,
                    critical_explosion_temp_c=50.0,
                    current_load_percentage=85.0 if a_type != AssetType.BATTERY_STORAGE else 60.0,
                    owner_type="B2B",
                    contact_email="grid-operations@phoenix-utility.com",
                )
            )
        return assets_list

    return list(ASSET_REGISTRY.values())


@router.get("/{asset_id}", response_model=InfrastructureAsset)
async def get_asset_by_id(asset_id: str) -> InfrastructureAsset:
    """Retrieve details for a single infrastructure asset."""
    all_assets = await list_registered_assets()
    for a in all_assets:
        if a.id == asset_id:
            return a
    if asset_id in ASSET_REGISTRY:
        return ASSET_REGISTRY[asset_id]
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail=f"Asset {asset_id} not found in database registry")


@router.post("/register", response_model=InfrastructureAsset)
async def register_asset(asset: InfrastructureAsset) -> InfrastructureAsset:
    """Register a new physical grid or building energy asset."""
    ASSET_REGISTRY[asset.id] = asset
    return asset
