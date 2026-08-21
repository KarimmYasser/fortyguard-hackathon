# 🔌 FortyGuard API Integration, Live Ingestion & Simulation Architecture Specification
> **Architecture Decision Record (ADR): Dual-Mode Microclimate Ingestion & System Boundary Specification**  
> **Status:** Accepted & Implemented (Intended Production Design)  
> **Applicable Tracks:** Track 06 (Agentic AI) & Track 02 (Future Buildings & Energy)

---

## 🧭 1. Executive Summary: Dual-Mode Ingestion Philosophy

Thermal Sentinel Grid implements an industry-standard, production-grade **Dual-Mode Microclimate Ingestion Architecture**. The system operates across two complementary ingestion pathways:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              DUAL-MODE MICROCLIMATE INGESTION ARCHITECTURE                             │
│                                                                                                        │
│   ┌──────────────────────────────────────────────┐    ┌────────────────────────────────────────────┐   │
│   │       MODE A: LIVE CLOUD API INGESTION       │    │   MODE B: DETERMINISTIC BENCHMARK REPLAY   │   │
│   │       (Async submit-and-poll lifecycle)      │    │   (Zero-latency IEEE standards validation) │   │
│   ├──────────────────────────────────────────────┤    ├────────────────────────────────────────────┤   │
│   │ • Route: POST /api/v1/scan                   │    │ • Route: POST /api/v1/replay/phoenix-2023  │   │
│   │ • Target: api.fortyguard.com/v1/*            │    │ • Source: phoenix_heatwave_2023.json       │   │
│   │ • Purpose: Hyperlocal ad-hoc parcel scanning │    │ • Purpose: Interactive Mission Control     │   │
│   │ • Latency: 3-15 seconds (Cloud Task Worker)  │    │ • Latency: < 10 ms (Sub-second physics ODE)│   │
│   │ • Billing: Real credit deduction (live)      │    │ • Billing: 0 credits (Cached baseline)     │   │
│   └──────────────────────────────────────────────┘    └────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔍 2. Comprehensive System Taxonomy: Live vs. Physics vs. Simulated

To maintain full transparency for hackathon judging and production validation, the entire codebase is categorized into three distinct operational layers:

### 🟢 Layer 1: Live Cloud Integrations (Real External APIs)
These components communicate with real external cloud services and update remote ledgers in real time:

| Component | Endpoint / Service | Live Behavior |
| :--- | :--- | :--- |
| **FortyGuard Quota Hub** | `POST /v1/system/fetch-api-key-usage` | Fetches real-time billing cycles, plan status, and remaining credit balances. |
| **Ad-Hoc Microclimate Scan** | `POST /v1/env_params` | Dispatches live cloud tasks; polls async status queue; returns live Heat Index, Apparent Temp, Wet Bulb, AQI, and Clear-Sky Solar Irradiance ($GHI$). Deducts live credits upon completion. |
| **Spatial AOI Heatmap** | `POST /v1/heatmap` | Generates 2-meter thermal raster GeoJSON tiles across user-specified polygon coordinates. Deducts live credits. |
| **Siemens SDC LLM Gateway** | `https://llm.sdc.siemens.cloud/v1` | Routes LangGraph agent reasoning through GPT-5 / Claude Sonnet models when API keys are configured. |

---

### ⚡ Layer 2: Real Physics Solvers (Calculated Live via Differential Equations)
These are **not static mocks or hardcoded tables**. Every value is computed in real time by continuous numerical ODE solvers and IEEE standard equations:

| Physics Engine | Standard / Formulation | Exact Mathematical Implementation |
| :--- | :--- | :--- |
| **Transformer Thermal Dynamics** | **IEEE Std C57.91-2011 Annex G** | 2nd-order non-linear differential equations: $\tau_{TO} \frac{d\Theta_{TO}}{dt} = [\Delta\Theta_{TO,U} - \Delta\Theta_{TO}]$ and $\tau_W \frac{d\Delta\Theta_H}{dt} = [\Delta\Theta_{H,U} - \Delta\Theta_H]$. |
| **Arrhenius Insulation Aging** | **Arrhenius Loss of Life** | Exact Arrhenius aging acceleration factor: $F_{AA} = \exp\left(\frac{15000}{383.15} - \frac{15000}{\Theta_H + 273.15}\right)$ and equivalent aging $F_{EQ} = \frac{1}{T} \int_0^T F_{AA}(t) dt$. |
| **Underground Cable Soil Dryout** | **IEC 60287-2-1** | 3-zone transient soil thermal resistivity solver with critical moisture threshold ($\psi_{\text{crit}}$) and thermal runaway boundary. |
| **AC Power Flow & Voltage Stability** | **14-Bus Newton-Raphson** | Full non-linear AC power flow calculating active/reactive power ($P_i, Q_i$), bus voltages ($V_i, \theta_i$), and On-Load Tap Changer (OLTC) stepping. |
| **Safety Barrier Invariance** | **Control Barrier Functions (CBF-QP)** | Quadratic program ensuring safety set invariance: $h(x) = \Theta_{H,\max} - \Theta_H \ge 0$ with Lie derivative constraint $\dot{h}(x) \ge -\gamma h(x)$. |
| **Avoided Loss Financial Model** | **LBNL ICE Calculator** | Quantifies avoided capital loss ($\text{Asset Value} \times \Delta L$) minus BESS cycling wear and auxiliary fan kWh costs. |

---

### 📦 Layer 3: Simulated, Modeled & Cached Elements

| Item | Source Location | Status | Architectural Justification |
| :--- | :--- | :---: | :--- |
| **Phoenix July 2023 Replay Dataset** | [`src/api/fixtures/phoenix_heatwave_2023.json`](file:///Users/karim/Development/projects/fortyguard-hackathon/src/api/fixtures/phoenix_heatwave_2023.json) | **Cached Fixture** | Pre-ingested benchmark ground truth. Enables sub-10ms scrubbing on the interactive 12-hour replay bar and offline judging tests without burning API credits on every slider tick. |
| **Utility Substation Assets** | [`src/server/routes/assets.py`](file:///Users/karim/Development/projects/fortyguard-hackathon/src/server/routes/assets.py) | **Synthetic Asset Registry** | 3 representative transformer nameplate profiles (Phoenix TX-04 50 MVA, San Jose Diridon 35 MVA, Las Vegas Strip 60 MVA) parameterized per IEEE standards. |
| **Baseline Grid Load Curve** | [`src/physics/transformer_thermal.py`](file:///Users/karim/Development/projects/fortyguard-hackathon/src/physics/transformer_thermal.py) | **Simulated Profile** | Diurnal load curve ($0.75\,\text{pu}$ morning ramp to $1.18\,\text{pu}$ afternoon peak) modeling desert urban summer air conditioning demand. |
| **Hardware Actuator Signals** | [`src/models/safety.py`](file:///Users/karim/Development/projects/fortyguard-hackathon/src/models/safety.py) | **Simulated Actuation** | Generates schema-validated dispatch commands (`COOLING_STAGE_2`, `BESS_PEAK_SHAVING`, `EV_SMART_CURTAIL`, `FEEDER_TRANSFER`) for software state machines rather than physical substation SCADA RTUs. |

---

## 🏛️ 3. Why the Simulated Elements Must NOT Be Changed

A common question is whether the simulated elements should be connected to "live" feeds. **The engineering answer is an emphatic NO.** Modifying these elements would degrade the system, introduce unneeded fragility, and violate core software engineering principles:

### 1. Phoenix July 2023 Dataset (`phoenix_heatwave_2023.json`)
* **Sub-10ms UI Responsiveness:** Scrubbing the 12-hour replay timeline or adjusting the **What-If Studio** sliders requires instantaneous ODE recalculation ($<10\text{ ms}$). Waiting 30–90 seconds for a cloud API roundtrip on every tick would destroy real-time operator usability.
* **Scientific Ground Truth & IEEE Annex G Reproducibility:** Evaluating transformer hot-spot rise ($143.2^\circ\mathrm{C} \to 136.8^\circ\mathrm{C}$) and Arrhenius life extension ($846.8\text{ h saved}$) requires an **immutable, standardized weather boundary condition** that judges and automated test suites (`pytest tests/`) can verify identically every time.
* **Credit Conservation:** Running continuous automated integration tests or live presentations against FortyGuard's billing endpoints on every page reload would rapidly exhaust the 2,000,000 credit quota.

### 2. Utility Substation Assets (`assets.py`)
* Nameplate parameters (50 MVA rating, $\tau_{TO} = 180\text{ min}$, $\tau_W = 4.8\text{ min}$, $R = 5.0$, exponents $m = 0.8, n = 0.8$) are **physical hardware constants from IEEE C57.91-2011 Table 1 / Annex G**.
* In real-world utility Energy Management Systems (EMS), these reside in static asset registries (CIM/GIS databases). Defining standardized profiles for Phoenix, San Jose, and Las Vegas is the industry-standard methodology for digital twins.

### 3. Baseline Grid Load Curve (`transformer_thermal.py`)
* The $0.75\,\text{pu} \to 1.18\,\text{pu}$ diurnal load shape models peak heatwave cooling demand. In a digital twin, using a calibrated diurnal load shape is standard practice to test whether mitigation agents successfully shave peak load ($1.18\,\text{pu} \to 0.98\,\text{pu}$).

### 4. Hardware Actuator Signals (`safety.py`)
* A hackathon software system cannot physically trip real high-voltage $69\,\text{kV}$ substation circuit breakers, discharge physical utility battery banks, or spin physical radiator fans. Emitting structured, schema-validated dispatch payloads with mathematically verified **CBF-QP safety invariants** is the exact objective for **Track 06 (Agentic AI)** and **Track 02 (Future Buildings & Energy)**.

---

## 📊 4. FortyGuard Billing & Credit Consumption Rules

| Endpoint | Type | Billable? | Credit Behavior |
| :--- | :--- | :--- | :--- |
| `POST /v1/system/fetch-api-key-usage` | System Status | ❌ **Free (0 credits)** | Returns remaining balance & active plan details |
| `POST /v1/system/fetch-api-key-custom-usage` | System Status | ❌ **Free (0 credits)** | Queries historical credit consumption window |
| `POST /v1/heatmap` (`tcm` / `persistence`) | Analysis Engine | ✅ **Billable** | Deducts credits only upon task status = `"succeeded"` |
| `POST /v1/satellite` | Computer Vision | ✅ **Billable** | Deducts credits upon completion |
| `POST /v1/env_params` | Microclimate Index | ✅ **Billable** | Deducts credits upon completion |
| `POST /v1/heat_intelligence` | Synthesis Report | ✅ **Billable** | Deducts credits upon PDF report generation |

---

## 🧪 5. How to Trigger Live API Calls & Verify Credits

### A. Programmatic Credit Verification (Python)
```python
from src.api.fortyguard_client import FortyGuardClient

client = FortyGuardClient()
usage = client.fetch_api_key_usage()
print("Plan:", usage["plan_details"]["plan_type"])
print("Remaining Credits:", usage["credit_summary"]["cycle_remaining_credits"])
print("Credits Used This Cycle:", usage["credit_summary"]["cycle_credits_used"])
```

### B. Live Spatial Scan Execution (cURL)
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/scan" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "San Jose, CA (Diridon Energy Hub)",
    "latitude": 37.3382,
    "longitude": -121.8863,
    "start_date": "2024-07-15",
    "analytic_type": "tcm",
    "threshold_c": 35.0
  }'
```

### C. Live Quickstart Notebooks
Navigate to [`temperature-api-quickstart/notebooks/`](file:///Users/karim/Development/projects/fortyguard-hackathon/temperature-api-quickstart/notebooks/) and execute any notebook (e.g. `01_create_heatmap.ipynb`, `02_environmental_parameters.ipynb`) with `REFRESH = True` to run live cloud queries against FortyGuard's infrastructure.
