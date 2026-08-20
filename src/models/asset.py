from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class AssetType(str, Enum):
    HVAC_COMPRESSOR = "hvac_compressor"
    TRANSFORMER_BOX = "transformer_box"
    SOLAR_INVERTER = "solar_inverter"
    BATTERY_STORAGE = "battery_storage"
    EV_CHARGER = "ev_charger"
    ELECTRICAL_PANEL = "electrical_panel"


class MountingLocation(str, Enum):
    GROUND_LEVEL = "ground_level"         # 0m - 1m above asphalt
    STREET_INTERFACE = "street_interface" # 1m - 2m above ground (FortyGuard 2m layer)
    BALCONY_FACADE = "balcony_facade"     # 2m - 5m facade
    ROOFTOP = "rooftop"


class RiskLevel(str, Enum):
    SAFE = "safe"
    ELEVATED = "elevated"
    CRITICAL = "critical"
    THERMAL_RUNAWAY_IMMINENT = "thermal_runaway_imminent"


class InfrastructureAsset(BaseModel):
    id: str = Field(..., description="Unique asset identifier")
    name: str = Field(..., description="Human readable asset name")
    asset_type: AssetType
    mounting_location: MountingLocation
    latitude: float
    longitude: float
    max_safe_ambient_temp_c: float = Field(
        default=40.0,
        description="Max operating ambient temperature before thermal derating / risk"
    )
    critical_explosion_temp_c: float = Field(
        default=50.0,
        description="Threshold where capacitor / lithium thermal runaway occurs"
    )
    current_load_percentage: float = Field(default=80.0, ge=0, le=100)
    owner_type: str = Field(default="B2B", description="'B2B' or 'B2C'")
    contact_email: Optional[str] = None


class ThermalRiskAssessment(BaseModel):
    asset_id: str
    asset_name: str
    asset_type: AssetType
    ambient_2m_temp_c: float
    persistence_hours: float = Field(
        description="Hours the asset has sat in continuous exceedance temperature"
    )
    exceedance_delta_c: float = Field(
        description="Degrees above max_safe_ambient_temp_c"
    )
    risk_level: RiskLevel
    forecast_12h_peak_temp_c: Optional[float] = None
    recommended_mitigation: List[str] = Field(default_factory=list)
    action_required: bool = False
