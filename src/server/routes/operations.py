"""Portfolio operations and MCP-compatible deterministic tool surface."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.operations.portfolio import (
    build_mitigation_evidence,
    calculate_worker_windows,
    load_default_environment_profile,
    rank_portfolio,
)
from src.db.database import db_manager
from src.server.routes.assets import ASSET_REGISTRY

router = APIRouter(tags=["Portfolio Operations"])


class OperationsRequest(BaseModel):
    max_wet_bulb_c: float = Field(default=23.0, ge=0.0, le=40.0)
    max_air_temp_c: float = Field(default=40.0, ge=-20.0, le=60.0)
    min_consecutive_hours: int = Field(default=2, ge=1, le=12)


class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: Optional[Any] = None
    method: str
    params: Dict[str, Any] = Field(default_factory=dict)


TOOLS: List[Dict[str, Any]] = [
    {
        "name": "rank_portfolio_risk",
        "description": "Rank registered grid assets with a transparent deterministic thermal-triage score.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "find_worker_intervention_windows",
        "description": "Screen measured wet-bulb and 2 m air-temperature hours for candidate field-work windows; not an occupational-safety certification.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "max_wet_bulb_c": {"type": "number", "default": 23.0},
                "max_air_temp_c": {"type": "number", "default": 40.0},
                "min_consecutive_hours": {"type": "integer", "minimum": 1, "maximum": 12, "default": 2},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "get_mitigation_evidence",
        "description": "Return content-addressed provenance, portfolio ranking, and intervention-screen evidence.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "max_wet_bulb_c": {"type": "number", "default": 23.0},
                "max_air_temp_c": {"type": "number", "default": 40.0},
                "min_consecutive_hours": {"type": "integer", "minimum": 1, "maximum": 12, "default": 2},
            },
            "additionalProperties": False,
        },
    },
]


async def _operations_snapshot(req: OperationsRequest) -> Dict[str, Any]:
    profile, metadata = load_default_environment_profile()
    worker_screen = calculate_worker_windows(
        profile,
        max_wet_bulb_c=req.max_wet_bulb_c,
        max_air_temp_c=req.max_air_temp_c,
        min_consecutive_hours=req.min_consecutive_hours,
    )
    # Prefer raw durable registry rows: adapting them through the public asset
    # schema would discard health and criticality and invent a common load.
    assets = await db_manager.get_grid_assets()
    if not assets:
        assets = list(ASSET_REGISTRY.values())
    rankings = rank_portfolio(assets, profile, worker_screen=worker_screen)
    evidence = build_mitigation_evidence(rankings, worker_screen, metadata)
    return {
        "status": "success",
        "portfolio": {
            "asset_count": len(rankings),
            "ranking_method": "portfolio_rank_v1",
            "rankings": rankings,
        },
        "worker_intervention_screen": worker_screen,
        "mitigation_evidence": evidence,
    }


@router.get("/operations/portfolio")
async def get_portfolio_operations() -> Dict[str, Any]:
    """Read-only default portfolio triage against the canonical replay profile."""
    return await _operations_snapshot(OperationsRequest())


@router.post("/operations/portfolio")
async def screen_portfolio_operations(req: OperationsRequest) -> Dict[str, Any]:
    """Read-only portfolio triage using caller-selected worker-screen thresholds."""
    return await _operations_snapshot(req)


@router.get("/operations/commercial-archetypes")
async def get_commercial_archetypes() -> Dict[str, Any]:
    """
    Returns the commercial early adopter archetypes catalog (Solar Farm, Data Center, Hospital, Utility).
    """
    from src.models.commercial_presets import COMMERCIAL_ARCHETYPES_CATALOG
    return {
        "status": "success",
        "archetypes": {k: v.model_dump() for k, v in COMMERCIAL_ARCHETYPES_CATALOG.items()},
    }


class COCOBriefRequest(BaseModel):
    sector_id: str = Field(default="UTILITY_SUBSTATION")
    prepared_for: str = Field(default="Enterprise Infrastructure Operations")


@router.post("/operations/coco-brief")
async def create_coco_brief(req: COCOBriefRequest) -> Dict[str, Any]:
    """
    Generates a structured COCO Customer Discovery Brief (Context, Outcomes, Constraints, Options)
    with sector-specific financial ROI and payback timeline.
    """
    from src.operations.portfolio import generate_coco_executive_brief
    brief = generate_coco_executive_brief(sector_id=req.sector_id, prepared_for=req.prepared_for)
    return {"status": "success", "brief": brief}

@router.get("/operations/urban-priority/default")
async def get_default_urban_priority() -> Dict[str, Any]:
    """
    Returns default urban cooling priority analysis using Mike Stelfox's 5-Layer Multiplicative Model
    on the canonical Walker Jones vs Vacant Lot benchmark.
    """
    from src.operations.urban_priority import UrbanParcel, UrbanPriorityEngine

    engine = UrbanPriorityEngine()
    benchmark_parcels = [
        UrbanParcel(
            parcel_id="DC_WALKER_JONES",
            name="Walker Jones Education Campus",
            latitude=38.9032,
            longitude=-77.0162,
            area_sq_meters=178061.0,
            land_use="school_campus",
            fortyguard_2m_ambient_c=40.8,
            persistence_hours_p_theta=7.5,
            exceedance_degree_hours=32.0,
            impervious_surface_ratio=0.79,
            tree_canopy_ratio=0.08,
            surface_albedo=0.18,
            canyon_height_to_width_hw=1.4,
            pedestrian_daily_traffic=1200,
            transit_bus_stops_count=5,
            vulnerable_occupants_count=418,
            critical_grid_assets_count=2,
            asthma_prevalence_percent=18.5,
            poverty_rate_percent=31.0,
            overnight_residential_soak=True,
            cdc_social_vulnerability_index_svi=0.88,
            plantable_ground_ratio=0.20,
            public_right_of_way=True,
        ),
        UrbanParcel(
            parcel_id="DC_SHAW_TRANSIT",
            name="Shaw-Howard Transit Substation Hub",
            latitude=38.9150,
            longitude=-77.0220,
            area_sq_meters=45000.0,
            land_use="transit_substation",
            fortyguard_2m_ambient_c=41.5,
            persistence_hours_p_theta=8.0,
            exceedance_degree_hours=36.0,
            impervious_surface_ratio=0.85,
            tree_canopy_ratio=0.05,
            surface_albedo=0.15,
            canyon_height_to_width_hw=1.8,
            pedestrian_daily_traffic=3500,
            transit_bus_stops_count=6,
            vulnerable_occupants_count=150,
            critical_grid_assets_count=4,
            asthma_prevalence_percent=16.0,
            poverty_rate_percent=24.0,
            overnight_residential_soak=True,
            cdc_social_vulnerability_index_svi=0.76,
            plantable_ground_ratio=0.15,
            public_right_of_way=True,
        ),
        UrbanParcel(
            parcel_id="DC_VACANT_ASPHALT",
            name="Vacant Industrial Storage Yard",
            latitude=38.9180,
            longitude=-76.9950,
            area_sq_meters=20000.0,
            land_use="vacant_parking_lot",
            fortyguard_2m_ambient_c=44.2,
            persistence_hours_p_theta=9.0,
            exceedance_degree_hours=42.0,
            impervious_surface_ratio=0.98,
            tree_canopy_ratio=0.01,
            surface_albedo=0.12,
            canyon_height_to_width_hw=0.2,
            pedestrian_daily_traffic=10,
            transit_bus_stops_count=0,
            vulnerable_occupants_count=0,
            critical_grid_assets_count=0,
            asthma_prevalence_percent=5.0,
            poverty_rate_percent=5.0,
            overnight_residential_soak=False,
            cdc_social_vulnerability_index_svi=0.20,
            plantable_ground_ratio=0.02,
            public_right_of_way=False,
        ),
    ]

    rankings = engine.rank_parcels(benchmark_parcels)
    return {
        "status": "success",
        "methodology": "5_layer_multiplicative_model_v1",
        "doctrine": "Hazard * Causes * Exposure * Vulnerability * Opportunity",
        "parcels_evaluated": len(rankings),
        "rankings": [r.model_dump() for r in rankings],
    }


@router.post("/operations/urban-priority/rank")
async def rank_custom_urban_parcels(parcels: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Evaluates and ranks caller-provided urban parcels using the 5-Layer Multiplicative Model.
    """
    from src.operations.urban_priority import UrbanParcel, UrbanPriorityEngine

    engine = UrbanPriorityEngine()
    parsed_parcels = [UrbanParcel(**p) for p in parcels]
    rankings = engine.rank_parcels(parsed_parcels)
    return {
        "status": "success",
        "parcels_evaluated": len(rankings),
        "rankings": [r.model_dump() for r in rankings],
    }


