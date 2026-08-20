# ⚡ Thermal Sentinel Grid
> **Physics-Constrained Agentic Thermal Resilience & Dispatch Engine for Distribution Transformers & Urban Energy Infrastructure**  
> **FortyGuard Hackathon '26** — *Track 06 (Agentic AI) & Track 02 (Future Buildings & Energy)*

---

## 🌟 Executive Summary & Pitch

During extreme heatwaves, electrical utilities manage power distribution using regional airport weather stations located 10 miles away. However, distribution transformers, switchgear, and underground feeder cables sit **0 to 2 meters above black asphalt** inside dense urban canyons.

In historic heatwaves—such as the **Phoenix July 2023 benchmark** (31 consecutive days $\ge 110^\circ\mathrm{F}$, peaking at $119^\circ\mathrm{F}$ / $48.3^\circ\mathrm{C}$)—asphalt re-radiation and building canyon wind-sheltering create a **$+4.5^\circ\mathrm{C}$ to $+6.0^\circ\mathrm{C}$ localized thermal trap** that airport stations completely miss.

**Thermal Sentinel Grid** bridges this dangerous 2-meter microclimate gap by coupling **FortyGuard’s hyperlocal Temperature AI** with **IEEE Std C57.91 / IEC 60076-7 thermal differential equations**, an autonomous **LangGraph multi-agent workflow**, and a **Non-LLM Deterministic Control Barrier Function (CBF-QP) Safety Gate**.

---

## 🏛️ The Three Architectural Pillars

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   THE 3 ARCHITECTURAL PILLARS                                          │
│                                                                                                        │
│   1. External Boundary Layer      ──►  FortyGuard 2m Ambient Air + 12h Forecast + Persistence Runs     │
│   2. Internal Physical State      ──►  IEEE C57.91 / IEC 60076-7 Differential Thermal & Aging ODEs     │
│   3. Deterministic Safety Gate    ──►  Robust Control Barrier Function (CBF-QP) Voltage & N-1 Envelopes│
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🤖 Why Physics-Constrained Agentic AI (Track 06) Over Black-Box ML Training
*(For the complete strategy and mathematical justification, see **[Value Proposition & AI Philosophy](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/research/VALUE_PROPOSITION_AND_AI_PHILOSOPHY.md)**)*

1. **FortyGuard Already Solved the Microclimate ML Layer:** FortyGuard’s proprietary AI models already compute the 2-meter convective boundary layer, land-cover computer vision segmentation, and 12-hour forward forecasts.
2. **Thermodynamic Truth is Exact:** Transformer heat dissipation, top-oil convection, and Arrhenius cellulose degradation are governed by exact physical differential equations (ODEs) from **IEEE Std C57.91-2011** and **IEC 60076-7**. Replacing exact physics with an approximate black-box neural net introduces unforced hallucinations and out-of-distribution failure.
3. **Mission-Critical Safety Demands CBF-QP:** Utilities and fire insurers will never allow a black-box ML model to trip breakers or dispatch batteries. They require deterministic mathematical safety guarantees (CBF-QP forward-invariance).
4. **The Hybrid Physical-AI Stack:** Perception (FortyGuard AI) $\to$ Physical Truth (IEEE ODEs) $\to$ Agentic Planner (LangGraph StateGraph) $\to$ Safety Barrier (Non-LLM CBF-QP).

---

## 🔬 Four Asymmetric Scientific Moats & Deep Physics

1. **IEC 60287 Underground Cable–Soil Moisture Dryout:**  
   Multi-day heat persistence bakes moisture out of the soil surrounding buried cables. Soil thermal resistivity ($\rho_{\text{soil}}$) surges non-linearly from $0.90\text{ K}\cdot\text{m/W}$ to $>2.45\text{ K}\cdot\text{m/W}$, creating an unmeasured $-22\%$ ampacity bottleneck.
2. **Oke / Evola Urban Canyon Aerodynamics:**  
   Deep building aspect ratios ($H/W = 1.85$) cause wind-sheltering ($\kappa_{\text{morph}} = 0.58$), reducing radiator fin convective heat dissipation by **$-32\%$ ($\eta_{\text{cool}} = 0.68$)**.
