"""
FastAPI Route for Live What-If Stress Studio (Interactive Physics Sandbox)
Allows judges & operators to dynamically modulate boundary conditions, multi-day persistence,
BESS capacity, and asset ratings, recalculating IEEE C57.91 and bounded model trajectories.
"""

from __future__ import annotations

import hashlib
import json
import logging

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.models.thermal import TransformerThermalParams
from src.models.provenance import canonical_provenance
from src.physics.transformer_thermal import TransformerThermalEngine
from src.physics.soil_cable import SoilCableEngine
from src.physics.urban_canyon import UrbanCanyonEngine, UrbanCanyonParameters
from src.physics.virtual_moisture import VirtualMoistureEngine
from src.physics.economic_model import EconomicEngine
from src.physics.integrated_scenario import evaluate_integrated_scenario
from src.physics.sensitivity import transformer_sensitivity_envelope
from src.safety.cbf_gate import CBFSafetyGate, ActionType, MitigationAction
from src.db.database import db_manager
from datetime import datetime, timezone

from src.db.models import ApiCallCacheRecord, SimulationRunRecord

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sandbox", tags=["What-If Stress Studio"])



class SandboxSimulationRequest(BaseModel):
    """Dynamic inputs for the what-if sandbox simulation."""
    intra_aoi_spread_c: float = Field(default=1.1, ge=0.0, le=8.0, description="Measured 2m spread across the AOI, hottest tile minus coolest (°C)")
    heatwave_day: int = Field(default=24, ge=1, le=31, description="Compounding heatwave day (soil dryout progression)")
    transformer_mva: float = Field(default=25.0, ge=10.0, le=100.0, description="Transformer nameplate rating (MVA)")
    bess_capacity_mwh: float = Field(default=25.0, ge=0.0, le=100.0, description="Available utility BESS capacity (MWh)")
    canyon_aspect_ratio: float = Field(default=1.85, ge=0.2, le=4.0, description="Building canyon height-to-width ratio (H/W)")
    forced_cooling_enabled: bool = Field(default=True, description="Whether active auxiliary cooling pumps are available")

    # Optional live-scan binding. Supply these to run the same physics against a
    # freshly scanned location instead of the frozen Phoenix benchmark curve.
    latitude: Optional[float] = Field(default=None, ge=-90.0, le=90.0, description="Run against a live 2m scan at this latitude")
    longitude: Optional[float] = Field(default=None, ge=-180.0, le=180.0, description="Run against a live 2m scan at this longitude")
    analysis_date: Optional[str] = Field(default=None, description="YYYY-MM-DD for the live scan; defaults to the benchmark date")
    city: Optional[str] = Field(default=None, description="Label recorded with the simulation run")
    hourly_forecast: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Pre-computed 12h hourly forecast from live scan to bypass redundant network refetching",
    )
    persistence_metrics: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Pre-computed persistence & exceedance metrics from live scan",
    )


def _simulation_cache_key(req: SandboxSimulationRequest) -> str:
    """
    Deterministic identity for a solve. The physics is a pure function of these
    inputs, so the same inputs must resolve to the same stored result forever
    rather than being recomputed and discarded.
    """
    payload = json.dumps(req.model_dump(), sort_keys=True, separators=(",", ":"))
    return "sim:" + hashlib.sha256(payload.encode()).hexdigest()[:40]