async def describe_mcp_server() -> Dict[str, Any]:
    return {
        "name": "thermal-sentinel-grid",
        "protocol": "MCP JSON-RPC tool subset",
        "transport": "HTTP",
        "read_only": True,
        "tools": TOOLS,
    }


@router.post("/mcp")
async def invoke_mcp_tool(request: MCPRequest) -> Dict[str, Any]:
    """Expose the deterministic operations core through MCP tool semantics."""
    if request.jsonrpc != "2.0":
        raise HTTPException(status_code=400, detail="Only JSON-RPC 2.0 is supported")

    if request.method == "initialize":
        result: Dict[str, Any] = {
            "protocolVersion": "2025-03-26",
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "thermal-sentinel-grid", "version": "1.0.0"},
        }
    elif request.method == "tools/list":
        result = {"tools": TOOLS}
    elif request.method == "tools/call":
        name = request.params.get("name")
        arguments = request.params.get("arguments") or {}
        try:
            req = OperationsRequest(**arguments)
        except Exception as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        snapshot = await _operations_snapshot(req)
        if name == "rank_portfolio_risk":
            structured = snapshot["portfolio"]
        elif name == "find_worker_intervention_windows":
            structured = snapshot["worker_intervention_screen"]
        elif name == "get_mitigation_evidence":
            structured = snapshot["mitigation_evidence"]
        else:
            return {
                "jsonrpc": "2.0",
                "id": request.id,
                "error": {"code": -32602, "message": f"Unknown tool: {name}"},
            }
        result = {
            "content": [{"type": "text", "text": f"{name} completed deterministically."}],
            "structuredContent": structured,
            "isError": False,
        }
    else:
        return {
            "jsonrpc": "2.0",
            "id": request.id,
            "error": {"code": -32601, "message": f"Method not found: {request.method}"},
        }

    return {"jsonrpc": "2.0", "id": request.id, "result": result}