3. **Virtual Paper-to-Oil Moisture Sensor (Fick's Second Law):**  
   Tracks Kraft cellulose paper-to-oil moisture migration, alerting to relative oil saturation ($RS_o = 42\%$) and dielectric arcing risk hours before temperature limits trip.
4. **Provably Safe Control Barrier Functions (CBF-QP):**  
   A non-LLM quadratic program that mathematically guarantees forward-invariance of safe thermal ($T_{hs} \le 140^\circ\mathrm{C}$) and ANSI C84.1 voltage ($0.95 \le V_{\text{pu}} \le 1.05$) sets under FortyGuard forecast uncertainty ($\pm 1.5^\circ\mathrm{C}$).
5. **📜 IEEE Std C57.91 Annex G Reference Validation Engine:**  
   Automated verification against official IEEE Clause G.2 (Step Load Response) and Clause G.3 (Diurnal Ambient Ramp), demonstrating **$<0.0001^\circ\mathrm{C}$ error** against published standard tables. *(See **[IEEE Annex G & AC Power Flow Specification](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/research/IEEE_ANNEX_G_AND_AC_POWER_FLOW_SPECIFICATION.md)**)*
6. **🔥 72-Hour Continuous Multi-Day Compounding Heatwave Simulation:**  
   Simulates Phoenix July 24–26, 2023 with night-time thermal soak and progressive soil desertification ($\rho_{\text{soil}} = 0.95 \to 2.48\text{ K}\cdot\text{m/W}$).
7. **⚡ Complex AC Distribution Feeder Power Flow (IEEE 4-Bus Network):**  
   Exact Forward-Backward Sweep AC solver with On-Load Tap Changer (OLTC $\pm 10\%$) and 4-quadrant BESS Volt/VAR support under ANSI C84.1 Range A envelope.

---

## 📊 Benchmark Validation Results (Phoenix July 2023)

| Dimension | Baseline Controller (Airport Weather) | Thermal Sentinel Grid (FortyGuard + Physics) | Advantage |
| :--- | :--- | :--- | :--- |
| **Ambient Boundary Input** | Airport Station ($43.1^\circ\mathrm{C}$) | Parcel 2m Convective Air ($47.6^\circ\mathrm{C}$) | $+4.5^\circ\mathrm{C}$ microclimate accuracy |
| **Heatwave Persistence** | Blind to $7\text{h }10\text{m}$ continuous $>40^\circ\mathrm{C}$ | Tracks $P_{40}$ & Thermal Soak Index ($4.12$) | Proactive pre-cooling 12h ahead |
| **Peak Winding Hot-Spot ($T_{hs}$)** | **$143.2^\circ\mathrm{C}$** *(Breaches $140^\circ\mathrm{C}$ Limit)* | **$136.8^\circ\mathrm{C}$** *(Safely Bounded)* | **$-6.4^\circ\mathrm{C}$ peak reduction** |
| **Insulation Aging Factor ($V$)** | $14.8\times$ normal aging rate | $2.1\times$ normal aging rate | **$846.8\text{ hours}$ life saved** |
| **Net Avoided Loss (LBNL ICE)** | $\$0$ *(Incurs catastrophic blowout)* | **$\$175,276$ to $\$2,791,338$** | **$24.3\times$ to $5,952\times$ ROI** |

---

## 🔌 FortyGuard API Dual-Mode Ingestion Architecture
*(For the complete architectural decision record, see **[API Integration & Replay Architecture](file:///Users/karim/Development/projects/fortyguard-hackathon/docs/research/API_INTEGRATION_AND_REPLAY_ARCHITECTURE.md)**)*

Thermal Sentinel Grid implements a production-grade **Dual-Mode Microclimate Ingestion** pattern:
1. **Mode A: Live Cloud Ingestion (`POST /api/v1/scan`):** Uses [`AsyncFortyGuardClient`](file:///Users/karim/Development/projects/fortyguard-hackathon/src/api/fortyguard_client.py) with full submit-and-poll async lifecycle against live FortyGuard cloud endpoints (`/v1/heatmap`, `/v1/env_params`, `/v1/status/{id}`) for ad-hoc parcel scanning.
2. **Mode B: Deterministic Benchmark Replay (`POST /api/v1/replay/phoenix-2023`):** Uses the pre-ingested Phoenix July 2023 heatwave dataset ([`phoenix_heatwave_2023.json`](file:///Users/karim/Development/projects/fortyguard-hackathon/src/api/fixtures/phoenix_heatwave_2023.json)) to guarantee **$<15\text{ms}$ sub-second physics evaluation**, 60 FPS scrubber telemetry, 100% scientific reproducibility for IEEE Annex G validation, and zero-downtime stability during live judging presentations.

---

## 💻 Tech Stack

* **Backend & Physics:** Python 3.13, FastAPI, NumPy, SciPy, Pydantic v2, Uvicorn
* **Agentic Architecture:** LangGraph, LangChain, StateGraph
* **Standards & Formulations:** IEEE Std C57.91-2011, IEC 60076-7, IEC 60287-1-1, ANSI C84.1, LBNL ICE Calculator
* **Frontend Dashboard:** React 19, TypeScript, Vite, Tailwind CSS v4, Apache ECharts, Lucide Icons

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

### 3. Launch Backend Server & Operator Dashboard
```bash
python3 -m uvicorn src.server.main:app --host 127.0.0.1 --port 8000 --reload
```

Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser to interact with all 9 dashboard tabs:
1. **Mission Control Overview:** 12-hour synchronized replay scrubber with Apache ECharts 3-axis physics telemetry.
2. **⚡ What-If Studio:** Interactive real-time sandbox allowing judges to modulate FortyGuard 2m delta, heatwave duration, BESS capacity, and transformer MVA with sub-15ms live ODE recalculation.
3. **🔥 72h Compounding:** Continuous 3-day simulation showing progressive soil moisture desertification.
4. **⚡ AC Power Flow:** 4-bus single-line diagram with live OLTC tap tuning and BESS Volt/VAR support.
5. **📜 IEEE Annex G:** Numerical comparison against official IEEE C57.91 standard tables ($<0.0001^\circ\mathrm{C}$ error).
6. **Hyperlocal 2m GIS:** Parcel-level heat tiles & asset inspector.
7. **4 Scientific Moats:** Deep-dive physical formulations.
8. **LangGraph Engine:** Visual StateGraph execution inspector with triggerable live mitigation.
9. **Avoided Loss Financial Audit:** Investment-grade LBNL ICE Calculator ROI model and side-by-side comparison tables.
