"""
Thermal Sentinel Grid State Schema for LangGraph
Defines the TypedDict state passed between the forecasting, physics, planning,
safety gate, and dispatch nodes.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, TypedDict


class ThermalSentinelState(TypedDict, total=False):
    """
    Unified LangGraph state schema for physical state estimation and autonomous dispatch.
    """
    target_city: str
    asset_id: str
    asset_name: str
    location: Dict[str, float]  # {"lat": float, "lon": float}
    
    # FortyGuard Environmental Boundary Data
    fortyguard_forecast: List[Dict[str, Any]]
    persistence_metrics: Dict[str, Any]
    urban_canyon_metrics: Dict[str, Any]
    soil_cable_metrics: Dict[str, Any]

    # Physics Engine Outputs
    baseline_trajectory: Dict[str, Any]
    mitigated_trajectory: Optional[Dict[str, Any]]
    virtual_moisture_state: Dict[str, Any]
    risk_level: str

    # Agent Action Synthesis & Non-LLM Safety Filter
    candidate_actions: List[Dict[str, Any]]
    safety_gate_verdict: Optional[Dict[str, Any]]
    economic_evaluation: Optional[Dict[str, Any]]

    # Dispatch & Downstream Channels
    b2b_work_order: Optional[Dict[str, Any]]
    b2c_advisory: Optional[Dict[str, Any]]
    defensible_finding: Optional[Dict[str, Any]]
    findings_report: Optional[Dict[str, Any]]
    audit_trail: List[Dict[str, Any]]
    errors: List[str]
    current_node: str

