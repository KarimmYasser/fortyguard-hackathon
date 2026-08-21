"""
FastAPI Route for Advanced Mathematical Physics & Grid Reliability Suite
Exposes endpoints for:
1. Dynamic Line Rating & Catenary Sag (IEEE Std 738-2012)
2. BESS Coupled Electro-Thermal ODEs & Arrhenius SEI Capacity Fade
3. Arrhenius-Weibull Asset Fragility & Cascading Outage Probability
4. Chance-Constrained AC Optimal Power Flow (CC-OPF) with SOCP Bounds
"""

from __future__ import annotations

from typing import Dict, Any, List, Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field

from src.physics.dynamic_line_rating import DynamicLineRatingEngine, DLRSolution
from src.physics.bess_electro_thermal import BESSElectroThermalEngine, BESSThermalStepResult
from src.physics.weibull_hazard import ArrheniusWeibullHazardEngine, CascadingOutageRiskReport
from src.physics.chance_constrained_opf import ChanceConstrainedOPFEngine, CC_OPF_Request, CC_OPF_Solution
from src.db.database import db_manager
from src.db.models import DLRCatenaryRecord

router = APIRouter(prefix="/physics", tags=["Advanced Mathematical Moats"])


# --- 1. DLR Models & Endpoint ---
class DLRSolveRequest(BaseModel):
    current_amps: float = Field(default=820.0, ge=0.0, le=2000.0, description="Load current (Amps)")
    t_ambient_c: float = Field(default=47.6, ge=0.0, le=60.0, description="FortyGuard 2m ambient air (°C)")
    wind_speed_m_per_s: float = Field(default=1.2, ge=0.0, le=25.0, description="Perpendicular wind velocity (m/s)")
    wind_angle_deg: float = Field(default=90.0, ge=0.0, le=90.0, description="Wind incidence angle (deg)")
    solar_irradiance_w_per_m2: float = Field(default=950.0, ge=0.0, le=1400.0, description="Solar irradiance (W/m²)")


@router.post("/dlr-solve", response_model=DLRSolution)
async def solve_dynamic_line_rating(req: DLRSolveRequest) -> DLRSolution:
    """
    Evaluates IEEE Std 738-2012 Dynamic Line Rating, ampacity headroom, and catenary sag, logging to database.
    """
    engine = DynamicLineRatingEngine()
    sol = engine.evaluate_line(
        current_amps=req.current_amps,
        t_ambient_c=req.t_ambient_c,
        wind_speed_m_per_s=req.wind_speed_m_per_s,
        wind_angle_deg=req.wind_angle_deg,
        solar_irradiance_w_per_m2=req.solar_irradiance_w_per_m2,
    )

    try:
        record = DLRCatenaryRecord(
            line_id="FEEDER-LINE-PHX-01",
            ambient_c=req.t_ambient_c,
            wind_speed_ms=req.wind_speed_m_per_s,
            conductor_temp_c=sol.conductor_temp_c,
            dynamic_ampacity_a=sol.dynamic_ampacity_amps,
            ampacity_headroom_pct=sol.ampacity_headroom_pct,
            catenary_sag_m=sol.catenary_sag_m,
            clearance_margin_m=sol.ground_clearance_margin_m,
        )
        await db_manager.log_dlr_telemetry(record)
    except Exception:
        pass

    return sol



# --- 2. BESS Electro-Thermal Endpoint ---
class BESSSimulateRequest(BaseModel):
    ambient_temps_c: Optional[List[float]] = None
    dispatch_powers_mw: Optional[List[float]] = None
    initial_soc: float = Field(default=0.85, ge=0.0, le=1.0)
    initial_core_temp_c: float = Field(default=35.0, ge=10.0, le=60.0)


@router.post("/bess-thermal", response_model=List[BESSThermalStepResult])
async def simulate_bess_thermal_trajectory(req: BESSSimulateRequest) -> List[BESSThermalStepResult]:
    """
    Simulates coupled 2-state core/surface thermal ODEs and continuous SEI capacity degradation.
    """
    engine = BESSElectroThermalEngine()
    ambient_temps = req.ambient_temps_c or [38.2, 40.5, 43.1, 45.8, 47.6, 46.9, 45.2, 43.0, 40.8, 39.0, 37.5, 36.0]
    dispatch_powers = req.dispatch_powers_mw or [2.0, 4.0, 6.5, 8.0, 7.5, 6.0, 4.5, 3.0, 2.0, 1.0, 0.0, 0.0]

    results = engine.simulate_dispatch_trajectory(
        ambient_temps_c=ambient_temps,
        dispatch_powers_mw=dispatch_powers,
        initial_soc=req.initial_soc,
        initial_core_temp_c=req.initial_core_temp_c,
    )

    # Persist BESS telemetry steps
    try:
        from src.db.models import BESSDegradationRecord
        for r in results:
            rec = BESSDegradationRecord(
                bess_id="BESS-PHX-CENTRAL-01",
                hour_step=r.hour_step,
                ambient_c=r.ambient_temp_c,
                dispatch_power_mw=r.dispatch_power_mw,
                core_temp_c=r.core_temp_c,
                surface_temp_c=r.surface_temp_c,
                soc_pct=r.soc_pct,
                soh_pct=r.soh_pct,
                degradation_cost_usd=r.degradation_cost_usd,
            )
            await db_manager.log_bess_degradation(rec)
    except Exception:
        pass

    return results


