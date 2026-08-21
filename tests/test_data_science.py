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
            "ambient_2m_c": 47.6,
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
        """Paired t-test p-value < 0.05 confirming systematic bias."""
        from src.data_science.etl_pipeline import ThermalDataPipeline
        from src.data_science.analytics_engine import ThermalAnalyticsEngine
        pipeline = ThermalDataPipeline()
        gold = pipeline.run_full_pipeline()
        engine = ThermalAnalyticsEngine()
        result = engine.compute_microclimate_divergence(gold)
        assert result["is_significant"], f"p-value = {result['p_value']} (expected < 0.05)"
        assert result["mean_delta_c"] > 0, "FortyGuard 2m should be warmer than airport"

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
