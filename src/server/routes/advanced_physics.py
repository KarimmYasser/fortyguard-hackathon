"""
FastAPI Route for Advanced Mathematical Physics & Grid Reliability Suite
Exposes endpoints for:
1. Dynamic Line Rating & Catenary Sag (IEEE Std 738-2012)
2. BESS Coupled Electro-Thermal ODEs & Arrhenius SEI Capacity Fade
3. Arrhenius-Weibull Scenario Fragility & Cascading-Risk Score
4. Analytical uncertainty-bounded dispatch screening
"""

from __future__ import annotations

import logging

from typing import Dict, Any, List, Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field

from src.physics.dynamic_line_rating import DynamicLineRatingEngine, DLRSolution
from src.physics.bess_electro_thermal import BESSElectroThermalEngine, BESSThermalStepResult
from src.physics.weibull_hazard import ArrheniusWeibullHazardEngine, CascadingOutageRiskReport
from src.physics.chance_constrained_opf import ChanceConstrainedOPFEngine, CC_OPF_Request, CC_OPF_Solution
from src.db.database import db_manager
from src.db.models import DLRCatenaryRecord

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/physics", tags=["Advanced Mathematical Moats"])


# --- 1. DLR Models & Endpoint ---
class DLRSolveRequest(BaseModel):
    current_amps: float = Field(default=820.0, ge=0.0, le=2000.0, description="Load current (Amps)")
    t_ambient_c: float = Field(default=42.7, ge=0.0, le=60.0, description="FortyGuard 2m ambient air (°C), measured benchmark peak")
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
            dynamic_ampacity_a=sol.max_dynamic_ampacity_amps,
            ampacity_headroom_pct=sol.capacity_margin_pct,
            catenary_sag_m=sol.catenary_sag_m,
            clearance_margin_m=round(
                sol.ground_clearance_m - engine.spec.min_ground_clearance_m, 2
            ),
        )
        await db_manager.log_dlr_telemetry(record)
    except Exception as exc:
        logger.warning("Failed to persist DLR telemetry: %s", exc, exc_info=True)

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
    # Measured FortyGuard 2m curve, downtown Phoenix AOI, 2023-07-19 06:00-17:00.
    ambient_temps = req.ambient_temps_c or [36.1, 37.34, 38.64, 39.49, 40.58, 41.53, 42.15, 42.46, 42.72, 42.74, 42.69, 42.61]
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
        # BESSThermalStepResult exposes time_minutes / discharge_power_mw /
        # state_of_charge_pct / state_of_health_pct / hourly_degradation_cost_usd.
        # Five of the nine fields here read names that never existed, so this
        # write raised on the first attribute and no BESS row was ever stored.
        for idx, r in enumerate(results):
            rec = BESSDegradationRecord(
                bess_id="BESS-PHX-CENTRAL-01",
                hour_step=idx,
                ambient_c=r.ambient_temp_c,
                dispatch_power_mw=r.discharge_power_mw,
                core_temp_c=r.core_temp_c,
                surface_temp_c=r.surface_temp_c,
                soc_pct=r.state_of_charge_pct,
                soh_pct=r.state_of_health_pct,
                degradation_cost_usd=r.hourly_degradation_cost_usd,
            )
            await db_manager.log_bess_degradation(rec)
    except Exception as exc:
        logger.warning("Failed to persist BESS degradation log: %s", exc, exc_info=True)

    return results


