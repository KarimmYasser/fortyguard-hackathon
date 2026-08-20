# 💰 Economic Model, Operator UI Architecture & 3-Minute Pitch Script
> **FortyGuard Hackathon '26 — Thermal Sentinel Grid**  
> Complete investment-grade avoided loss formulation, React/Vite operator dashboard layout, and second-by-second video pitch script.

---

## 1. 💵 Economic & Loss-of-Life Cost Quantifier

### 1.1 Core Economic Principle
Separate thermal risk into two mutually exclusive, non-overlapping cost buckets:
1. **Gradual Asset-Life Consumption:** Accelerated insulation aging bringing forward future capital replacement ($\Delta PV_{\text{aging}}$).
2. **Acute Failure Consequence ($C_{\text{consequence}}$):** Probabilistic catastrophic event including emergency replacement, customer interruption ($VoLL$), crew overtime, and regulatory penalties.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                     NET AVOIDED LOSS EQUATION                                            │
│                                                                                                          │
│   Net Avoided Loss = [p_{f,base} - p_{f,mitigated}] · C_{consequence} + ΔPV_{aging} - C_{mitigation}     │
│                                                                                                          │
│   Where:                                                                                                 │
│   • p_f: Logistic failure probability under thermal soak & hot-spot trajectory                          │
│   • C_{consequence}: Emergency replacement + Interruption (VoLL) + Crew + Reliability penalties         │
│   • ΔPV_{aging}: Present value of deferred capital replacement from avoided loss-of-life (ΔL_{eq})      │
│   • C_{mitigation}: BESS dispatch degradation + Fan/pump cooling energy + Load shift inconvenience      │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 1.2 Asset-Life Consumption & Replacement Cost
* **Standard Design Life:** $L_{\text{design}} = 180{,}000\text{ equivalent hours}$ ($\approx 20\text{ years}$ at reference $110^\circ\mathrm{C}$).
* **Straight-Line Aging Cost Rate:**
  $$C_{\text{aging/hr}} = \frac{C_{\text{replace}}}{L_{\text{design}}}$$
* **Discounted Replacement Deferral Model:**
  $$Y_{\text{replace},s} = \frac{L_{\text{design}} - L_{\text{used}} - L_{\text{eq},s}}{\bar{L}_{\text{eq,annual},s}}$$
  $$\Delta PV_{\text{aging}} = \frac{C_{\text{replace}}}{(1 + r)^{Y_{\text{replace,baseline}}}} - \frac{C_{\text{replace}}}{(1 + r)^{Y_{\text{replace,mitigated}}}}$$

---

### 1.3 Failure Probability & Consequence Formulation

#### A. Calibrated Logistic Failure Model
$$p_f = \sigma(z) = \frac{1}{1 + e^{-z}}$$
$$z = \beta_0 + \beta_1 \max(0, T_{hs}^U - T_{hs,\text{warn}}) + \beta_2 \max(0, T_o^U - T_{o,\text{warn}}) + \beta_3 \mathrm{TSI} + \beta_4 L_{\text{used}}^{*} + \beta_5 A_{\text{cooling}}$$

#### B. Full Consequence Breakdown
$$C_{\text{consequence}} = C_{\text{emg-replace}} + C_{\text{interruption}} + C_{\text{critical}} + C_{\text{crew}} + C_{\text{collateral}} + C_{\text{reliability}}$$
* **Customer Interruption ($C_{\text{interruption}}$):** $\sum_c E_{\text{unserved},c} \cdot VoLL_c$ (using LBNL Interruption Cost Estimate / ICE Calculator standards).
* **Reliability Metrics ($\Delta\mathrm{SAIDI}, \Delta\mathrm{SAIFI}$):** Tracking average customer interruption duration and frequency.

---

### 1.4 Mitigation Cost Model
$$C_{\text{mitigation}} = C_{\text{BESS}} + C_{\text{curtailment}} + C_{\text{cooling}} + C_{\text{switching}}$$
* $C_{\text{BESS}} = E_{\text{discharged}} \cdot (c_{\text{degradation}} + c_{\text{opportunity}}) + C_{\text{recharge}}$
* $C_{\text{cooling}} = \int P_{\text{fan/pump}}(t) \cdot p_{\text{electricity}}(t)\,dt$

---

