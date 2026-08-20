"""
Buried Cable–Soil Moisture Dryout Engine (IEC 60287 & IEC 60853)
Models non-linear soil thermal resistivity surge (rho_soil) driven by cumulative
multi-day heat persistence and evaporative moisture loss, exposing the hidden
underground cable thermal bottleneck.
"""

from __future__ import annotations

import math
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class SoilCableParameters(BaseModel):
    """Parameters for underground cable and soil thermal dynamics."""
    rho_wet: float = Field(default=0.90, description="Thermal resistivity of wet soil (K·m/W)")
    rho_dry: float = Field(default=2.50, description="Thermal resistivity of completely dried soil (K·m/W)")
    theta_crit: float = Field(default=0.12, description="Critical volumetric soil moisture threshold (m^3/m^3)")
    logistic_steepness_a: float = Field(default=35.0, description="Steepness of soil drying curve")
    tau_evaporation_days: float = Field(default=14.0, description="Soil moisture depletion time constant in days")
    
    # Cable physical parameters
    t_c_max_c: float = Field(default=90.0, description="Continuous conductor temperature limit for XLPE cable (°C)")
    t_c_emergency_c: float = Field(default=105.0, description="Emergency cable conductor temperature limit (°C)")
    r_ac_per_km: float = Field(default=0.08, description="AC conductor resistance at rated temp (Ohm/km)")
    depth_m: float = Field(default=1.2, description="Burial depth in meters")
    diameter_m: float = Field(default=0.075, description="Cable outer diameter in meters")
    ambient_soil_temp_inf_c: float = Field(default=28.0, description="Deep soil baseline temperature (°C)")


class SoilCableEngine:
    """
    Computes dynamic soil thermal resistivity, cable conductor temperature,
    and underground ampacity derates based on FortyGuard multi-day heat persistence.
    """

    def __init__(self, params: Optional[SoilCableParameters] = None) -> None:
        self.params = params or SoilCableParameters()

    def estimate_volumetric_soil_moisture(
        self,
        initial_moisture: float,
        consecutive_heatwave_days: float,
    ) -> float:
        """
        Estimates depleted volumetric soil moisture theta_v:
        theta_v = max(theta_v_init * exp(-days / tau_evap), 0.02)
        """
        p = self.params
        moisture = initial_moisture * math.exp(-consecutive_heatwave_days / p.tau_evaporation_days)
        return float(max(moisture, 0.02))

    def calculate_soil_thermal_resistivity(
        self,
        volumetric_moisture_theta_v: float,
    ) -> float:
        """
        Non-linear logistic soil thermal resistivity:
        rho_soil = rho_wet + (rho_dry - rho_wet) / (1 + exp(a * (theta_v - theta_crit)))
        """
        p = self.params
        exponent = p.logistic_steepness_a * (volumetric_moisture_theta_v - p.theta_crit)
        clamped_exp = min(max(exponent, -20.0), 20.0)
        rho = p.rho_wet + (p.rho_dry - p.rho_wet) / (1.0 + math.exp(clamped_exp))
        return float(rho)

    def calculate_cable_thermal_resistance(self, rho_soil: float) -> float:
        """
        Kennelly approximation for external soil thermal resistance (K·m/W):
        T4 = (rho_soil / (2 * pi)) * ln(4 * depth / diameter)
        """
        p = self.params
        geom_ratio = (4.0 * p.depth_m) / max(p.diameter_m, 1e-4)
        t4_soil = (rho_soil / (2.0 * math.pi)) * math.log(geom_ratio)
        internal_cable_res = 0.35  # Insulation + jacket thermal resistance
        return float(internal_cable_res + t4_soil)

    def calculate_cable_temperature(
        self,
        current_ampacity_ratio: float,
        rho_soil: float,
        ambient_soil_temp_c: Optional[float] = None,
    ) -> float:
        """
        T_c = T_soil_inf + q_loss * R_th(rho_soil)
        """
        p = self.params
        t_inf = ambient_soil_temp_c or p.ambient_soil_temp_inf_c
        r_th = self.calculate_cable_thermal_resistance(rho_soil)
        
        # Rated heat loss at 1.0 pu load is ~45 W/m
        q_loss = 45.0 * (current_ampacity_ratio ** 2)
        t_conductor = t_inf + q_loss * (r_th / 3.0)  # normalized per phase
        return float(t_conductor)

    def compute_cable_ampacity_derate(self, rho_soil: float) -> float:
        """
        Ampacity derate factor relative to standard wet soil (rho = 0.9 K·m/W):
        Derate = sqrt(R_th(rho_wet) / R_th(rho_soil))
        """
        p = self.params
        r_th_wet = self.calculate_cable_thermal_resistance(p.rho_wet)
        r_th_current = self.calculate_cable_thermal_resistance(rho_soil)
        derate = math.sqrt(r_th_wet / max(r_th_current, 1e-4))
        return float(min(derate, 1.0))

    def evaluate_compound_site_margin(
        self,
        consecutive_heatwave_days: float,
        initial_moisture: float,
        cable_load_k: float,
        transformer_top_oil_c: float,
        transformer_hot_spot_c: float,
    ) -> Dict[str, Any]:
        """
        Evaluates the shared multi-physics site risk margin across the buried cable
        and the surface transformer at the same parcel.
        """
        p = self.params
        theta_v = self.estimate_volumetric_soil_moisture(initial_moisture, consecutive_heatwave_days)
        rho_soil = self.calculate_soil_thermal_resistivity(theta_v)
        derate = self.compute_cable_ampacity_derate(rho_soil)
        t_cable = self.calculate_cable_temperature(cable_load_k, rho_soil)

        margin_cable = p.t_c_max_c - t_cable
        margin_top_oil = 110.0 - transformer_top_oil_c
        margin_hot_spot = 140.0 - transformer_hot_spot_c

        shared_margin = min(margin_cable, margin_top_oil, margin_hot_spot)

        return {
            "volumetric_moisture_theta_v": round(theta_v, 4),
            "soil_thermal_resistivity_rho_soil": round(rho_soil, 2),
            "cable_ampacity_derate": round(derate, 3),
            "cable_conductor_temp_c": round(t_cable, 2),
            "cable_margin_c": round(margin_cable, 2),
            "transformer_hot_spot_margin_c": round(margin_hot_spot, 2),
            "compound_site_margin_c": round(shared_margin, 2),
            "is_cable_bottleneck": margin_cable < margin_hot_spot,
        }
