"""
Virtual Moisture & Dielectric Breakdown Sensor (Fick's Law & IEC 60422)
Models Arrhenius-driven moisture desorption from cellulose paper insulation into oil
under thermal soak, predicting relative oil saturation (RS_o) and dielectric arcing risk.
"""

from __future__ import annotations

import math
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class MoistureParameters(BaseModel):
    """Physicochemical constants for cellulose paper and mineral insulating oil."""
    d_p0: float = Field(default=1.2e-6, description="Reference diffusion coefficient (m^2/s)")
    activation_energy_ea: float = Field(default=45000.0, description="Activation energy for moisture migration (J/mol)")
    r_gas: float = Field(default=8.314, description="Universal gas constant (J/mol·K)")
    
    # Paper-Oil equilibrium parameters
    initial_paper_moisture_pct: float = Field(default=2.5, description="Initial moisture in Kraft paper (wt %)")
    initial_oil_moisture_ppm: float = Field(default=12.0, description="Initial moisture in oil (ppm)")
    k_po_base: float = Field(default=0.08, description="Paper-to-oil rate constant (1/h)")
    k_op_base: float = Field(default=0.02, description="Oil-to-paper rate constant (1/h)")

    critical_relative_saturation_rs: float = Field(default=0.50, description="Dielectric warning threshold (50% RS)")
    breakdown_relative_saturation_rs: float = Field(default=0.75, description="Imminent dielectric arcing threshold (75% RS)")


class VirtualMoistureEngine:
    """
    Virtual software sensor calculating real-time paper-oil moisture migration
    and dielectric breakdown risk index.
    """

    def __init__(self, params: Optional[MoistureParameters] = None) -> None:
        self.params = params or MoistureParameters()

    def oil_moisture_saturation_limit(self, t_oil_c: float) -> float:
        """
        Moisture solubility limit in standard mineral oil w_sat(T_o) in ppm:
        log10(w_sat) = 7.0895 - 1567 / (T_o + 273.15)
        """
        t_k = max(t_oil_c + 273.15, 250.0)
        log_wsat = 7.0895 - (1567.0 / t_k)
        return float(10.0 ** log_wsat)

    def calculate_diffusion_coefficient(self, t_hot_spot_c: float) -> float:
        """
        Fickian diffusion coefficient D_p(T) in m^2/s:
        D_p(T) = D_p,0 * exp(-E_a / (R_g * T_hs))
        """
        p = self.params
        t_k = max(t_hot_spot_c + 273.15, 250.0)
        d_p = p.d_p0 * math.exp(-p.activation_energy_ea / (p.r_gas * t_k))
        return float(d_p)

    def step_moisture_migration(
        self,
        paper_moisture_pct: float,
        oil_moisture_ppm: float,
        t_hot_spot_c: float,
        t_oil_c: float,
        dt_hours: float = 1.0,
    ) -> Dict[str, Any]:
        """
        Computes dynamic paper-oil moisture exchange over time step dt_hours.
        """
        p = self.params
        t_k = max(t_hot_spot_c + 273.15, 273.15)
        temp_acceleration = math.exp((t_k - 383.0) / 25.0)  # accelerates at high hot-spot

        # Thermal desorption rate from paper into oil
        k_po = p.k_po_base * temp_acceleration
        k_op = p.k_op_base

        # Desorption flux (ppm/hr)
        desorption_flux = k_po * paper_moisture_pct * 10.0 - k_op * oil_moisture_ppm
        delta_oil_ppm = desorption_flux * dt_hours

        new_oil_ppm = max(oil_moisture_ppm + delta_oil_ppm, 1.0)
        new_paper_pct = max(paper_moisture_pct - (delta_oil_ppm / 1000.0), 0.5)

        # Relative oil saturation RS_o = w_oil / w_sat(T_o)
        w_sat = self.oil_moisture_saturation_limit(t_oil_c)
        rs_oil = min(new_oil_ppm / max(w_sat, 1.0), 1.0)

        # Logistic dielectric breakdown probability
        z = -6.5 + 8.5 * rs_oil + 0.03 * (t_hot_spot_c - 100.0)
        p_dielectric = 1.0 / (1.0 + math.exp(-min(max(z, -10.0), 10.0)))

        is_alarm = rs_oil >= p.critical_relative_saturation_rs

        return {
            "paper_moisture_pct": round(new_paper_pct, 3),
            "oil_moisture_ppm": round(new_oil_ppm, 2),
            "oil_saturation_limit_ppm": round(w_sat, 2),
            "relative_saturation_rs_oil": round(rs_oil, 3),
            "dielectric_breakdown_probability": round(p_dielectric, 4),
            "dielectric_alarm": is_alarm,
            "dielectric_status": "CRITICAL ARCING RISK" if rs_oil >= p.breakdown_relative_saturation_rs else ("ELEVATED DESORPTION" if is_alarm else "NORMAL"),
        }
