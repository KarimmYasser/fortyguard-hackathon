# ⚡ Thermal Sentinel Grid — FortyGuard Hackathon '26
> **Physics-Constrained Agentic Thermal Resilience & Dispatch Engine for Grid Assets & Transformers**  
> *Building the World's Temperature AI · Global AI Hackathon (August 18–30, 2026)*

[![Track: Agentic AI](https://img.shields.io/badge/Track%2006-Agentic%20AI-0e9ec4?style=for-the-badge)](https://www.fortyguard.com/hackathon26)
[![Track: Future Buildings & Energy](https://img.shields.io/badge/Track%2002-Future%20Buildings%20%26%20Energy-e8762d?style=for-the-badge)](https://www.fortyguard.com/hackathon26)
[![Standards: IEEE & IEC](https://img.shields.io/badge/Standards-IEEE%20C57.91%20%7C%20IEC%2060076--7-blue?style=for-the-badge)](https://standards.ieee.org/)
[![Safety: Robust CBF-QP](https://img.shields.io/badge/Safety%20Gate-Robust%20CBF--QP-success?style=for-the-badge)](https://github.com/KarimmYasser/fortyguard-hackathon)

---

## 🧭 Executive Summary

During extreme urban heatwaves, standard meteorological forecasts report broad, regional temperatures measured miles away at airports or high above open terrain (e.g., 38°C–42°C). However, critical grid infrastructure—**substation distribution transformers, underground MV cables, padmount switchgear, and outdoor Battery Energy Storage Systems (BESS)**—operates directly within the **2-meter boundary layer** above radiating asphalt and urban street canyons, where convective air temperatures regularly exceed **48°C–52°C**.

This microclimate heat trap creates massive **cumulative thermal soak**, pushing transformer top-oil and winding hot-spot temperatures past critical limits, accelerating insulation aging by orders of magnitude, and driving catastrophic substation blowouts and grid outages.

**Thermal Sentinel Grid** bridges this critical gap by fusing **FortyGuard’s 2-meter hyperlocal Temperature API** with **IEEE C57.91 / IEC 60076-7 thermal differential equations** and an autonomous **LangGraph multi-agent harness guarded by a deterministic Control Barrier Function (CBF-QP) Safety Gate**.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   THE 3 ARCHITECTURAL PILLARS                                            │
│                                                                                                          │
│   1. External Boundary Condition  ──►  FortyGuard 2m Ambient Air + 12h Forecast + Persistence Runs       │
│   2. Physical State Estimation    ──►  IEEE C57.91 / IEC 60076-7 Differential Thermal & Aging Equations  │
│   3. Deterministic Safety Gate    ──►  Robust Control Barrier Function (CBF-QP) Voltage & N-1 Envelopes │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛡️ Four Asymmetric Scientific Moats

Generic hackathon entries rely on simple threshold rules (*"if temp > 40°C, shed load"*). **Thermal Sentinel Grid** models four unmeasured physical cascades that utility SCADA and generic AI miss:

```mermaid
flowchart LR
    A[FortyGuard 2m Microclimate\n12h Forecast, P_theta, H_theta] --> D[Physics Model]
    B[Urban Morphology\nH/W, Imperviousness %, Albedo] --> D
    C[SCADA / Smart-Meter Feeder Load\nAsset Metadata] --> D
    
    D --> E1[1. Cable-Soil Dryout\nSurging rho_soil > 2.5 K·m/W]
    D --> E2[2. Canyon Aerodynamics\nCooling Fin Derate eta_cool]
    D --> E3[3. IEEE Winding Hot-Spot\nTransient Rise T_o & T_hs]
    D --> E4[4. Virtual Paper Moisture\nFickian Dielectric Breakdown]
    
    E1 --> F[Risk Forecaster\n12h Uncertainty Tube]
    E2 --> F
    E3 --> F
    E4 --> F
    
    G[Multi-Agent Planner\nBESS, Cooling, EV Shift] --> H{Robust CBF-QP Safety Gate\nNon-LLM Deterministic Filter}
    F --> H
    H -->|Provably Safe| I[Autonomous Dispatch / Work Order]
```

1. **Buried Cable–Soil Moisture Dryout (IEC 60287):** Ingests 5-day FortyGuard persistence to infer non-linear soil thermal resistivity surge ($\rho_{\text{soil}}$ from $0.9$ to $> 2.5\text{ K}\cdot\text{m/W}$), exposing the hidden underground cable bottleneck.
2. **Provably Safe Control Barrier Functions (CBF-QP):** Enforces forward-invariance of safe thermal sets $\mathcal{C} = \{x : h_o(x) \ge 0, h_{hs}(x) \ge 0\}$ under bounded FortyGuard forecast uncertainty ($\widehat{T}_a \pm \epsilon$).
3. **Urban Canyon Aerodynamic Throttling (Oke / Evola):** Computes morphological wind-sheltering ($\kappa_{\text{morph}}$) and equipment cooling derate ($\eta_{\text{cool}}$) caused by deep building canyons ($H/W$) and reflected facade irradiance.
4. **Virtual Moisture & Dielectric Risk Sensor (Fick's Law):** Models temperature-driven moisture desorption from cellulose paper into oil, alerting to dielectric arcing risk before emergency hot-spot limits trip.

---

## 🔑 Why FortyGuard's 2-Meter Layer is Indispensable

| Dimension | Standard Weather APIs / Satellite LST | FortyGuard Temperature AI |
| :--- | :--- | :--- |
| **Measurement Target** | Coarse regional towers (10–30 km) / Satellite skin LST | **Exact 2-meter convective ambient air at asset parcel (60–100m)** |
| **Microclimate Context** | Blind to asphalt, street canyons, and building shade | **Incorporates land-cover morphology & solar irradiance ($S(t)$)** |
| **Duration Intelligence** | Instantaneous snapshot only | **Continuous Persistence ($P_\theta$) & Degree-Hour Exceedance ($H_\theta$)** |
| **Predictive Horizon** | Macroscopic synoptic forecast | **12-Hour Hyperlocal Forward Forecast** for proactive intervention |
| **Actionability** | *"Airport says 39°C — status normal"* ❌ | *"Asset ambient 47.6°C with 7h persistence"* ⚠️ (Proactive cooling dispatch) |

---

## 🔌 FortyGuard API Dual-Mode Architecture (Live Ingestion vs. Benchmark Replay)
*(For the complete architectural design record, see **[API Integration & Replay Architecture](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/research/API_INTEGRATION_AND_REPLAY_ARCHITECTURE.md)**)*

Thermal Sentinel Grid is built with a dual-mode ingestion pattern:
1. **Mode A: Live Cloud Ingestion (`AsyncFortyGuardClient` / `POST /api/v1/scan`):** Fully integrated with FortyGuard's async submit-and-poll lifecycle (`/v1/heatmap`, `/v1/env_params`, `/v1/status/{activity_id}`, `/v1/system/fetch-api-key-usage`).
2. **Mode B: Deterministic Benchmark Replay (`PhoenixHeatwaveReplayEngine` / `POST /api/v1/replay/phoenix-2023`):** Uses high-resolution pre-ingested Phoenix July 2023 heatwave fixtures ([`phoenix_heatwave_2023.json`](file:///Users/karim/Development/projects/fortyguard-hackathon/src/api/fixtures/phoenix_heatwave_2023.json)). This delivers **$<15\text{ms}$ sub-second ODE solving**, smooth 60 FPS timeline scrubbing, 100% scientific reproducibility for IEEE Annex G validation, and zero-downtime stability during live judging presentations.

---

## ☀️ Historical Benchmark Replay: Phoenix Heatwave (July 2023)

To validate real-world performance, Thermal Sentinel Grid is benchmarked against the historic **Phoenix, Arizona July 2023 heatwave** (31 consecutive days $\ge 110^\circ\mathrm{F}$, peaking at $119^\circ\mathrm{F}$ / $48.3^\circ\mathrm{C}$):

```text
┌───────────────────────────────────────────────┬───────────────────────────────────────────────┐
│ BASELINE CONTROLLER (Airport Weather + Static)│ THERMAL SENTINEL GRID (FortyGuard + Physical) │
├───────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ • Relies on distant airport weather (43.1°C)  │ • Detects parcel 2m ambient (47.6°C, +4.5°C)  │
│ • Blind to 7h 10m continuous persistence      │ • 12h forward warning triggers proactive pre-cool│
│ • Hot-spot breaches 140°C emergency ceiling   │ • Projected hot-spot safely capped at 136.8°C  │
│ • Accelerated insulation aging (V = 14.8x)    │ • 73.4 avoided equivalent aging hours (L_eq)  │
│ • Unplanned emergency load shedding           │ • Zero voltage (0.95-1.05pu) & N-1 violations │
└───────────────────────────────────────────────┴───────────────────────────────────────────────┘
```

---

## 💰 Investment-Grade Economic Model

Thermal Sentinel Grid computes non-overlapping, auditable avoided loss metrics:

$$\boxed{\text{Net Avoided Loss} = \left[p_{f,\text{base}} - p_{f,\text{mitigated}}\right] \cdot C_{\text{consequence}} + \Delta PV_{\text{aging}} - C_{\text{mitigation}}}$$

* **Avoided Outage Consequence ($C_{\text{consequence}}$):** Emergency replacement + customer interruption costs ($VoLL$ via LBNL ICE Calculator) + SAIDI/SAIFI reliability incentives.
* **Capital Deferral ($\Delta PV_{\text{aging}}$):** Present value of deferred transformer capital replacement ($C_{\text{replace}}$ over 180,000-hour design life).
* **Net Operational ROI:** Replay demonstrates **$175,276 net avoided loss per extreme heat event** at an ROI multiple of $> 24\text{x}$.

---

## 📁 Repository Structure

```
fortyguard-hackathon/
├── README.md                           # Main Project Overview & Architecture
├── AGENT_CONTEXT.md                    # Master Knowledge Reservoir (All Ideas, Background, Research)
├── docs/                               # Comprehensive Documentation & Reference Hub
│   ├── README.md                       # Master Documentation Index
│   ├── official/                       # Hackathon Official Rules, FAQ, Tracks & Announcements
│   ├── research/                       # Physical AI Specs, Math Equations, CBF-QP & Pitch Script
│   │   ├── README.md                   # Research Catalog Index
│   │   ├── THERMAL_SENTINEL_GRID_SPECIFICATION.md # Full math, IEEE/IEC equations & StateGraph
│   │   ├── ASYMMETRIC_INNOVATION_AND_PHYSICAL_MECHANISMS.md # 4 asymmetric scientific moats
│   │   ├── ECONOMIC_MODEL_DASHBOARD_AND_PITCH_SCRIPT.md # Avoided loss ROI & 3-min video script
│   │   ├── RESEARCH_AGENT_SYNTHESIS_AND_PHYSICAL_MODELS.md # 2m meteorological gap & standards
│   │   └── MENTOR_INSIGHTS_AND_IDEA_FRAMEWORK.md # Mentorship keynote synthesis
│   ├── sessions-dialogue/              # Full Webinar Transcripts (Fawad, Jordana, Ashan, Onboarding)
│   ├── api-documentation/              # OpenAPI Schemas & FortyGuard Endpoint Guides
│   ├── handbook/                       # Participant Handbook & Official Scoring Rubrics
│   ├── project-registration/           # PyreShield Registration Pitch & Strategy History
│   └── context/                        # Chat Transcripts & Brainstorming Action Logs
├── temperature-api-quickstart/         # Official FortyGuard Quickstart SDK & Notebooks
├── src/                                # Thermal Sentinel Core Application
│   ├── api/                            # FortyGuard Async Submit-and-Poll Client & Tool Adapters
│   ├── physics/                        # IEEE C57.91 / IEC 60076-7 Solvers & Soil Moisture State
│   ├── safety/                         # Robust CBF-QP Deterministic Safety Gate
│   ├── models/                         # Asset, Risk, and Thermal Pydantic Schemas
│   ├── agent/                          # LangGraph StateGraph, Evaluators & Planners
│   └── server/                         # FastAPI Application & Operator Dashboard API
└── tests/                              # Automated Pytest Physics & Safety Validation Suite
```

---

## 🚀 Quick Start & How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
cd frontend && npm install && cd ..
```

### 2. Run Automated Pytest Suite (23 Tests Passing)
```bash
pytest tests/ -v
```

### 3. Launch Backend API & Interactive Dashboard
```bash
python3 -m uvicorn src.server.main:app --host 127.0.0.1 --port 8000 --reload
```
Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

---

## 🖥️ Interactive Operator Dashboard Features

* **Mission Control Overview:** 12-hour synchronized replay scrubber with Apache ECharts 3-axis physics telemetry.
* **⚡ Live "What-If" Physics Stress Studio:** Interactive real-time sandbox allowing judges to modulate FortyGuard 2m delta ($0^\circ\mathrm{C} \to +6^\circ\mathrm{C}$), multi-day heatwave dryout (Day 1 to 31), BESS capacity ($0 \to 50\text{ MWh}$), and transformer MVA with sub-15ms live ODE recalculation.
* **Hyperlocal 2-Meter GIS Viewer:** Parcel-level convective heat tiles ($60\text{m}$ resolution) and interactive asset inspector.
* **Four Scientific Moats Viewer:** First-principles deep dives into Cable-Soil dryout, CBF-QP safety filter, Canyon aerodynamics, and Virtual moisture sensor.
* **LangGraph Engine:** Visual StateGraph execution inspector with triggerable live mitigation.
* **Avoided Loss Financial Audit:** Investment-grade LBNL ICE Calculator ROI model and side-by-side comparison tables.

---

## 👨‍💻 Author & Research Background

**Karim Yasser** — *Computer Engineering, Cairo University Faculty of Engineering*  
* **AI Research Intern at Nile University SESC Research Center:** Architected autonomous multi-agent OpenFOAM CFD/thermal numerical pipeline; co-authoring upcoming research publication.
* **Software Engineering Intern at Siemens Digital Industries Software:** High-performance CAT RTS engine (54.5x speedup, large-scale concurrent data ingestion).
* **Portfolio:** [karim-yasser.vercel.app](https://karim-yasser.vercel.app) · **GitHub:** [@KarimmYasser](https://github.com/KarimmYasser)

