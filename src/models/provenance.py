"""Shared provenance contract for every simulation response."""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

EvidenceKind = Literal[
    "measured", "externally_modelled", "derived", "assumed", "simulated", "validated", "unvalidated"
]


class EvidenceItem(BaseModel):
    field: str
    kind: EvidenceKind
    source: str
    note: Optional[str] = None


class SimulationProvenance(BaseModel):
    """Machine-readable separation of evidence, assumptions and model outputs."""

    schema_version: str = "1.0"
    model_version: str = "thermal-sentinel-grid/1.0"
    operating_mode: Literal["demo", "hybrid", "operational"]
    scenario_id: str
    boundary_source: str
    evidence: List[EvidenceItem]
    validation_status: Literal["environment_only", "partially_validated", "unvalidated"]
    limitations: List[str] = Field(default_factory=list)


def canonical_provenance(
    *,
    scenario_id: str,
    boundary_source: str,
    operating_mode: Literal["demo", "hybrid", "operational"] = "demo",
    solar_kind: EvidenceKind = "derived",
) -> Dict[str, Any]:
    """Build the common evidence contract used by replay and sandbox APIs."""
    return SimulationProvenance(
        operating_mode=operating_mode,
        scenario_id=scenario_id,
        boundary_source=boundary_source,
        validation_status="environment_only",
        evidence=[
            EvidenceItem(field="fortyguard_2m_ambient_c", kind="measured", source=boundary_source),
            EvidenceItem(field="relative_humidity_pct", kind="measured", source=boundary_source),
            EvidenceItem(field="wet_bulb_temp_c", kind="measured", source=boundary_source),
            EvidenceItem(field="solar_irradiance_w_m2", kind=solar_kind, source=boundary_source),
            EvidenceItem(field="persistence_and_exceedance", kind="derived", source="FortyGuard boundary series"),
            EvidenceItem(field="wind_speed_m_s", kind="assumed", source="regional/model default", note="FortyGuard env_params does not expose wind"),
            EvidenceItem(field="grid_load_and_topology", kind="assumed", source="demo feeder scenario"),
            EvidenceItem(field="soil_and_asset_initial_state", kind="assumed", source="engineering scenario defaults"),
            EvidenceItem(field="equipment_and_grid_trajectories", kind="simulated", source="deterministic engineering models"),
            EvidenceItem(field="economic_and_failure_risk", kind="unvalidated", source="scenario assumptions"),
        ],
        limitations=[
            "No utility SCADA, relay, transformer, cable, soil-probe, or BESS telemetry is connected.",
            "Environmental validation does not validate simulated equipment temperature or failure risk.",
            "Safety results apply only to the configured model and are not field certification.",
            "Dispatch outputs are recommendations/work orders; this service does not actuate equipment.",
        ],
    ).model_dump()
