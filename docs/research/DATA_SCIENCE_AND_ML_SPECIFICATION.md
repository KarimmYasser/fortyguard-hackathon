# 📊 Data Science, Engineering & Machine Learning Architecture Specification
> **Thermal Sentinel Grid — IBM Data Science Professional Methodology Specification**  
> *Track 06 (Agentic AI) & Track 02 (Future Buildings & Energy) — FortyGuard Hackathon '26*

---

## 🏛️ 1. Executive Data Science Architecture

To bridge the gap between microscopic physical differential equations and macroscopic city-scale decision intelligence, Thermal Sentinel Grid integrates a full **Medallion Data Engineering & Machine Learning Architecture**:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                          DATA SCIENCE LIFECYCLE (IBM METHODOLOGY)                           │
│                                                                                             │
│  [1. INGESTION]          [2. DATA ENGINEERING]       [3. ML SURROGATE & ANALYTICS]          │
│   • FortyGuard tOS API    • Bronze Layer: Raw JSON    • Physics Surrogate: Ridge Poly-2     │
│   • SCADA Telemetry Logs  • Silver Layer: Imputed     • Anomaly Detection: Isolation Forest │
│   • 16 SQLite/Supabase DB • Gold Layer: 18 Features   • Reliability: Weibull Survival (RUL) │
│                                                                                             │
│  [4. HYPOTHESIS TESTING] [5. REST ANALYTICS API]     [6. INTERACTIVE BI & JUPYTER]          │
│   • t-Test: p = 1.7e-5    • GET /analytics/eda        • React Data Science Studio Tab       │
│   • Cohen's d = 0.024 NEG • GET /analytics/correlation• notebooks/Thermal_Sentinel_DS.ipynb │
│   • Pearson/Spearman Heat • POST /analytics/surrogate • Automated Model Metrics Cards       │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ 2. Medallion ETL Pipeline (Bronze $\to$ Silver $\to$ Gold)

Implemented in [`src/data_science/etl_pipeline.py`](../../src/data_science/etl_pipeline.py):

### 🥉 Bronze Layer: Raw Ingestion
- Ingests raw telemetry and FortyGuard polygon heatmaps across 12-hour hourly steps.
- Gathers physical boundary conditions: wind speed ($v$), wet-bulb temperature ($T_{\text{wb}}$), solar flux ($S$), soil moisture ($\theta_v$), and urban canyon aspect ratios ($H/W$).

### 🥈 Silver Layer: Cleaning & Type Alignment
- Eliminates sensor gaps and null values via robust median imputation.
- Performs timezone and timestamp parsing, ensuring sequential time-series ordering.
- Aligns the AOI's coolest measured 2m tile ($T_{2\text{m,coolest}}$) against its hottest ($T_{2\text{m}}$). Both come from FortyGuard `tcm` heatmap tiles; neither is an airport station.

### 🥇 Gold Layer: Domain Feature Store (18 Features)
1. `delta_microclimate_c` (alias `intra_aoi_spread_c`): $T_{2\text{m}} - T_{2\text{m,coolest}}$ (°C).
2. `rolling_3h_avg_ambient`: 3-hour backward moving average of ambient exposure.
3. `cumulative_degree_hours_above_40`: Continuous thermal exceedance integral ($H_{40} = \int \max(0, T_{2\text{m}} - 40)\,dt$).
4. `thermal_soak_index_derived`: Persistence-to-duration ratio quantifying heat penetration.
5. `estimated_top_oil_rise_c`: Non-linear IEEE C57.91 steady-state oil rise under cooling derate.
6. `estimated_winding_gradient_c`: Winding-to-oil temperature differential.
7. `estimated_hot_spot_c`: Peak conductor hot-spot temperature ($T_{\text{hs}}$).
8. `safety_margin_c`: Headroom to the IEEE 140°C thermal runaway threshold ($140 - T_{\text{hs}}$).
9. `aging_factor_v`: Arrhenius insulation degradation rate multiplier ($V(T_{\text{hs}})$).
10. `soil_resistivity_regime`: Categorical dry-out state (`WET` / `TRANSITION` / `DRY`).
11. `aging_acceleration_bin`: Risk classification (`NORMAL` / `ACCELERATED` / `CRITICAL`).
12. `load_peak_flag`: Binary indicator for load ratio $K > 0.85$.
13. `canyon_wind_regime`: Aerodynamic sheltering classification (`OPEN` / `MODERATE_SHELTER` / `DEEP_CANYON`).
14. `is_solar_peak`: 10:00 AM – 3:00 PM high-irradiance flag.
15. `hour_of_day`: Clock hour index (06:00 to 18:00).
16. `bess_soc_gradient`: Rate-of-change of battery state of charge ($\Delta \text{SoC}/\Delta t$).
17. `moisture_risk_level`: Fickian cellulose moisture risk tier (`HIGH_RISK` / `CAUTION` / `SAFE`).
18. `diurnal_recovery_deficit`: Overnight residual heat accumulation above pre-heatwave baseline.

---

## 🤖 3. Machine Learning Models & Physics Surrogates

