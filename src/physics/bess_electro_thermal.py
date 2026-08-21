"""
Coupled Electro-Thermal Battery Energy Storage (BESS) Degradation & SEI Engine
Implements 2-state lumped thermal differential equations (Core Tc and Surface Ts),
internal ohmic Joule heating with Arrhenius temperature dependence, continuous
Solid Electrolyte Interphase (SEI) capacity fade kinetics, real-time $/MWh degradation cost,
and thermal runaway boundary barrier protection (Tc < 55°C).
"""

from __future__ import annotations

import math
from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field


class BESSContainerSpecification(BaseModel):
    """Specification of utility-scale Lithium-Ion (LFP/NMC) BESS container."""
    container_id: str = Field(default="BESS-PHX-01")
    nominal_energy_mwh: float = Field(default=25.0, description="Nameplate storage capacity (MWh)")
    rated_power_mw: float = Field(default=10.0, description="Max 4-quadrant inverter power (MW)")
    nominal_cell_capacity_ah: float = Field(default=280.0, description="Cell capacity (Ah)")
    nominal_pack_voltage_v: float = Field(default=1000.0, description="DC bus voltage (V)")
    r_int_nominal_ohm: float = Field(default=0.015, description="Pack internal DC resistance at 25°C (Ohm)")
    c_core_thermal_j_per_k: float = Field(default=4.5e6, description="Core thermal heat capacity (J/K)")
    c_surface_thermal_j_per_k: float = Field(default=2.2e6, description="Surface thermal heat capacity (J/K)")
    r_conduction_k_per_w: float = Field(default=0.0085, description="Internal conduction resistance (K/W)")
    r_convection_k_per_w: float = Field(default=0.0120, description="External convection resistance (K/W)")
    e_activation_sei_j_per_mol: float = Field(default=35000.0, description="SEI growth Arrhenius activation energy (J/mol)")
    b_sei_constant: float = Field(default=0.0028, description="SEI kinetic pre-exponential factor")
    max_safe_core_temp_c: float = Field(default=45.0, description="Normal operational core ceiling (°C)")
    thermal_runaway_temp_c: float = Field(default=55.0, description="Exothermic SEI decomposition boundary (°C)")
    stack_replacement_capex_usd: float = Field(default=2_500_000.0, description="Total battery stack capital cost ($)")
    eol_capacity_loss_threshold: float = Field(default=0.20, description="End-of-life capacity loss fraction (20% loss = 80% SOH)")


class BESSThermalStepResult(BaseModel):
    """BESS state output for a single simulation timestep."""
    time_minutes: float
    ambient_temp_c: float
    discharge_power_mw: float
    current_amps: float
    state_of_charge_pct: float
    core_temp_c: float
    surface_temp_c: float
    joule_heat_generation_kw: float
    cooling_dissipation_kw: float
    sei_degradation_rate_pct_per_hr: float
    cumulative_capacity_loss_pct: float
    state_of_health_pct: float
    hourly_degradation_cost_usd: float
    thermal_runaway_warning: bool
    status: str  # "OPTIMAL", "ELEVATED_DEGRADATION", "THERMAL_BARRIER_ALERT"


