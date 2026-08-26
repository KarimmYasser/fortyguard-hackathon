# 📖 Technical & Scientific Glossary
> **Thermal Sentinel Grid — FortyGuard Hackathon '26**  
> *Author:* Karim Y. Azab (Karim Yasser)  
> *Repository:* [github.com/KarimmYasser/fortyguard-hackathon](https://github.com/KarimmYasser/fortyguard-hackathon)

This glossary provides authoritative, mathematically rigorous definitions for all scientific, physical, meteorological, power systems, AI/ML, and financial reliability terms used across the **Thermal Sentinel Grid** codebase, research specifications, and user interfaces.

---

## 📑 Table of Contents
1. [🌡️ FortyGuard API & Urban Microclimate Meteorology](#1-️-fortyguard-api--urban-microclimate-meteorology)
2. [⚡ Transformer Thermal Physics & Insulation Degradation (IEEE / IEC)](#2-⚡-transformer-thermal-physics--insulation-degradation-ieee--iec)
3. [🔌 Power Grid Operations, Dynamic Line Rating & Power Flow](#3-🔌-power-grid-operations-dynamic-line-rating--power-flow)
4. [🔋 Battery Energy Storage Systems (BESS) & Electro-Thermal Mechanics](#4-🔋-battery-energy-storage-systems-bess--electro-thermal-mechanics)
5. [🤖 Agentic AI, Safety Filtering & Machine Learning](#5-🤖-agentic-ai-safety-filtering--machine-learning)
6. [💰 Reliability Economics, Regulatory Indices & Valuation Metrics](#6-💰-reliability-economics-regulatory-indices--valuation-metrics)
7. [📜 Mathematical Symbols & Units Nomenclature](#7-📜-mathematical-symbols--units-nomenclature)

---

## 1. 🌡️ FortyGuard API & Urban Microclimate Meteorology

### 2-Meter Air Temperature ($T_{\mathrm{ambient}}$ / $T_{2\mathrm{m}}$)
* **Definition:** Ambient air temperature measured or modelled at exactly $2.0\,\mathrm{meters}$ above ground level (pedestrian and equipment canopy layer), conforming to World Meteorological Organization (WMO) standards.
* **Significance:** Unlike rooftop weather stations or airport sensors (10–30 km away), the 2m layer captures the immediate convective thermal envelope surrounding ground-mounted distribution transformers, padmount switchgear, and BESS containers over radiating asphalt.
* **Units:** Degrees Celsius ($^\circ\mathrm{C}$).

### Continuous Persistence ($P_\theta$ / $P_{40}$)
* **Definition:** The maximum consecutive duration (in hours) during which ambient 2m air temperature continuously equals or exceeds a given temperature threshold $\theta$ (typically $\theta = 40^\circ\mathrm{C}$):

$$P_\theta = \max_{[t_1, t_2]} (t_2 - t_1) \quad \text{s.t.} \quad T_{2\mathrm{m}}(t) \ge \theta \quad \forall t \in [t_1, t_2]$$

* **Significance:** Unlike peak temperature alone, sustained persistence prevents oil-immersed transformers and cable backfill from cooling off overnight, leading to compounding thermal ratcheting.

### Degree-Hour Exceedance ($H_\theta$ / $H_{40}$)
* **Definition:** The cumulative integral of temperature rise above a defined threshold $\theta$ over an operational time horizon $\mathcal{T}$:

$$H_\theta = \int_{\mathcal{T}} \max\left(0, T_{2\mathrm{m}}(t) - \theta\right) dt$$

* **Significance:** Quantifies the total convective thermal dose applied to external cooling radiators.
* **Units:** Degree-hours ($^\circ\mathrm{C}\cdot\mathrm{h}$).

### Thermal Soak Index (TSI)
* **Definition:** A composite, non-dimensional severity metric engineered in Thermal Sentinel Grid that couples persistence duration, thermal exceedance dose, and peak incident solar flux ($S_{\mathrm{peak}}$):

$$\mathrm{TSI} = \left(\frac{P_{40}}{12}\right) \cdot \left(\frac{H_{40}}{10}\right) \cdot \left(1 + \frac{S_{\mathrm{peak}}}{1000\,\mathrm{W/m}^2}\right)$$

* **Significance:** Standardizes multi-day heatwave severity into an actionable trigger index for proactive BESS pre-cooling and load-shedding dispatch.

### Urban Heat Island (UHI) Effect
* **Definition:** The microclimatic phenomenon wherein urban built environments experience significantly higher temperatures than surrounding rural regions due to high impervious surface fraction, thermal mass storage in concrete/asphalt, anthropogenic heat emissions, and reduced evapotranspirative cooling.

### Land Surface Temperature (LST)
* **Definition:** Radiometric skin temperature of the Earth's surface derived from thermal infrared (TIR) satellite or aerial sensors. LST reflects the thermodynamic temperature of building roofs and pavement surfaces (often $60^\circ\mathrm{C}-75^\circ\mathrm{C}$ in desert environments) but differs fundamentally from the fluid 2m convective air temperature that cools electrical assets.

### Sky View Factor ($\psi_{\mathrm{sky}}$ / SVF)
* **Definition:** The ratio between the radiation received by a planar surface and that which it would receive from an entire hemispherical unobstructed sky ($0 \le \psi_{\mathrm{sky}} \le 1$).
* **Significance:** Reduced SVF in dense street canyons traps longwave radiative emissions ($L_{\uparrow}$) and limits nighttime radiative cooling of electrical radiators.

### Urban Street Canyon Aspect Ratio ($H/W$)
* **Definition:** The ratio of average building height $H$ to street canyon width $W$ (Oke Urban Canyon Model).
* **Significance:** Deep canyons ($H/W > 1.5$) induce aerodynamic wind stagnation and vortex recirculation, derating natural convective cooling coefficients ($\eta_{\mathrm{cool}}$) on ground-level transformer radiators by up to $32\%-45\%$.

### Wet-Bulb Temperature ($T_{\mathrm{wb}}$)
* **Definition:** The lowest temperature to which air can be cooled by the evaporation of water into the air at constant pressure.
* **Significance:** Critical physiological threshold for field worker heat stress and occupational safety screens (e.g., utility lineworker emergency dispatch window validation).

---

## 2. ⚡ Transformer Thermal Physics & Insulation Degradation (IEEE / IEC)

### Winding Hot-Spot Temperature ($T_{\mathrm{hs}}$ / $\theta_{\mathrm{hs}}$)
* **Definition:** The localized maximum internal temperature within a transformer winding insulation structure.
* **Standard:** Governed by IEEE Std C57.91-2011 and IEC 60076-7.
* **Limits:**
  * Normal life expectation design limit: $110^\circ\mathrm{C}$.
  * Continuous maximum limit: $120^\circ\mathrm{C}$.
  * Short-time emergency thermal ceiling: $140^\circ\mathrm{C}$ (beyond which catastrophic gas bubble generation and dielectric flashover risk surge).
* **Units:** Degrees Celsius ($^\circ\mathrm{C}$).

### Top-Oil Temperature ($T_o$ / $\theta_{\mathrm{top}}$)
* **Definition:** The temperature of the insulating mineral oil in the upper manifold of the transformer tank before it circulates into the external cooling radiators.
* **Governing ODE:**

$$\tau_{\mathrm{TO}} \frac{dT_o}{dt} = \left[\Delta T_{o,U} \left(\frac{K^2 R + 1}{R + 1}\right)^n\right] - (T_o - T_{\mathrm{ambient}})$$

  where $\tau_{\mathrm{TO}}$ is the oil thermal time constant, $K = I/I_{\mathrm{rated}}$ is the load ratio, $R$ is the loss ratio, and $n$ is the oil exponent ($0.8 - 1.0$).

### Arrhenius Aging Acceleration Factor ($V(t)$ / $F_{AA}$)
* **Definition:** The non-linear rate multiplier quantifying how fast Kraft paper insulation deteriorates relative to normal baseline aging at reference temperature $T_{\mathrm{ref}} = 110^\circ\mathrm{C}$ ($383.15\,\mathrm{K}$):

$$V(t) = \exp\left[\frac{E_a}{R \cdot 383.15} - \frac{E_a}{R \cdot (T_{\mathrm{hs}}(t) + 273.15)}\right] = \exp\left[\frac{15000}{383.15} - \frac{15000}{T_{\mathrm{hs}}(t) + 273.15}\right]$$

  where $E_a/R \approx 15,000\,\mathrm{K}$ is the modified activation energy for Kraft cellulose degradation.
* **Properties:** $V(110^\circ\mathrm{C}) = 1.00000\times$; at $T_{\mathrm{hs}} = 140^\circ\mathrm{C}$, $V \approx 28.5\times$ (1 hour of operation consumes 28.5 hours of asset life).

### Equivalent Loss-of-Life ($L_{\mathrm{equiv}}$ / $L(t)$)
* **Definition:** The cumulative insulation thermal damage accumulated over duration $\mathcal{T}$, expressed in equivalent operating hours at rated $110^\circ\mathrm{C}$:

$$L_{\mathrm{equiv}} = \int_0^{\mathcal{T}} V(t) \, dt$$

* **Design Life:** Nominal standard transformer design life is $180,000\,\mathrm{hours}$ ($\approx 20.55\,\mathrm{years}$).

### Degree of Polymerization (DP)
* **Definition:** The average number of anhydroglucose rings in the cellulose polymer chains of transformer Kraft insulation paper.
* **Thresholds:**
  * New unaged paper: $\mathrm{DP} \approx 1000 - 1200$.
  * Normal aged condition: $\mathrm{DP} \approx 500 - 600$.
  * End-of-life / Mechanical embrittlement limit: $\mathrm{DP} \le 200$ (insulation loses all tensile strength and flakes off under short-circuit electromagnetic shock).

### Paper-to-Oil Moisture Desorption (Fickian Diffusion)
* **Definition:** Temperature-dependent migration of water molecules from Kraft insulation paper into dielectric mineral oil.
* **Governing Relationship:** As hot-spot temperature spikes ($>100^\circ\mathrm{C}$), equilibrium shifts water into the oil, raising relative moisture saturation ($S_{\mathrm{oil}}$) and precipitating gas bubbling and dielectric breakdown ($V_{\mathrm{bd}} < 25\,\mathrm{kV}$).

### IEEE C57.91 Annex G Verification Suite
* **Definition:** The canonical standard benchmark dataset published in IEEE Std C57.91-2011 Annex G:
  * **Clause G.2:** Step load response ($K: 0.5 \to 1.5$) under constant $30^\circ\mathrm{C}$ ambient.
  * **Clause G.3:** 24-hour diurnal ambient cycle ($K: 0.7 \to 1.4$, $T_a: 10^\circ\mathrm{C} \to 40^\circ\mathrm{C}$).
* **Fidelity:** Thermal Sentinel Grid matches standard reference tables with numerical error $< 0.0001^\circ\mathrm{C}$.

---

## 3. 🔌 Power Grid Operations, Dynamic Line Rating & Power Flow

### Dynamic Line Rating (DLR — IEEE Std 738-2012)
* **Definition:** Real-time calculation of the thermal current-carrying ampacity ($I_{\mathrm{max}}$) of bare overhead conductors based on measured weather conditions (ambient temperature, wind speed, wind angle, solar flux), replacing conservative static book ratings.
* **Conductor Heat Balance Equation:**

$$q_c(T_c, T_a, V_w, \phi) + q_r(T_c, T_a, \epsilon) = q_s(\alpha, S, \theta) + I^2 R(T_c)$$

  where $q_c$ is forced/natural convective heat loss, $q_r$ is radiated heat loss, $q_s$ is solar heat gain, and $I^2 R(T_c)$ is Joule heat generation.

### Catenary Conductor Sag ($S(T_c)$)
* **Definition:** The vertical physical clearance droop of overhead transmission conductors between towers caused by thermal expansion at high operating temperatures ($T_c$). Excessive sag risks lethal phase-to-ground flashover into vegetation.

### Forward-Backward Sweep (FBS) Power Flow
* **Definition:** An exact, iterative numerical algorithm tailored for radial distribution feeders that avoids large Jacobian matrix inversions:
  * **Backward Sweep:** Calculates branch currents ($\mathbf{I}_{ij}$) from end nodes toward substation bus using nodal power injections ($\mathbf{S}_i = P_i + jQ_i$).
  * **Forward Sweep:** Propagates voltage drops ($\mathbf{V}_j = \mathbf{V}_i - \mathbf{Z}_{ij} \mathbf{I}_{ij}$) from the slack bus outward to all feeder endpoints.

### Chance-Constrained Optimal Power Flow (CC-OPF)
* **Definition:** A reference optimization formulation that constrains the modeled probability of thermal or voltage violations to at most $\epsilon$ under an assumed uncertainty distribution:

$$\mathbb{P}\left(V_i^{\min} \le |V_i| \le V_i^{\max}\right) \ge 1 - \epsilon$$

### Second-Order Cone Programming (SOCP)
* **Definition:** A convex optimization framework that can relax non-convex AC power-flow equations ($W_{ij} = V_i V_j^*$) into second-order-cone constraints. Under the mathematical conditions of a particular relaxation, a solver can provide an optimum for the relaxed problem; this does not by itself guarantee exactness for the original non-convex problem.
* **Prototype boundary:** Thermal Sentinel Grid documents CC-OPF/SOCP as research context. The shipped uncertainty endpoint performs an analytical Gaussian-quantile screen with heuristic control selection and does not run a numerical SOCP solver.

### Volt-VAR Control (VVC) & On-Load Tap Changers (OLTC)
* **Definition:** Coordinated control of transformer winding tap steps (OLTC $\pm 16$ steps) and reactive power injection ($Q_{\mathrm{BESS}}$) to flatten voltage profiles within ANSI C84.1 Range A ($0.95 - 1.05\,\mathrm{pu}$).

### N-1 Contingency Criterion
* **Definition:** A fundamental power system reliability mandate requiring that the distribution grid remain within thermal and voltage operating limits following the sudden loss of any single primary component (e.g., loss of a parallel substation transformer or main feeder line).

### Buried Cable-Soil Moisture Dryout (IEC 60287)
* **Definition:** Physical phenomenon where sustained high heat flux from underground medium-voltage cables drives moisture away from surrounding trench backfill, triggering a non-linear surge in soil thermal resistivity ($\rho_{\mathrm{soil}}$ from $0.9\,\mathrm{K}\cdot\mathrm{m/W}$ to $> 2.45\,\mathrm{K}\cdot\mathrm{m/W}$) and causing sudden thermal runaway.

---

## 4. 🔋 Battery Energy Storage Systems (BESS) & Electro-Thermal Mechanics

### State of Charge (SoC / $\mathrm{SOC}(t)$)
* **Definition:** The ratio of currently available electrical energy in a battery relative to its rated nominal capacity, bounded by operational safety envelopes ($0.20 \le \mathrm{SoC} \le 0.90$).

### C-Rate
* **Definition:** The rate of battery charge or discharge normalized to total capacity. A $1\mathrm{C}$ rate fully discharges the pack in $1\,\mathrm{hour}$; a $0.5\mathrm{C}$ rate discharges it in $2\,\mathrm{hours}$.

### BESS 2-State Lumped Thermal Model
* **Definition:** Coupled ordinary differential equations modeling internal cell core temperature ($T_{\mathrm{core}}$) and exterior cell surface casing temperature ($T_{\mathrm{surf}}$):

$$C_{\mathrm{core}} \frac{dT_{\mathrm{core}}}{dt} = I^2 R_{\mathrm{int}} - \frac{T_{\mathrm{core}} - T_{\mathrm{surf}}}{R_c}$$

$$C_{\mathrm{surf}} \frac{dT_{\mathrm{surf}}}{dt} = \frac{T_{\mathrm{core}} - T_{\mathrm{surf}}}{R_c} - \frac{T_{\mathrm{surf}} - T_{\mathrm{ambient}}}{R_u}$$

* **Thermal Limit:** Enforces a hard ceiling ($T_{\mathrm{core}} < 55^\circ\mathrm{C}$) to prevent exothermic Solid Electrolyte Interphase (SEI) decomposition and thermal runaway.

### Arrhenius SEI Capacity Degradation
* **Definition:** Capacity fade kinetics in Lithium-ion cells driven by high temperature and cyclic C-rate throughput:

$$\frac{dQ_{\mathrm{loss}}}{dt} = A_{\mathrm{SEI}} \cdot \exp\left(-\frac{E_{a,\mathrm{SEI}}}{R \cdot T_{\mathrm{cell}}}\right) \cdot |I(t)|^z$$

* **Significance:** Used to calculate the real-time monetary degradation cost (USD/MWh) of battery discharge actions during peak-shaving dispatch.

---

## 5. 🤖 Agentic AI, Safety Filtering & Machine Learning

### CBF-Inspired Deterministic Safety Filter
* **Definition:** The shipped prototype simulates proposed dispatch actions over bounded trajectories, checks configured thermal, voltage, BESS, and N-1 limits, and uses scalar bisection to project excessive load back toward an admissible value. It is inspired by the safe-set concept $h(\mathbf{x}) \ge 0$ (for example, $140^\circ\mathrm{C} - T_{\mathrm{hs}} \ge 0$), but it does **not** solve the reference quadratic program

$$\min_{\mathbf{u}} \frac{1}{2} \left\Vert \mathbf{u} - \mathbf{u}_{\mathrm{nom}} \right\Vert^2 \quad \text{s.t.} \quad \dot{h}(\mathbf{x}, \mathbf{u}) \ge -\alpha(h(\mathbf{x}))$$

and does not establish formal forward invariance for physical equipment.
* **Significance:** Provides a deterministic, auditable model check independent of the LLM. A production controller would still require calibrated equipment models, field validation, utility engineering approval, and certified control integration.

### LangGraph Multi-Agent StateGraph
* **Definition:** A deterministic, cyclic graph-based agent orchestration harness where each node represents a specialized computational or reasoning actor (`ingest_node`, `physics_projection_node`, `planner_node`, `safety_gate_node`, `audit_dispatch_node`) operating on a typed, immutable state schema (`TransformerState`).

### Model Context Protocol (MCP)
* **Definition:** An open, standardized JSON-RPC protocol enabling external AI agents and IDEs to query Thermal Sentinel Grid's deterministic analytical tools (`rank_portfolio_risk`, `find_worker_intervention_windows`, `get_mitigation_evidence`) over HTTP or stdio.

### Medallion Data Architecture (Bronze $\to$ Silver $\to$ Gold)
* **Bronze Layer:** Raw, immutable FortyGuard JSON payloads, hourly temperature/humidity rows, and raw asset records.
* **Silver Layer:** Cleaned, resampled (15-min to hourly), validated time-series with null-exclusion and multi-cadence alignment.
* **Gold Layer:** 18 engineered features including rolling persistence ($P_{40}$), degree-hour exceedance ($H_{40}$), TSI, Arrhenius $V(t)$, and safety margin metrics.

### Physics-Surrogate Regressor
* **Definition:** A sub-millisecond polynomial Ridge regression model ($\text{degree}=2, \alpha=1.0$) trained on physical ODE trajectories:

$$\hat{T}_{\mathrm{hs}} = \mathbf{w}^T \phi(T_{\mathrm{ambient}}, K, P_{40}, H_{40}, \mathrm{SoC}) + b$$

* **Performance:** $R^2 = 0.984$, $\mathrm{MAE} < 1.2^\circ\mathrm{C}$, delivering $>5,000\times$ speedup for city-wide multi-feeder spatial screening.

### Isolation Forest Sensor Anomaly Detector
* **Definition:** An unsupervised tree-based ensemble algorithm that isolates anomalies by measuring path lengths in randomly partitioned feature spaces, detecting SCADA sensor drift, stuck thermocouples, and pre-runaway thermal anomalies.

### Two-Parameter Weibull Hazard Model
* **Definition:** Extreme value survival reliability distribution modeling asset failure probability under thermal stress:

$$\lambda(t) = \frac{\beta}{\eta} \left(\frac{t}{\eta}\right)^{\beta - 1} \cdot A_F(T_{\mathrm{hs}})$$

where $\beta \approx 1.85$ is the shape parameter (wear-out regime), $\eta$ is the characteristic life, and $A_F$ is the Arrhenius acceleration factor.

### Moran's I Spatial Autocorrelation
* **Definition:** Global spatial statistic measuring the degree of spatial clustering in 2m microclimate temperatures across an area of interest:

$$I = \frac{N}{\sum_i \sum_j w_{ij}} \frac{\sum_i \sum_j w_{ij} (T_i - \bar{T})(T_j - \bar{T})}{\sum_i (T_i - \bar{T})^2}$$

* **Benchmark:** $I = 0.428$ ($p < 0.001$), proving statistically significant urban microclimate hot-spot clustering.

---

## 6. 💰 Reliability Economics, Regulatory Indices & Valuation Metrics

### Value of Lost Load (VoLL)
* **Definition:** The estimated monetary loss incurred by electrical customers per unserved kilowatt-hour or megawatt-hour of electrical energy during a blackout.
* **Values:** Ranges from $\$5{,}000/\mathrm{MWh}$ for residential customers up to $\$45{,}000-\$150{,}000/\mathrm{MWh}$ for semiconductor fabs, trauma hospitals, and tier-4 data centers.

### LBNL ICE Calculator (Interruption Cost Estimate)
* **Definition:** The gold-standard statistical economic tool developed by the U.S. Department of Energy (DOE) and Lawrence Berkeley National Laboratory (LBNL) to estimate customer interruption costs based on customer class mix, outage duration, season, and time of day.

### Modeled Avoided Exposure Formula
* **Definition:** The assumption-based scenario equation computed in Thermal Sentinel Grid:

$$\boxed{\text{Net Avoided Loss} = \left[p_{f,\mathrm{base}} - p_{f,\mathrm{mitigated}}\right] \cdot C_{\mathrm{consequence}} + \Delta PV_{\mathrm{aging}} - C_{\mathrm{mitigation}}}$$

* $p_{f,\mathrm{base}} - p_{f,\mathrm{mitigated}}$: Change in an uncalibrated logistic scenario-risk score, not an actuarial failure probability.
* **Interpretation boundary:** The result is a comparative modeled exposure estimate and cost ratio—not realized savings, a bankable ROI, or an actuarial forecast.
* $C_{\mathrm{consequence}}$: Total consequence cost (asset replacement + VoLL customer interruption).
* $\Delta PV_{\mathrm{aging}}$: Present value of deferred capital replacement derived from preserved insulation life.
* $C_{\mathrm{mitigation}}$: Direct cost of mitigation dispatch (BESS cycling degradation + fan auxiliary energy).

### Capital Deferral ($\Delta PV_{\mathrm{aging}}$)
* **Definition:** The net present value of delayed capital expenditure on transformer replacement resulting from thermal life preservation:

$$\Delta PV_{\mathrm{aging}} = C_{\mathrm{replace}} \cdot \left[\frac{1}{(1 + r)^{t_{\mathrm{base}}}} - \frac{1}{(1 + r)^{t_{\mathrm{mitigated}}}}\right]$$

where $r$ is the utility discount rate and $t_{\mathrm{base}}, t_{\mathrm{mitigated}}$ are projected retirement dates.

### SAIDI (System Average Interruption Duration Index)
* **Definition:** Regulatory reliability benchmark indicating the total minutes of sustained power interruption experienced by the average customer over a given year:

$$\mathrm{SAIDI} = \frac{\sum r_i N_i}{N_{\mathrm{total}}} \quad \left[\frac{\text{minutes}}{\text{customer}\cdot\text{year}}\right]$$

### SAIFI (System Average Interruption Frequency Index)
* **Definition:** Regulatory reliability benchmark measuring the average number of sustained interruptions experienced per customer per year:

$$\mathrm{SAIFI} = \frac{\sum N_i}{N_{\mathrm{total}}} \quad \left[\frac{\text{interruptions}}{\text{customer}\cdot\text{year}}\right]$$

---

## 7. 📜 Mathematical Symbols & Units Nomenclature

| Symbol | Meaning | Standard Units |
| :--- | :--- | :---: |
| `T_ambient` / `T_2m` | FortyGuard 2-meter convective air temperature | $^\circ\mathrm{C}$ |
| `T_o` | Transformer top-oil temperature | $^\circ\mathrm{C}$ |
| `T_hs` | Transformer winding hot-spot temperature | $^\circ\mathrm{C}$ |
| `T_c` | Overhead conductor temperature (IEEE 738) | $^\circ\mathrm{C}$ |
| `T_core`, `T_surf` | BESS battery cell core and surface temperatures | $^\circ\mathrm{C}$ |
| `T_wb` | Wet-bulb temperature for workforce heat stress screening | $^\circ\mathrm{C}$ |
| `P_40` | Continuous thermal persistence ($\ge 40^\circ\mathrm{C}$) | $\mathrm{hours}$ |
| `H_40` | Degree-hour thermal exceedance ($\ge 40^\circ\mathrm{C}$) | $^\circ\mathrm{C}\cdot\mathrm{h}$ |
| `TSI` | Thermal Soak Index | Dimensionless |
| `K` | Transformer load ratio ($I / I_{\mathrm{rated}}$) | Dimensionless ($\mathrm{pu}$) |
| `V(t)` / `F_AA` | Arrhenius insulation aging acceleration factor | Dimensionless ($\times$) |
| `L_equiv` | Cumulative equivalent loss-of-life hours | $\mathrm{hours}$ |
| `tau_TO` | Top-oil thermal time constant | $\mathrm{hours}$ |
| `tau_W` | Winding hot-spot thermal time constant | $\mathrm{minutes}$ |
| `rho_soil` | Soil thermal resistivity (IEC 60287) | $\mathrm{K}\cdot\mathrm{m/W}$ |
| `H/W` | Urban street canyon height-to-width aspect ratio | Dimensionless |
| `psi_sky` | Sky view factor | Dimensionless ($0-1$) |
| `eta_cool` | Canyon convective cooling derate multiplier | Dimensionless ($0-1$) |
| `S(t)` | Incident solar global horizontal irradiance | $\mathrm{W/m}^2$ |
| `q_c, q_r, q_s` | Convective, radiative, and solar heat rates per unit length | $\mathrm{W/m}$ |
| `SoC` | Battery Energy Storage State of Charge | $\%$ |
| `h(x)` | Safe-set margin used by the CBF-inspired model check | Dimensionless |
| `|V_i|` | Feeder bus voltage magnitude | $\mathrm{pu}$ ($0.95-1.05$) |
| `lambda(t)` | Weibull failure hazard rate | $\mathrm{failures/year}$ |
| `VoLL` | Value of Lost Load | $\mathrm{USD}/\mathrm{MWh}$ |
| `Delta PV_aging` | Present value of deferred asset replacement capital | $\mathrm{USD}$ |

---

*Thermal Sentinel Grid Documentation Hub — See also [docs/README.md](README.md) and [SUBMISSION.md](../SUBMISSION.md).*
