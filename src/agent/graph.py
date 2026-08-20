"""
LangGraph Multi-Agent StateGraph
Assembles the complete compiled Thermal Sentinel Grid workflow:
Forecast Ingest -> Physics Estimation -> Mitigation Planner -> CBF-QP Safety Gate -> Audit & Dispatch
"""

from __future__ import annotations

from typing import Any, Dict
from langgraph.graph import StateGraph, START, END

from src.agent.state import ThermalSentinelState
from src.agent.nodes import (
    forecast_node,
    physics_node,
    planner_node,
    safety_gate_node,
    audit_dispatch_node,
)


def create_thermal_sentinel_graph():
    """
    Creates and compiles the deterministic StateGraph workflow.
    """
    workflow = StateGraph(ThermalSentinelState)

    # Register all specialized agent and physics nodes
    workflow.add_node("forecast_node", forecast_node)
    workflow.add_node("physics_node", physics_node)
    workflow.add_node("planner_node", planner_node)
    workflow.add_node("safety_gate_node", safety_gate_node)
    workflow.add_node("audit_dispatch_node", audit_dispatch_node)

    # Establish linear deterministic safety-gated sequence
    workflow.add_edge(START, "forecast_node")
    workflow.add_edge("forecast_node", "physics_node")
    workflow.add_edge("physics_node", "planner_node")
    workflow.add_edge("planner_node", "safety_gate_node")
    workflow.add_edge("safety_gate_node", "audit_dispatch_node")
    workflow.add_edge("audit_dispatch_node", END)

    return workflow.compile()


async def run_thermal_sentinel_agent(
    target_city: str = "Phoenix, AZ",
    asset_id: str = "SUB-PHX-DOWNTOWN-04",
    asset_name: str = "Phoenix Central Substation TX-04",
    location: Dict[str, float] = None,
) -> Dict[str, Any]:
    """
    Convenience function to run the compiled LangGraph workflow end-to-end.
    """
    graph = create_thermal_sentinel_graph()
    initial_state: ThermalSentinelState = {
        "target_city": target_city,
        "asset_id": asset_id,
        "asset_name": asset_name,
        "location": location or {"lat": 33.4484, "lon": -112.0740},
        "audit_trail": [],
        "errors": [],
    }

    result = await graph.ainvoke(initial_state)
    return result
