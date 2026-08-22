# 🎙️ Thermal Sentinel Grid - Official Pitch Deck & Presentation Guide
> **Track 06 (Agentic AI) & Track 02 (Future Buildings & Energy) - FortyGuard Hackathon '26**  
> *Author:* Karim Yasser · *Live Demo:* **[https://www.thermal-sentinel-grid.live](https://www.thermal-sentinel-grid.live)** (Zero install, no login, full incognito compatibility)

---

## ⏱️ PART 1: 3-Minute Video Pitch Script (Official Video Submission)

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               3-MINUTE VIDEO SCRIPT TIMELINE (180s)                              │
│                                                                                                  │
│   0:00 - 0:30 (30s)  ──► The Hook: The 2-Meter Microclimate Blindspot ($2.8M Problem)            │
│   0:30 - 1:00 (30s)  ──► The Solution: FortyGuard 2m AI + IEEE Differential Physical Engine      │
│   1:00 - 1:30 (30s)  ──► Agentic Stack: LangGraph + Deterministic Safety-Envelope Gate          │
│   1:30 - 2:15 (45s)  ──► Live Demo: What-If Studio, 72h Compounding & AC Power Flow Network      │
│   2:15 - 2:45 (30s)  ──► Auditable Financial Value: $2.58M Net Avoided Loss (5,495x ROI)         │
│   2:45 - 3:00 (15s)  ──► Call to Action & Conclusion                                             │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 🎬 Scene 1: The Hook & Market Blindspot (0:00 - 0:30)
* **Visual:** Split-screen showing South Mountain natural desert terrain ($41.6^\circ\mathrm{C}$) vs. Downtown Substation sitting 2 meters above black asphalt ($42.7^\circ\mathrm{C}$, $+1.1^\circ\mathrm{C}$ measured delta).
* **Voiceover:**
  > *"During extreme heatwaves, electrical utilities manage hundreds of millions of dollars in power infrastructure using airport weather stations 10 miles away. Multi-billion dollar SCADA giants like Siemens, GE, and Schneider only react when an alarm trips at 135°C - when failure is already locked in.*  
  > *In Phoenix July 2023, downtown asphalt held 2m air temperature above 40°C for 12 unbroken hours — a +1.1°C land-cover delta over natural desert, sustained. It is the persistence, not the peak, that accelerates transformer insulation aging. Standard weather apps and legacy SCADA report neither."*

---

### 🎬 Scene 2: The Solution (0:30 - 1:00)
* **Visual:** Architecture diagram showing FortyGuard 2m Layer $\to$ IEEE C57.91 Thermal ODE Solver $\to$ 4 Scientific Moats.
* **Voiceover:**
  > *"Introducing Thermal Sentinel Grid: a physics-constrained agentic resilience engine for urban energy infrastructure.*
  > *We combine FortyGuard's 2-meter Temperature AI with exact IEEE C57.91 and IEC 60287 differential thermal equations. We model four latent physical cascades standard SCADA misses: underground soil moisture dryout, building canyon wind throttling, virtual paper-oil moisture desorption, and exact winding hot-spots."*

---

### 🎬 Scene 3: Why Agentic Physical AI (1:00 - 1:30)
* **Visual:** LangGraph StateGraph visualizer and the deterministic Safety Gate card showing $K_{\text{safe}} = 0.98\text{ pu}$.
* **Voiceover:**
  > *"Rather than training an unverified black-box neural net that hallucinates, we built a hybrid Physical-AI architecture:*  
  > *Standards-based physics ODEs handle the thermal math, FortyGuard provides the 12-hour environmental forecast, LangGraph coordinates multi-agent dispatch planning, and a deterministic Control Barrier Function safety gate rejects or modifies actions that violate the modelled voltage and temperature envelope."*

---

### 🎬 Scene 4: Live Dashboard Demo (1:30 - 2:15)
* **Visual:** Screen capture of `https://www.thermal-sentinel-grid.live`. Show scrubber moving through 12-hour timeline, switch to **⚡ What-If Studio** dragging sliders, and show the **⚡ AC Power Flow** single-line diagram.
* **Voiceover:**
  > *"In our live Mission Control dashboard, the baseline controller breaches the 140°C hot-spot limit at 1:00 PM. Thermal Sentinel Grid engages 12 hours ahead, pre-cooling radiators at 8:00 AM off-peak and discharging 5 MW of BESS to cap the hot-spot at 109.43°C while the baseline reaches 159.53°C.*
  > *In our What-If Studio, judges can modulate microclimate deltas, multi-day heatwaves, and battery sizes in real time with sub-15 millisecond ODE re-solving, while our AC power flow solver evaluates On-Load Tap Changers and BESS Volt/VAR support for the modelled hospital feeder."*

---

### 🎬 Scene 5: Auditable ROI & Impact (2:15 - 2:45)
* **Visual:** Avoided Loss Financial Audit tab showing the LBNL ICE Calculator breakdown and $5,495.3\text{x}$ ROI badge.
* **Voiceover:**
  > *"Our economic engine uses an LBNL ICE-informed value-of-lost-load assumption: we model avoided outage risk, capital asset life extension, and mitigation energy costs.*
  > *For a single heatwave event, Thermal Sentinel Grid delivers $2.58 million in net avoided loss at a 5,495x ROI, avoiding 374.3 equivalent aging hours and protecting critical medical feeders."*

---

### 🎬 Scene 6: Outro (2:45 - 3:00)
* **Visual:** Summary slide with Track 06 & Track 02 badges, IEEE compliance badge, and GitHub repository link.
* **Voiceover:**
  > *"By coupling FortyGuard's Temperature AI with standards-based physics and deterministic model checks, Thermal Sentinel Grid helps operators plan for urban heat risk.*
  > *Thank you, and we invite you to test our live platform!"*

---

## 🏛️ PART 2: 5-Minute Live Presentation Slide Deck & Judge Defense

### Slide 1: The Invisible 2-Meter Hazard
* **Key Takeaway:** Station weather is blind to *duration*. The measured land-cover delta is $+1.1^\circ\mathrm{C}$, but it is held for $12$ unbroken hours above $40^\circ\mathrm{C}$ — and thermal damage integrates over time.
* **Talking Points:** Phoenix July 2023 case study; $119^\circ\mathrm{F}$ peak; 31 consecutive days $\ge 110^\circ\mathrm{F}$; why SCADA fails without $2\text{m}$ boundary layer data.

### Slide 2: The Physical-AI Architecture
* **Key Takeaway:** 4-Layer Hybrid Stack (Perception $\to$ Physical Truth $\to$ Agentic Planner $\to$ Safety Barrier).
* **Talking Points:** Why we do NOT use black-box ML; IEEE C57.91 Annex G verification ($<0.0001^\circ\mathrm{C}$ error); LangGraph StateGraph decision flow.

### Slide 3: Eight Asymmetric Scientific & Heavy Computational Moats
* **Key Takeaway:** Unmeasured physical cascades and convex optimization:
  1. IEC 60287 Cable-Soil Dryout (72h end-of-day $\rho_{\text{soil}} = 1.52 \to 2.13 \to 2.41\text{ K}\cdot\text{m/W}$)
  2. Oke/Evola Canyon Aerodynamics ($-32\%$ cooling derate)
  3. Fickian Virtual Moisture Sensor ($RS_o = 42\%$ arcing warning)
  4. Deterministic Safety-Envelope Gate ($0.95 \le V_{\text{pu}} \le 1.05$)
  5. IEEE Std 738-2012 Dynamic Line Rating ($q_c+q_r=q_s+I^2R$, $+22.5\%$ ampacity headroom, sag $S(T_c)$)
  6. Coupled 2-State BESS Thermal ODEs & Arrhenius SEI Capacity Fade ($55^\circ\mathrm{C}$ runaway ceiling)
  7. Arrhenius-Weibull Grid Fragility & Cascading Blackout Risk ($\lambda_i(t,T)$, joint $P_{\text{cascade}}$)
  8. Analytical Uncertainty-Bounded Dispatch (Gaussian quantile bounds)

### Slide 4: Multi-Day Compounding & AC Distribution Feeder Network
* **Key Takeaway:** A frozen live FortyGuard 24×3 capture drives the 72-hour continuous model (daily 2m peaks 42.44/42.76/42.52°C), alongside a 4-bus distribution feeder with OLTC and analytical uncertainty-bounded dispatch.


### Slide 5: Portfolio Operations & Worker Intervention Screening
* **Key Takeaway:** The same deterministic service ranks registered assets, screens candidate field-work windows, and emits content-addressed mitigation evidence for both the dashboard and MCP clients.
* **Talking Points:** The score is transparent triage rather than failure probability; missing registry fields are excluded instead of invented. The worker window uses measured wet-bulb and 2m air temperature but is explicitly not an OSHA/WBGT certification. The current demo applies one common Phoenix scenario to the portfolio rather than claiming a separate scan for every asset.

### Slide 6: Investment-Grade Avoided Loss (LBNL ICE)
* **Key Takeaway:** $\$2,576,849$ Net Avoided Loss; $5,495\text{x}$ ROI; $\$12.50/\text{kWh}$ VoLL.

### Slide 7: Durable Hybrid Persistence Architecture (16 Tables)
* **Key Takeaway:** 16-table dual-storage persistence (Local SQLite + PostgREST Supabase PostgreSQL) with Supabase as the durable source of truth, SQLite as an offline fallback, and request-addressed API/solve caching.
* **Talking Points:** MD5-addressed FortyGuard responses save paid credits; SHA-256-addressed, non-expiring full solve payloads let saved parcels replay across serverless cold starts; work orders, safety certificates, and financial snapshots remain separately auditable.

### Slide 8: Data Science, Analytics & ML Intelligence (IBM-Style Lifecycle)
* **Key Takeaway:** End-to-end data lifecycle: Bronze→Silver→Gold ETL Medallion pipeline (18 engineered features), fast Ridge Physics-Surrogate ($R^2 > 0.98, 5000\times$ speedup), Isolation Forest sensor anomaly detector, and Weibull Remaining Useful Life (RUL) survival analysis.
* **Talking Points:** Standalone Jupyter Notebook (`notebooks/Thermal_Sentinel_DataScience.ipynb`) + interactive in-app Data Science Studio tab; paired $t$-test is statistically significant ($p=1.74\times10^{-5}$) but the effect is negligible (Cohen's $d=0.024$), so the product correctly leads on duration rather than spatial spread.

---

## 🛡️ Judge Q&A Defense Cheat-Sheet

| Likely Judge Question | Winning Technical Defense |
| :--- | :--- |
| **"Why didn't you train an ML model to predict temperature?"** | *"FortyGuard already provides state-of-the-art 2m Temperature AI and 12h forecasts. Furthermore, transformer heat rise and Arrhenius aging are governed by exact physical ODEs (IEEE Std C57.91). Rather than replacing exact physics, we built a Physics-Surrogate ML Regressor ($R^2 > 0.98$) that accelerates the ODE solver by $5000\times$ for city-scale screening of 10,000+ assets."* |
| **"What data science and engineering principles did you apply?"** | *"We implemented the complete IBM Data Science Lifecycle: a Bronze→Silver→Gold medallion architecture extracting 18 engineered features, rigorous hypothesis testing (paired $t$-test on the measured urban-vs-natural land-cover delta, $+1.1^\circ\mathrm{C}$), Isolation Forest unsupervised anomaly detection for sensor drift, and Weibull survival analysis for asset RUL forecasting."* |
| **"How is this different from existing utility SCADA alarms?"** | *"SCADA alarms are reactive - they trip 5 minutes before failure when equipment is already overheated. Thermal Sentinel Grid ingests FortyGuard's 12-hour forecast to proactively pre-cool radiators at 8:00 AM off-peak and schedule BESS peak shaving hours in advance."* |
| **"Why is AI justified here versus simple threshold scripts?"** | *"Deterministic scripts cannot orchestrate multi-asset, cross-feeder trade-offs (e.g. balancing BESS State of Charge, transformer top-oil time constants, and hospital feeder voltage constraints). LangGraph acts as the cognitive planner that evaluates complex multi-step mitigation paths, while the deterministic safety filter checks proposals against the configured model envelope."* |
| **"Would utilities trust an autonomous AI agent with circuit breakers?"** | *"No utility should trust an unconstrained LLM. The prototype therefore places a deterministic, non-LLM Control Barrier Function safety gate after planning. Under the documented model and uncertainty bounds, it rejects or modifies proposals outside $K_{\text{safe}}$; production actuation would still require utility integration, validation, and operating approval."* |
| **"Are the avoided loss numbers realistic?"** | *"They are model outputs, not booked savings. The benchmark uses a $12.50/\text{kWh}$ VoLL assumption informed by the LBNL ICE framework, plus documented outage-risk, replacement-life, and mitigation-cost assumptions. Judges can inspect and vary the inputs."* |
| **"How do you handle data persistence and API cost scaling?"** | *"We built an enterprise 16-table dual-storage persistence layer (SQLite + Supabase PostgreSQL). FortyGuard calls are durably cached by request identity, stored parcel rows are selectable in Cloud DB, and identical physics requests replay a complete non-expiring solve from Supabase across serverless cold starts. Audit summaries, work orders, and CBF certificates remain separately indexed."* |
| **"How does this scale from one transformer to a utility portfolio?"** | *"Portfolio Ops applies a transparent deterministic ranking to registered assets, exposes evidence coverage when fields are missing, and identifies candidate crew windows. The browser and MCP clients use the same code path and SHA-256 evidence identity. The demo currently applies one common Phoenix stress boundary; production deployment would attach a cached location-specific FortyGuard profile to each asset."* |
| **"Is the worker window OSHA- or WBGT-certified?"** | *"No. It is an explicit wet-bulb and 2m air-temperature screening policy. We do not fabricate globe temperature or omit workload, clothing, acclimatization, and jurisdiction-specific requirements. A qualified safety program must evaluate those before dispatching crews."* |

