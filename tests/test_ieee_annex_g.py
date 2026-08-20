import pytest
from src.physics.ieee_annex_g_benchmark import IEEEAnnexGBenchmarkEngine


def test_ieee_annex_g2_step_load_response():
    engine = IEEEAnnexGBenchmarkEngine()
    result = engine.run_clause_g2_step_load_benchmark()

    assert result.passed_ieee_tolerance is True
    assert result.max_absolute_error_top_oil_c < 0.05
    assert result.max_absolute_error_hot_spot_c < 0.05
    assert len(result.comparison_table) == 8


def test_ieee_annex_g3_diurnal_ambient_ramp():
    engine = IEEEAnnexGBenchmarkEngine()
    result = engine.run_clause_g3_diurnal_ambient_benchmark()

    assert result.passed_ieee_tolerance is True
    assert len(result.comparison_table) == 24


def test_ieee_arrhenius_exact_normal_life():
    engine = IEEEAnnexGBenchmarkEngine()
    summary = engine.run_all_benchmarks()

    assert summary["all_benchmarks_passed"] is True
    assert summary["arrhenius_reference_at_110c"]["verified"] is True
    assert abs(summary["arrhenius_reference_at_110c"]["evaluated_v"] - 1.0) < 1e-5
