"""Deterministic portfolio triage and worker-intervention planning.

The service deliberately keeps measured environmental observations separate from
asset-registry metadata and derived decision scores. It does not claim that
FortyGuard supplies grid telemetry or occupational-safety certification.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional

FIXTURE_PATH = Path(__file__).parents[1] / "api" / "fixtures" / "phoenix_heatwave_2023.json"


def load_default_environment_profile() -> tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Load the frozen, live-captured Phoenix profile used by deterministic replay."""
    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    return payload["hourly_forecast_12h"], payload["scenario_metadata"]


def _number(value: Any, default: float = 0.0) -> float:
    return float(value) if value is not None else default


def _asset_value(asset: Any, key: str, default: Any = None) -> Any:
    if isinstance(asset, Mapping):
        return asset.get(key, default)
    return getattr(asset, key, default)


def _asset_id(asset: Any) -> str:
    return str(_asset_value(asset, "asset_id", _asset_value(asset, "id", "UNKNOWN")))


def _asset_name(asset: Any) -> str:
    return str(_asset_value(asset, "name", _asset_id(asset)))


def _asset_type(asset: Any) -> str:
    value = _asset_value(asset, "type", _asset_value(asset, "asset_type", "unknown"))
    return str(getattr(value, "value", value))


def calculate_worker_windows(
    hourly_profile: Iterable[Mapping[str, Any]],
    *,
    max_wet_bulb_c: float = 23.0,
    max_air_temp_c: float = 40.0,
    min_consecutive_hours: int = 2,
) -> Dict[str, Any]:
    """Find contiguous candidate intervention windows using explicit thresholds.

    This is an operational screening rule, not an OSHA/WBGT determination. The
    fixture contains FortyGuard wet-bulb and 2 m air-temperature observations;
    no globe-temperature measurement is available, so WBGT is not fabricated.
    """
    rows: List[Dict[str, Any]] = []
    safe_indices: List[int] = []
    for index, raw in enumerate(hourly_profile):
        air = raw.get("fortyguard_2m_ambient_c")
        wet_bulb = raw.get("wet_bulb_temp_c")
        eligible = (
            air is not None
            and wet_bulb is not None
            and float(air) <= max_air_temp_c
            and float(wet_bulb) <= max_wet_bulb_c
        )
        if eligible:
            safe_indices.append(index)
        rows.append({
            "hour_index": int(raw.get("hour_index", index)),
            "timestamp": raw.get("timestamp"),
            "air_temp_2m_c": air,
            "wet_bulb_temp_c": wet_bulb,
            "eligible": eligible,
            "data_source": raw.get("data_source"),
        })

    windows: List[Dict[str, Any]] = []
    if safe_indices:
        groups: List[List[int]] = [[safe_indices[0]]]
        for index in safe_indices[1:]:
            if index == groups[-1][-1] + 1:
                groups[-1].append(index)
            else:
                groups.append([index])
        for group in groups:
            if len(group) < min_consecutive_hours:
                continue
            selected = [rows[i] for i in group]
            windows.append({
                "start_timestamp": selected[0]["timestamp"],
                "end_timestamp": selected[-1]["timestamp"],
                "duration_hours": len(selected),
                "peak_air_temp_2m_c": max(_number(r["air_temp_2m_c"]) for r in selected),
                "peak_wet_bulb_temp_c": max(_number(r["wet_bulb_temp_c"]) for r in selected),
                "hour_indices": [r["hour_index"] for r in selected],
            })

    return {
        "method": "threshold_screen_v1",
        "classification": "derived_operational_screen",
        "occupational_safety_certification": False,
        "limitations": "Wet-bulb and 2 m air temperature screen only; no globe-temperature, workload, clothing, acclimatization, or WBGT compliance determination.",
        "thresholds": {
            "max_wet_bulb_c": max_wet_bulb_c,
            "max_air_temp_c": max_air_temp_c,
            "min_consecutive_hours": min_consecutive_hours,
        },
        "windows": windows,
        "hourly_screen": rows,
    }


