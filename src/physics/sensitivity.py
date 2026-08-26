"""Transparent deterministic sensitivity envelope for transformer outputs."""

from __future__ import annotations

from typing import Any, Dict, List

from src.physics.transformer_thermal import TransformerThermalEngine


def transformer_sensitivity_envelope(
    engine: TransformerThermalEngine,
    forecast: List[Dict[str, Any]],
    loads_k: List[float],
    cooling_derate: float,
) -> Dict[str, Any]:
    """Evaluate a small disclosed corner set; this is not a confidence interval."""
    cases = [
        ("cool", -1.5, 0.90, 1.10),
        ("nominal", 0.0, 1.00, 1.00),
        ("hot", 1.5, 1.10, 0.90),
    ]
    rows = []
    for name, ambient_delta, load_factor, cooling_factor in cases:
        shifted = [
            {**hour, "fortyguard_2m_ambient_c": float(hour.get("fortyguard_2m_ambient_c", 25.0)) + ambient_delta}
            for hour in forecast
        ]
        trajectory = engine.simulate_trajectory(
            asset_id=f"SENSITIVITY-{name.upper()}",
            hourly_forecast=shifted,
            load_k_series=[max(0.0, k * load_factor) for k in loads_k],
            cooling_derate=max(0.1, cooling_derate * cooling_factor),
        )
        rows.append({
            "case": name,
            "ambient_delta_c": ambient_delta,
            "load_multiplier": load_factor,
            "cooling_multiplier": cooling_factor,
            "peak_hot_spot_c": trajectory.peak_hot_spot_c,
            "loss_of_life_hours": trajectory.total_loss_of_life_hours,
        })
    return {
        "method": "deterministic_three_corner_sensitivity_not_confidence_interval",
        "assumptions": {"ambient_delta_c": 1.5, "load_pct": 10.0, "cooling_pct": 10.0},
        "peak_hot_spot_c": {
            "low": min(r["peak_hot_spot_c"] for r in rows),
            "nominal": next(r["peak_hot_spot_c"] for r in rows if r["case"] == "nominal"),
            "high": max(r["peak_hot_spot_c"] for r in rows),
        },
        "loss_of_life_hours": {
            "low": min(r["loss_of_life_hours"] for r in rows),
            "nominal": next(r["loss_of_life_hours"] for r in rows if r["case"] == "nominal"),
            "high": max(r["loss_of_life_hours"] for r in rows),
        },
        "cases": rows,
    }
