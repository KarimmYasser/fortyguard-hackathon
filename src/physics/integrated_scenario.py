"""Integrated scenario evaluation over one shared environmental/load timeline.

This module couples the previously standalone BESS, feeder, overhead-line and
reliability engines to the same baseline/mitigated transformer trajectories.
It remains a demonstration feeder, not utility SCADA or a digital-twin claim.
"""

from __future__ import annotations

from typing import Any, Dict, List

from src.physics.bess_electro_thermal import BESSElectroThermalEngine
from src.physics.dynamic_line_rating import DynamicLineRatingEngine
from src.physics.power_flow import DistributionPowerFlowEngine
from src.physics.weibull_hazard import ArrheniusWeibullHazardEngine


def evaluate_integrated_scenario(
    *,
    forecast: List[Dict[str, Any]],
    baseline_hotspots_c: List[float],
    mitigated_hotspots_c: List[float],
    baseline_loads_k: List[float],
    mitigated_loads_k: List[float],
    transformer_rating_mva: float = 25.0,
    soil_resistivity_rho: float = 1.0,
) -> Dict[str, Any]:
    """Evaluate all advanced engines from the same indexed scenario inputs."""
    if not forecast:
        return {"status": "not_evaluated", "reason": "empty forecast"}

    n = min(len(forecast), len(baseline_hotspots_c), len(mitigated_hotspots_c), len(baseline_loads_k), len(mitigated_loads_k))
    ambients = [float(forecast[i].get("fortyguard_2m_ambient_c", 25.0)) for i in range(n)]
    dispatch_mw = [max(0.0, (baseline_loads_k[i] - mitigated_loads_k[i]) * transformer_rating_mva) for i in range(n)]

    bess = BESSElectroThermalEngine().simulate_dispatch_trajectory(
        ambient_temps_c=ambients,
        dispatch_powers_mw=dispatch_mw,
        initial_soc=0.85,
    )

    peak_i = max(range(n), key=lambda i: baseline_loads_k[i])
    baseline_pf = DistributionPowerFlowEngine(oltc_tap=4).solve_power_flow(
        tx_load_multiplier_k=baseline_loads_k[peak_i],
        soil_resistivity_rho=soil_resistivity_rho,
    )
    mitigated_pf = DistributionPowerFlowEngine(oltc_tap=4).solve_power_flow(
        tx_load_multiplier_k=baseline_loads_k[peak_i],
        bess_discharge_mw=dispatch_mw[peak_i],
        bess_volt_var_q_mvar=min(4.0, dispatch_mw[peak_i] * 0.5),
        soil_resistivity_rho=soil_resistivity_rho,
    )

    line_current = baseline_pf.branches[-1].branch_current_amps
    peak_weather = forecast[peak_i]
    dlr = DynamicLineRatingEngine().evaluate_line(
        current_amps=line_current,
        t_ambient_c=ambients[peak_i],
        wind_speed_m_per_s=float(peak_weather.get("wind_speed_m_s") or 1.2),
        solar_irradiance_w_per_m2=float(peak_weather.get("solar_irradiance_w_m2") or 0.0),
    )

    # Cable and line trajectories use the shared timeline and transparent
    # engineering approximations; they are not measurements.
    cable_baseline = [min(105.0, 35.0 + 30.0 * k * k + 4.0 * (soil_resistivity_rho - 0.9)) for k in baseline_loads_k[:n]]
    cable_mitigated = [min(105.0, 35.0 + 30.0 * k * k + 4.0 * (soil_resistivity_rho - 0.9)) for k in mitigated_loads_k[:n]]
    line_baseline = [dlr.conductor_temp_c] * n
    line_mitigated = [max(ambients[i], dlr.conductor_temp_c - 8.0 * max(baseline_loads_k[i] - mitigated_loads_k[i], 0.0)) for i in range(n)]
    hazard = ArrheniusWeibullHazardEngine()
    base_risk = hazard.evaluate_grid_cascading_risk(
        transformer_temp_trajectory=baseline_hotspots_c[:n],
        cable_temp_trajectory=cable_baseline,
        line_temp_trajectory=line_baseline,
        ambient_peak_c=max(ambients),
    )
    mitigated_risk = hazard.evaluate_grid_cascading_risk(
        transformer_temp_trajectory=mitigated_hotspots_c[:n],
        cable_temp_trajectory=cable_mitigated,
        line_temp_trajectory=line_mitigated,
        is_mitigated=True,
        ambient_peak_c=max(ambients),
    )

    return {
        "status": "modelled_demo_feeder",
        "timeline_hours": n,
        "bess": {
            "peak_core_temp_c": max(x.core_temp_c for x in bess),
            "minimum_soc_pct": min(x.state_of_charge_pct for x in bess),
            "cumulative_capacity_loss_pct": bess[-1].cumulative_capacity_loss_pct,
            "dispatch_mw": [round(x, 3) for x in dispatch_mw],
        },
        "power_flow_peak_hour": {
            "hour_index": peak_i,
            "baseline": baseline_pf.model_dump(),
            "mitigated": mitigated_pf.model_dump(),
        },
        "overhead_line_peak_hour": dlr.model_dump(),
        "reliability": {
            "status": "uncalibrated_scenario_risk",
            "baseline": base_risk.model_dump(),
            "mitigated": mitigated_risk.model_dump(),
        },
    }