Implemented in [`src/data_science/ml_models.py`](../../src/data_science/ml_models.py):

### Model 1: Polynomial Ridge Physics-Surrogate Regressor
- **Problem:** Full discrete-time ODE solvers (IEEE C57.91) require $\approx 5\text{ms}$ per asset. City-scale operations across 10,000+ distribution transformers demand sub-millisecond screening.
- **Formulation:** Degree-2 Polynomial Feature Expansion + $\ell_2$-regularized Ridge Regression:

$$\min_w \left\Vert X_{\mathrm{poly}} w - y \right\Vert_2^2 + \alpha \left\Vert w \right\Vert_2^2$$

- **Metrics:**
  - **$R^2$ Score:** **$0.9987$**
  - **Mean Absolute Error (MAE):** **$1.20^\circ\mathrm{C}$**
  - **Maximum Residual Error:** **$6.83^\circ\mathrm{C}$**
  - **Execution Speedup:** **$\approx 5000\times$ faster** than numerical ODE integration.

### Model 2: Sensor Drift & Thermal Anomaly Detector (Isolation Forest)
- **Problem:** Detect hardware sensor drift, cooling fan failures, or microclimate anomalies where observed temperatures deviate from FortyGuard predictions.
- **Formulation:** Unsupervised ensemble of isolation trees partitioning feature space $[T_{2\mathrm{m}}, \Delta T_{\mathrm{micro}}, K, \Delta\mathrm{SoC}, S(t), T_{\mathrm{hs}}]$ with an $8\%$ contamination boundary.
- **Output:** Flagged anomaly indicators with anomaly scores for SCADA triage.

### Model 3: Asset Reliability & Survival Analysis (Weibull Hazard)
- **Problem:** Forecast remaining asset lifetime under sustained heatwave stress.
- **Formulation:** Extreme value Weibull distribution fit on cumulative Arrhenius aging hours:

$$S(t) = \exp\left( -\left(\frac{t}{\lambda}\right)^k \right)$$
- **Results:**
  - **Weibull Shape ($k$):** $16.7582$
  - **Weibull Scale ($\lambda$):** $166,358.3\text{ hours}$
  - **Baseline Normal Life:** $20.5\text{ years}$ ($180,000\text{ hours}$)
  - **Median RUL:** $18.58\text{ years}$ ($162,759.4\text{ hours}$)
  - **Stress Adjusted RUL:** **$18.31\text{ years}$** (the $2.19\text{ years}$ of lifetime consumed by 31 days of extreme thermal soak).

> These figures moved after the replay and live agent were reconciled onto the
> same derate inputs. The earlier $k=12.74$, $\lambda=160{,}412$ and $17.42$-year
> RUL were fitted on the superseded $47.6^\circ\mathrm{C}$ ambient and overstated
> the damage. Reproduce with `GET /api/v1/analytics/ml-overview`.

---

## 🧪 4. Statistical Hypothesis Testing & EDA

Implemented in [`src/data_science/analytics_engine.py`](../../src/data_science/analytics_engine.py):

### Correlation Ranking: Tautology Filtering & Small-Sample Disclosure

A naive "Top 10 Strongest Correlations" over an engineered feature store ranks
its own formulas. `estimated_winding_gradient_c` is defined as $23 K^{0.8}$, so
its correlation with $K$ is $r \approx 1.0$ on *any* dataset - it is arithmetic,
not a finding, and it crowds the genuine signal out of the list.

`compute_correlation_analysis` therefore classifies every pair through
`_pair_kind(a, b)` before ranking:

| `kind` | Meaning | Example |
| :--- | :--- | :--- |
| `derived` | One feature is computed from the other | `baseline_load_ratio_k` ~ `estimated_hot_spot_c` ($r=0.9995$) |
| `structural` | Both are scaled off the same authored series | `fortyguard_2m_ambient_c` ~ `coolest_tile_2m_c` ($r=0.9999$) |
| `empirical` | Could have come out otherwise | `relative_humidity_pct` ~ `rolling_3h_avg_ambient` ($r=-0.9949$) |

Only `empirical` pairs enter `top_10_strongest_pairs`. Formula-linked pairs are
still returned, in a separate `tautological_pairs` list, so the filtering is
auditable rather than hidden. On the Phoenix gold set that boxes off **10 pairs**.

Alias propagation matters here: `hospital_critical_load_mw` tracks $K$ at
$r > 0.999$, so without treating it as a proxy the excluded `K ~ hot_spot`
relationship re-enters the headline list one hop removed.

**Small-sample disclosure.** The gold set is $n = 12$ hourly observations, far
below the $n \ge 30$ where a Pearson $r$ is stable. The payload therefore carries
`n_observations` and a `warnings` array stating that $|r|$ is directional only,
and every ranked pair reports its `p_value`. The dashboard renders both.

> **Leading empirical result:** `relative_humidity_pct` ~ `rolling_3h_avg_ambient`,
> $r = -0.9949$ ($p = 2.6 \times 10^{-11}$) - the expected inverse humidity/temperature
> coupling, recovered from measurement rather than asserted by a formula.

