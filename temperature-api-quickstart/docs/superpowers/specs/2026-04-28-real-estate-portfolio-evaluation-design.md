# Real-Estate Portfolio Heat Evaluation — Design Spec

- **Date:** 2026-04-28
- **Target file (modified in place):** `notebooks/use_cases/real_estate_portfolio_heat_risk.ipynb`
- **Pattern reference (idea only, not data):** `notebooks/use_cases/urban_planner_bus_stop_prioritization.ipynb`
- **Untouched:** `notebooks/use_cases/urban_forestry_tree_prioritization.ipynb`, the bus-stop notebook, all other use-case notebooks
- **Status:** Approved for implementation

## 1. Audience and goal

A **real-estate agent** (primary) preparing a portfolio review with a client, plus REIT asset managers / portfolio-investment leads / property operations (secondary). The notebook produces a defensible, slide-ready heat evaluation of a 10-property San Jose portfolio, with two scores per asset (risk and opportunity), business-translated numbers, three folium maps, four matplotlib charts, and a CSV ready to paste into a CRM or client report. The notebook runs end-to-end without API keys when `CACHED=True` (default).

## 2. Scope

**In scope**
- Rewrite the existing real-estate notebook into a 10-step workflow.
- Wire in the 6 new `data/real_*_san_jose_*` files as the primary data source (in cached mode).
- Add cached/offline duals for all four FortyGuard endpoints: `create_heatmap`, `satellite_segmentation`, `street_view_segmentation`, `environmental_parameters`.
- Add diurnal (24-hour) temperature analysis per property (peak temp, peak hour, min temp, swing, AOI percentile).
- Add a street-view ground-truth step (was not in current notebook).
- Add an opportunity score alongside the existing heat-risk score.
- Re-tune heat-risk weights to `0.40 / 0.20 / 0.20 / 0.20`.
- Refresh maps and charts; rename the output CSV to `outputs/portfolio_evaluation.csv`.
- Reference the heat-intelligence PDF as a hyperlink at the end.

**Out of scope**
- Any retrofit-tagging rule (`cool roof`/`shade trees`/etc.) — explicitly excluded.
- Renaming the data files (the `real_state_*` typo on 5 of 6 files is preserved).
- Touching any other notebook.
- Changing the FortyGuard SDK or any code outside the target notebook.
- Embedding the heat-intelligence PDF inline (link only).

## 3. Inputs

| Path | Used in step | Mode |
|---|---|---|
| `data/real_estate_san_jose_portfolio_sample.csv` | Step 1 | always |
| `data/real_state_san_jose_heatmap_sample_day_2024-10-02.geojson` | Step 2b | `CACHED=True` |
| `data/real_state_san_jose_satellite_segmentation_sample_day_2024-10-02.json` | Step 6b | `CACHED=True` (P01 only) |
| `data/real_state_san_jose_street_view_segmentation_sample_day_2024-10-02.json` | Step 7b | `CACHED=True` (P01 only) |
| `data/real_state_san_jose_env_paramaters_sample_day_2024-10-02.json` | Step 8b | `CACHED=True` (P01 only) |
| `data/real_state_san_jose_heat_intelligence_sample_day_2024-10-02.pdf` | Step 10 | hyperlink only |

The portfolio CSV schema is `property_id, name, type, year_built, sqft, market_value_musd, latitude, longitude` (10 rows, total ~$2.1B and ~2.7M sqft).

## 4. Configuration constants (top of notebook)

```
STUDY_DATE          = '2024-10-02'         # matches cached files
STUDY_HOUR          = '14:00'              # design-peak snapshot for online API
GRANULARITY_M       = 100                  # heatmap resolution
TOP_N_TO_ENRICH     = 3                    # API budget for satellite / env-params
CACHED              = True                 # default; flip to False for live API
BASELINE_C          = 24.0                 # comfortable-baseline reference
COOLING_KWH_PER_SF  = 0.18                 # extra kWh per sf per °C above baseline
KWH_PRICE_USD       = 0.24                 # electricity price
SLA_HI_C            = 32.0                 # tenant-comfort heat-index threshold (°C)
TEMP_C_SANITY       = (15.0, 55.0)         # F→C conversion sanity check
```

## 5. Notebook structure — 10 steps

