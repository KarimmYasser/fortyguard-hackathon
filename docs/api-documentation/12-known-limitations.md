# Known Limitations & Plan Comparison - FortyGuard Temperature API®

> **Official Docs Source:** [https://docs-api.fortyguard.com/docs/limitations](https://docs-api.fortyguard.com/docs/limitations)

This document details the operational, technical, geographic, and subscription constraints governing the FortyGuard Temperature API®.

---

## 📊 Plan Limits Matrix

| Capability | API Basic | API Premium | API Startup |
| :--- | :--- | :--- | :--- |
| **Monthly Credits** | **1,000,000** | **5,000,000** | **1,000,000** |
| **Commercial License** | Included | Included | Included |
| **Heatmap Generation (Max Area)** | **Up to 10 mi²** | **Up to 50 mi²** | **Up to 10 mi²** |
| **Map Statistics** | Full access | Full access | Full access |
| **Environmental Parameters** | Up to 3 parameters/request | **Full access to all parameters** | Up to 3 parameters/request |
| **Satellite View Segmentation** | ❌ Not included | **✅ Included** | ❌ Not included |
| **Street View Segmentation** | ❌ Not included | **✅ Included** | ❌ Not included |
| **Heat Intelligence Reports** | ❌ Not included | **✅ Included** | ❌ Not included |
| **Access Window** | Monthly (renews each cycle) | Monthly (renews each cycle) | 6 months (one-time) |
| **Regional Coverage** | United States only | United States only | United States only |

---

## ⚙️ Input Constraints & Validation Rules

Requests violating these constraints return `400 Bad Request` and are **not charged** against your credit balance:

1. **Coordinates:**
 - `latitude` must be in range `[-90, 90]`.
 - `longitude` must be in range `[-180, 180]`.
 - In the current release, coordinates must fall within the **United States**.
2. **Polygon Area of Interest (AOI):**
 - Must be a valid GeoJSON `FeatureCollection` or `Feature` whose geometry is a closed `Polygon` (first and last coordinate vertices must be identical).
 - Maximum area limit: $le 10	ext{ mi}^2$ on Basic/Startup, $le 50	ext{ mi}^2$ on Premium.
3. **Date & Time Formatting:**
 - `start_date` and `end_date` must be formatted as `YYYY-MM-DD`.
 - `start_time` and `end_time` must be formatted as `HH:MM` in 24-hour time.
4. **Date Range & Forecasting Rules:**
 - Historical lower bound: `2019-01-01`.
 - Heatmap forecasting upper bound: `now + 12 hours`.
 - Any date prior to 2019-01-01 or exceeding +12h forecast is rejected with `400 Bad Request`.
 - For Satellite, Streetview, Environmental Parameters, and Heat Intelligence, date/time should match the heatmap generated for the same location.
5. **Filter Types:**
 - `filter_type` must be `1` (Single Hour), `2` (Range of Hours, max 23h), `3` (Single Day), or `4` (Range of Days, max 1 month).
6. **Granularity:**
 - Must be one of `60m`, `80m`, or `100m`.
7. **Heat Intelligence Analysis:**
 - `analysis` array must be a subset of `["geographic", "environmental", "urban", "events", "anthropogenic"]`.

---

## 💳 Billing & Credit Rules

- **Deduction Trigger:** Credits are deducted **only** upon successful task completion (`status: "Completed"`).
- **Failed Tasks:** Tasks failing during engine execution (`status: "Failed"`) do **not** consume credits.
- **Cycle Rollover:** Unused monthly credits do not roll over; they reset on your `credits_reset_date`.
- **Support Contact:** If you encounter unexpected behavior or limits, reach out to `support@fortyguard.com`.
