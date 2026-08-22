"""
Tests for Data Science, Analytics & ML Pipeline
Validates ETL pipeline, feature engineering, ML model accuracy,
statistical analytics, and survival analysis.
"""

from __future__ import annotations

import pytest
import numpy as np
import pandas as pd


class TestETLPipeline:
    """Tests for the Bronze → Silver → Gold ETL pipeline."""

    def test_bronze_extraction_returns_dataframe(self):
        """Verify Phoenix fixture loads into a non-empty DataFrame."""
        from src.data_science.etl_pipeline import ThermalDataPipeline
        pipeline = ThermalDataPipeline()
        df = pipeline._extract_bronze()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0, "Bronze layer should extract at least 1 record"
        assert len(df) == 12, "Phoenix fixture has exactly 12 hourly records"

    def test_silver_transformation_no_nulls(self):
        """Confirm null cleaning and type casting in Silver layer."""
        from src.data_science.etl_pipeline import ThermalDataPipeline
        pipeline = ThermalDataPipeline()
        bronze = pipeline._extract_bronze()
        silver = pipeline._transform_silver(bronze)
        numeric_nulls = silver.select_dtypes(include=[np.number]).isna().sum().sum()
        assert numeric_nulls == 0, f"Silver layer should have 0 numeric nulls, found {numeric_nulls}"

    def test_gold_feature_engineering_columns(self):
        """Verify all 15+ engineered feature columns exist in Gold."""
        from src.data_science.etl_pipeline import ThermalDataPipeline
        pipeline = ThermalDataPipeline()
        gold = pipeline.run_full_pipeline()
        required_features = [
            "delta_microclimate_c",
            "rolling_3h_avg_ambient",
            "cumulative_degree_hours_above_40",
            "estimated_hot_spot_c",
            "safety_margin_c",
            "aging_factor_v",
            "load_peak_flag",
            "is_solar_peak",
            "hour_of_day",
            "bess_soc_gradient",
            "risk_tier",
            "soil_resistivity_regime",
            "aging_acceleration_bin",
            "canyon_wind_regime",
            "moisture_risk_level",
        ]
        for feature in required_features:
            assert feature in gold.columns, f"Gold dataset missing required feature: {feature}"
        assert len(gold.columns) >= 15, f"Expected 15+ columns, got {len(gold.columns)}"

    def test_correlation_matrix_shape(self):
        """Correlation matrix is square and matches feature count."""
        from src.data_science.etl_pipeline import ThermalDataPipeline
        pipeline = ThermalDataPipeline()
        corr = pipeline.get_feature_correlation_matrix()
        n_cols = len(corr["columns"])
        matrix = corr["matrix"]
        assert len(matrix) == n_cols, "Matrix should be square"
        assert len(matrix[0]) == n_cols, "Matrix rows should match column count"

    def test_distribution_stats_complete(self):
        """Distribution stats should cover all numeric columns."""
        from src.data_science.etl_pipeline import ThermalDataPipeline
        pipeline = ThermalDataPipeline()
        stats = pipeline.get_distribution_stats()
        assert len(stats) > 0, "Should have stats for at least one feature"
        required_keys = ["feature", "mean", "std", "min", "max", "skewness", "kurtosis"]
        for s in stats:
            for key in required_keys:
                assert key in s, f"Missing key '{key}' in stats for {s.get('feature')}"


class TestMLModels:
    """Tests for Machine Learning models."""

    def test_surrogate_r2_above_threshold(self):
        """Ridge surrogate achieves R² > 0.95 against the physics ODE."""
        from src.data_science.ml_models import PhysicsSurrogateModel
        model = PhysicsSurrogateModel()
        metrics = model.train()
        assert metrics["r2_score"] > 0.95, f"R² = {metrics['r2_score']} (expected > 0.95)"
        assert metrics["mae_celsius"] < 5.0, f"MAE = {metrics['mae_celsius']} (expected < 5.0°C)"

    def test_surrogate_prediction_returns_float(self):
        """Surrogate model should return a float prediction."""
        from src.data_science.ml_models import PhysicsSurrogateModel
        model = PhysicsSurrogateModel()
        model.train()
        result = model.predict_hotspot({
            "ambient_2m_c": 42.74,
            "solar_irradiance": 960.0,
            "load_ratio_k": 1.0,
            "cooling_derate_eta": 0.68,
            "soil_resistivity": 2.45,
            "canyon_hw_ratio": 1.85,
        })
        assert isinstance(result, float), f"Expected float, got {type(result)}"
        assert 50 < result < 250, f"Prediction {result}°C out of physical range"

    def test_anomaly_detector_labels(self):
        """Every record gets a NORMAL or ANOMALY label."""
        from src.data_science.etl_pipeline import ThermalDataPipeline
        from src.data_science.ml_models import SensorAnomalyDetector
        pipeline = ThermalDataPipeline()
        gold = pipeline.run_full_pipeline()
        detector = SensorAnomalyDetector()
        results = detector.train_and_detect(gold)
        assert "records" in results
        for rec in results["records"]:
            assert rec["label"] in ("NORMAL", "ANOMALY"), f"Invalid label: {rec['label']}"

    def test_rul_survival_curve_monotonic(self):
        """Survival probability is monotonically decreasing."""
        from src.data_science.etl_pipeline import ThermalDataPipeline
        from src.data_science.ml_models import SurvivalAnalysisEngine
        pipeline = ThermalDataPipeline()
        gold = pipeline.run_full_pipeline()
        engine = SurvivalAnalysisEngine()
        results = engine.fit_and_estimate(gold)
        probs = results["survival_curve"]["survival_probability"]
        assert len(probs) > 1, "Survival curve should have multiple points"
        for i in range(1, len(probs)):
            assert probs[i] <= probs[i - 1] + 0.001, \
                f"Survival probability not monotonically decreasing at index {i}"