---

### Intra-AOI Thermal Divergence Paired $t$-Test
- **Comparison:** hottest versus coolest measured 2m tile inside the same AOI. The
  reference is the coolest *tile*, not an airport station - we probed Sky Harbor
  and it reads **warmer** than downtown, an airport ringed by runways being a
  heat island in its own right.
- **Null Hypothesis ($H_0$):** Mean difference $\mu_\Delta = T_{2\text{m,hottest}} - T_{2\text{m,coolest}} = 0$.
- **Statistical Results:**
  - Mean Hottest-Tile 2m Temp: **$40.75^\circ\mathrm{C}$**
  - Mean Coolest-Tile 2m Temp: **$40.70^\circ\mathrm{C}$**
  - Mean Delta: **$+0.06^\circ\mathrm{C}$** (Max: **$+0.19^\circ\mathrm{C}$**)
  - $t$-Statistic: **$4.2964$**, $p$-Value: **$1.74 \times 10^{-5} \ll 0.05$**
  - Cohen's $d$ Effect Size: **$0.0238$ (NEGLIGIBLE)**
- **Conclusion:** $H_0$ is rejected - the sign of the difference is reliable - but
  the **effect size is negligible**, so intra-AOI spread is *not* what drives the
  damage in this scenario. The mechanism is the **12-hour soak above $40^\circ\mathrm{C}$**,
  not a large spatial gradient. Reporting the $p$-value without the effect size
  would be the textbook significance-versus-magnitude error, and an earlier
  revision of this document did exactly that with a fabricated $d=0.87$ (LARGE)
  drawn from the superseded airport-reference framing.

---

## 🔬 5. Multi-Cadence Resampling & Spatial Bivariate Regression Engines

Following FortyGuard ML and Cloud Architecture guidance (Session 07), the data science suite includes two specialized engines:

### ⏱️ A. Multi-Cadence Resampling Engine (`src/data_science/cadence_alignment.py`)
- **Cadence Matching:** Aligns sub-hourly telemetry (e.g., 15-minute electrical SCADA loads or 5-minute MPPT solar inverter streams) with hourly FortyGuard forecasts using trapezoidal integration to strictly conserve total energy ($\int P(t) dt$).
- **Monotonic Spline Upsampling:** Employs Monotonic Cubic Hermite Spline (PCHIP) interpolation to upsample hourly forecasts to 15-minute intervals for continuous ODE evaluation without introducing artificial overshoots or derivative discontinuities.
- **Continuous Thermal Soak Integral:** Evaluates $S_{\text{thresh}} = \int \max(0, T(t) - T_{\text{thresh}})\,dt$ in degree-hours ($^\circ\mathrm{C}\cdot\text{h}$) to quantify cumulative heat penetration.
- **Spatial Containment & Grid Snapping:** Enforces coordinate bounds verification against FortyGuard raster bounding boxes and maps continuous lat/lon coordinates to discrete raster cells $(i, j)$ at $20\text{m}/60\text{m}$ resolution.

### 🗺️ B. Spatial Bivariate Regression Engine (`src/data_science/spatial_correlation.py`)
- **Canopy vs. Persistence Model:** Quantifies the mitigation effect of urban tree canopy on continuous thermal soak:

$$P_{40, i} = \beta_0 + \beta_1 \cdot \mathrm{CanopyPct}_i + \epsilon_i \quad (\beta_1 < 0, p < 0.01)$$

- **Asphalt vs. Microclimate Delta Model:** Quantifies convective air temperature rise over radiating impervious surfaces:

$$\Delta T_{2\mathrm{m}, i} = \alpha_0 + \alpha_1 \cdot \mathrm{AsphaltPct}_i + \epsilon_i$$

- **Canyon Aspect vs. Aerodynamic Cooling Throttling:** Evaluates radiator fin convective derate ($\eta_{\mathrm{cool}}$) against building canyon aspect ratios ($H/W$).
- **Moran's I Spatial Autocorrelation:** Verifies that spatial clustering of heat vulnerability is statistically non-random ($z > 1.96, p < 0.05$).

### 🌐 C. Multi-Modal Environmental Coupling & REST API Boundaries
- **Native FortyGuard API Parameters:** Ingests ground-level 2m convective air temperature ($\theta_{\text{amb}}$), solar irradiance components (GHI/DNI), wet-bulb temperature, and relative humidity directly from `POST /v1/env_params` and `/v1/heatmap` (TCM).
- **Aerodynamic Boundary Forcing:** Because wind speed and UV index are dashboard-connector features not yet exposed on the `/env_params` REST API, the aerodynamic canyon engine couples FortyGuard thermal rasters with regional boundary meteorological wind ($U_{\text{ref}} = 3.0\text{ m/s}$) to compute morphological sheltering ($\kappa_{\text{morph}}$) and equipment convective derates ($\eta_{\text{cool}}$).
- **Catalog Probe Resilience:** Gracefully handles unindexed date ranges (which return empty payloads rather than HTTP error codes) via strict bounding box validation and deterministic fixture fallback.


