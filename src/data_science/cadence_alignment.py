"""Multi-Cadence Resampling, Time-Series Integration & Spatial Coordinate Alignment Engine.

Aligned with FortyGuard ML and Cloud Architecture guidance (Session 07):
- Enforces strict spatial containment and coordinate snapping to 20m/60m raster tiles.
- Handles multi-rate time series (e.g. 15-minute electrical SCADA loads vs 1-hour FortyGuard forecasts)
  using continuous moving integrals and trapezoidal energy conservation.
- Normalizes all timezone representations to UTC to eliminate spurious temporal phase shifts.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List, Tuple, Sequence, Dict, Any
import numpy as np


class CadenceAligner:
    """Utility class for multi-cadence time-series resampling and spatial coordinate bounds checking."""

    @staticmethod
    def normalize_to_utc(dt: datetime, default_tz: timezone = timezone.utc) -> datetime:
        """Ensure a datetime is timezone-aware and normalized to UTC."""
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=default_tz)
        return dt.astimezone(timezone.utc)

    @staticmethod
    def resample_to_hourly_mean(
        timestamps: Sequence[datetime],
        values: Sequence[float],
        target_hours: Sequence[datetime],
    ) -> List[float]:
        """Downsample high-frequency (e.g. 5-min or 15-min) telemetry to hourly means using trapezoidal integration.
        
        Preserves total energy under the curve: ∫ P(t) dt.
        """
        if len(timestamps) != len(values):
            raise ValueError("timestamps and values must have the same length")
        if not timestamps or not target_hours:
            return []

        ts_utc = [CadenceAligner.normalize_to_utc(t) for t in timestamps]
        val_arr = np.asarray(values, dtype=float)
        
        # Convert timestamps to epoch seconds
        t_sec = np.array([t.timestamp() for t in ts_utc])
        sort_idx = np.argsort(t_sec)
        t_sec = t_sec[sort_idx]
        val_arr = val_arr[sort_idx]

        hourly_means: List[float] = []
        for target_h in target_hours:
            h_utc = CadenceAligner.normalize_to_utc(target_h)
            h_start = h_utc.timestamp()
            h_end = h_start + 3600.0

            # Find points falling within [h_start, h_end]
            mask = (t_sec >= h_start) & (t_sec <= h_end)
            matching_t = t_sec[mask]
            matching_v = val_arr[mask]

            if len(matching_v) == 0:
                # Interpolate if within overall range, else nearest
                if h_start < t_sec[0]:
                    hourly_means.append(float(val_arr[0]))
                elif h_start > t_sec[-1]:
                    hourly_means.append(float(val_arr[-1]))
                else:
                    v_interp = float(np.interp(h_start + 1800.0, t_sec, val_arr))
                    hourly_means.append(v_interp)
            elif len(matching_v) == 1:
                hourly_means.append(float(matching_v[0]))
            else:
                # Trapezoidal integration across the window
                window_integral = np.trapezoid(matching_v, matching_t)
                window_duration = matching_t[-1] - matching_t[0]
                if window_duration > 0:
                    hourly_means.append(float(window_integral / window_duration))
                else:
                    hourly_means.append(float(np.mean(matching_v)))

        return hourly_means

    @staticmethod
    def resample_to_hourly_peak(
        timestamps: Sequence[datetime],
        values: Sequence[float],
        target_hours: Sequence[datetime],
    ) -> List[float]:
        """Extract the true peak telemetry value within each hourly window."""
        if len(timestamps) != len(values):
            raise ValueError("timestamps and values must have the same length")
        if not timestamps or not target_hours:
            return []

        ts_utc = [CadenceAligner.normalize_to_utc(t) for t in timestamps]
        val_arr = np.asarray(values, dtype=float)
        t_sec = np.array([t.timestamp() for t in ts_utc])

        hourly_peaks: List[float] = []
        for target_h in target_hours:
            h_utc = CadenceAligner.normalize_to_utc(target_h)
            h_start = h_utc.timestamp()
            h_end = h_start + 3600.0

            mask = (t_sec >= h_start) & (t_sec <= h_end)
            matching_v = val_arr[mask]
            if len(matching_v) > 0:
                hourly_peaks.append(float(np.max(matching_v)))
            else:
                v_interp = float(np.interp(h_start + 1800.0, t_sec, val_arr))
                hourly_peaks.append(v_interp)

        return hourly_peaks

    @staticmethod
    def interpolate_hourly_to_subhourly(
        hourly_datetimes: Sequence[datetime],
        hourly_values: Sequence[float],
        interval_minutes: int = 15,
    ) -> Tuple[List[datetime], List[float]]:
        """Upsample hourly FortyGuard forecasts to 15-minute intervals for ODE solver evaluation.
        
        Uses Monotonic Cubic Spline (PCHIP) to preserve derivative continuity without spurious oscillations.
        """
        if len(hourly_datetimes) != len(hourly_values):
            raise ValueError("hourly_datetimes and hourly_values must have the same length")
        if len(hourly_values) < 2:
            return list(hourly_datetimes), list(hourly_values)

        dts_utc = [CadenceAligner.normalize_to_utc(d) for d in hourly_datetimes]
        t_sec = np.array([d.timestamp() for d in dts_utc])
        val_arr = np.asarray(hourly_values, dtype=float)

        total_duration_sec = t_sec[-1] - t_sec[0]
        step_sec = interval_minutes * 60.0
        n_steps = int(np.round(total_duration_sec / step_sec)) + 1
        t_sub_sec = np.linspace(t_sec[0], t_sec[-1], n_steps)

        # Monotonic cubic interpolation or fallback linear
        try:
            from scipy.interpolate import PchipInterpolator
            pchip = PchipInterpolator(t_sec, val_arr)
            v_sub = pchip(t_sub_sec)
        except Exception:
            v_sub = np.interp(t_sub_sec, t_sec, val_arr)

        sub_dts = [datetime.fromtimestamp(ts, tz=timezone.utc) for ts in t_sub_sec]
        return sub_dts, [float(v) for v in v_sub]

    @staticmethod
    def compute_thermal_soak_integral(
        timestamps: Sequence[datetime],
        temperatures_c: Sequence[float],
        threshold_c: float = 40.0,
    ) -> float:
        """Compute the cumulative thermal soak integral above threshold_c in degree-hours (°C·h).
        
        S_thresh = ∫ max(0, T(t) - threshold_c) dt
        """
        if len(timestamps) != len(temperatures_c) or len(temperatures_c) < 2:
            return 0.0

        ts_utc = [CadenceAligner.normalize_to_utc(t) for t in timestamps]
        t_hours = np.array([(t.timestamp() - ts_utc[0].timestamp()) / 3600.0 for t in ts_utc])
        temp_arr = np.asarray(temperatures_c, dtype=float)

        exceedance = np.maximum(0.0, temp_arr - threshold_c)
        integral_deg_hours = float(np.trapezoid(exceedance, t_hours))
        return max(0.0, integral_deg_hours)

    @staticmethod
    def validate_spatial_containment(
        lat: float,
        lon: float,
        bbox: Tuple[float, float, float, float],
    ) -> bool:
        """Validate if coordinates (lat, lon) lie within bounding box (min_lat, min_lon, max_lat, max_lon)."""
        min_lat, min_lon, max_lat, max_lon = bbox
        return bool(min_lat <= lat <= max_lat and min_lon <= lon <= max_lon)

    @staticmethod
    def snap_coordinate_to_grid(
        lat: float,
        lon: float,
        bbox: Tuple[float, float, float, float],
        grid_resolution_deg: float = 0.0005,  # ~50-60m
    ) -> Tuple[int, int]:
        """Snap continuous lat/lon point to discrete raster grid cell indices (row, col)."""
        min_lat, min_lon, max_lat, max_lon = bbox
        if not CadenceAligner.validate_spatial_containment(lat, lon, bbox):
            raise ValueError(f"Coordinate ({lat}, {lon}) is outside bounding box {bbox}")

        row = int(np.floor((max_lat - lat) / grid_resolution_deg))
        col = int(np.floor((lon - min_lon) / grid_resolution_deg))
        return max(0, row), max(0, col)