class TestAnalyticsEngine:
    """Tests for the Statistical Analytics Engine."""

    def test_risk_distribution_sums_to_100(self):
        """Risk tier percentages should sum to 100%."""
        from src.data_science.etl_pipeline import ThermalDataPipeline
        from src.data_science.analytics_engine import ThermalAnalyticsEngine
        pipeline = ThermalDataPipeline()
        gold = pipeline.run_full_pipeline()
        engine = ThermalAnalyticsEngine()
        risk = engine.compute_risk_distribution(gold)
        total_pct = sum(t["percentage"] for t in risk["risk_tiers"])
        assert abs(total_pct - 100.0) < 0.1, f"Risk tiers sum to {total_pct}% (expected 100%)"

    def test_microclimate_divergence_significant(self):
        """Paired t-test reaches significance on the intra-AOI tile spread."""
        from src.data_science.etl_pipeline import ThermalDataPipeline
        from src.data_science.analytics_engine import ThermalAnalyticsEngine
        pipeline = ThermalDataPipeline()
        gold = pipeline.run_full_pipeline()
        engine = ThermalAnalyticsEngine()
        result = engine.compute_microclimate_divergence(gold)
        assert result["is_significant"], f"p-value = {result['p_value']} (expected < 0.05)"
        assert result["mean_delta_c"] > 0, "hottest tile should exceed the coolest tile in the same AOI"

    def test_temporal_patterns_12_hours(self):
        """Should return exactly 12 hourly aggregated records."""
        from src.data_science.etl_pipeline import ThermalDataPipeline
        from src.data_science.analytics_engine import ThermalAnalyticsEngine
        pipeline = ThermalDataPipeline()
        gold = pipeline.run_full_pipeline()
        engine = ThermalAnalyticsEngine()
        result = engine.compute_temporal_patterns(gold)
        assert result["total_hours"] == 12, f"Expected 12 hours, got {result['total_hours']}"
        assert len(result["hourly_records"]) == 12

    def test_eda_summary_structure(self):
        """EDA summary should have complete structure."""
        from src.data_science.etl_pipeline import ThermalDataPipeline
        from src.data_science.analytics_engine import ThermalAnalyticsEngine
        pipeline = ThermalDataPipeline()
        gold = pipeline.run_full_pipeline()
        engine = ThermalAnalyticsEngine()
        eda = engine.compute_eda_summary(gold)
        assert "total_records" in eda
        assert "feature_statistics" in eda
        assert eda["total_records"] == 12

    def test_correlation_analysis_top_pairs(self):
        """Correlation analysis should identify top pairs."""
        from src.data_science.etl_pipeline import ThermalDataPipeline
        from src.data_science.analytics_engine import ThermalAnalyticsEngine
        pipeline = ThermalDataPipeline()
        gold = pipeline.run_full_pipeline()
        engine = ThermalAnalyticsEngine()
        result = engine.compute_correlation_analysis(gold)
        assert "top_10_strongest_pairs" in result
        assert len(result["top_10_strongest_pairs"]) > 0
        for pair in result["top_10_strongest_pairs"]:
            assert -1.0 <= pair["pearson_r"] <= 1.0

    def test_headline_correlations_are_not_tautologies(self):
        """The ranked list must not be padded with restated formulas.

        estimated_winding_gradient_c = 23 * K**0.8 is monotone in K, so that pair
        reports r ~ +1 on *any* dataset. Ranking it as the #2 discovery tells a
        judge nothing about the grid, and it crowds out the real signal.
        """
        from src.data_science.etl_pipeline import ThermalDataPipeline
        from src.data_science.analytics_engine import ThermalAnalyticsEngine
        gold = ThermalDataPipeline().run_full_pipeline()
        result = ThermalAnalyticsEngine().compute_correlation_analysis(gold)

        for pair in result["top_10_strongest_pairs"]:
            assert pair["kind"] == "empirical", (
                f"{pair['feature_a']} ~ {pair['feature_b']} is {pair['kind']} "
                "by construction and must not be ranked as a finding"
            )

        boxed = {
            frozenset({p["feature_a"], p["feature_b"]})
            for p in result["tautological_pairs"]
        }
        # physics features vs their own input
        assert frozenset({"baseline_load_ratio_k", "estimated_winding_gradient_c"}) in boxed
        assert frozenset({"baseline_load_ratio_k", "estimated_hot_spot_c"}) in boxed
        # two scenario columns scaled off the same authored ramp
        assert frozenset({"baseline_load_ratio_k", "hospital_critical_load_mw"}) in boxed

    def test_hospital_load_does_not_launder_load_tautologies(self):
        """hospital_critical_load_mw tracks K at r > 0.999, so it is a proxy for K.

        Without alias propagation, `hospital ~ estimated_hot_spot_c` sneaks the
        excluded `K ~ estimated_hot_spot_c` pair back into the headline list one
        hop removed.
        """
        from src.data_science.analytics_engine import _pair_kind
        assert _pair_kind("hospital_critical_load_mw", "estimated_hot_spot_c") == "derived"
        assert _pair_kind("hospital_critical_load_mw", "estimated_winding_gradient_c") == "derived"
        assert _pair_kind("coolest_tile_2m_c", "rolling_3h_avg_ambient") == "derived"
        # genuinely independent measurements stay empirical
        assert _pair_kind("relative_humidity_pct", "wind_speed_m_s") == "empirical"
        assert _pair_kind("solar_irradiance_w_m2", "baseline_load_ratio_k") == "empirical"

    def test_small_sample_is_disclosed(self):
        """12 hourly rows cannot support a confident |r|; say so in the payload."""
        from src.data_science.etl_pipeline import ThermalDataPipeline
        from src.data_science.analytics_engine import ThermalAnalyticsEngine
        gold = ThermalDataPipeline().run_full_pipeline()
        result = ThermalAnalyticsEngine().compute_correlation_analysis(gold)
        assert result["n_observations"] == len(gold)
        assert any("n = " in w for w in result["warnings"])
        for pair in result["top_10_strongest_pairs"]:
            assert pair["p_value"] is not None


