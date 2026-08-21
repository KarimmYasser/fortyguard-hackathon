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

---

## 🔬 Observed Constraints (Not In The Official Docs)

Measured during live integration. Full detail and reproduction steps in
[14 — Field Notes: Live Integration](./14-field-notes-live-integration.md).

| Observation | Practical consequence |
| :--- | :--- |
| **`env_params` echoes `location.temperature`** back unchanged — it is an index endpoint, not a measurement source. | Measured 2m air temperature is available **only** from `/v1/heatmap` with `analytic_type: "tcm"`. |
| **`cloud_cover_octas` is reported on a 0–100 percent scale**, despite the name (octas cap at 8). | Dividing by 8 produces attenuation factors below zero. Normalise by 100 and clamp. |
| **No time-series endpoint exists.** | An hourly curve requires N single-hour `tcm` calls (`filter_type: 1`) — the dominant cost and latency driver. |
| **Work appears to serialise per API key.** A small `env_params` job batched behind 12 heatmap jobs sat in `processing` for >600 s; the same call alone takes ~5 s. | Issue latency-sensitive calls first, and bound fan-out with a semaphore. |
| **`solar_irradiance.clear_sky.ghi` is a daily aggregate**, while the comfort indices are 24-point hourly arrays. | Hourly irradiance must be reconstructed from the daily total. |
| **`persistence` / `exceedance` use a flat stats shape** (`{units, n_cells, min, max, mean}`), unlike `tcm`'s nested `stats_data.temperature_stats`. | One parser cannot serve both analytic types. |
| **`overall_temperature_distribution` is a 5-point quantile summary**, not one entry per cell. | Use `n_cells` for the true tile count. |
| **Spatial contrast at 100m granularity is ~0.1–1 °C.** A 1.9 mi² AOI spans 0.06 °C; 7.7 mi² spans 0.31 °C. Sky Harbor airport measured *warmer* than downtown Phoenix. | Urban-heat-island deltas must be drawn against **natural land cover**, not against an airport station. |
| **Clock skew silently breaks everything.** A host clock ahead of the archive puts every request outside `2019-01-01 → now + 12h`. | Requests fail as `400` and any fallback path will mask it. Pin an explicit analysis date. |

### Measured latencies (Basic plan, ~1.9 mi², granularity 100m)

| Call | Cold |
| :--- | :--- |
| `env_params`, `filter_type: 3`, uncontended | ~5 s |
| `heatmap` `tcm`, `filter_type: 1` | ~20 s |
| `heatmap` `persistence` + `exceedance` concurrently | ~21 s |
| 12-hour scan (12 × `tcm`, semaphore 6) | ~90 s |
| Same scan from cache | ~1.2 s |

> A 12-hour scan exceeds the default serverless function timeout on most
> platforms. Cache by request hash and raise `maxDuration` accordingly.
