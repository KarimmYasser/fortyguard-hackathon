"""
Investment-Grade Economic Model & Avoided Loss Quantifier
Computes non-overlapping, auditable avoided loss metrics:
Net Avoided Loss = [p_f,base - p_f,mitigated] * C_consequence + Delta PV_aging - C_mitigation
"""

from __future__ import annotations

import math
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class EconomicParameters(BaseModel):
    """Financial parameters for utility avoided loss and insurance risk reduction."""
    transformer_replacement_cost_usd: float = Field(default=350000.0, description="Cost of new distribution transformer")
    emergency_procurement_premium_pct: float = Field(default=40.0, description="Expedited delivery & crane staging (+40%)")
    design_life_equivalent_hours: float = Field(default=180000.0, description="20-year IEEE design life at reference 110°C")
    discount_rate_annual: float = Field(default=0.06, description="Utility weighted average cost of capital (WACC)")
    
    # Interruption & VoLL (LBNL ICE Calculator)
    value_of_lost_load_per_kwh_usd: float = Field(default=12.50, description="VoLL for commercial/hospital feeders ($/kWh)")
    unserved_energy_mwh_if_blown: float = Field(default=180.0, description="12-hour outage across 15 MW substation")
    crew_emergency_overtime_usd: float = Field(default=45000.0, description="Emergency repair crew & fire marshal inspection")
    regulatory_saidi_penalty_usd: float = Field(default=75000.0, description="Public Utility Commission reliability penalty")

    # Mitigation costs
    bess_degradation_cost_per_mwh_usd: float = Field(default=42.0, description="Battery throughput degradation cost")
    cooling_fan_power_kw: float = Field(default=25.0, description="Auxiliary forced cooling pumps & fans")
    electricity_peak_rate_per_kwh_usd: float = Field(default=0.28, description="Peak summer commercial energy tariff")


class EconomicEngine:
    """
    Computes rigorous, investment-grade ROI and avoided failure cost metrics.
    """

    def __init__(self, params: Optional[EconomicParameters] = None) -> None:
        self.params = params or EconomicParameters()

    def calculate_outage_consequence_cost(self) -> float:
        """
        Total consequence cost if catastrophic blowout occurs:
        C_consequence = C_emg_replace + C_interruption + C_crew + C_regulatory
        """
        p = self.params
        c_replace = p.transformer_replacement_cost_usd * (1.0 + p.emergency_procurement_premium_pct / 100.0)
        c_interruption = p.unserved_energy_mwh_if_blown * 1000.0 * p.value_of_lost_load_per_kwh_usd
        c_crew = p.crew_emergency_overtime_usd
        c_reg = p.regulatory_saidi_penalty_usd
        return float(c_replace + c_interruption + c_crew + c_reg)

    def calculate_failure_probability(
        self,
        peak_hot_spot_c: float,
        persistence_hours_p40: float,
        thermal_soak_index: float,
    ) -> float:
        """
        Calibrated logistic failure model:
        z = beta_0 + beta_1 * max(0, T_hs - 120) + beta_2 * TSI
        """
        # Baseline calibrated logit
        z = -5.8 + 0.16 * max(peak_hot_spot_c - 120.0, 0.0) + 0.25 * thermal_soak_index
        # Extreme penalty if emergency ceiling breached
        if peak_hot_spot_c >= 140.0:
            z += 0.85
        prob = 1.0 / (1.0 + math.exp(-min(max(z, -12.0), 12.0)))
        return float(prob)

    def calculate_capital_aging_deferral(
        self,
        baseline_loss_of_life_hours: float,
        mitigated_loss_of_life_hours: float,
    ) -> float:
        """
        Delta PV_aging: Financial savings from deferred capital replacement
        based on avoided equivalent aging hours Delta L_eq.
        """
        p = self.params
        delta_hours = max(baseline_loss_of_life_hours - mitigated_loss_of_life_hours, 0.0)
        cost_per_aging_hour = p.transformer_replacement_cost_usd / p.design_life_equivalent_hours
        return float(delta_hours * cost_per_aging_hour)

    def calculate_mitigation_cost(
        self,
        bess_energy_discharged_mwh: float = 12.5,
        cooling_runtime_hours: float = 8.0,
    ) -> float:
        """
        C_mitigation = C_BESS_cycling + C_cooling_electricity
        """
        p = self.params
        c_bess = bess_energy_discharged_mwh * p.bess_degradation_cost_per_mwh_usd
        c_cooling = (
            (p.cooling_fan_power_kw * cooling_runtime_hours)
            * p.electricity_peak_rate_per_kwh_usd
        )
        return float(c_bess + c_cooling)

    def evaluate_net_avoided_loss(
        self,
        baseline_peak_hot_spot_c: float = 143.2,
        mitigated_peak_hot_spot_c: float = 136.8,
        baseline_loss_of_life_hours: float = 88.6,
        mitigated_loss_of_life_hours: float = 15.2,
        persistence_hours: float = 12.0,
        thermal_soak_index: float = 3.68,
        bess_discharged_mwh: float = 12.5,
        cooling_runtime_hours: float = 8.0,
    ) -> Dict[str, Any]:
        """
        Full investment-grade evaluation comparing baseline vs. Thermal Sentinel Grid.
        """
        c_consequence = self.calculate_outage_consequence_cost()

        p_f_base = self.calculate_failure_probability(
            baseline_peak_hot_spot_c, persistence_hours, thermal_soak_index
        )
        p_f_mitigated = self.calculate_failure_probability(
            mitigated_peak_hot_spot_c, persistence_hours, thermal_soak_index
        )

        avoided_outage_risk_usd = (p_f_base - p_f_mitigated) * c_consequence
        delta_pv_aging_usd = self.calculate_capital_aging_deferral(
            baseline_loss_of_life_hours, mitigated_loss_of_life_hours
        )
        c_mitigation_usd = self.calculate_mitigation_cost(
            bess_discharged_mwh, cooling_runtime_hours
        )

        net_avoided_loss_usd = avoided_outage_risk_usd + delta_pv_aging_usd - c_mitigation_usd
        roi_multiple = (
            (avoided_outage_risk_usd + delta_pv_aging_usd) / max(c_mitigation_usd, 1.0)
        )

        return {
            "total_outage_consequence_usd": round(c_consequence, 2),
            "baseline_failure_probability_pct": round(p_f_base * 100.0, 2),
            "mitigated_failure_probability_pct": round(p_f_mitigated * 100.0, 2),
            "avoided_outage_risk_usd": round(avoided_outage_risk_usd, 2),
            "avoided_aging_hours": round(baseline_loss_of_life_hours - mitigated_loss_of_life_hours, 1),
            "capital_aging_deferral_usd": round(delta_pv_aging_usd, 2),
            "mitigation_cost_usd": round(c_mitigation_usd, 2),
            "net_avoided_loss_usd": round(net_avoided_loss_usd, 2),
            "roi_multiple": round(roi_multiple, 1),
        }
