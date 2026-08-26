"""
Database Models & Schemas for Thermal Sentinel Grid Persistence Layer
Supports dual persistence in Local SQLite (Zero-config) and Supabase PostgreSQL.
Defines records for all 17 application tables and their audit payloads.
"""

from __future__ import annotations

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field


# 1. API Call Cache
class ApiCallCacheRecord(BaseModel):
    """Cached response from external FortyGuard API endpoints."""
    query_hash: str = Field(description="MD5 hash of endpoint + request payload")
    endpoint: str = Field(description="API path e.g. /v1/heatmap or /v1/env_params")
    bounding_box: Optional[List[float]] = Field(default=None, description="[min_lon, min_lat, max_lon, max_lat]")
    request_params: Optional[Dict[str, Any]] = Field(default=None)
    response_payload: Dict[str, Any] = Field(description="Cached JSON payload")
    credits_spent: float = Field(default=0.0, description="Credits charged for call")
    hit_count: int = Field(default=1, description="Number of times served from cache")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expires_at: Optional[str] = None


# 2. Dispatch Work Orders
class DispatchWorkOrderRecord(BaseModel):
    """Historical record of authorized B2B dispatch work orders."""
    work_order_id: str
    asset_id: str
    calculated_k_safe: float
    bess_dispatch_mw: float = 0.0
    bess_volt_var_q_mvar: float = 0.0
    oltc_tap_step: int = 0
    forced_cooling_active: bool = True
    gpt_narrative: Optional[str] = None
    safety_status: str = "AUTHORIZED"
    cbf_barrier_compliant: bool = True
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# 3. Credit Accounting Ledger
class CreditLedgerRecord(BaseModel):
    """Audit ledger entry for FortyGuard API credit accounting."""
    transaction_id: str
    activity_id: Optional[str] = None
    endpoint: str
    credits_debited: float
    remaining_balance: Optional[float] = None
    ip_or_caller: Optional[str] = "internal-service"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# 4. Academic Research Papers Corpus
class AcademicPaperRecord(BaseModel):
    """Peer-reviewed academic paper indexed in SQLite & Supabase."""
    paper_id: str
    title: str
    authors: List[str] = Field(default_factory=list)
    year: int
    category: str
    journal_or_venue: Optional[str] = None
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    alphaxiv_url: Optional[str] = None
    pdf_url: Optional[str] = None
    abstract: str
    latex_formula: Optional[str] = None
    key_findings: Optional[str] = None
    relevance_to_fortyguard: Optional[str] = None
    citation_count: int = 0
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# 5. Substation SCADA Physical Telemetry Logs
class SubstationTelemetryRecord(BaseModel):
    """12-hour hourly physical telemetry log."""
    asset_id: str
    hour_step: int
    ambient_c: float
    top_oil_c: float
    hot_spot_c: float
    aging_factor: float
    load_ratio: float
    bess_dispatch_mw: float = 0.0
    is_mitigated: bool = False
    recorded_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# 6. What-If Sandbox Simulation Runs & Snapshots
class SimulationRunRecord(BaseModel):
    """User-executed What-If Sandbox scenario snapshot."""
    simulation_id: str
    scenario_name: str
    delta_c: float
    heatwave_day: int
    transformer_mva: float
    bess_mwh: float
    canyon_hw_ratio: float
    cooling_fans_stage: int
    peak_hot_spot_c: float
    hours_above_140c: float
    net_avoided_loss: float
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# 7. 72-Hour Multi-Day Compounding Heatwave Logs
class MultiDayHeatwaveRecord(BaseModel):
    """Continuous 72-hour multi-day simulation log."""
    simulation_id: Optional[str] = None
    day_number: int
    soil_resistivity: float
    cumulative_aging_hours: float
    max_hot_spot_c: float
    recorded_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# 8. IEEE 738 Dynamic Line Rating & Catenary Sag Telemetry
