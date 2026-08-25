# ⚡ Thermal Sentinel Grid
> **Physics-Constrained Agentic Thermal Resilience & Dispatch Engine for Distribution Transformers & Urban Energy Infrastructure**  
> **FortyGuard Hackathon '26** - *Track 06 (Agentic AI) & Track 02 (Future Buildings & Energy)*

---

## 📝 Official Hackathon Submission Form Fields (Copy-Paste Ready)

*Official Submission Form URL:* **[https://forms.gle/jLgBzVTG1NhJ3gNe6](https://forms.gle/jLgBzVTG1NhJ3gNe6)**  
*Submission Deadline:* **30 August 2026, 11:59 PM GST**

| Form Field | Exact Submission Content |
| :--- | :--- |
| **Project Title** | **Thermal Sentinel Grid** |
| **One-Line Pitch** | Physics-Constrained Agentic Thermal Resilience & Dispatch Engine for Distribution Transformers & Urban Energy Infrastructure |
| **Primary Track** | **Track 06 - Agentic AI** |
| **Secondary Track Tags** | **Track 02 (Future Buildings & Energy)** & **Track 03 (Industrial & Enterprise / Critical Assets)** |
| **Target Audience (Who It's For)** | Substation Reliability Engineers & Grid Operators at Electric Utilities (APS, ConEd, ERCOT, PG&E) and Mission-Critical Facility Managers (Data Centers, Hospitals, Military Bases). |
| **Location & Time Period Analyzed** | **Downtown Phoenix, Arizona (33.4484° N, 112.0740° W)** — canonical FortyGuard capture on **2023-07-19** ($42.74^\circ\mathrm{C}$ parcel peak, 12 sampled hours above $40^\circ\mathrm{C}$), plus a complete 72-hour live capture for **2023-07-24 through 2023-07-26** (daily peaks $42.44/42.76/42.52^\circ\mathrm{C}$). The historical regional record reached $119^\circ\mathrm{F}$; it is context, not the API boundary. |
| **How FortyGuard API Was Used** | Programmatically calls FortyGuard's async submit-and-poll REST API (`POST /v1/heatmap`, `POST /v1/env_params`, `GET /v1/status/{id}`, `GET /v1/system/fetch-api-key-usage`). Ingests 2-meter convective ambient air temperature tiles ($60\text{m}$ resolution) and 12-hour forward forecasts to compute Continuous Persistence ($P_{40} = 12.0\text{h}$), Exceedance Degree-Hours ($H_{40} = 17.48\text{ }^\circ\mathrm{C}\cdot\text{h}$), and Thermal Soak Index ($3.68$), driving proactive 12-hour BESS and transformer cooling dispatch. |
| **AI & Data Science Tools Used** | 1. **LangGraph StateGraph**: Autonomous cognitive multi-agent orchestration.<br>2. **Siemens SDC Gateway (`gpt-5.4` default)**: Optional narrative synthesis for operator work orders, with deterministic fallback when unavailable.<br>3. **Non-LLM CBF-Inspired Safety Filter**: Deterministic bounded-trajectory validation and bisection over permissible load, checking ANSI C84.1 voltage ($0.95-1.05\text{ pu}$), thermal, BESS, and N-1 limits in the model.<br>4. **Physics Surrogate Regressor (Ridge + Poly2)**: $5000\times$ faster city-wide screening ($R^2 > 0.98, \text{MAE} < 1.5^\circ\mathrm{C}$).<br>5. **Sensor Anomaly Detection (Isolation Forest)**: Identifies sensor drift and thermal runaway pre-cursors.<br>6. **Weibull RUL Survival Analysis**: Extreme value lifetime hazard forecasting under sustained thermal stress.<br>7. **Bronze→Silver→Gold ETL Pipeline**: Medallion architecture generating 18 engineered features for real-time analytics. |
| **Live Demo URL** | **[https://www.thermal-sentinel-grid.live](https://www.thermal-sentinel-grid.live)** (Zero install, no login, full incognito compatibility) · *Local:* `http://localhost:8000` |
| **Demo Video Link (3 min max)** | YouTube / Loom unlisted URL with full narration & voiceover (Available locally as Motion Pitch `videos/thermal-sentinel-pitch/renders/video.mp4` and Live UI Walkthrough `videos/thermal-sentinel-pitch/renders/live_product_demo.mp4`, also embedded directly into the Home screen at `/`). |
| **GitHub Repository Link** | **[https://github.com/KarimmYasser/fortyguard-hackathon](https://github.com/KarimmYasser/fortyguard-hackathon)** *(Collaborator `hackathon@fortyguard.com` / `Hackathon-FG` invited)*. |
| **Data Science Portfolio** | Dedicated Jupyter Notebook in `notebooks/Thermal_Sentinel_DataScience.ipynb` and interactive in-app Data Science Studio tab. |
| **Development Timeline Note** | *Initial repo setup & mock-data structure: 17 August 2026. Real FortyGuard API integration and core functionality: 18 August 2026 onward.* |


---

## 🌟 Executive Summary & Pitch

During extreme heatwaves, electrical utilities manage power distribution using regional airport weather stations located 10 miles away. However, distribution transformers, switchgear, and underground feeder cables sit **0 to 2 meters above radiating black asphalt** inside dense urban canyons.

During the historic Phoenix July 2023 heatwave, the regional record reached $119^\circ\mathrm{F}$, while the pinned FortyGuard parcel capture measured $42.74^\circ\mathrm{C}$ and remained above $40^\circ\mathrm{C}$ for all 12 sampled hours. Direct probing showed Sky Harbor slightly *warmer* than downtown, so the product does not claim an airport-to-asset delta; it leads on measured duration and parcel conditions.

**Thermal Sentinel Grid** bridges this dangerous 2-meter microclimate gap by coupling **FortyGuard’s hyperlocal Temperature AI** with **IEEE Std C57.91 / IEC 60076-7 thermal differential equations**, an autonomous **LangGraph multi-agent workflow**, and a **non-LLM deterministic, CBF-inspired safety-envelope filter**. Its Portfolio Ops module ranks registered assets, screens candidate crew-intervention windows, and exposes content-addressed evidence through both the dashboard and an MCP-compatible tool interface. See the [as-built operations and MCP specification](docs/research/PORTFOLIO_OPERATIONS_AND_MCP.md).

---

## 📋 The 15-Minute Pre-Build Decision Checklist (Judge Alignment)

*Evaluated against the official Hackathon Judge Framework (Ahmed Abdelkhalek - Head of Startups, Google Cloud):*

| Dimension | Thermal Sentinel Grid Implementation |
| :--- | :--- |
| **Hero (Exact Buyer)** | **Substation Reliability Engineers & Grid Operators** (Utilities e.g. APS, ConEd, ERCOT) & **Mission-Critical Facility Directors** (Data Centers, Hospitals). |
| **Pain** | **$2.8M in substation blowouts and 15x accelerated insulation aging** caused by unmeasured 2m asphalt thermal soak during 12-hour heatwaves. |
| **AI Justification** | **Autonomous 12-Hour Proactive Dispatch:** Cognitive multi-agent planning connecting FortyGuard's forecast with BESS peak-shaving, OLTC tap tuning, and radiator pre-cooling. Exact physics ODEs handle math, while AI handles multi-asset policy synthesis. |
| **Kill Switch (24h Validation)** | **Sub-15ms Real-Time Simulation Engine:** Interactive What-If Studio allowing judges to modulate microclimate deltas and see live ODE recalculations in $<15\text{ms}$. |

---

## 🏆 Official Scoring Rubric & Judging Alignment

| Weight | Official Criterion | What Judges Look For | Thermal Sentinel Grid Moat & Evidence |
| :---: | :--- | :--- | :--- |
| **40%** | **Impact & Relevance** | Real-world problem, client benefit, commercial viability over toy demos. | **$2.58M avoided catastrophic loss per heat event**; solves the 2-meter asphalt heat-soak blind spot for utilities (APS, ConEd, PG&E) and mission-critical facilities. |
| **35%** | **Technical Execution** | Code quality, proper FortyGuard API usage, live deployment stability. | **97 automated pytest tests passing**, clean Medallion ETL feature pipeline, sub-15ms simulation engine, zero-install incognito live deployment, and server-side secret management. |
| **15%** | **Innovation** | Novel concepts, multi-source coupling, Physical-AI hybrid synthesis. | **Physical-AI Hybrid Stack (Prof. Reichental Model):** Perception (FortyGuard 2m AI) $\to$ Physics Truth (IEEE C57.91 / IEC 60287) $\to$ Cognitive Planner (LangGraph) $\to$ Deterministic Safety Guardrail. |
| **10%** | **Communication** | Pitch clarity, video quality, documentation, conveying the core "Why". | **3-minute high-velocity screen demo** of the working software UI, second-by-second narrative script, 22 academic citations with LaTeX proofs, and full webinar alignment. |

---

## 🏛️ The Three Architectural Pillars & Strategic Market Positioning

### Strategic Positioning: "Tickling the Giants"

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              LEGACY SCADA & WEATHER vs. THERMAL SENTINEL GRID                          │
│                                                                                                        │
│   Dimension            Legacy SCADA (Siemens, GE, Schneider)     Thermal Sentinel Grid (Our Stack)     │
│   ──────────────────   ───────────────────────────────────────   ───────────────────────────────────   │
│   Weather Input        Airport Station 10 miles away (10m air)   FortyGuard 2-Meter Microclimate AI    │
│   Reaction Time        Reactive: Trips alarm at 135°C (5m left)  Proactive: Dispatches 12h ahead       │
│   Physical Cascades    Blind to soil dryout & canyon winds       4 Deep Physics & Aerodynamic Moats    │
│   Safety Screening     Rule-based / human operator triage        Deterministic Model-Envelope Filter   │
│   Financial Value      Incurs emergency blackout replacement     $2.58M Net Avoided Loss (5,495x ROI)  │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🤖 Why Physics-Constrained Agentic AI (Track 06) Over Black-Box ML Training
*(For the complete strategy and mathematical justification, see **[Value Proposition & AI Philosophy](docs/research/VALUE_PROPOSITION_AND_AI_PHILOSOPHY.md)**)*

1. **FortyGuard Already Solved the Microclimate ML Layer:** FortyGuard’s proprietary AI models already compute the 2-meter convective boundary layer, land-cover computer vision segmentation, and 12-hour forward forecasts.
2. **Thermodynamic Truth is Exact:** Transformer heat dissipation, top-oil convection, and Arrhenius cellulose degradation are governed by exact physical differential equations (ODEs) from **IEEE Std C57.91-2011** and **IEC 60076-7**. Replacing exact physics with an approximate black-box neural net introduces unforced hallucinations and out-of-distribution failure.
3. **Mission-Critical Safety Demands Deterministic Validation:** A black-box LLM must not directly control breakers or batteries. The prototype therefore checks candidate actions against bounded thermal, voltage, BESS, and N-1 trajectories before they can proceed.
4. **The Hybrid Physical-AI Stack:** Perception (FortyGuard AI) $\to$ Physical Model (IEEE-based ODEs) $\to$ Agentic Planner (LangGraph StateGraph) $\to$ Deterministic Safety Envelope.

---

## 📈 Data Science & Spatial Rigor: Turning Heat Data into Real Signal
*(Aligned with FortyGuard ML & Cloud Architecture Guidance - Session 7)*

* **The "Fact vs. Finding" Principle:** Standard systems output static facts (e.g., *"Substation reached 42.7°C"*). Thermal Sentinel Grid couples FortyGuard 2m air temperature with IEEE ODEs to produce **comparative, defensible findings** (e.g., *"Asset #3 entered an 8.4h continuous thermal soak, accelerating Arrhenius aging by 58% and exhausting BESS cooling margins 3.1 hours before peak load"*).
* **Multi-Modal Spatial & Temporal Coupling:** Vector asset locations are matched to FortyGuard 20m/60m raster cells. Multi-rate telemetry (15-minute load profiles vs. hourly microclimate forecasts) are coupled via continuous rolling integrals and UTC alignment, eliminating spurious spatial-temporal correlations.

---

## 💼 Commercial Validation & Product-Market Fit (PMF) Strategy
*(Informed by the BreezoMeter $\to$ Google Acquisition & Cultivators Discovery Playbook - Session 8)*

* **COCO Customer Discovery Alignment:**
  * **Context:** Extreme summer heatwaves in Sunbelt (Phoenix, Texas) and MENA causing unmeasured 2-meter heat soak across urban infrastructure.
  * **Outcomes:** Zero unforced transformer blowouts, avoiding $2.58M in outage losses, and extending capital asset life by 374+ equivalent hours.
  * **Constraints:** Utilities currently operate reactively via coarse weather stations; switching to Thermal Sentinel Grid requires zero hardware retrofits (software-only API integration).
* **Early Adopter Beachhead vs. Enterprise ICP:**
  * **Phase 1 Beachhead (Immediate Revenue):** Private solar farm operators, BESS storage facilities, and mission-critical data center chiller operators in Sunbelt/MENA experiencing immediate thermal trip penalties.
  * **Phase 2 Enterprise ICP (Scale):** Regulated investor-owned utilities (APS, ConEd, ERCOT, DEWA) and property casualty reinsurers.

---

## 🔬 Four Asymmetric Scientific Moats & Deep Physics

1. **IEC 60287 Underground Cable-Soil Moisture Dryout:**  
   Multi-day heat persistence bakes moisture out of the soil surrounding buried cables. Soil thermal resistivity ($\rho_{\text{soil}}$) surges non-linearly from $0.90\text{ K}\cdot\text{m/W}$ to $>2.45\text{ K}\cdot\text{m/W}$, creating an unmeasured $-22\%$ ampacity bottleneck.
2. **Oke / Evola Urban Canyon Aerodynamics:**  
   Deep building aspect ratios ($H/W = 1.85$) cause wind-sheltering ($\kappa_{\text{morph}} = 0.58$), reducing radiator fin convective heat dissipation by **$-32\%$ ($\eta_{\text{cool}} = 0.68$)**.
3. **Virtual Paper-to-Oil Moisture Sensor (Fick's Second Law):**  
   Tracks Kraft cellulose paper-to-oil moisture migration, alerting to relative oil saturation ($RS_o = 42\%$) and dielectric arcing risk hours before temperature limits trip.
4. **Deterministic CBF-Inspired Safety Filter:**
   A non-LLM validator simulates the forecast with a $+1.5^\circ\mathrm{C}$ uncertainty margin, checks thermal, voltage, BESS, and N-1 bounds, and uses bisection to calculate a safe maximum load. It is not a numerical QP or a field-certified controller.
5. **📜 IEEE Std C57.91 Annex G Reference Validation Engine:**  
   Automated verification against official IEEE Clause G.2 (Step Load Response) and Clause G.3 (Diurnal Ambient Ramp), demonstrating **$<0.0001^\circ\mathrm{C}$ error** against published standard tables. *(See **[IEEE Annex G & AC Power Flow Specification](docs/research/IEEE_ANNEX_G_AND_AC_POWER_FLOW_SPECIFICATION.md)**)*
6. **🔥 72-Hour Continuous Multi-Day Compounding Heatwave Simulation:**  
   Replays 72 consecutive live FortyGuard hourly boundaries for Phoenix, July 24–26, 2023 (daily peaks $42.44/42.76/42.52^\circ\mathrm{C}$), then models night-time thermal soak and progressive soil dryout ($\rho_{\text{soil}}$ end-of-day $1.52 \to 2.13 \to 2.41\text{ K}\cdot\text{m/W}$).
7. **⚡ Complex AC Distribution Feeder Power Flow (IEEE 4-Bus Network):**  
   Exact Forward-Backward Sweep AC solver with On-Load Tap Changer (OLTC $\pm 10\%$) and 4-quadrant BESS Volt/VAR support under ANSI C84.1 Range A envelope.
8. **Dynamic Line Rating & Conductor Catenary Sag (IEEE Std 738-2012):**  
   Iterative Newton-Raphson convective, radiative, and solar heat equilibrium ($q_c + q_r = q_s + I^2R$) unlocking $+22.5\%$ dynamic ampacity headroom while preventing ground flashover sag ($S(T_c)$).
9. **Coupled 2-State BESS Electro-Thermal & Arrhenius SEI Capacity Fade:**  
   2-state lumped core ($T_c$) vs. surface ($T_s$) differential thermal equations with continuous electrochemical SEI growth ($dQ_{\text{loss}}/dt$), tracking real-time degradation cost (\$/MWh) and enforcing the $55^\circ\mathrm{C}$ thermal runaway ceiling.
10. **Arrhenius-Weibull Grid Fragility & Cascading Blackout Risk:**  
    Time-dependent non-homogeneous Poisson-Weibull failure hazard model $\lambda_i(t, T)$ with Arrhenius acceleration $A_F(T)$ integrated across substation assets to output joint cascading failure probability ($P_{\text{cascade}}$).
11. **Analytical Uncertainty-Bounded Dispatch Screen:**
    A simplified 4-bus model applies Gaussian 90%/95%/99% quantile bounds and heuristically selects BESS, OLTC, and load-shedding actions. The code does not invoke a numerical SOCP optimizer.


---

## 📊 Benchmark Validation Results (Phoenix July 2023)

| Dimension | Baseline Controller (Airport Weather) | Thermal Sentinel Grid (FortyGuard + Physics) | Advantage |
| :--- | :--- | :--- | :--- |
| **Ambient Boundary Input** | Natural-terrain reference ($41.6^\circ\mathrm{C}$, South Mountain) | Parcel 2m Convective Air ($42.7^\circ\mathrm{C}$, downtown core) | $+1.1^\circ\mathrm{C}$ measured land-cover delta |
| **Heatwave Persistence** | Blind to $12\text{h}$ continuous $>40^\circ\mathrm{C}$ | Tracks $P_{40}$ & Thermal Soak Index ($3.68$) | Proactive pre-cooling 12h ahead |
| **Peak Winding Hot-Spot ($T_{hs}$)** | **$159.53^\circ\mathrm{C}$** *(breaches limit)* | **$109.43^\circ\mathrm{C}$** | **$-50.10^\circ\mathrm{C}$ peak reduction** |
| **Insulation Aging** | $88.36\times$ peak acceleration; $377.77\text{ h}$ equivalent loss | $0.94\times$ peak; $3.51\text{ h}$ loss | **$374.3\text{ hours}$ avoided** |
| **Net Avoided Loss (LBNL ICE)** | $\$0$ *(Incurs catastrophic blowout)* | **$\$162,088$ to $\$2,576,849$** | **$24.3\times$ to $5,495\times$ ROI** |

---

## 🔌 FortyGuard API Dual-Mode Ingestion & System Taxonomy
*(For the complete architectural decision record, see **[API Integration & Replay Architecture](docs/research/API_INTEGRATION_AND_REPLAY_ARCHITECTURE.md)**)*

Thermal Sentinel Grid implements a production-grade **Dual-Mode Microclimate Ingestion** pattern:
1. **Mode A: Live Cloud Ingestion (`POST /api/v1/scan`):** Uses [`AsyncFortyGuardClient`](src/api/fortyguard_client.py) with full submit-and-poll async lifecycle against live FortyGuard cloud endpoints (`/v1/heatmap`, `/v1/env_params`, `/v1/status/{id}`) for ad-hoc parcel scanning with real credit billing.
2. **Mode B: Deterministic Benchmark Replay (`GET /api/v1/replay/phoenix-2023`):** Uses the pre-ingested Phoenix July 2023 heatwave dataset ([`phoenix_heatwave_2023.json`](src/api/fixtures/phoenix_heatwave_2023.json)) for **$<15\text{ms}$ benchmark physics evaluation**, smooth scrubber telemetry, deterministic IEEE Annex G validation, and independence from live vendor calls during judging presentations.

### 🏛️ System Boundary & Simulation Taxonomy
| Layer | Implementation | Status | Purpose |
| :--- | :--- | :---: | :--- |
| **FortyGuard Live API** | `/v1/env_params`, `/v1/heatmap`, `/v1/system/fetch-api-key-usage` | 🟢 **LIVE** | On-demand parcel scanning, microclimate index lookup & real-time quota accounting. |
| **Physics & Grid Solvers** | IEEE C57.91, Arrhenius aging, IEC 60287 soil, 4-bus FBS power flow | ⚡ **CALCULATED LIVE** | Deterministic thermal trajectories, radial-feeder flow, and safety-envelope evaluations. |
| **Substation Asset Digital Twin** | IEEE C57.91 standard transformer parameters (50 MVA, $\tau_{TO}$, $\tau_W$, $R$) | 📦 **SIMULATED TWIN** | Industry-standard CIM/GIS substation nameplate profiles for digital twin benchmarking. |
| **Benchmark Weather Fixture** | Phoenix July 19, 2023 capture ($42.74^\circ\mathrm{C}$ peak, $889.8\,\mathrm{W/m}^2$ peak derived solar, $P_{40}=12.0\,\mathrm{h}$) | 📦 **FROZEN LIVE CAPTURE** | Fast 12h timeline scrubbing and deterministic physics replay. |
| **Hardware Actuators** | Dispatch payloads (BESS discharge, fan stage 2, EV curtailment) | 📦 **SIMULATED ACTUATORS** | Emits schema-validated recommendations checked against the modelled safety envelope; no physical SCADA is connected. |

---

## 💻 Tech Stack

* **Backend & Physics:** Python 3.13, FastAPI, NumPy, pandas, Pydantic v2, Uvicorn (scikit-learn optional, lazily imported for the ML surrogates)
* **Agentic Architecture:** LangGraph, LangChain, StateGraph, Siemens SDC Gateway (`gpt-5.4` default, environment-configurable), plus read-only MCP-compatible deterministic operations tools
* **Enterprise Persistence:** Supabase PostgreSQL is the durable source of truth; SQLite is the local/offline fallback. PostgREST spans 16 application tables, with stored scans and full deterministic solves replayable across serverless cold starts.
* **Standards & Formulations:** IEEE Std C57.91-2011, IEEE Std 738-2012, IEC 60076-7, IEC 60287-1-1, ANSI C84.1, LBNL ICE Calculator
* **Frontend Dashboard:** React 19, TypeScript, Vite, Tailwind CSS v4, Apache ECharts, Lucide Icons

---

## 🗄️ Durable Hybrid Database Layer (16 Tables)

Thermal Sentinel Grid incorporates a **Graceful Dual-Storage Persistence Layer** (Local SQLite + PostgREST Live Supabase Cloud PostgreSQL) across 16 application tables. Supabase is authoritative in production; SQLite is an ephemeral serverless fallback:
1. **`api_call_cache`:** Stores raw FortyGuard responses under MD5 request identities and full deterministic solves under SHA-256 request identities. The Supabase-backed entries prevent duplicate credit billing and replay identical simulations across cold starts without expiry.
2. **`dispatch_work_orders`:** Historical record of authorized B2B SCADA mitigation orders ($K_{\text{safe}}$, BESS MW, OLTC tap steps).
3. **`credit_accounting_ledger`:** Audit trail of FortyGuard credit deductions per activity and remaining balances.
4. **`academic_research_papers`:** 22 indexed research records with LaTeX equations and alphaXiv links.
5. **`substation_telemetry_logs`:** 12-hour modelled asset telemetry steps ($\theta_o, \theta_w, V(t)$, MVA load).
6. **`simulation_runs`:** What-If inputs and scalar-output audit summaries; complete trajectories live in `api_call_cache`.
7. **`multi_day_heatwave_logs`:** Per-step audit records for modelled 72h soil and aging progression; the environmental boundary is the separate frozen 72-row live capture.
8. **`dlr_catenary_telemetry`:** Dynamic Line Rating heat balance ($q_c, q_r, q_s, I^2R$) and catenary sag.
9. **`agent_execution_traces`:** Multi-agent LangGraph StateGraph DAG execution logs and GPT narratives.
10. **`financial_audit_snapshots`:** LBNL ICE investment-grade avoided loss calculations ($2.58M net avoided loss, 5,495× ROI).
11. **`microclimate_parcel_store`:** Saved FortyGuard parcel geometry, measured peak/spread, coordinates, city, and catalog date; these rows are selectable from Cloud DB to run or replay dashboard calculations.
12. **`bess_degradation_logs`:** 2-state core/surface thermal ODEs & continuous Arrhenius SEI capacity fade (\$/hr).
13. **`cascading_risk_snapshots`:** Poisson-Weibull cascading failure probability ($P_{\text{cascade}}$) & $VoLL$ at risk.
14. **`chance_constrained_opf_logs`:** Analytical quantile-bounded dispatch results under Gaussian uncertainty ($z_{1-\alpha}$).
15. **`cbf_safety_certificates`:** Control Barrier Function QP slack ($\xi^*$) & forward invariance proofs.
16. **`grid_assets_registry`:** Digital twin asset catalog (transformers, substations, BESS units, health scores).

---

## 🚀 Quick Start & How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
cd frontend && npm install && cd ..
```

### 2. Run Automated Pytest Suite (97 Tests Passing)
```bash
pytest tests/ -v
```


### 3. Launch Backend Server & Operator Dashboard
```bash
python3 -m uvicorn src.server.main:app --host 0.0.0.0 --port 8000 --reload
```

Open **[https://www.thermal-sentinel-grid.live](https://www.thermal-sentinel-grid.live)** (or local **[http://localhost:8000](http://localhost:8000)**) in your browser to interact with all 13 dashboard tabs:
1. **Home:** Interactive pitch, live demo video player, and operational launchpad.
2. **Mission Control Overview:** 12-hour synchronized replay scrubber with Apache ECharts 3-axis physics telemetry.
3. **Portfolio Ops:** Deterministic fleet ranking, configurable candidate crew windows, SHA-256 evidence export, and MCP call generation. The current view applies one common Phoenix boundary to the registry and does not claim per-asset scans or occupational-safety certification.
4. **What-If Studio:** Interactive real-time sandbox with multi-physics sliders and 2-state BESS electro-thermal & SEI degradation sub-engine.
5. **72h Compounding:** Continuous 3-day simulation showing progressive soil moisture desertification.
6. **AC Power Flow & DLR:** 4-bus single-line diagram, IEEE 738 Dynamic Line Rating, Arrhenius-Weibull cascading risk, and analytical uncertainty-bounded dispatch.
7. **IEEE Annex G:** Numerical comparison against official IEEE C57.91 standard tables ($<0.0001^\circ\mathrm{C}$ error).
8. **Scientific Provenance:** 22 indexed papers with LaTeX proofs and alphaXiv live search engine.
9. **Hyperlocal 2m GIS:** Parcel-level heat tiles & asset inspector with live FortyGuard cloud scan.
10. **4 Scientific Moats:** Deep-dive physical formulations.
11. **LangGraph Engine:** Visual StateGraph execution inspector with triggerable live mitigation and optional `gpt-5.4` narrative synthesis plus deterministic fallback.
12. **Avoided Loss Financial Audit:** Investment-grade LBNL ICE Calculator ROI model and side-by-side comparison tables.
13. **Data Science Studio:** ETL diagnostics, empirical correlation analysis, surrogate metrics, anomaly detection, and Weibull RUL.


### 4. Launch 3-Minute Video Pitch (HyperFrames Studio Timeline)
```bash
npx hyperframes preview videos/thermal-sentinel-pitch --port 3005
```
Open **[http://localhost:3005/#project/thermal-sentinel-pitch](http://localhost:3005/#project/thermal-sentinel-pitch)** in your browser.

### 5. Launch 5-Minute Live Presentation Slide Deck (Presenter Mode)
```bash
npx hyperframes present decks/thermal-sentinel-slides --port 3004
```
Open **[http://localhost:3004](http://localhost:3004)** in your browser (Press `P` for Audience display / `Space` to advance).

### 6. Render 3-Minute Video Pitch to 1080p MP4
```bash
npx hyperframes render videos/thermal-sentinel-pitch --quality high --output videos/thermal-sentinel-pitch/renders/video.mp4
```

---

### Data Provenance & Measurement Notes

Every metric above is returned by the live FortyGuard API for the pinned
benchmark AOI (downtown Phoenix, `2023-07-19`) and is reproducible by replaying
the same request. Responses carry an explicit `data_source` field:

| `data_source` | Meaning |
| :--- | :--- |
| `fortyguard_live` | 2m temperature, persistence, exceedance and hourly humidity all returned by the API. |
| `fortyguard_live_partial` | Live 2m temperature and persistence; `env_params` was unavailable, so humidity/solar fell back to the benchmark. |
| `phoenix_fixture` | Fully offline replay of the bundled July 2023 fixture. |

Two measurement caveats we think are worth stating plainly:

- **The land-cover delta is $+1.1^\circ\mathrm{C}$, not the $+4.5^\circ\mathrm{C}$ we
  originally assumed.** Measured directly: downtown core $42.74^\circ\mathrm{C}$ vs
  South Mountain natural desert $41.60^\circ\mathrm{C}$ at 15:00. We also probed Sky
  Harbor airport and found it within $0.1^\circ\mathrm{C}$ of downtown — an airport
  ringed by asphalt runways is itself a heat island, so it is *not* a cool
  reference. The honest contrast is urban-vs-natural land cover.
- **Persistence is $12.0\text{h}$, the full width of our forecast window.** The
  2m temperature stayed above $40^\circ\mathrm{C}$ for every sampled hour, so
  $P_{40}$ is bounded below by the window, not by the weather.

Grid-side quantities (`wind_speed_m_s`, `baseline_load_ratio_k`,
`hospital_critical_load_mw`, `bess_soc_pct`) are **modelled**, not measured —
FortyGuard is an environmental API and does not expose SCADA telemetry.