# --- 3. Arrhenius-Weibull Cascading Risk Endpoint ---
@router.get("/cascading-hazard", response_model=CascadingOutageRiskReport)
async def get_grid_cascading_hazard(is_mitigated: bool = False) -> CascadingOutageRiskReport:
    """
    Computes an uncalibrated Poisson-Weibull scenario risk score for the demo feeder.
    """
    engine = ArrheniusWeibullHazardEngine()
    if is_mitigated:
        tx_traj = [94.0, 102.0, 110.0, 118.0, 126.0, 132.0, 136.0, 134.0, 130.0, 122.0, 114.0, 106.0]
        cable_traj = [65.0, 70.0, 76.0, 82.0, 86.0, 84.0, 80.0, 75.0, 70.0, 66.0, 62.0, 58.0]
        line_traj = [52.0, 58.0, 64.0, 70.0, 73.5, 71.0, 66.0, 60.0, 55.0, 50.0, 46.0, 42.0]
        ambient_peak = 42.74
    else:
        tx_traj = [98.0, 110.0, 124.0, 138.0, 151.2, 158.0, 163.0, 159.5, 154.0, 145.0, 132.0, 118.0]
        cable_traj = [70.0, 78.0, 88.0, 98.0, 106.0, 102.0, 94.0, 86.0, 79.0, 73.0, 68.0, 63.0]
        line_traj = [56.0, 64.0, 72.0, 81.0, 86.4, 83.0, 76.0, 68.0, 61.0, 55.0, 50.0, 45.0]
        ambient_peak = 42.74

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
            heatwave_severity=(
                "CRITICAL" if report.system_cascading_risk_pct > 12.0
                else "ELEVATED" if report.system_cascading_risk_pct > 4.0
                else "LOW"
            ),
            # The risk model exposes a percentage reserve margin; retain that
            # value in the legacy database column rather than fabricating MW.
            n1_reserve_margin_mw=report.n_minus_1_reserve_margin_pct,
            n1_compliant=report.n_minus_1_reserve_margin_pct >= 10.0,
            cascade_outage_probability=report.system_cascading_risk_pct / 100.0,
            expected_unserved_energy_mwh=report.expected_unserved_energy_mwh,
            total_voll_risk_usd=report.economic_loss_risk_usd,
        )
        await db_manager.save_cascading_risk_snapshot(snap)
    except Exception as exc:
        logger.warning("Failed to persist cascading risk snapshot: %s", exc, exc_info=True)

    return report


# --- 4. Chance-Constrained OPF Endpoint ---
@router.post("/cc-opf-solve", response_model=CC_OPF_Solution)
async def solve_chance_constrained_opf(req: CC_OPF_Request) -> CC_OPF_Solution:
    """
    Runs an analytical uncertainty-bounded dispatch screen with Gaussian quantile bounds.
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
        await db_manager.log_chance_constrained_opf(opf_rec)
    except Exception as exc:
        logger.warning("Failed to persist chance-constrained OPF log: %s", exc, exc_info=True)

    return solution


# --- 5. Human Thermal Comfort & Mean Radiant Temperature (MRT) Endpoints ---
@router.post("/human-comfort")
async def evaluate_human_comfort(req: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes Mean Radiant Temperature (MRT), Universal Thermal Climate Index (UTCI),
    and safe outdoor exertion limits.
    """
    from src.physics.human_comfort import HumanComfortEngine, MicroclimateInput

    engine = HumanComfortEngine()
    inp = MicroclimateInput(**req)
    metrics = engine.evaluate_comfort(inp)
    return {
        "status": "success",
        "inputs": inp.model_dump(),
        "comfort_metrics": metrics.model_dump(),
    }


@router.post("/shading-simulation")
async def simulate_shading_and_albedo_retrofit(
    req: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Simulates urban tree canopy, transit shade sails, and cool pavement albedo retrofits.
    Demonstrates that while 2m dry-bulb air temperature drops marginally (-0.35°C),
    Mean Radiant Temperature (MRT) drops by 15-22°C and UTCI drops by 5-8°C.
    """
    from src.physics.human_comfort import HumanComfortEngine, MicroclimateInput

    engine = HumanComfortEngine()
    req = req or {}
    baseline_data = req.get("baseline", {
        "fortyguard_2m_ambient_c": 41.5,
        "relative_humidity_pct": 25.0,
        "wind_speed_2m_m_s": 1.5,
        "solar_irradiance_w_m2": 850.0,
        "surface_albedo": 0.15,
        "tree_canopy_cover_pct": 8.0,
        "artificial_shade_fraction": 0.0,
        "canyon_height_to_width_hw": 1.4,
    })
    baseline = MicroclimateInput(**baseline_data)
    added_canopy = req.get("added_canopy_pct", 30.0)
    added_shade = req.get("added_shade_fraction", 0.50)
    cool_albedo = req.get("cool_pavement_albedo", 0.45)

    comp = engine.simulate_cooling_intervention(
        baseline=baseline,
        added_canopy_pct=added_canopy,
        added_shade_fraction=added_shade,
        cool_pavement_albedo=cool_albedo,
    )

    return {
        "status": "success",
        "simulation": comp.model_dump(),
    }