class BESSElectroThermalEngine:
    """
    Simulates coupled electro-thermal state dynamics and Arrhenius SEI capacity fade.
    """

    GAS_CONSTANT_R = 8.314  # J / (mol * K)

    def __init__(self, spec: Optional[BESSContainerSpecification] = None) -> None:
        self.spec = spec or BESSContainerSpecification()

    def get_internal_resistance(self, t_core_c: float, soc: float) -> float:
        """
        Calculates temperature and SOC-dependent internal DC resistance:
        R_int(T, SOC) = R_0 * (1 + 0.5 * (1 - SOC)^2) * exp(E_act / R * (1/T - 1/T_ref))
        """
        t_core_k = t_core_c + 273.15
        t_ref_k = 298.15  # 25°C
        soc_factor = 1.0 + 0.4 * ((1.0 - max(min(soc, 1.0), 0.0)) ** 2)
        arrhenius = math.exp((12000.0 / self.GAS_CONSTANT_R) * (1.0 / t_core_k - 1.0 / t_ref_k))
        return float(self.spec.r_int_nominal_ohm * soc_factor * arrhenius)

    def calculate_sei_capacity_loss_rate(
        self, t_core_c: float, c_rate: float, elapsed_hours: float = 1.0
    ) -> float:
        """
        Continuous SEI layer growth rate (Arrhenius capacity fade % per hour):
        dQ_loss/dt = B_SEI * exp(-E_a / (R * T_core)) * (C_rate)^0.8 * (t)^(-0.5)
        """
        t_core_k = t_core_c + 273.15
        arrhenius_sei = math.exp(-self.spec.e_activation_sei_j_per_mol / (self.GAS_CONSTANT_R * t_core_k))
        c_rate_factor = max(c_rate, 0.1) ** 0.8
        time_factor = (max(elapsed_hours, 0.1)) ** (-0.5)

        # Rate of capacity loss (% per hour)
        rate = self.spec.b_sei_constant * arrhenius_sei * c_rate_factor * time_factor * 100.0
        return float(round(rate, 6))

    def step_thermal_ode(
        self,
        t_core_prev: float,
        t_surface_prev: float,
        t_ambient: float,
        current_amps: float,
        soc: float,
        dt_seconds: float = 60.0,
    ) -> Tuple[float, float, float, float]:
        """
        Integrates 2-state lumped thermal ODEs over timestep dt:
        dT_c/dt = (I²R_int + (T_s - T_c) / R_cond) / C_core
        dT_s/dt = ((T_c - T_s) / R_cond - (T_s - T_amb) / R_conv) / C_surface
        """
        r_int = self.get_internal_resistance(t_core_prev, soc)
        q_joule = (current_amps**2) * r_int  # Watts

        q_cond = (t_surface_prev - t_core_prev) / self.spec.r_conduction_k_per_w  # Watts
        q_conv = (t_surface_prev - t_ambient) / self.spec.r_convection_k_per_w  # Watts

        # Derivatives
        d_tc_dt = (q_joule + q_cond) / self.spec.c_core_thermal_j_per_k
        d_ts_dt = (-q_cond - q_conv) / self.spec.c_surface_thermal_j_per_k

        # Forward Euler numerical update
        t_core_next = t_core_prev + d_tc_dt * dt_seconds
        t_surface_next = t_surface_prev + d_ts_dt * dt_seconds

        return float(t_core_next), float(t_surface_next), float(q_joule / 1000.0), float(q_conv / 1000.0)

    def simulate_dispatch_trajectory(
        self,
        ambient_temps_c: List[float],
        dispatch_powers_mw: List[float],
        initial_soc: float = 0.85,
        initial_core_temp_c: float = 35.0,
        initial_surface_temp_c: float = 33.0,
        time_step_hours: float = 1.0,
    ) -> List[BESSThermalStepResult]:
        """
        Simulates multi-hour BESS thermal and degradation progression under varying ambient and dispatch.
        """
        results: List[BESSThermalStepResult] = []
        t_core = initial_core_temp_c
        t_surf = initial_surface_temp_c
        soc = initial_soc
        cumulative_loss_pct = 0.0

        total_steps = len(ambient_temps_c)

        for step_idx in range(total_steps):
            t_amb = ambient_temps_c[step_idx]
            p_mw = dispatch_powers_mw[step_idx] if step_idx < len(dispatch_powers_mw) else 0.0

            # Calculate DC current (Amps) = Power (W) / Voltage (V)
            current_amps = (p_mw * 1e6) / self.spec.nominal_pack_voltage_v
            c_rate = p_mw / self.spec.nominal_energy_mwh

            # Sub-step 60-second integration for stability
            substeps = int((time_step_hours * 3600.0) / 60.0)
            q_joule_kw_avg = 0.0
            q_conv_kw_avg = 0.0

            for _ in range(substeps):
                t_core, t_surf, q_j, q_c = self.step_thermal_ode(
                    t_core, t_surf, t_amb, current_amps, soc, dt_seconds=60.0
                )
                q_joule_kw_avg += q_j / substeps
                q_conv_kw_avg += q_c / substeps

            # Update SOC
            delta_soc = (p_mw * time_step_hours) / self.spec.nominal_energy_mwh
            soc = max(min(soc - delta_soc, 1.0), 0.05)

            # SEI Degradation calculation
            elapsed_h = (step_idx + 1) * time_step_hours
            sei_rate = self.calculate_sei_capacity_loss_rate(t_core, c_rate, elapsed_h)
            cumulative_loss_pct += sei_rate * time_step_hours
            soh_pct = max(100.0 - cumulative_loss_pct, 0.0)

            # Degradation cost ($/hr) = (dLoss / EOL_threshold) * Replacement CAPEX
            fractional_loss_step = (sei_rate / 100.0) * time_step_hours
            hourly_cost = (fractional_loss_step / self.spec.eol_capacity_loss_threshold) * self.spec.stack_replacement_capex_usd

            runaway_alert = t_core >= self.spec.thermal_runaway_temp_c

            if runaway_alert:
                status = "THERMAL_BARRIER_ALERT"
            elif t_core >= self.spec.max_safe_core_temp_c:
                status = "ELEVATED_DEGRADATION"
            else:
                status = "OPTIMAL"

            results.append(
                BESSThermalStepResult(
                    time_minutes=float((step_idx + 1) * time_step_hours * 60.0),
                    ambient_temp_c=round(t_amb, 2),
                    discharge_power_mw=round(p_mw, 2),
                    current_amps=round(current_amps, 1),
                    state_of_charge_pct=round(soc * 100.0, 1),
                    core_temp_c=round(t_core, 2),
                    surface_temp_c=round(t_surf, 2),
                    joule_heat_generation_kw=round(q_joule_kw_avg, 2),
                    cooling_dissipation_kw=round(q_conv_kw_avg, 2),
                    sei_degradation_rate_pct_per_hr=round(sei_rate, 5),
                    cumulative_capacity_loss_pct=round(cumulative_loss_pct, 5),
                    state_of_health_pct=round(soh_pct, 5),
                    hourly_degradation_cost_usd=round(hourly_cost, 2),
                    thermal_runaway_warning=runaway_alert,
                    status=status,
                )
            )

        return results