@router.post("/simulate")
async def run_sandbox_simulation(req: SandboxSimulationRequest) -> Dict[str, Any]:
    """
    Executes multi-physics simulation and deterministic safety preflight under customized parameters.

    Results are content-addressed and persisted, so re-opening the same stored
    scan returns the solved trajectory it produced before instead of paying for
    the FortyGuard hours and the solve again.
    """
    cache_key = _simulation_cache_key(req)
    cached = await db_manager.get_cached_api_call(cache_key)
    if isinstance(cached, dict) and cached.get("timeline_steps"):
        cached = dict(cached)
        cached["cache"] = {
            "hit": True,
            "key": cache_key,
            "stored_at": cached.get("cache", {}).get("stored_at"),
            "note": "Replayed from the persisted solve; inputs are identical.",
        }
        return cached
    # Coolest-tile and solar series from the 2023-07-19 capture. These were
    # invented curves peaking at 43.1 C / 980 W/m^2, which no longer matched
    # anything the API returns.
    coolest_tile_temps = [
        35.91, 37.05, 38.29, 39.13, 40.18, 41.09, 41.68, 41.98, 42.24, 42.26, 42.21, 42.13
    ]
    solar_fluxes = [
        110.5, 325.0, 520.6, 686.0, 811.5, 889.8, 882.1, 823.1, 665.4, 577.9, 477.7, 320.1
    ]
    time_labels = [
        "06:00 AM", "07:00 AM", "08:00 AM", "09:00 AM",
        "10:00 AM", "11:00 AM", "12:00 PM", "01:00 PM",
        "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM",
    ]

    # When coordinates or pre-supplied forecast are supplied, replace the benchmark curve
    # with a real 2m profile for that location and date. Same solver, same gate, same economics
    # - only the measured inputs change, which is what makes the study portable
    # off Phoenix.
    scan_binding: Dict[str, Any] = {"mode": "benchmark_replay", "city": "Phoenix, AZ"}
    spread_c = req.intra_aoi_spread_c
    usable: List[Dict[str, Any]] = []

    if req.hourly_forecast is not None:
        usable = [h for h in req.hourly_forecast if h.get("fortyguard_2m_ambient_c") is not None]
        if len(usable) < 2:
            raise HTTPException(
                status_code=502,
                detail=(
                    "Pre-supplied 2m profile had fewer than 2 valid hours, so the "
                    "simulation was not run."
                ),
            )
        coolest_tile_temps = [h.get("coolest_tile_2m_c", h["fortyguard_2m_ambient_c"]) for h in usable]
        solar_fluxes = [h.get("solar_irradiance_w_m2") or 0.0 for h in usable]
        time_labels = [h.get("time_label", f"H{h.get('hour_index', i)}") for i, h in enumerate(usable)]
        peak = max(usable, key=lambda h: h["fortyguard_2m_ambient_c"])
        spread_c = peak.get("intra_aoi_spread_c")
        if spread_c is None:
            spread_c = round(peak["fortyguard_2m_ambient_c"] - peak.get("coolest_tile_2m_c", peak["fortyguard_2m_ambient_c"]), 3)

        live_persistence = req.persistence_metrics or {}
        analysis_date = req.analysis_date or (usable[0].get("timestamp", "").split("T")[0] if usable else None)
        city_label = req.city or (f"{req.latitude:.4f}, {req.longitude:.4f}" if req.latitude is not None and req.longitude is not None else "Scanned AOI")

        scan_binding = {
            "mode": "live_scan",
            "city": city_label,
            "latitude": req.latitude,
            "longitude": req.longitude,
            "analysis_date": analysis_date,
            "n_hours": len(usable),
            "peak_2m_ambient_c": round(peak["fortyguard_2m_ambient_c"], 2),
            "measured_intra_aoi_spread_c": spread_c,
            "data_source": usable[0].get("data_source") or (req.persistence_metrics or {}).get("data_source", "fortyguard_live"),
            "scenario_metadata_patch": {
                "location": {
                    "city": city_label,
                    "substation_name": f"Generic {req.transformer_mva:.0f} MVA asset model (unregistered site)",
                    "latitude": req.latitude,
                    "longitude": req.longitude,
                },
                "date_range": {"start_date": analysis_date},
                "persistence_metrics": live_persistence or None,
            },
        }
    elif req.latitude is not None and req.longitude is not None:
        from src.api.fortyguard_client import AsyncFortyGuardClient

        client = AsyncFortyGuardClient()
        live = await client.get_12h_forecast(
            latitude=req.latitude,
            longitude=req.longitude,
            start_time=req.analysis_date,
        )
        usable = [h for h in (live or []) if h.get("fortyguard_2m_ambient_c") is not None]
        if len(usable) < 2:
            raise HTTPException(
                status_code=502,
                detail=(
                    "Live 2m profile unavailable for that location/date, so the "
                    "simulation was not run. Refusing to silently fall back to the "
                    "Phoenix benchmark curve and report it as your scan."
                ),
            )
        coolest_tile_temps = [h.get("coolest_tile_2m_c", h["fortyguard_2m_ambient_c"]) for h in usable]
        solar_fluxes = [h.get("solar_irradiance_w_m2") or 0.0 for h in usable]
        time_labels = [h.get("time_label", f"H{h.get('hour_index', i)}") for i, h in enumerate(usable)]
        # Use the measured spread rather than the slider default.
        peak = max(usable, key=lambda h: h["fortyguard_2m_ambient_c"])
        spread_c = peak.get("intra_aoi_spread_c")
        if spread_c is None:
            spread_c = round(peak["fortyguard_2m_ambient_c"] - peak.get("coolest_tile_2m_c", peak["fortyguard_2m_ambient_c"]), 3)
        # Persistence for the scanned location. Without this the dashboard kept
        # showing the Phoenix P40 / TSI beside the scanned city's ambient curve.
        live_persistence = {}
        try:
            live_persistence = await client.get_persistence_and_exceedance(
                latitude=req.latitude,
                longitude=req.longitude,
                threshold_c=40.0,
                start_date=req.analysis_date,
                hourly_forecast=usable,
            )
        except Exception as exc:
            logger.warning("Live persistence unavailable for scan binding: %s", exc, exc_info=True)

        scan_binding = {
            "mode": "live_scan",
            "city": req.city or f"{req.latitude:.4f}, {req.longitude:.4f}",
            "latitude": req.latitude,
            "longitude": req.longitude,
            "analysis_date": req.analysis_date,
            "n_hours": len(usable),
            "peak_2m_ambient_c": round(peak["fortyguard_2m_ambient_c"], 2),
            "measured_intra_aoi_spread_c": spread_c,
            "data_source": usable[0].get("data_source"),
        }
        # Patched onto the dashboard's scenario metadata so the header, date and
        # persistence row track the scan instead of the benchmark.
        scan_binding["scenario_metadata_patch"] = {
            "location": {
                "city": req.city or f"{req.latitude:.4f}, {req.longitude:.4f}",
                # There is no asset registry entry for an arbitrary scan, so name
                # the modelled asset rather than keeping the Phoenix substation.
                "substation_name": f"Generic {req.transformer_mva:.0f} MVA asset model (unregistered site)",
                "latitude": req.latitude,
                "longitude": req.longitude,
            },
            "date_range": {"start_date": req.analysis_date},
            "persistence_metrics": live_persistence or None,
        }

    # 1. Physical parameters scaled to user MVA
    tx_params = TransformerThermalParams(
        rated_mva=req.transformer_mva,
        tau_o=2.8 * (req.transformer_mva / 25.0) ** 0.35,
        tau_w=0.10,
    )
    thermal_solver = TransformerThermalEngine(tx_params)
    soil_engine = SoilCableEngine()
    canyon_engine = UrbanCanyonEngine(
        UrbanCanyonParameters(height_to_width_ratio_hw=req.canyon_aspect_ratio)
    )
    moisture_engine = VirtualMoistureEngine()
    economic_engine = EconomicEngine()
    safety_gate = CBFSafetyGate(thermal_params=tx_params)

    # 2. Canyon Aerodynamics
    canyon_res = canyon_engine.calculate_cooling_derate_factor(
        fortyguard_2m_ambient_c=max(coolest_tile_temps) + spread_c,
        solar_irradiance_w_m2=max(solar_fluxes),
    )
    eta_cool = canyon_res["cooling_derate_eta_cool"]

    # 3. Build Forecast Stream with user's microclimate delta
    forecast_dicts: List[Dict[str, Any]] = []
    for idx, (time_lbl, t_air, s_w) in enumerate(zip(time_labels, coolest_tile_temps, solar_fluxes)):
        hour_of_day = 6 + idx
        t_2m = t_air + spread_c
        source_row = usable[idx] if idx < len(usable) else {}
        forecast_dicts.append(
            {
                "hour_index": idx,
                "time_label": time_lbl,
                "timestamp": source_row.get("timestamp") or f"2023-07-19T{hour_of_day:02d}:00:00-07:00",
                "fortyguard_2m_ambient_c": t_2m,
                "solar_irradiance_w_m2": s_w,
            }
        )

    # 3b. Persistence / exceedance measured off the constructed curve.
    threshold_c = 40.0
    hours_above = [
        f["fortyguard_2m_ambient_c"] for f in forecast_dicts
        if f["fortyguard_2m_ambient_c"] > threshold_c
    ]
    sandbox_p40 = float(len(hours_above))
    sandbox_h40 = round(sum(v - threshold_c for v in hours_above), 2)
    # Same TSI definition the thermal engine and the API client use.
    sandbox_tsi = round((sandbox_p40 / 3.5) + 0.5 * (sandbox_h40 / (3.5 * 10.0)), 2)

    # 4. Baseline Simulation (nominal load 1.18 pu peak)
    load_template = [0.85, 0.92, 1.02, 1.12, 1.18, 1.16, 1.10, 1.05, 0.98, 0.90, 0.82, 0.75]
    base_loads = [load_template[min(i, len(load_template) - 1)] for i in range(len(forecast_dicts))]
    baseline_traj = thermal_solver.simulate_trajectory(
        asset_id="SUB-PHX-DOWNTOWN-04",
        hourly_forecast=forecast_dicts,
        load_k_series=base_loads,
        cooling_derate=eta_cool,
        forced_cooling_active=False,
        persistence_hours_p40=sandbox_p40,
        exceedance_degree_hours_h40=sandbox_h40,
    )

    # 5. Mitigated Actions & Load Profile
    mit_loads = list(base_loads)
    candidate_actions: List[MitigationAction] = []

    if req.forced_cooling_enabled:
        candidate_actions.append(
            MitigationAction(
                action_type=ActionType.COOLING_STAGE_2,
                target_asset_id="SUB-PHX-DOWNTOWN-04",
                target_hour_start=4,
                target_hour_end=11,
                cooling_boost_factor=1.35,
            )
        )

    if req.bess_capacity_mwh > 0.0:
        bess_shave_k = min(0.25, (req.bess_capacity_mwh / 25.0) * 0.22)
        candidate_actions.append(
            MitigationAction(
                action_type=ActionType.BESS_PEAK_SHAVING,
                target_asset_id="SUB-PHX-DOWNTOWN-04",
                target_hour_start=5,
                target_hour_end=10,
                load_ratio_delta_k=bess_shave_k,
                power_delta_mw=bess_shave_k * req.transformer_mva,
                bess_discharge_mw=min(5.0, req.bess_capacity_mwh / 4.0),
            )
        )
        for i in range(4, 10):
            mit_loads[i] = max(0.65, mit_loads[i] - bess_shave_k)

    mitigated_traj = thermal_solver.simulate_trajectory(
        asset_id="SUB-PHX-DOWNTOWN-04",
        hourly_forecast=forecast_dicts,
        load_k_series=mit_loads,
        cooling_derate=eta_cool,
        forced_cooling_active=req.forced_cooling_enabled,
        persistence_hours_p40=sandbox_p40,
        exceedance_degree_hours_h40=sandbox_h40,
    )

    # 6. Safety Gate Preflight
    safety_verdict = safety_gate.preflight_check(
        asset_id="SUB-PHX-DOWNTOWN-04",
        hourly_forecast=forecast_dicts,
        candidate_actions=candidate_actions,
        cooling_derate=eta_cool,
        bess_initial_soc_pct=85.0,
        bess_capacity_mwh=max(req.bess_capacity_mwh, 1.0),
        transformer_rating_mva=req.transformer_mva,
    )
    await safety_gate.persist_pending_certificates()

    # 7. Soil Dryout & Virtual Moisture
    soil_eval = soil_engine.evaluate_compound_site_margin(
        consecutive_heatwave_days=req.heatwave_day,
        initial_moisture=0.18,
        cable_load_k=1.18,
        transformer_top_oil_c=mitigated_traj.peak_top_oil_c,
        transformer_hot_spot_c=mitigated_traj.peak_hot_spot_c,
    )
    moisture_eval = moisture_engine.step_moisture_migration(
        paper_moisture_pct=2.5,
        oil_moisture_ppm=16.0,
        t_hot_spot_c=mitigated_traj.peak_hot_spot_c,
        t_oil_c=mitigated_traj.peak_top_oil_c,
        dt_hours=1.0,
    )

    # 8. Avoided Loss Model
    bess_discharged_mwh = min(req.bess_capacity_mwh * 0.4, 12.5) if req.bess_capacity_mwh > 0 else 0.0
    economic_eval = economic_engine.evaluate_net_avoided_loss(
        baseline_peak_hot_spot_c=baseline_traj.peak_hot_spot_c,
        mitigated_peak_hot_spot_c=mitigated_traj.peak_hot_spot_c,
        baseline_loss_of_life_hours=baseline_traj.total_loss_of_life_hours,
        mitigated_loss_of_life_hours=mitigated_traj.total_loss_of_life_hours,
        persistence_hours=sandbox_p40,
        thermal_soak_index=sandbox_tsi,
        bess_discharged_mwh=bess_discharged_mwh,
        cooling_runtime_hours=7.0 if req.forced_cooling_enabled else 0.0,
    )

    # 9. Timeline Steps
    timeline_steps = []
    bess_soc = 85.0
    for idx, (f_dict, b_step, m_step) in enumerate(
        zip(forecast_dicts, baseline_traj.steps, mitigated_traj.steps)
    ):
        if req.bess_capacity_mwh > 0 and 4 <= idx <= 9:
            bess_soc = max(30.0, bess_soc - (bess_discharged_mwh / req.bess_capacity_mwh * 100.0 / 6.0))

        timeline_steps.append(
            {
                "hour_index": idx,
                "timestamp": f_dict["timestamp"],
                "time_label": f_dict["time_label"],
                "coolest_tile_2m_c": coolest_tile_temps[idx],
                "fortyguard_2m_ambient_c": f_dict["fortyguard_2m_ambient_c"],
                "intra_aoi_spread_c": round(f_dict["fortyguard_2m_ambient_c"] - coolest_tile_temps[idx], 1),
                "solar_irradiance_w_m2": f_dict["solar_irradiance_w_m2"],
                "baseline_top_oil_c": b_step.t_top_oil_c,
                "baseline_hot_spot_c": b_step.t_hot_spot_c,
                "baseline_aging_factor_v": b_step.aging_acceleration_factor_v,
                "baseline_load_k": base_loads[idx],
                "mitigated_top_oil_c": m_step.t_top_oil_c,
                "mitigated_hot_spot_c": m_step.t_hot_spot_c,
                "mitigated_aging_factor_v": m_step.aging_acceleration_factor_v,
                "mitigated_load_k": mit_loads[idx],
                "bess_soc_pct": round(bess_soc, 1),
            }
        )

    sensitivity = transformer_sensitivity_envelope(
        thermal_solver, forecast_dicts, base_loads, eta_cool
    )
    integrated = evaluate_integrated_scenario(
        forecast=forecast_dicts,
        baseline_hotspots_c=[s.t_hot_spot_c for s in baseline_traj.steps],
        mitigated_hotspots_c=[s.t_hot_spot_c for s in mitigated_traj.steps],
        baseline_loads_k=base_loads,
        mitigated_loads_k=mit_loads,
        transformer_rating_mva=req.transformer_mva,
        soil_resistivity_rho=soil_eval["soil_thermal_resistivity_rho_soil"],
    )

    # Persist simulation run snapshot
    try:
        import uuid
        sim_id = f"SIM-{uuid.uuid4().hex[:8].upper()}"
        sim_record = SimulationRunRecord(
            simulation_id=sim_id,
            scenario_name=f"WhatIf Delta={req.intra_aoi_spread_c}C Day={req.heatwave_day}",
            delta_c=req.intra_aoi_spread_c,
            heatwave_day=req.heatwave_day,
            transformer_mva=req.transformer_mva,
            bess_mwh=req.bess_capacity_mwh,
            canyon_hw_ratio=req.canyon_aspect_ratio,
            cooling_fans_stage=2 if req.forced_cooling_enabled else 0,
            peak_hot_spot_c=baseline_traj.peak_hot_spot_c,
            hours_above_140c=sum(1.0 for s in baseline_traj.steps if s.t_hot_spot_c >= 140.0),
            # 0.0 rather than the retired 2,791,338 - a missing key should read as
            # absent, not as a fabricated headline figure.
            net_avoided_loss=float(economic_eval.get("net_avoided_loss", 0.0)),
        )
        await db_manager.save_simulation_run(sim_record)
    except Exception as exc:
        logger.warning("Failed to persist sandbox simulation run: %s", exc, exc_info=True)

    boundary_source = str(scan_binding.get("data_source") or "phoenix_fixture")
    result: Dict[str, Any] = {
        "status": "success",
        "provenance": canonical_provenance(
            scenario_id=(
                f"live_scan:{req.latitude}:{req.longitude}:{req.analysis_date}"
                if scan_binding["mode"] == "live_scan"
                else "phoenix_2023_what_if"
            ),
            boundary_source=boundary_source,
            operating_mode="hybrid" if scan_binding["mode"] == "live_scan" else "demo",
            solar_kind="externally_modelled",
        ),
        # Says plainly whether these numbers came from a live scan of the
        # requested coordinates or from the frozen Phoenix benchmark curve.
        "scan_binding": scan_binding,
        "inputs_applied": req.model_dump(),
        "timeline_steps": timeline_steps,
        "baseline_summary": {
            "peak_top_oil_c": baseline_traj.peak_top_oil_c,
            "peak_hot_spot_c": baseline_traj.peak_hot_spot_c,
            "peak_aging_acceleration_v": baseline_traj.peak_aging_acceleration_v,
            "total_loss_of_life_hours": baseline_traj.total_loss_of_life_hours,
            "breached_emergency_ceiling": baseline_traj.breached_hot_spot_ceiling,
        },
        "mitigated_summary": {
            "peak_top_oil_c": mitigated_traj.peak_top_oil_c,
            "peak_hot_spot_c": mitigated_traj.peak_hot_spot_c,
            "peak_aging_acceleration_v": mitigated_traj.peak_aging_acceleration_v,
            "total_loss_of_life_hours": mitigated_traj.total_loss_of_life_hours,
            "breached_emergency_ceiling": mitigated_traj.breached_hot_spot_ceiling,
            "avoided_loss_of_life_hours": round(
                baseline_traj.total_loss_of_life_hours - mitigated_traj.total_loss_of_life_hours, 1
            ),
        },
        "safety_gate_verdict": safety_verdict.model_dump(),
        "economic_evaluation": economic_eval,
        "soil_cable_state": soil_eval,
        "virtual_moisture_state": moisture_eval,
        "urban_canyon_state": canyon_res,
        "sensitivity_analysis": sensitivity,
        "integrated_grid_evaluation": integrated,
    }

    stored_at = datetime.now(timezone.utc).isoformat()
    result["cache"] = {"hit": False, "key": cache_key, "stored_at": stored_at}

    # Persist the whole solved payload, not a summary of it. simulation_runs
    # keeps scalars for the audit trail but cannot reconstruct a trajectory, so
    # without this the work is recomputed on every visit and the result is lost.
    try:
        await db_manager.save_cached_api_call(
            ApiCallCacheRecord(
                query_hash=cache_key,
                endpoint="sandbox/simulate",
                request_params=req.model_dump(),
                response_payload=result,
                credits_spent=0.0,
                created_at=stored_at,
                expires_at=None,
            )
        )
    except Exception as exc:
        logger.warning("Failed to persist simulation result %s: %s", cache_key, exc, exc_info=True)

    return result
