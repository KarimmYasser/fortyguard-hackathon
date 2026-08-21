"""
FastAPI Routes for Data Science, Analytics & Machine Learning Studio
Provides ETL pipeline status, EDA, correlation analysis, risk profiling,
ML model metrics, and physics surrogate predictions.
"""

from __future__ import annotations

from typing import Any, Dict
from fastapi import APIRouter
from pydantic import BaseModel, Field

from src.data_science.etl_pipeline import ThermalDataPipeline
from src.data_science.ml_models import (
    PhysicsSurrogateModel,
    SensorAnomalyDetector,
    SurvivalAnalysisEngine,
)
from src.data_science.analytics_engine import ThermalAnalyticsEngine

router = APIRouter(prefix="/analytics", tags=["Data Science & Analytics Studio"])

# ── Singleton instances (cached across requests) ──
_pipeline = ThermalDataPipeline()
_surrogate = PhysicsSurrogateModel()
_anomaly_detector = SensorAnomalyDetector()
_survival_engine = SurvivalAnalysisEngine()
_analytics_engine = ThermalAnalyticsEngine()


class SurrogatePredictionRequest(BaseModel):
    """Input features for Physics Surrogate hot-spot prediction."""
    ambient_2m_c: float = Field(default=47.6, description="FortyGuard 2m ambient temperature (°C)")
    solar_irradiance: float = Field(default=960.0, description="Solar irradiance (W/m²)")
    load_ratio_k: float = Field(default=1.0, description="Per-unit load ratio K")
    cooling_derate_eta: float = Field(default=0.68, description="Canyon cooling derate factor")
    soil_resistivity: float = Field(default=2.45, description="Soil thermal resistivity (K·m/W)")
    canyon_hw_ratio: float = Field(default=1.85, description="Building canyon H/W aspect ratio")


@router.get("/pipeline-status")
async def get_pipeline_status() -> Dict[str, Any]:
    """Return ETL pipeline metadata and execution summary."""
    return _pipeline.get_pipeline_summary()


@router.get("/eda")
async def get_eda_summary() -> Dict[str, Any]:
    """
    Full Exploratory Data Analysis: descriptive statistics, distribution shapes,
    skewness, kurtosis, and null percentages for all Gold features.
    """
    gold_df = _pipeline.get_gold_dataset()
    eda = _analytics_engine.compute_eda_summary(gold_df)
    eda["pipeline"] = _pipeline.get_pipeline_summary()
    return eda


@router.get("/correlation")
async def get_correlation_analysis() -> Dict[str, Any]:
    """
    Pearson & Spearman correlation matrices with top-10 strongest feature pairs.
    """
    gold_df = _pipeline.get_gold_dataset()
    return _analytics_engine.compute_correlation_analysis(gold_df)


@router.get("/risk-distribution")
async def get_risk_distribution() -> Dict[str, Any]:
    """
    Risk tier distribution (LOW / MODERATE / HIGH / CRITICAL)
    based on IEEE C57.91 hot-spot temperature thresholds.
    """
    gold_df = _pipeline.get_gold_dataset()
    risk = _analytics_engine.compute_risk_distribution(gold_df)
    divergence = _analytics_engine.compute_microclimate_divergence(gold_df)
    temporal = _analytics_engine.compute_temporal_patterns(gold_df)
    return {
        "risk_distribution": risk,
        "microclimate_divergence": divergence,
        "temporal_patterns": temporal,
    }


@router.post("/ml-surrogate")
async def predict_with_surrogate(req: SurrogatePredictionRequest) -> Dict[str, Any]:
    """
    Run Physics Surrogate prediction for given input features.
    Returns predicted peak hot-spot temperature in sub-millisecond latency.
    """
    if not _surrogate.is_trained:
        _surrogate.train()

    predicted = _surrogate.predict_hotspot(req.model_dump())
    return {
        "predicted_peak_hot_spot_c": round(predicted, 2),
        "safety_margin_c": round(140.0 - predicted, 2),
        "risk_tier": "CRITICAL" if predicted >= 140 else "HIGH" if predicted >= 120 else "MODERATE" if predicted >= 100 else "LOW",
        "input_features": req.model_dump(),
        "model_metrics": _surrogate.get_metrics(),
    }


@router.get("/ml-overview")
async def get_ml_overview() -> Dict[str, Any]:
    """
    Returns all ML model metrics: Physics Surrogate R², Anomaly Detection counts,
    and Weibull RUL survival estimates.
    """
    gold_df = _pipeline.get_gold_dataset()

    # Train surrogate if needed
    if not _surrogate.is_trained:
        _surrogate.train()

    # Run anomaly detection
    anomaly_results = _anomaly_detector.train_and_detect(gold_df)

    # Run survival analysis
    survival_results = _survival_engine.fit_and_estimate(gold_df)

    return {
        "physics_surrogate": _surrogate.get_metrics(),
        "anomaly_detection": {
            k: v for k, v in anomaly_results.items() if k != "records"
        },
        "anomaly_records": anomaly_results.get("records", []),
        "survival_analysis": survival_results,
        "pipeline_summary": _pipeline.get_pipeline_summary(),
    }
