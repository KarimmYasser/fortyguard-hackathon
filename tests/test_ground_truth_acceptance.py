import pytest

from src.data_science.ground_truth_validation import (
    GroundTruthValidationError,
    validate_fortyguard_curve,
)


def test_validation_rejects_low_coverage_even_if_minimum_pair_count_passes():
    baseline = [
        {"timestamp": f"2023-01-01T{i:02d}:00:00Z", "fortyguard_2m_ambient_c": 30 + i}
        for i in range(10)
    ]
    truth = {
        "data_source": "ground_truth_live",
        "provider": "iem_asos",
        "provenance": {"evidence_class": "in-situ station observation"},
        "series": [
            {"timestamp": f"2023-01-01T{i:02d}:00:00Z", "temperature_2m_c": 30 + i}
            for i in range(6)
        ],
    }
    with pytest.raises(GroundTruthValidationError, match="below the 80.0%"):
        validate_fortyguard_curve(baseline, truth, minimum_pairs=6)


def test_quality_gate_is_explicit_in_accepted_report():
    baseline = [{"timestamp": "t", "fortyguard_2m_ambient_c": 30}]
    truth = {
        "data_source": "ground_truth_cached", "provider": "iem_asos",
        "provenance": {"evidence_class": "in-situ station observation"},
        "series": [{"timestamp": "t", "temperature_2m_c": 29}],
    }
    report = validate_fortyguard_curve(baseline, truth)
    assert report["quality_gate"] == {
        "accepted": True, "minimum_pairs": 1,
        "minimum_coverage_pct": 80.0, "missing_values_imputed": False,
    }
