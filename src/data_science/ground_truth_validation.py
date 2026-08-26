"""Timestamp-aligned validation of FortyGuard curves against external benchmarks."""

from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Mapping, Sequence


class GroundTruthValidationError(ValueError):
    """Raised when two curves cannot support a defensible comparison."""


def _canonical_timestamp(value: str) -> str:
    """Canonicalize ISO-8601 timestamps to UTC; retain opaque test keys."""
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return value
    if parsed.tzinfo is None:
        raise GroundTruthValidationError(f"timestamp has no timezone offset: {value}")
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _finite(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def _index_unique(rows: Iterable[Mapping[str, Any]], timestamp_field: str) -> Dict[str, Mapping[str, Any]]:
    indexed: Dict[str, Mapping[str, Any]] = {}
    for row in rows:
        timestamp = row.get(timestamp_field)
        if not isinstance(timestamp, str) or not timestamp:
            continue
        canonical = _canonical_timestamp(timestamp)
        if canonical in indexed:
            raise GroundTruthValidationError(f"duplicate timestamp: {canonical}")
        indexed[canonical] = row
    return indexed


def _rank(values: Sequence[float]) -> list[float]:
    """Average ranks with deterministic tie handling."""
    ordered = sorted(enumerate(values), key=lambda item: item[1])
    ranks = [0.0] * len(values)
    index = 0
    while index < len(ordered):
        end = index + 1
        while end < len(ordered) and ordered[end][1] == ordered[index][1]:
            end += 1
        average_rank = (index + 1 + end) / 2.0
        for offset in range(index, end):
            ranks[ordered[offset][0]] = average_rank
        index = end
    return ranks


def _correlation(left: Sequence[float], right: Sequence[float]) -> float | None:
    if len(left) != len(right) or len(left) < 2:
        return None
    left_mean, right_mean = sum(left) / len(left), sum(right) / len(right)
    left_dev = [value - left_mean for value in left]
    right_dev = [value - right_mean for value in right]
    denominator = math.sqrt(
        sum(value * value for value in left_dev) * sum(value * value for value in right_dev)
    )
    return None if denominator == 0 else sum(a * b for a, b in zip(left_dev, right_dev)) / denominator


def _heat_exposure(values: Sequence[float], threshold_c: float) -> Dict[str, float | int]:
    longest = current = 0
    degree_hours = 0.0
    exceedance_hours = 0
    for value in values:
        if value >= threshold_c:
            current += 1
            longest = max(longest, current)
            exceedance_hours += 1
            degree_hours += value - threshold_c
        else:
            current = 0
    return {
        "threshold_c": threshold_c,
        "exceedance_hours": exceedance_hours,
        "longest_persistence_hours": longest,
        "exceedance_degree_hours": round(degree_hours, 4),
    }


def compute_error_metrics(
    baseline: Sequence[Mapping[str, Any]],
    ground_truth: Sequence[Mapping[str, Any]],
    *,
    baseline_field: str = "fortyguard_2m_ambient_c",
    ground_truth_field: str = "temperature_2m_c",
    timestamp_field: str = "timestamp",
    minimum_pairs: int = 1,
) -> Dict[str, Any]:
    """Compute paired MAE/RMSE and peak deltas after exact UTC-hour alignment.

    ``error`` and ``peak_delta`` use FortyGuard minus ground truth, preserving
    direction. Missing/non-finite measurements are excluded and reported via
    coverage rather than silently imputed.
    """
    if minimum_pairs < 1:
        raise ValueError("minimum_pairs must be at least 1")
    predicted = _index_unique(baseline, timestamp_field)
    observed = _index_unique(ground_truth, timestamp_field)
    pairs = []
    for timestamp in sorted(predicted.keys() & observed.keys()):
        prediction = _finite(predicted[timestamp].get(baseline_field))
        truth = _finite(observed[timestamp].get(ground_truth_field))
        if prediction is not None and truth is not None:
            pairs.append((timestamp, prediction, truth))

    if len(pairs) < minimum_pairs:
        raise GroundTruthValidationError(
            f"only {len(pairs)} valid aligned pairs; at least {minimum_pairs} required"
        )

    errors = [prediction - truth for _, prediction, truth in pairs]
    baseline_peak = max(prediction for _, prediction, _ in pairs)
    truth_peak = max(truth for _, _, truth in pairs)
    possible = max(len(predicted), 1)
    mean_prediction = sum(prediction for _, prediction, _ in pairs) / len(pairs)
    mean_truth = sum(truth for _, _, truth in pairs) / len(pairs)
    mean_error = sum(errors) / len(errors)
    prediction_deviations = [prediction - mean_prediction for _, prediction, _ in pairs]
    truth_deviations = [truth - mean_truth for _, _, truth in pairs]
    covariance = sum(a * b for a, b in zip(prediction_deviations, truth_deviations))
    variance_product = (
        sum(value * value for value in prediction_deviations)
        * sum(value * value for value in truth_deviations)
    )
    pearson_r = covariance / math.sqrt(variance_product) if variance_product > 0 else None
    predictions = [prediction for _, prediction, _ in pairs]
    truths = [truth for _, _, truth in pairs]
    spearman_r = _correlation(_rank(predictions), _rank(truths))
    positive_hours = sum(error > 0 for error in errors)
    thresholds = (35.0, 40.0, 45.0)
    heat_exposure = {
        str(int(threshold)): {
            "baseline": _heat_exposure(predictions, threshold),
            "ground_truth": _heat_exposure(truths, threshold),
        }
        for threshold in thresholds
    }
    for comparison in heat_exposure.values():
        comparison["delta"] = {
            key: round(float(comparison["baseline"][key]) - float(comparison["ground_truth"][key]), 4)
            for key in ("exceedance_hours", "longest_persistence_hours", "exceedance_degree_hours")
        }
    return {
        "baseline_field": baseline_field,
        "ground_truth_field": ground_truth_field,
        "n_pairs": len(pairs),
        "baseline_points": len(predicted),
        "ground_truth_points": len(observed),
        "coverage_pct": round(100.0 * len(pairs) / possible, 2),
        "mae": round(sum(abs(error) for error in errors) / len(errors), 4),
        "rmse": round(math.sqrt(sum(error * error for error in errors) / len(errors)), 4),
        "mean_bias": round(mean_error, 4),
        "mean_delta_t_c": round(mean_error, 4),
        "positive_delta_hours": positive_hours,
        "positive_delta_pct": round(100.0 * positive_hours / len(errors), 2),
        "pearson_r": None if pearson_r is None else round(pearson_r, 4),
        "spearman_r": None if spearman_r is None else round(spearman_r, 4),
        "heat_exposure": heat_exposure,
        "baseline_peak": round(baseline_peak, 4),
        "ground_truth_peak": round(truth_peak, 4),
        "peak_delta": round(baseline_peak - truth_peak, 4),
        "peak_absolute_delta": round(abs(baseline_peak - truth_peak), 4),
        "first_timestamp": pairs[0][0],
        "last_timestamp": pairs[-1][0],
        "paired_series": [
            {
                "timestamp": timestamp,
                "fortyguard_2m_c": round(prediction, 4),
                "station_ground_truth_c": round(truth, 4),
                "delta_t_c": round(prediction - truth, 4),
            }
            for timestamp, prediction, truth in pairs
        ],
        "urban_station_anomaly": {
            "observed": mean_error > 0,
            "mean_delta_positive": mean_error > 0,
            "majority_positive": positive_hours > len(errors) / 2,
            "interpretation": (
                "Positive urban-minus-station temperature anomaly in this aligned sample"
                if mean_error > 0
                else "No positive urban-minus-station temperature anomaly in this aligned sample"
            ),
        },
        "urban_heat_island": {
            "verified": False,
            "status": "not_established_by_station_comparison",
            "criterion": (
                "A UHI claim requires a verified same-time urban-versus-rural or representative "
                "multi-station reference design; positive ΔT against one airport is insufficient."
            ),
            "interpretation": "This comparison is validation/context, not causal proof of UHI.",
        },
    }


def validate_fortyguard_curve(
    baseline: Sequence[Mapping[str, Any]],
    ground_truth_payload: Mapping[str, Any],
    *,
    minimum_pairs: int = 1,
    minimum_coverage_pct: float = 80.0,
) -> Dict[str, Any]:
    """Validate available fields and enforce minimum timestamp coverage."""
    if not 0 < minimum_coverage_pct <= 100:
        raise ValueError("minimum_coverage_pct must be in (0, 100]")
    source = ground_truth_payload.get("data_source")
    if source not in {"ground_truth_live", "ground_truth_cached", "ground_truth_replay"}:
        raise GroundTruthValidationError(f"untrusted ground-truth provenance: {source!r}")
    series = ground_truth_payload.get("series")
    if not isinstance(series, list):
        raise GroundTruthValidationError("ground-truth payload has no series")

    metrics: Dict[str, Any] = {
        "temperature_2m": compute_error_metrics(
            baseline, series, minimum_pairs=minimum_pairs
        )
    }
    if metrics["temperature_2m"]["coverage_pct"] < minimum_coverage_pct:
        raise GroundTruthValidationError(
            f"aligned coverage {metrics['temperature_2m']['coverage_pct']}% is below "
            f"the {minimum_coverage_pct}% acceptance gate"
        )
    if (
        any(_finite(row.get("solar_irradiance_w_m2")) is not None for row in baseline)
        and any(_finite(row.get("solar_ghi_w_m2")) is not None for row in series)
    ):
        metrics["solar_ghi"] = compute_error_metrics(
            baseline,
            series,
            baseline_field="solar_irradiance_w_m2",
            ground_truth_field="solar_ghi_w_m2",
            minimum_pairs=minimum_pairs,
        )
    evidence_class = str((ground_truth_payload.get("provenance") or {}).get("evidence_class", ""))
    evidence_class_lower = evidence_class.lower()
    evidence_tier = (
        "A_colocated_field" if "co-located" in evidence_class_lower
        else "C_gridded" if "gridded" in evidence_class_lower
        else "C_modeled" if "model" in evidence_class_lower or "not in-situ" in evidence_class_lower
        else "B_in_situ_station" if "in-situ" in evidence_class_lower
        else "C_contextual"
    )
    return {
        "data_source": source,
        "provider": ground_truth_payload.get("provider"),
        "provenance": ground_truth_payload.get("provenance", {}),
        "evidence_tier": evidence_tier,
        "quality_gate": {
            "accepted": True,
            "minimum_pairs": minimum_pairs,
            "minimum_coverage_pct": minimum_coverage_pct,
            "missing_values_imputed": False,
        },
        "metrics": metrics,
    }