def rank_portfolio(
    assets: Iterable[Any],
    hourly_profile: Iterable[Mapping[str, Any]],
    *,
    worker_screen: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Rank assets using a transparent deterministic score (0–100)."""
    profile = list(hourly_profile)
    air_values = [_number(row.get("fortyguard_2m_ambient_c")) for row in profile if row.get("fortyguard_2m_ambient_c") is not None]
    peak_air = max(air_values) if air_values else 0.0
    worker_screen = worker_screen or calculate_worker_windows(profile)
    next_window = worker_screen["windows"][0] if worker_screen["windows"] else None

    ranked: List[Dict[str, Any]] = []
    for asset in assets:
        safe_ambient = _number(_asset_value(asset, "max_safe_ambient_temp_c", 40.0), 40.0)
        raw_load = _asset_value(asset, "current_load_percentage")
        raw_health = _asset_value(asset, "current_health_score")
        raw_criticality = _asset_value(asset, "criticality_tier")
        load_pct = _number(raw_load) if raw_load is not None else None
        health = _number(raw_health) if raw_health is not None else None
        criticality = int(raw_criticality) if raw_criticality is not None else None
        exceedance = max(0.0, peak_air - safe_ambient)

        # Explicit weighted score, normalized over available evidence. Missing
        # registry fields contribute neither risk nor false reassurance.
        environmental_component = min(35.0, exceedance * 8.75)
        loading_component = (
            min(30.0, max(0.0, load_pct - 60.0) * 0.75)
            if load_pct is not None else None
        )
        health_component = (
            min(20.0, max(0.0, 100.0 - health) * 0.4)
            if health is not None else None
        )
        criticality_component = (
            {1: 15.0, 2: 9.0, 3: 4.0}.get(criticality, 4.0)
            if criticality is not None else None
        )
        components = [
            (environmental_component, 35.0),
            (loading_component, 30.0),
            (health_component, 20.0),
            (criticality_component, 15.0),
        ]
        available_weight = sum(weight for value, weight in components if value is not None)
        earned = sum(value for value, _ in components if value is not None)
        score = round(100.0 * earned / available_weight, 1) if available_weight else 0.0
        level = "critical" if score >= 70 else "high" if score >= 50 else "elevated" if score >= 25 else "watch"

        ranked.append({
            "asset_id": _asset_id(asset),
            "asset_name": _asset_name(asset),
            "asset_type": _asset_type(asset),
            "risk_score": score,
            "risk_level": level,
            "rank_components": {
                "environmental_exceedance": round(environmental_component, 1),
                "asset_loading": round(loading_component, 1) if loading_component is not None else None,
                "asset_health": round(health_component, 1) if health_component is not None else None,
                "criticality": round(criticality_component, 1) if criticality_component is not None else None,
            },
            "inputs": {
                "peak_air_temp_2m_c": round(peak_air, 2),
                "max_safe_ambient_temp_c": safe_ambient,
                "ambient_exceedance_c": round(exceedance, 2),
                "current_load_percentage": load_pct,
                "current_health_score": health,
                "criticality_tier": criticality,
                "available_score_weight": available_weight,
            },
            "next_candidate_worker_window": next_window,
            "action": "prioritize_intervention" if score >= 50 else "monitor",
        })

    ranked.sort(key=lambda row: (-row["risk_score"], row["asset_id"]))
    for index, row in enumerate(ranked, start=1):
        row["rank"] = index
    return ranked


def build_mitigation_evidence(
    rankings: List[Mapping[str, Any]],
    worker_screen: Mapping[str, Any],
    metadata: Mapping[str, Any],
) -> Dict[str, Any]:
    """Produce content-addressed evidence for a read-only decision snapshot."""
    evidence_body = {
        "schema_version": "1.0",
        "decision_type": "portfolio_thermal_intervention_triage",
        "scenario_id": metadata.get("scenario_id"),
        "analysis_date": metadata.get("persistence_metrics", {}).get("analysis_date"),
        "rankings": rankings,
        "worker_intervention_screen": worker_screen,
        "provenance": {
            "environmental_inputs": "measured FortyGuard fields preserved in a frozen live-capture fixture",
            "asset_inputs": "grid asset registry metadata",
            "decision_outputs": "deterministically derived by portfolio_rank_v1 and threshold_screen_v1",
            "data_source": metadata.get("persistence_metrics", {}).get("data_source"),
        },
    }
    canonical = json.dumps(evidence_body, sort_keys=True, separators=(",", ":"), default=str)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return {
        **evidence_body,
        "evidence_id": f"EVIDENCE-{digest[:16].upper()}",
        "sha256": digest,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "immutable_input_digest": True,
        "read_only": True,
    }