# --- 3. Arrhenius-Weibull Cascading Risk Endpoint ---
@router.get("/cascading-hazard", response_model=CascadingOutageRiskReport)
async def get_grid_cascading_hazard(is_mitigated: bool = False) -> CascadingOutageRiskReport:
    """
    Computes time-dependent Poisson-Weibull hazard rates and grid-wide cascading blackout probability.
    """
    engine = ArrheniusWeibullHazardEngine()
    if is_mitigated:
        tx_traj = [92.0, 102.0, 114.0, 126.0, 136.8, 134.0, 125.0, 115.0, 104.0, 95.0, 88.0, 82.0]
        cable_traj = [65.0, 70.0, 76.0, 82.0, 86.0, 84.0, 80.0, 75.0, 70.0, 66.0, 62.0, 58.0]
        line_traj = [52.0, 58.0, 64.0, 70.0, 73.5, 71.0, 66.0, 60.0, 55.0, 50.0, 46.0, 42.0]
        ambient_peak = 47.6
    else:
        tx_traj = [98.0, 110.0, 124.0, 138.0, 151.2, 148.0, 137.0, 126.0, 115.0, 105.0, 96.0, 89.0]
        cable_traj = [70.0, 78.0, 88.0, 98.0, 106.0, 102.0, 94.0, 86.0, 79.0, 73.0, 68.0, 63.0]
        line_traj = [56.0, 64.0, 72.0, 81.0, 86.4, 83.0, 76.0, 68.0, 61.0, 55.0, 50.0, 45.0]
        ambient_peak = 47.6

    report = engine.evaluate_grid_cascading_risk(
        transformer_temp_trajectory=tx_traj,
        cable_temp_trajectory=cable_traj,
        line_temp_trajectory=line_traj,
        is_mitigated=is_mitigated,
        ambient_peak_c=ambient_peak,
    )

    # Persist Cascading Risk Snapshot
    try:
        import uuid
        from src.db.models import CascadingRiskRecord
        snap = CascadingRiskRecord(
            snapshot_id=f"RISK-{uuid.uuid4().hex[:8].upper()}",
            heatwave_severity=report.heatwave_severity,
            n1_reserve_margin_mw=report.n_1_reserve_margin_mw,
            n1_compliant=report.n_1_security_compliant,
            cascade_outage_probability=report.system_cascading_blackout_prob_pct / 100.0,
            expected_unserved_energy_mwh=report.expected_unserved_energy_mwh,
            total_voll_risk_usd=report.total_voll_financial_risk_usd,
        )
        await db_manager.save_cascading_risk_snapshot(snap)
    except Exception:
        pass

    return report


# --- 4. Chance-Constrained OPF Endpoint ---
@router.post("/cc-opf-solve", response_model=CC_OPF_Solution)
async def solve_chance_constrained_opf(req: CC_OPF_Request) -> CC_OPF_Solution:
    """
    Solves Chance-Constrained Second-Order Cone AC-OPF with Gaussian forecast variance quantile bounds.
    """
    import time
    engine = ChanceConstrainedOPFEngine()
    solution = engine.solve_cc_opf(req)

    # Persist CC-OPF solution
    try:
        from src.db.models import ChanceConstrainedOPFRecord
        opf_rec = ChanceConstrainedOPFRecord(
            solve_id=f"cc_opf_{int(time.time())}",
            confidence_level_pct=solution.confidence_level_pct,
            total_generation_mw=req.total_grid_load_mw,
            bess_optimal_power_mw=solution.optimal_bess_active_mw,
            oltc_optimal_tap=solution.optimal_oltc_tap_step,
            total_dispatch_cost_usd=solution.objective_cost_usd_per_hr,
            solver_status=solution.robustness_status,
        )
        db_manager.save_chance_constrained_opf_log(opf_rec)
    except Exception:
        pass

    return solution
