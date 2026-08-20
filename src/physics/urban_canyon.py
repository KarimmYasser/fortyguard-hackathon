"""
Urban Canyon Aerodynamics & Heat Rejection Throttling Engine (Oke / Evola)
Models morphological wind-sheltering (kappa_morph), convective heat transfer degradation,
and equipment cooling derate (eta_cool) caused by deep street canyons and building facade reflections.
"""

from __future__ import annotations

import math
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class UrbanCanyonParameters(BaseModel):
    """Morphological and thermodynamic properties of the urban street canyon."""
    height_to_width_ratio_hw: float = Field(default=1.85, description="Building height to street width (H/W)")
    frontal_area_density_lambda_f: float = Field(default=0.32, description="Building frontal area index")
    canyon_albedo: float = Field(default=0.22, description="Surrounding facade & pavement surface albedo")
    open_canyon_orientation_phi: float = Field(default=0.20, description="Fraction of canyon aligned with prevailing wind")
    
    beta_1: float = Field(default=0.35, description="H/W aerodynamic damping factor")
    beta_2: float = Field(default=0.40, description="Frontal density damping factor")
    beta_3: float = Field(default=0.25, description="Alignment enhancement factor")
    kappa_min: float = Field(default=0.35, description="Minimum wind penetration factor")

    reference_wind_speed_m_s: float = Field(default=3.0, description="Regional 10m weather station wind speed (m/s)")
    stefan_boltzmann_sigma: float = Field(default=5.67e-8, description="W/m^2·K^4")
    emissivity_epsilon: float = Field(default=0.90, description="Radiator fin surface emissivity")


class UrbanCanyonEngine:
    """
    Evaluates microclimate wind sheltering and equipment cooling derate.
    """

    def __init__(self, params: Optional[UrbanCanyonParameters] = None) -> None:
        self.params = params or UrbanCanyonParameters()

    def calculate_morphological_sheltering(
        self,
        hw_ratio: Optional[float] = None,
        lambda_f: Optional[float] = None,
    ) -> float:
        """
        Computes the wind sheltering factor kappa_morph:
        U_eff = U_ref * clip(exp(-beta_1 * (H/W) - beta_2 * lambda_f + beta_3 * phi), kappa_min, 1.0)
        """
        p = self.params
        hw = hw_ratio if hw_ratio is not None else p.height_to_width_ratio_hw
        lf = lambda_f if lambda_f is not None else p.frontal_area_density_lambda_f

        exponent = -p.beta_1 * hw - p.beta_2 * lf + p.beta_3 * p.open_canyon_orientation_phi
        kappa = math.exp(exponent)
        return float(min(max(kappa, p.kappa_min), 1.0))

    def calculate_convective_heat_transfer_coefficient(
        self,
        wind_speed_m_s: float,
        kappa_morph: float,
    ) -> float:
        """
        Calculates local convective heat transfer coefficient h_c (W/m^2·K):
        h_c = 5.7 + 3.8 * U_eff
        """
        u_eff = wind_speed_m_s * kappa_morph
        h_c = 5.7 + 3.8 * max(u_eff, 0.2)
        return float(h_c)

    def calculate_cooling_derate_factor(
        self,
        fortyguard_2m_ambient_c: float,
        reference_wind_speed_m_s: float = 3.0,
        equipment_surface_temp_c: float = 85.0,
        solar_irradiance_w_m2: float = 850.0,
    ) -> Dict[str, Any]:
        """
        Calculates the equipment cooling derate factor eta_cool:
        eta_cool = (Convective + Radiative Heat Rejection in Canyon) / (Standard Open Terrain Heat Rejection)
        """
        p = self.params
        kappa = self.calculate_morphological_sheltering()
        h_c_local = self.calculate_convective_heat_transfer_coefficient(
            reference_wind_speed_m_s, kappa
        )
        h_c_ref = 5.7 + 3.8 * reference_wind_speed_m_s  # Open terrain reference

        t_s_k = equipment_surface_temp_c + 273.15
        t_canyon_k = fortyguard_2m_ambient_c + 273.15
        # Facades reflect solar irradiance, increasing effective radiation background
        reflected_solar_delta = (p.canyon_albedo * solar_irradiance_w_m2) / 25.0
        t_rad_k = t_canyon_k + reflected_solar_delta

        # Heat flux components (W/m^2)
        q_conv_local = h_c_local * max(equipment_surface_temp_c - fortyguard_2m_ambient_c, 1.0)
        q_rad_local = p.emissivity_epsilon * p.stefan_boltzmann_sigma * max(t_s_k**4 - t_rad_k**4, 0.0)
        q_total_local = q_conv_local + q_rad_local

        # Reference open terrain heat flux
        t_ref_ambient_c = fortyguard_2m_ambient_c - 4.5  # open terrain is cooler
        q_conv_ref = h_c_ref * max(equipment_surface_temp_c - t_ref_ambient_c, 1.0)
        q_rad_ref = p.emissivity_epsilon * p.stefan_boltzmann_sigma * max(t_s_k**4 - (t_ref_ambient_c + 273.15)**4, 0.0)
        q_total_ref = q_conv_ref + q_rad_ref

        eta_cool = min(max(q_total_local / max(q_total_ref, 1e-4), 0.40), 1.0)

        return {
            "morphological_sheltering_kappa": round(kappa, 3),
            "effective_wind_speed_m_s": round(reference_wind_speed_m_s * kappa, 2),
            "convective_h_c_w_m2_k": round(h_c_local, 2),
            "cooling_derate_eta_cool": round(eta_cool, 3),
            "cooling_capacity_loss_pct": round((1.0 - eta_cool) * 100.0, 1),
        }
