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


@router.get("/mcp")

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