### Setup
Imports, `dotenv`, ROOT path, `FortyGuardClient()`, constants, file paths, single-line "Authenticated to <base_url>" print.

### Step 1 — Load your portfolio
Read CSV, print `assets / total $ / total sqft / asset-type counts`, display the dataframe.
Markdown frames the agent take-away: "this is the book we're screening."

### Step 2 — Heat layer
- **2a (online, when `CACHED=False`):** `client.create_heatmap(polygon_aoi=SAN_JOSE_POLYGON, start_date=STUDY_DATE, start_time=STUDY_HOUR, filter_type=1, granularity=GRANULARITY_M)`. Single hour.
- **2b (cached, default):** load `real_state_san_jose_heatmap_sample_day_2024-10-02.geojson`. Each feature has `properties` keyed `'00'..'23'` (hourly) plus `min_temperature/max_temperature/average_temperature` (all in **°F**).
  - Convert °F→°C with sanity assert (every tile peak temperature must be within `TEMP_C_SANITY`).
  - Build helper `tile_temp_at(lat, lon, hour: int)` → °C, with point-in-polygon lookup and nearest-centroid fallback.
- AOI in cached mode = bounding box of the geojson features (derived dynamically). AOI in online mode = `SAN_JOSE_POLYGON`.
- Print: tile count, AOI bounds (lat/lon range), portfolio-wide temperature range.

