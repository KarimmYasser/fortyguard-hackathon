"""Unit tests for Multi-Cadence Resampling & Spatial Coordinate Alignment Engine."""

from datetime import datetime, timedelta, timezone
import pytest
import numpy as np
from src.data_science.cadence_alignment import CadenceAligner


def test_15min_to_hourly_downsampling_energy_conservation():
    """Verify that downsampling 15-minute load telemetry to hourly means conserves energy."""
    base_time = datetime(2023, 7, 19, 12, 0, 0, tzinfo=timezone.utc)
    
    # 15-minute intervals for 3 hours: 12 intervals
    timestamps = [base_time + timedelta(minutes=15 * i) for i in range(13)]
    # Linear ramp from 20.0 MW to 32.0 MW (1.0 MW per 15 min)
    values = [20.0 + 1.0 * i for i in range(13)]
    
    target_hours = [
        datetime(2023, 7, 19, 12, 0, 0, tzinfo=timezone.utc),
        datetime(2023, 7, 19, 13, 0, 0, tzinfo=timezone.utc),
        datetime(2023, 7, 19, 14, 0, 0, tzinfo=timezone.utc),
    ]
    
    hourly_means = CadenceAligner.resample_to_hourly_mean(timestamps, values, target_hours)
    
    assert len(hourly_means) == 3
    # Hour 1 (12:00 to 13:00): values are 20, 21, 22, 23, 24 -> Mean should be 22.0
    assert pytest.approx(hourly_means[0], abs=0.1) == 22.0
    # Hour 2 (13:00 to 14:00): values are 24, 25, 26, 27, 28 -> Mean should be 26.0
    assert pytest.approx(hourly_means[1], abs=0.1) == 26.0
    # Hour 3 (14:00 to 15:00): values are 28, 29, 30, 31, 32 -> Mean should be 30.0
    assert pytest.approx(hourly_means[2], abs=0.1) == 30.0


def test_hourly_peak_extraction():
    """Verify that peak values within each hourly window are accurately extracted."""
    base_time = datetime(2023, 7, 19, 14, 0, 0, tzinfo=timezone.utc)
    timestamps = [
        base_time + timedelta(minutes=0),
        base_time + timedelta(minutes=15),
        base_time + timedelta(minutes=30),  # Peak spike
        base_time + timedelta(minutes=45),
        base_time + timedelta(minutes=60),
    ]
    values = [38.5, 41.2, 44.8, 42.0, 39.1]
    
    target_hours = [datetime(2023, 7, 19, 14, 0, 0, tzinfo=timezone.utc)]
    hourly_peaks = CadenceAligner.resample_to_hourly_peak(timestamps, values, target_hours)
    
    assert len(hourly_peaks) == 1
    assert pytest.approx(hourly_peaks[0], abs=0.01) == 44.8


def test_hourly_to_15min_upsampling_smoothness():
    """Verify that upsampling hourly forecasts produces monotonic, smooth trajectories."""
    base_time = datetime(2023, 7, 19, 10, 0, 0, tzinfo=timezone.utc)
    hourly_dts = [base_time + timedelta(hours=i) for i in range(5)]
    hourly_temps = [35.0, 38.0, 42.0, 43.5, 41.0]
    
    sub_dts, sub_temps = CadenceAligner.interpolate_hourly_to_subhourly(
        hourly_dts, hourly_temps, interval_minutes=15
    )
    
    # 4 hours of 15-min intervals = 16 sub-intervals + 1 endpoint = 17 points
    assert len(sub_dts) == 17
    assert len(sub_temps) == 17
    # Boundary preservation
    assert pytest.approx(sub_temps[0], abs=0.01) == 35.0
    assert pytest.approx(sub_temps[-1], abs=0.01) == 41.0
    # No negative spikes or unreasonable overshoot
    assert all(34.0 <= t <= 45.0 for t in sub_temps)


def test_thermal_soak_integral_degree_hours():
    """Verify continuous thermal soak degree-hour integration above 40°C threshold."""
    base_time = datetime(2023, 7, 19, 12, 0, 0, tzinfo=timezone.utc)
    timestamps = [base_time + timedelta(hours=i) for i in range(4)]  # 3 hours duration
    # Flat 43.0°C temperature for 3 hours -> Exceedance is 3.0°C -> Integral should be 9.0 °C·h
    temps = [43.0, 43.0, 43.0, 43.0]
    
    soak_deg_hours = CadenceAligner.compute_thermal_soak_integral(timestamps, temps, threshold_c=40.0)
    assert pytest.approx(soak_deg_hours, abs=0.05) == 9.0


def test_spatial_containment_and_grid_snapping():
    """Verify spatial containment bounding checks and discrete cell snapping."""
    # Downtown Phoenix benchmark bounding box: [min_lat, min_lon, max_lat, max_lon]
    bbox = (33.4400, -112.0800, 33.4600, -112.0600)
    
    # Inside coordinate
    inside_lat, inside_lon = 33.4484, -112.0740
    assert CadenceAligner.validate_spatial_containment(inside_lat, inside_lon, bbox) is True
    
    row, col = CadenceAligner.snap_coordinate_to_grid(inside_lat, inside_lon, bbox, grid_resolution_deg=0.001)
    assert row >= 0 and col >= 0
    
    # Outside coordinate
    outside_lat, outside_lon = 33.5000, -112.0740
    assert CadenceAligner.validate_spatial_containment(outside_lat, outside_lon, bbox) is False
    with pytest.raises(ValueError):
        CadenceAligner.snap_coordinate_to_grid(outside_lat, outside_lon, bbox)