## 2. 🖥️ React/Vite Operator Dashboard Architecture

### 2.1 Layout Wireframe & Panel Composition

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ Header: Event Status | City: Phoenix, AZ | Asset: TX-04 | Replay Clock: 14:30│
├───────────────────────────────┬─────────────────────────────────────────────┤
│                               │  Risk Command Panel                         │
│  Geospatial Microclimate Map  │  • Risk Tier: OPERATOR ACTION REQUIRED      │
│  Deck.gl / MapLibre GL        │  • Projected Hot-Spot: 136.8°C (Max: 140°C) │
│  • FortyGuard 2m Heat Raster  │  • Continuous Persistence: 7h 10m > 40°C    │
│  • Substation & BESS Glyphs   │  • Failure-Risk Delta: -6.5 pp              │
│  • Land-Cover Segmentation    │  • Net Avoided Loss: $175,276               │
│  • Airport Reference Marker   │  • Action: Enable Stage 2 Cooling + BESS    │
├───────────────────────────────┴─────────────────────────────────────────────┤
│ Physics Telemetry (Apache ECharts 3-Axis Synchronized Timeline):            │
│ Chart A: Boundary Temp (Airport 43.1°C vs FortyGuard 2m 47.6°C [+4.5°C])   │
│ Chart B: Internal State (Top-Oil 104.2°C < 110°C, Hot-Spot 136.8°C < 140°C) │
│ Chart C: Aging Factor V(t) (Log scale: 1x -> 14.8x) & Load Ratio K(t)       │
├───────────────────────────────────────────────┬─────────────────────────────┤
│ Deterministic Safety Gate Preflight           │ Audit & Action Ledger       │
│ [✓ ACCEPT]  [△ MODIFY]  [✕ REJECT]            │ 14:05 Ingest 7h persistence │
│ ✓ IEEE C57.91 Hot-Spot Envelope               │ 14:06 Baseline hot-spot 143C│
│ ✓ Voltage Envelope (0.963 - 1.032 pu)         │ 14:07 Safety Gate modifies  │
│ ✓ N-1 Feeder & Inverter Contingency           │ 14:08 Operator approval     │
│ ✓ BESS Reserve (SOC 38% > 30% min)            │ 14:30 Hotspot capped 136.8C │
└───────────────────────────────────────────────┴─────────────────────────────┘
```

### 2.2 Technology Stack
* **Framework:** React 19 + Vite + TypeScript
* **State Management:** Zustand (incident/replay state) + TanStack Query (API caching & async polling)
* **Geospatial Rendering:** Deck.gl + MapLibre GL / Mapbox GL
* **Physics Charts:** Apache ECharts (multi-axis, high-performance synchronized time-series)
* **UI & Styling:** Tailwind CSS + Lucide Icons + Glassmorphic dark aesthetic

---

## 3. 🎬 3-Minute Video Pitch Script (Second-by-Second)

```
                                  VIDEO PITCH TIMELINE (180 SECONDS)
   0:00 ─────────── 0:45 ─────────── 1:45 ─────────── 2:30 ─────────── 3:00
   [  Problem &   ] [ Live Replay  ] [  Safety Gate  ] [ Commercial   ]
   [ Physical Gap ] [ Demonstration] [ & Architecture] [  ROI & GTM   ]
