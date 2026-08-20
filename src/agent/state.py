from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from src.models.asset import InfrastructureAsset, ThermalRiskAssessment, RiskLevel


class AgentState(BaseModel):
    """
    LangGraph Agent State for PyreShield thermal risk and mitigation pipeline.
    """
    target_city: str = Field(default="Phoenix, AZ")
    bounding_box: Optional[Dict[str, float]] = None
    assets: List[InfrastructureAsset] = Field(default_factory=list)
    raw_api_data: Dict[str, Any] = Field(default_factory=dict)
    assessments: List[ThermalRiskAssessment] = Field(default_factory=list)
    highest_risk_level: RiskLevel = Field(default=RiskLevel.SAFE)
    mitigation_plan: Dict[str, Any] = Field(default_factory=dict)
    b2b_alerts: List[Dict[str, Any]] = Field(default_factory=list)
    b2c_alerts: List[Dict[str, Any]] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    execution_trace: List[str] = Field(default_factory=list)
