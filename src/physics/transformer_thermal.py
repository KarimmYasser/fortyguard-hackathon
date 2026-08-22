"""
IEEE C57.91 / IEC 60076-7 Transformer Thermal & Insulation Degradation Engine
Implements exact discrete-time exponential state updates (Delta t = 5 min / 1 hour),
equivalent solar ambient increment, Arrhenius aging acceleration factor V(T_hs),
and Thermal Soak Index (TSI).
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from src.models.thermal import (
    ThermalStepState,
    ThermalTrajectory,
    TransformerThermalParams,
)


class TransformerThermalEngine:
    """
    Physical simulation engine for oil-immersed power and distribution transformers
    under dynamic hyperlocal 2-meter ambient temperature and solar forcing.
    """

    def __init__(self, params: Optional[TransformerThermalParams] = None) -> None:
        self.params = params or TransformerThermalParams()

    def calculate_solar_increment(self, solar_irradiance_w_m2: float) -> float:
        """
        Calculates the equivalent ambient temperature increment due to solar radiation:
        Delta T_solar = (alpha_abs * S * A_proj * F_view) / (h_eff * A_surf)
        """
        if solar_irradiance_w_m2 <= 0:
            return 0.0
        p = self.params
        numerator = p.alpha_abs * solar_irradiance_w_m2 * p.A_proj * p.F_view
        denominator = p.h_eff * p.A_surf
        return float(numerator / max(denominator, 1e-6))

    def effective_ambient(self, t_ambient_2m: float, solar_irradiance_w_m2: float) -> float:
        """T_a,eff = T_a(2m) + Delta T_solar"""
        return t_ambient_2m + self.calculate_solar_increment(solar_irradiance_w_m2)

    def steady_state_top_oil_rise(self, load_k: float, cooling_derate: float = 1.0) -> float:
        """
        theta_o,u(K) = (Delta theta_o,r / eta_cool) * ((1 + R * K^2) / (1 + R))^n
        """
        p = self.params
        effective_derate = max(cooling_derate, 0.1)
        base_rise = p.delta_theta_or / effective_derate
        loss_factor = (1.0 + p.R * (load_k ** 2)) / (1.0 + p.R)
        return float(base_rise * (loss_factor ** p.n))

    def steady_state_winding_rise(self, load_k: float) -> float:
        """
        theta_w,u(K) = Delta theta_w,r * K^(2m)
        """
        p = self.params
        return float(p.delta_theta_wr * (max(load_k, 0.0) ** (2.0 * p.m)))

    def step_discrete(
        self,
        theta_o_prev: float,
        theta_w_prev: float,
        t_ambient_2m: float,
        solar_irradiance_w_m2: float,
        load_k: float,
        dt_hours: float = 1.0,
        cooling_derate: float = 1.0,
    ) -> Tuple[float, float, float, float, float]:
        """
        Computes one exact discrete exponential step:
        theta_o,k+1 = theta_o,u + (theta_o,k - theta_o,u) * exp(-dt / tau_o)
        theta_w,k+1 = theta_w,u + (theta_w,k - theta_w,u) * exp(-dt / tau_w)
        T_o = T_a,eff + theta_o,k+1
        T_hs = T_o + theta_w,k+1

        Returns:
            (theta_o_next, theta_w_next, t_ambient_eff, t_top_oil, t_hot_spot)
        """
        p = self.params
        t_eff = self.effective_ambient(t_ambient_2m, solar_irradiance_w_m2)

        theta_ou = self.steady_state_top_oil_rise(load_k, cooling_derate)
        theta_wu = self.steady_state_winding_rise(load_k)

        # Exact exponential updates
        exp_o = math.exp(-dt_hours / max(p.tau_o, 1e-3))
        exp_w = math.exp(-dt_hours / max(p.tau_w, 1e-3))

        theta_o_next = theta_ou + (theta_o_prev - theta_ou) * exp_o
        theta_w_next = theta_wu + (theta_w_prev - theta_wu) * exp_w

        t_top_oil = t_eff + theta_o_next
        t_hot_spot = t_top_oil + theta_w_next

        return float(theta_o_next), float(theta_w_next), float(t_eff), float(t_top_oil), float(t_hot_spot)

    @staticmethod
    def arrhenius_aging_factor(t_hot_spot_c: float) -> float:
        """
        IEEE C57.91 / IEC 60076-7 Arrhenius insulation aging acceleration factor:
        V(T_hs) = exp(15000 / 383.15 - 15000 / (T_hs + 273.15))
        where 383.15 K = 110 °C reference temperature where V = 1.0.
        """
        t_kelvin = t_hot_spot_c + 273.15
        exponent = (15000.0 / 383.15) - (15000.0 / max(t_kelvin, 100.0))
        # Prevent numerical overflow on extreme anomalies
        clamped_exponent = min(max(exponent, -10.0), 10.0)
        return float(math.exp(clamped_exponent))

    def compute_thermal_soak_index(
        self,
        persistence_hours_p_theta: float,
        exceedance_degree_hours_h_theta: float,
        theta_scale: float = 10.0,
        lam: float = 0.5,
    ) -> float:
        """
        TSI_theta = (P_theta / tau_o) + lambda * (H_theta / (tau_o * theta_scale))
        """
        p = self.params
        tsi = (persistence_hours_p_theta / p.tau_o) + lam * (
            exceedance_degree_hours_h_theta / (p.tau_o * theta_scale)
        )
        return float(tsi)

    def simulate_trajectory(
        self,
        asset_id: str,
        hourly_forecast: List[Dict[str, Any]],
        load_k_series: Optional[List[float]] = None,
        initial_t_o: Optional[float] = None,
        initial_t_hs: Optional[float] = None,
        cooling_derate: float = 1.0,
        forced_cooling_active: bool = False,
        persistence_hours_p40: Optional[float] = None,
        exceedance_degree_hours_h40: Optional[float] = None,
    ) -> ThermalTrajectory:
        """
        Simulates the full 12-hour forward physical trajectory step-by-step.

        `persistence_hours_p40` / `exceedance_degree_hours_h40` come from the
        FortyGuard persistence & exceedance analytics. When omitted they fall
        back to the Phoenix July 2023 benchmark so offline replay is unchanged.
        """
        p = self.params
        steps: List[ThermalStepState] = []
        cumulative_loss_of_life = 0.0

        effective_derate = cooling_derate
        if forced_cooling_active:
            # Active auxiliary fans enhance convective heat dissipation
            effective_derate = min(effective_derate * 1.35, 1.25)

        # Initialize steady state from first hour if not provided
        first_hour = hourly_forecast[0]
        first_t_a = first_hour.get("fortyguard_2m_ambient_c", 35.0)
        first_solar = first_hour.get("solar_irradiance_w_m2", 100.0)
        first_k = (
            load_k_series[0]
            if (load_k_series and len(load_k_series) > 0)
            else first_hour.get("baseline_load_ratio_k", 0.70)
        )

        curr_theta_o = self.steady_state_top_oil_rise(first_k, effective_derate)
        curr_theta_w = self.steady_state_winding_rise(first_k)

        if initial_t_o is not None:
            curr_theta_o = initial_t_o - self.effective_ambient(first_t_a, first_solar)
        if initial_t_hs is not None and initial_t_o is not None:
            curr_theta_w = initial_t_hs - initial_t_o

        peak_t_o = -100.0
        peak_t_hs = -100.0
        peak_v = 0.0

        for i, hour_data in enumerate(hourly_forecast):
            t_a = hour_data.get("fortyguard_2m_ambient_c", 40.0)
            solar = hour_data.get("solar_irradiance_w_m2", 500.0)
            k = (
                load_k_series[i]
                if (load_k_series and i < len(load_k_series))
                else hour_data.get("baseline_load_ratio_k", 1.0)
            )
            timestamp = hour_data.get("timestamp", f"2023-07-24T{i+6:02d}:00:00Z")

            solar_inc = self.calculate_solar_increment(solar)
            curr_theta_o, curr_theta_w, t_eff, t_o, t_hs = self.step_discrete(
                theta_o_prev=curr_theta_o,
                theta_w_prev=curr_theta_w,
                t_ambient_2m=t_a,
                solar_irradiance_w_m2=solar,
                load_k=k,
                dt_hours=1.0,
                cooling_derate=effective_derate,
            )

            v_aging = self.arrhenius_aging_factor(t_hs)
            cumulative_loss_of_life += v_aging * 1.0  # 1 hour delta

            peak_t_o = max(peak_t_o, t_o)
            peak_t_hs = max(peak_t_hs, t_hs)
            peak_v = max(peak_v, v_aging)

            steps.append(
                ThermalStepState(
                    timestamp=timestamp,
                    hour_index=i,
                    t_ambient_2m_c=round(t_a, 2),
                    t_solar_increment_c=round(solar_inc, 2),
                    t_ambient_eff_c=round(t_eff, 2),
                    load_ratio_k=round(k, 3),
                    theta_o_c=round(curr_theta_o, 2),
                    theta_w_c=round(curr_theta_w, 2),
                    t_top_oil_c=round(t_o, 2),
                    t_hot_spot_c=round(t_hs, 2),
                    aging_acceleration_factor_v=round(v_aging, 3),
                    cumulative_loss_of_life_hours=round(cumulative_loss_of_life, 2),
                    cooling_derate_eta=round(effective_derate, 2),
                )
            )

        # Previously hardcoded to the Phoenix benchmark, which meant the soak
        # index ignored the live persistence layer entirely.
        # Defaults mirror the 2023-07-19 capture. They are a last resort:
        # every caller now forwards the measured values explicitly.
        p_40 = 12.0 if persistence_hours_p40 is None else float(persistence_hours_p40)
        h_40 = 17.48 if exceedance_degree_hours_h40 is None else float(exceedance_degree_hours_h40)
        tsi = self.compute_thermal_soak_index(p_40, h_40)
        rho_o = 1.0 - math.exp(-p_40 / p.tau_o)
        rho_w = 1.0 - math.exp(-p_40 / p.tau_w)

        return ThermalTrajectory(
            asset_id=asset_id,
            steps=steps,
            peak_top_oil_c=round(peak_t_o, 2),
            peak_hot_spot_c=round(peak_t_hs, 2),
            peak_aging_acceleration_v=round(peak_v, 2),
            total_loss_of_life_hours=round(cumulative_loss_of_life, 2),
            thermal_soak_index_tsi=round(tsi, 2),
            top_oil_response_ratio=round(rho_o, 3),
            winding_response_ratio=round(rho_w, 3),
            breached_hot_spot_ceiling=peak_t_hs >= p.t_hs_max_c,
            breached_top_oil_ceiling=peak_t_o >= p.t_o_max_c,
        )
