"""Unit tests for Spatial Bivariate Regression & Land-Cover Correlation Engine."""

import pytest
import numpy as np
from src.data_science.spatial_correlation import (
    SpatialCorrelationEngine,
    SpatialRegressionResult,
    MoransIResult,
)


def test_bivariate_ols_synthetic_exactness():
    """Verify OLS parameter estimation on a known linear system y = 2.5x + 10.0."""
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])
    y = 2.5 * x + 10.0
    
    result = SpatialCorrelationEngine.fit_bivariate_ols(
        x, y,
        model_id="test_model",
        title="Test Model",
        x_name="X Variable",
        x_unit="units",
        y_name="Y Variable",
        y_unit="units",
    )
    
    assert isinstance(result, SpatialRegressionResult)
    assert pytest.approx(result.slope, abs=1e-4) == 2.5
    assert pytest.approx(result.intercept, abs=1e-4) == 10.0
    assert pytest.approx(result.r_squared, abs=1e-4) == 1.0
    assert pytest.approx(result.pearson_r, abs=1e-4) == 1.0
    assert result.p_value < 1e-5


def test_canopy_persistence_regression():
    """Verify that tree canopy percentage exhibits a statistically significant negative slope with P40."""
    result = SpatialCorrelationEngine.compute_canopy_persistence_regression()
    
    assert result.model_id == "canopy_vs_persistence"
    assert result.slope < 0.0  # Canopy reduces persistence hours
    assert result.pearson_r < -0.60  # Negative correlation
    assert result.r_squared > 0.40  # Empirical R^2 on parcel grid
    assert result.p_value < 0.05  # Statistically significant
    assert len(result.scatter_points) == 12
    assert len(result.trendline_points) > 0



def test_asphalt_delta_t_regression():
    """Verify that asphalt coverage exhibits a positive correlation with 2m temperature delta."""
    result = SpatialCorrelationEngine.compute_asphalt_delta_t_regression()
    
    assert result.model_id == "asphalt_vs_delta_t"
    assert result.slope > 0.0  # More asphalt increases temperature delta
    assert result.r_squared > 0.70
    assert result.p_value < 0.01
    assert result.sample_size == 12


def test_canyon_aerodynamic_regression():
    """Verify urban canyon aspect ratio (H/W) correlation with convective cooling derate."""
    result = SpatialCorrelationEngine.compute_canyon_aerodynamic_regression()
    
    assert result.model_id == "canyon_aspect_vs_cooling_derate"
    assert result.slope > 0.0  # Deeper canyon increases derate %
    assert result.r_squared > 0.50
    assert result.p_value < 0.05


def test_morans_i_spatial_clustering():
    """Verify that Global Moran's I correctly detects spatial clustering in the parcel grid."""
    coords = np.array([[p["lat"], p["lon"]] for p in SpatialCorrelationEngine.DEFAULT_PARCEL_BENCHMARKS])
    values = np.array([p["p40_hours"] for p in SpatialCorrelationEngine.DEFAULT_PARCEL_BENCHMARKS])
    
    morans = SpatialCorrelationEngine.compute_morans_i_spatial_autocorrelation(coords, values, k_neighbors=3)
    
    assert isinstance(morans, MoransIResult)
    assert morans.morans_i > -1.0
    assert isinstance(morans.is_clustered, bool)
    assert morans.z_score != 0.0


def test_full_spatial_correlation_suite_payload():
    """Verify the comprehensive data science payload structure."""
    suite = SpatialCorrelationEngine.get_full_spatial_correlation_suite()
    
    assert suite["status"] == "success"
    assert "canopy_vs_persistence" in suite["models"]
    assert "asphalt_vs_delta_t" in suite["models"]
    assert "canyon_aspect_vs_cooling_derate" in suite["models"]
    assert "spatial_autocorrelation" in suite
    assert len(suite["summary_findings"]) >= 3