class DLRCatenaryRecord(BaseModel):
    """Dynamic Line Rating & Conductor Catenary Sag telemetry."""
    line_id: str
    ambient_c: float
    wind_speed_ms: float
    conductor_temp_c: float
    dynamic_ampacity_a: float
    ampacity_headroom_pct: float
    catenary_sag_m: float
    clearance_margin_m: float
    recorded_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# 9. LangGraph Multi-Agent Execution Traces
class AgentExecutionTraceRecord(BaseModel):
    """End-to-end execution trace of LangGraph StateGraph pipeline."""
    trace_id: str
    asset_id: str
    duration_ms: float
    node_sequence: List[str]
    cbf_safety_passed: bool
    gpt_work_order_id: Optional[str] = None
    gpt_advisory_text: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# 10. Financial Avoided Loss Audit Snapshots
class FinancialAuditRecord(BaseModel):
    """Investment-grade avoided loss calculation snapshot (LBNL ICE)."""
    audit_id: str
    asset_id: str
    avoided_equipment_loss: float
    avoided_customer_outage_loss: float
    avoided_aging_deferral: float
    net_avoided_loss: float
    economic_roi_multiplier: float
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# 11. Hyperlocal Microclimate Parcel Store
class MicroclimateParcelRecord(BaseModel):
    """FortyGuard 2-meter microclimate parcel GeoJSON record."""
    parcel_id: str
    polygon_geojson: Dict[str, Any]
    surface_temp_c: float
    convective_temp_2m_c: float
    asphalt_heat_trap_delta: float
    scanned_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# 12. BESS Electro-Thermal & SEI Degradation Logs
class BESSDegradationRecord(BaseModel):
    """Coupled core/surface thermal ODE and SEI capacity degradation record."""
    bess_id: str
    hour_step: int
    ambient_c: float
    dispatch_power_mw: float
    core_temp_c: float
    surface_temp_c: float
    soc_pct: float
    soh_pct: float
    degradation_cost_usd: float
    recorded_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# 13. System-Wide Cascading Outage Risk Snapshots
class CascadingRiskRecord(BaseModel):
    """Arrhenius-Weibull non-homogeneous Poisson cascading outage risk report."""
    snapshot_id: str
    heatwave_severity: str
    n1_reserve_margin_mw: float
    n1_compliant: bool
    cascade_outage_probability: float
    expected_unserved_energy_mwh: float
    total_voll_risk_usd: float
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# 14. Chance-Constrained SOCP OPF Dispatch Logs
class ChanceConstrainedOPFRecord(BaseModel):
    """Second-Order Cone Optimal Power Flow solution under forecast variance."""
    solve_id: str
    confidence_level_pct: float
    total_generation_mw: float
    bess_optimal_power_mw: float
    oltc_optimal_tap: int
    total_dispatch_cost_usd: float
    solver_status: str = "OPTIMAL_FEASIBLE"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# 15. CBF Control Barrier Function Safety Proof Certificates
class CBFSafetyCertificateRecord(BaseModel):
    """Control Barrier Function forward invariance mathematical certificate."""
    certificate_id: str
    asset_id: str
    nominal_k_load: float
    filtered_k_safe: float
    barrier_value_h: float
    qp_slack_xi: float
    is_safe_invariant: bool
    mathematical_proof: Optional[str] = None
    certified_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# 16. Dynamic Grid Asset Digital Twin Registry
class ValidationRunRecord(BaseModel):
    """Immutable external-evidence validation report."""
    validation_id: str
    scenario_id: str
    provider: str
    evidence_class: str
    baseline_identity: str
    reference_identity: str
    configuration: Dict[str, Any]
    report: Dict[str, Any]
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class GridAssetRegistryRecord(BaseModel):
    """Physical grid asset metadata and health state."""
    asset_id: str
    name: str
    type: str
    rated_mva: float
    latitude: float
    longitude: float
    cooling_type: str = "ONAN/ONAF"
    criticality_tier: int = 1
    current_health_score: float = 95.0
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
