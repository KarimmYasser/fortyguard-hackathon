"""
Physics State Estimation Node
Executes IEEE C57.91 / IEC 60076-7 baseline thermal simulation, soil dryout,
urban canyon cooling derating, and virtual paper-oil moisture tracking.
"""

from __future__ import annotations

import time
from typing import Any, Dict
from src.agent.state import ThermalSentinelState
from src.models.asset import RiskLevel
from src.physics.transformer_thermal import TransformerThermalEngine
from src.physics.soil_cable import SoilCableEngine
from src.physics.urban_canyon import UrbanCanyonEngine
from src.physics.virtual_moisture import VirtualMoistureEngine


async def physics_node(state: ThermalSentinelState) -> Dict[str, Any]:
    """
    Computes 4 unmonitored physical states across the 12-hour horizon.
    """
    asset_id = state.get("asset_id", "SUB-PHX-DOWNTOWN-04")
    forecast = state.get("fortyguard_forecast", [])
    persist = state.get("persistence_metrics", {})

    thermal_engine = TransformerThermalEngine()
    soil_engine = SoilCableEngine()
    canyon_engine = UrbanCanyonEngine()
    moisture_engine = VirtualMoistureEngine()

    # 1. Urban Canyon Cooling Derate
    canyon_res = canyon_engine.calculate_cooling_derate_factor(
        fortyguard_2m_ambient_c=forecast[7].get("fortyguard_2m_ambient_c", 47.6),
        reference_wind_speed_m_s=3.0,
    )
    eta_cool = canyon_res.get("cooling_derate_eta_cool", 0.68)

    # 2. Transformer Thermal Trajectory (Baseline without mitigation)
    baseline_traj = thermal_engine.simulate_trajectory(
        asset_id=asset_id,
        hourly_forecast=forecast,
        cooling_derate=eta_cool,
        forced_cooling_active=False,
    )

    # 3. Underground Cable - Soil Dryout State
    soil_res = soil_engine.evaluate_compound_site_margin(
        consecutive_heatwave_days=persist.get("consecutive_heatwave_days", 24),
        initial_moisture=0.18,
        cable_load_k=forecast[7].get("baseline_load_ratio_k", 1.18),
        transformer_top_oil_c=baseline_traj.peak_top_oil_c,
        transformer_hot_spot_c=baseline_traj.peak_hot_spot_c,
    )

    # 4. Virtual Moisture Migration State
    moisture_res = moisture_engine.step_moisture_migration(
        paper_moisture_pct=2.5,
        oil_moisture_ppm=16.0,
        t_hot_spot_c=baseline_traj.peak_hot_spot_c,
        t_oil_c=baseline_traj.peak_top_oil_c,
        dt_hours=1.0,
    )

    # Risk level classification
    if baseline_traj.peak_hot_spot_c >= 140.0:
        risk = RiskLevel.CRITICAL.value
    elif baseline_traj.peak_hot_spot_c >= 120.0 or moisture_res.get("dielectric_alarm"):
        risk = RiskLevel.ELEVATED.value
    else:
        risk = RiskLevel.SAFE.value

    audit_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime()),
        "node": "physics_node",
        "message": f"Physics State Computed: Baseline Hot-Spot {baseline_traj.peak_hot_spot_c}°C, Top-Oil {baseline_traj.peak_top_oil_c}°C, Aging Acceleration {baseline_traj.peak_aging_acceleration_v}x, Soil Resistivity {soil_res['soil_thermal_resistivity_rho_soil']} K·m/W, Canyon Cooling Derate {eta_cool}",
    }

    audit_trail = list(state.get("audit_trail", []))
    audit_trail.append(audit_entry)

    return {
        "urban_canyon_metrics": canyon_res,
        "soil_cable_metrics": soil_res,
        "virtual_moisture_state": moisture_res,
        "baseline_trajectory": baseline_traj.model_dump(),
        "risk_level": risk,
        "audit_trail": audit_trail,
        "current_node": "physics_node",
    }