class TestReportingHonesty:
    """The analytics output is judge-facing; these lock its claims to the data."""

    def _divergence(self):
        from src.data_science.etl_pipeline import ThermalDataPipeline
        from src.data_science.analytics_engine import ThermalAnalyticsEngine
        gold = ThermalDataPipeline().run_full_pipeline()
        return ThermalAnalyticsEngine().compute_microclimate_divergence(gold)

    def test_no_airport_labels_remain(self):
        """The column was renamed to coolest_tile_2m_c; the labels lagged behind.

        Sky Harbor measures *warmer* than downtown, so describing the reference
        series as an airport reading is factually wrong, and the stale
        `airport_mean_c` key silently broke the analysis notebook.
        """
        result = self._divergence()
        assert "airport_mean_c" not in result, "stale airport_mean_c key is back"
        assert "coolest_tile_mean_c" in result
        blob = f"{result['test_name']} {result['interpretation']}".lower()
        assert "airport" not in blob, f"'airport' still in reported text: {blob}"

    def test_interpretation_does_not_overclaim_a_negligible_effect(self):
        """A small p-value on n=12 must not be sold as a large real-world effect."""
        result = self._divergence()
        interp = result["interpretation"].lower()
        if abs(result["cohens_d"]) < 0.5:
            assert result["effect_size"] in ("NEGLIGIBLE", "SMALL")
            assert "negligible" in interp or "small" in interp, (
                "effect size is not large, but the interpretation omits that"
            )
            assert "confirms the microclimate heat trap" not in interp

    def test_gold_dataset_exposes_the_renamed_column(self):
        """Guards the notebook and docs, which both index this column by name."""
        from src.data_science.etl_pipeline import ThermalDataPipeline
        gold = ThermalDataPipeline().run_full_pipeline()
        assert "coolest_tile_2m_c" in gold.columns
        assert "airport_reference_temp_c" not in gold.columns