### Step 3 — Diurnal temperature attach (per property)
For each property compute and attach:
- `peak_temp_c` (max over 24 hours of the property's tile)
- `peak_hour` (argmax, 0–23)
- `min_temp_c`
- `diurnal_swing_c` = `peak_temp_c - min_temp_c`
- `aoi_percentile` (rank of `peak_temp_c` against the full 16,507-tile distribution of `max_temperature`).

Sort by `peak_temp_c` descending, insert `temp_rank`. Display analysis-ready table (T1).

### Step 4 — Portfolio overview map (M1)
Folium, `cartodbpositron`, centered on portfolio centroid, zoom ~13.
`CircleMarker` per property: radius scales with `peak_temp_c`, color from a fixed asset-type palette (Office / Residential / Retail / Mixed-Use / Industrial). Popup shows `name`, `$ value (M)`, `sqft`, `peak_temp_c`, `peak_hour`, `aoi_percentile`. Add a legend (HTML `MacroElement`) for asset-type colors.

### Step 5 — Above-average hot exposures (zoom)
Filter to `peak_temp_c >= portfolio median peak_temp_c`. New zoomed folium map (M2): underlay = a sampled subset of AOI tiles whose `max_temperature` is at or above the AOI 90th percentile (rendered as red translucent polygons, capped at ~500 tiles for browser performance); overlay = the above-average properties. Display the hot-exposures table.

### Step 6 — Surface diagnosis (satellite segmentation)
- **6a (online, when `CACHED=False`):** loop over the top-N exposures, call `client.satellite_segmentation(latitude, longitude, start_date=STUDY_DATE, start_time=STUDY_HOUR, filter_type=1, granularity=GRANULARITY_M)`.
- **6b (cached, default):** load the cached JSON. The cache covers only **property P01** (Adobe Campus Tower, 37.2963, -121.8341).
  - The notebook prints a clear `⚠` notice in markdown: "Cached deep-dive applies to P01 only. Set `CACHED=False` to enrich the full top-N."
  - The notebook continues with whatever properties match the cached coordinate (here just P01).
- Compute `impervious_pct` (sum of road/pavement/building/sidewalk/earth segment values) and `vegetation_pct` (sum of tree/grass/vegetation values), using the existing keyword-bucket helper.
- Render stacked bar chart C2 (matplotlib) of segment classes for the available enriched properties.

### Step 7 — Street-view ground truth on #1
"Property #1" is defined as the highest-`temp_rank` property *within the enriched subset* from Step 6 (in cached mode this is P01; in online mode it is the top of the top-N).
- **7a (online, when `CACHED=False`):** `client.street_view_segmentation` for property #1.
- **7b (cached, default):** load `real_state_san_jose_street_view_segmentation_sample_day_2024-10-02.json` (front view only).
- Side-by-side rendering: original image | segmented image. The cached JSON exposes both via `front.original_image` and `front.segmented_image`. Use `IPython.display.HTML` to render both as base64-data URLs side-by-side.
- Print front-view composition table (sky / building / tree / road / sidewalk / car / grass).
- Markdown caveat: "Imagery date 2022-10-01 (front view only)."

### Step 8 — Diurnal driver profile (env-params)
- **8a (online, when `CACHED=False`):** loop over top-N, `client.environmental_parameters(latitude, longitude, temperature=peak_temp_c, start_date=STUDY_DATE, start_time='09:00', end_time='18:00', filter_type=2)`.
- **8b (cached, default):** load `real_state_san_jose_env_paramaters_sample_day_2024-10-02.json`. Has 1 location (P01), 24 hourly readings; the notebook business-hours window (09–18) is sliced from indices 9..18.
- Per available property, compute:
  - `peak_heat_index_c` (max of `parameters.heat_index_celsius`)
  - `peak_apparent_temp_c`
  - `hours_above_sla` (count where `heat_index_celsius > SLA_HI_C` within 09–18)
  - `peak_solar_irradiance` (max of `solar_irradiance`)
- Render chart C3 for property #1 as a 2-row matplotlib subplot (shared x-axis = 0..23 hours):
  - **Top subplot:** HI and apparent_temp on the primary y-axis (°C); RH on a twin y-axis (%). Horizontal dashed reference line at `SLA_HI_C` on the primary axis.
  - **Bottom subplot:** solar irradiance (W/m²).

### Step 9 — Composite scores (TWO scores)
Min-max normalize on the analyzed subset (the available enriched properties — full top-N online, P01 only when cached):

```
temp_n   = mm(peak_temp_c)
imp_n    = mm(impervious_pct)
hi_n     = mm(peak_heat_index_c)
sla_n    = mm(hours_above_sla)
veg_def  = mm(100 - vegetation_pct)

heat_risk_score   = 0.40·temp_n + 0.20·imp_n + 0.20·hi_n + 0.20·sla_n
opportunity_score = 0.50·temp_n + 0.30·imp_n + 0.20·veg_def
```

Min-max degenerate case (single property in cached mode): `mm` returns 0 for any constant column, so both scores resolve to 0 for the single property. The notebook prints a notice when the analyzed subset has fewer than 3 properties, and explicitly states the scores are not comparable to a multi-asset run. **No retrofit tagging.** Show ranked table with both scores side-by-side.

### Step 10 — Business translation + investment summary
For every property in the portfolio (not only enriched):

- `cooling_opex_uplift_usd = max(0, peak_temp_c - BASELINE_C) × sqft × COOLING_KWH_PER_SF × KWH_PRICE_USD`, rounded to whole dollars (existing formula, applied to `peak_temp_c` rather than single-hour `temperature_c`).
- `insurance_tier`: A (`heat_risk_score < 0.33`), B (`< 0.67`), C (`≥ 0.67`); `unranked` for properties not in the analyzed subset.
- `comfort_sla_risk` = `peak_heat_index_c > SLA_HI_C` (boolean, `None` if no env-params).

Final folium map M3: priority circles ∝ `heat_risk_score` (analyzed subset) + city-wide 90th-percentile tile overlay.

Chart C4 (matplotlib): scatter `heat_risk_score` (x) vs `opportunity_score` (y), 4 quadrants labeled (Hold / Watch / Treat / Divest framing for the agent — quadrant labels only, no tag column added to the data).

Optional chart C1 (matplotlib): per-property diurnal temperature curves for the analyzed subset.

Write `outputs/portfolio_evaluation.csv` with columns:
`temp_rank, property_id, name, type, sqft, market_value_musd, peak_temp_c, peak_hour, diurnal_swing_c, aoi_percentile, impervious_pct, vegetation_pct, peak_heat_index_c, hours_above_sla, heat_risk_score, opportunity_score, cooling_opex_uplift_usd, insurance_tier, comfort_sla_risk`.

Print aggregate `cooling_opex_uplift_usd.sum()` for the portfolio.

End-of-notebook markdown contains the link:
`[Download the heat-intelligence PDF report](../../data/real_state_san_jose_heat_intelligence_sample_day_2024-10-02.pdf)` — link only, do not embed.

### Wrap-up
Markdown table summarizing artifacts (M1/M2/M3, C1–C4, T1–T3, L1) and the audience for each (slide deck / CRM / client / committee), and a one-paragraph note on rerunning with `CACHED=False` against any portfolio.

## 6. Output artifacts (canonical)

| ID | Artifact | Format | Step |
|---|---|---|---|
| M1 | Portfolio overview map | folium | 4 |
| M2 | Hot-exposures zoom map | folium | 5 |
| M3 | Final ranked priority map | folium | 10 |
| C1 | Diurnal temperature curves | matplotlib | 10 |
| C2 | Surface composition stacked bar | matplotlib | 6 |
| C3 | HI / apparent / RH / solar curve (#1) | matplotlib | 8 |
| C4 | Risk vs Opportunity scatter (4 quadrants) | matplotlib | 10 |
| T1 | Analysis-ready portfolio table | DataFrame | 3 |
| T2 | Top-N enriched table | DataFrame | 6 / 8 |
| T3 | `outputs/portfolio_evaluation.csv` | CSV | 10 |
| L1 | Hyperlink to PDF report | markdown | 10 |

## 7. File-mode contract

`CACHED=True` (default):
- Step 2b reads the geojson, no API call.
- Step 6b/7b/8b read JSON caches that cover only P01 — the notebook continues with the cache's coverage and prints a notice.
- Notebook is fully runnable with no `.env` / no API key.

`CACHED=False`:
- Step 2a calls `create_heatmap` (single-hour). Diurnal columns `peak_*`, `min_temp_c`, `diurnal_swing_c`, `aoi_percentile` are degenerate — they collapse to the single-hour temperature with `peak_hour=STUDY_HOUR` and `diurnal_swing_c=0`. The notebook prints a banner that diurnal analysis is meaningful only with the cached 24-hour geojson (or a future 24-hour API call), and the rest of the workflow proceeds unchanged.
- Steps 6a/7a/8a call APIs for the full top-N (and #1 for street view).

## 8. Data-quality assumptions enforced

| # | Item | Mitigation |
|---|---|---|
| Q1 | Heatmap geojson is in °F. | Convert F→C on load; assert `TEMP_C_SANITY = (15, 55)` on the maximum across all tiles. |
| Q2 | Cached deep-dive covers P01 only. | Markdown notice + automatic fallback. Scoring is computed on whichever subset is available. |
| Q3 | Filename typos (`real_state_*` vs `real_estate_*`). | Reference each path verbatim; do not rename. |
| Q4 | Imagery dates differ across cached files. | Print imagery dates next to each step. |
| Q5 | Portfolio CSV lacks operational fields. | Keep the existing `0.18 kWh/sf/°C` heuristic, expose it as a constant, footnote in markdown. |
| Q6 | `STUDY_DATE` mismatch with cached files. | Set `STUDY_DATE = '2024-10-02'` (matches cache). |
| Q7 | AOI bounds in cached mode may differ from `SAN_JOSE_POLYGON`. | In cached mode AOI is derived from geojson feature bounds; in online mode it is `SAN_JOSE_POLYGON`. |

## 9. Acceptance criteria

The implementation is complete when **all** are true:

1. Running the notebook top-to-bottom with `CACHED=True` and no API key produces, without exceptions: M1, M2, M3, C1, C2, C3, C4, T1, T2, T3, and the PDF hyperlink.
2. `outputs/portfolio_evaluation.csv` exists and has all 19 columns listed in §5 Step 10, one row per property (10 rows).
3. The intro paragraphs lead with "real-estate agent" as primary audience.
4. The four FortyGuard endpoints are each demonstrated with explicit `CACHED` dual-paths in their respective steps.
5. F→C conversion sanity assert passes on the cached geojson without manual override.
6. Setting `CACHED=False` and rerunning Steps 1, 2a, and 3–10 succeeds against a live API key (the diurnal columns will be degenerate as documented).
7. The tree notebook and the bus-stop notebook are byte-identical to their pre-change versions (`git diff` shows no changes there).

## 10. Out-of-scope follow-ups (not done in this change)

- Standardize file naming to `real_estate_*` (would require renaming 5 files and updating any other references).
- Build a portfolio-wide cache (env-params, satellite, street-view for all 10 properties) so the cached deep-dive covers more than P01.
- Provide a 24-hour heatmap from the live API (current SDK exposes a single-hour call only).
- A formal HVAC / cooling-system data join to refine the OpEx uplift formula.