```

### ⏱️ 0:00–0:12 — Opening Hook
* **Visual:** Split screen. Left: generic airport weather reading ($43.1^\circ\mathrm{C}$). Right: FortyGuard parcel-level Phoenix thermal map ($47.6^\circ\mathrm{C}$). Center: Substation transformer turning from amber to blinking red.
* **Voiceover:** *"Utilities still protect billion-dollar grid assets using weather data measured miles away at airports. But during heatwaves, the temperature at a shaded airport is NOT the temperature enveloping a transformer sitting on sun-baked asphalt."*
* **On-Screen Text:** `AIRPORT WEATHER ≠ ASSET MICROCLIMATE`

### ⏱️ 0:12–0:25 — The Physical Blind Spot
* **Visual:** Zoom into Phoenix urban substation. Overlay: `Airport: 43.1°C`, `FortyGuard 2m: 47.6°C`, `Microclimate Delta: +4.5°C`. Highlight land cover (asphalt, concrete buildings, zero canopy).
* **Voiceover:** *"FortyGuard gives us the missing convective and radiative boundary condition: exact 2-meter ambient air temperature, solar irradiance, land-cover context, and—critically—how long dangerous heat persists."*

### ⏱️ 0:25–0:45 — Thermal Soak & Failure Physics
* **Visual:** Transition to internal transformer cutaway diagram with dynamic heat equation: $T_{hs} = T_a + \theta_o + \theta_w$. Show oil boiling and insulation aging curve accelerating exponentially.
* **Voiceover:** *"Transformers do not fail from a brief temperature spike. Disasters occur from cumulative thermal soak. A few hours of persistent heat pushes top-oil and winding hot-spots past critical insulation thresholds, accelerating aging by up to 15 times."*

### ⏱️ 0:45–1:00 — Phoenix July 2023 Replay Setup
* **Visual:** Operator dashboard loading the **Phoenix July 24–25, 2023 heatwave** (31 consecutive days $\ge 110^\circ\mathrm{F}$, peaking at $119^\circ\mathrm{F}$ / $48.3^\circ\mathrm{C}$).
* **Voiceover:** *"We replayed the record-breaking Phoenix 2023 heatwave across an urban substation with parallel distribution transformers, critical hospital loads, and battery storage."*

### ⏱️ 1:00–1:15 — Baseline Failure Mode
* **Visual:** Baseline toggle active. Static rating mode. The red hot-spot curve climbs continuously and breaches the $140^\circ\mathrm{C}$ emergency ceiling at 15:40.
* **Voiceover:** *"Under the baseline controller using airport weather and static ratings, the transformer remains heavily loaded into peak heat—and the projected hot-spot breaches its emergency safety ceiling."*
* **On-Screen Text:** `BASELINE: CRITICAL THERMAL ENVELOPE BREACH`

### ⏱️ 1:15–1:30 — FortyGuard Early Warning & Autonomous Planning
* **Visual:** FortyGuard layer activated. Dashboard displays `7h 10m persistence > 40°C`. LangGraph StateGraph nodes light up: `Thermal Forecast -> Physics Simulation -> Mitigation Planner`.
* **Voiceover:** *"Thermal Sentinel detects 7 continuous hours of extreme persistence. Twelve hours ahead of peak, our LangGraph agent synthesizes an autonomous mitigation package: activate forced cooling, dispatch the battery, and shift flexible EV load."*

### ⏱️ 1:30–1:45 — Deterministic Safety Gate
* **Visual:** Full-screen zoom into the Safety Gate panel. Checklist items animate green: `IEEE C57.91 Envelope [PASS]`, `Voltage 0.963–1.032 pu [PASS]`, `N-1 Contingency [PASS]`, `BESS Reserve 38% > 30% [PASS]`.
* **Voiceover:** *"Crucially, the LLM never controls equipment directly. Every action enters a deterministic Safety Gate that mathematically validates transformer limits, grid voltage, N-1 redundancy, and battery reserves."*

### ⏱️ 1:45–2:15 — Technical Defensibility & Avoided Aging
* **Visual:** Side-by-side comparison table showing Baseline vs. Thermal Sentinel Grid. Hot-spot capped at $136.8^\circ\mathrm{C}$ safe, avoiding $73.4\text{ hours}$ of insulation loss-of-life.
* **Voiceover:** *"Under the hood, we integrate IEEE C57.91 and IEC 60076-7 thermal differential equations with power-flow validation. The agent keeps the hot-spot safely below limits and preserves critical hospital supply."*

### ⏱️ 2:15–2:45 — Commercial ROI & Avoided Loss
* **Visual:** Net Avoided Loss ROI card highlighting: `Avoided Outage Risk: $182K`, `Avoided Aging: $486`, `Net Avoided Loss: $175,276`, `ROI: 24.3x`.
* **Voiceover:** *"For utilities, this prevents multi-million dollar transformer blowouts and SAIDI penalties. For property and fire insurers, it provides an auditable risk-reduction ledger."*

### ⏱️ 2:45–3:00 — Final Closing Hook
* **Visual:** Clean logo animation: **Thermal Sentinel Grid · Powered by FortyGuard Temperature AI**.
* **Voiceover:** *"We do not use AI to guess at grid safety. We use AI to orchestrate physics, constraints, and accountable physical action—before heat becomes an outage."*
