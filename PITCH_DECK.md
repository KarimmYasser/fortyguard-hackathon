# 🎙️ Thermal Sentinel Grid - Official Pitch Deck & Presentation Guide
> **Track 06 (Agentic AI) & Track 02 (Future Buildings & Energy) - FortyGuard Hackathon '26**  
> *Author:* Karim Yasser · *Live Demo:* **[https://fortyguard-hackathon.vercel.app](https://fortyguard-hackathon.vercel.app)** (Zero install, no login, full incognito compatibility)

---

## ⏱️ PART 1: 3-Minute Video Pitch Script (Official Video Submission)

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               3-MINUTE VIDEO SCRIPT TIMELINE (180s)                              │
│                                                                                                  │
│   0:00 - 0:30 (30s)  ──► The Hook: The 2-Meter Microclimate Blindspot ($2.8M Problem)            │
│   0:30 - 1:00 (30s)  ──► The Solution: FortyGuard 2m AI + IEEE Differential Physical Engine      │
│   1:00 - 1:30 (30s)  ──► The Agentic AI Stack: LangGraph + Non-LLM CBF-QP Safety Gate            │
│   1:30 - 2:15 (45s)  ──► Live Demo: What-If Studio, 72h Compounding & AC Power Flow Network      │
│   2:15 - 2:45 (30s)  ──► Auditable Financial Value: $2.79M Net Avoided Loss (5,952x ROI)         │
│   2:45 - 3:00 (15s)  ──► Call to Action & Conclusion                                             │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 🎬 Scene 1: The Hook & Market Blindspot (0:00 - 0:30)
* **Visual:** Split-screen showing Phoenix Sky Harbor Airport station ($43.1^\circ\mathrm{C}$) vs. Downtown Substation sitting 2 meters above black asphalt ($47.6^\circ\mathrm{C}$, $+4.5^\circ\mathrm{C}$ delta).
* **Voiceover:**
  > *"During extreme heatwaves, electrical utilities manage hundreds of millions of dollars in power infrastructure using airport weather stations 10 miles away. Multi-billion dollar SCADA giants like Siemens, GE, and Schneider only react when an alarm trips at 135°C - when failure is already locked in.*  
  > *In Phoenix July 2023, an invisible +4.5°C radiating asphalt microclimate accelerated transformer insulation aging by 15 times, triggering catastrophic substation blowouts and $2.8 million in blackout damages. Standard weather apps and legacy SCADA completely missed it."*

---

### 🎬 Scene 2: The Solution (0:30 - 1:00)
* **Visual:** Architecture diagram showing FortyGuard 2m Layer $\to$ IEEE C57.91 Thermal ODE Solver $\to$ 4 Scientific Moats.
* **Voiceover:**
  > *"Introducing Thermal Sentinel Grid: the world's first physics-constrained agentic resilience engine for urban energy infrastructure.*  
  > *We combine FortyGuard's 2-meter Temperature AI with exact IEEE C57.91 and IEC 60287 differential thermal equations. We model four latent physical cascades standard SCADA misses: underground soil moisture dryout, building canyon wind throttling, virtual paper-oil moisture desorption, and exact winding hot-spots."*

---

### 🎬 Scene 3: Why Agentic Physical AI (1:00 - 1:30)
* **Visual:** LangGraph StateGraph visualizer and the CBF-QP Safety Gate card showing $K_{\text{safe}} = 0.98\text{ pu}$.
* **Voiceover:**
  > *"Rather than training an unverified black-box neural net that hallucinates, we built a hybrid Physical-AI architecture:*  
  > *Exact physics ODEs handle the thermal math, FortyGuard provides the 12-hour environmental forecast, LangGraph coordinates autonomous multi-agent dispatch planning, and a deterministic Control Barrier Function (CBF-QP) acts as a mathematical firewall, guaranteeing that physical voltage and temperature limits are never violated."*

---

### 🎬 Scene 4: Live Dashboard Demo (1:30 - 2:15)
* **Visual:** Screen capture of `https://fortyguard-hackathon.vercel.app`. Show scrubber moving through 12-hour timeline, switch to **⚡ What-If Studio** dragging sliders, and show the **⚡ AC Power Flow** single-line diagram.
* **Voiceover:**
  > *"In our live Mission Control dashboard, the baseline controller breaches the 140°C hot-spot limit at 1:00 PM. Thermal Sentinel Grid engages 12 hours ahead, pre-cooling radiators at 8:00 AM off-peak and discharging 5 MW of BESS to cap the hot-spot safely at 136.8°C.*  
  > *In our What-If Studio, judges can modulate microclimate deltas, multi-day heatwaves, and battery sizes in real time with sub-15 millisecond ODE re-solving, while our AC power flow solver optimizes On-Load Tap Changers and BESS Volt/VAR support to maintain 100% hospital feeder uptime."*

---

### 🎬 Scene 5: Auditable ROI & Impact (2:15 - 2:45)
* **Visual:** Avoided Loss Financial Audit tab showing the LBNL ICE Calculator breakdown and $5,952.7\text{x}$ ROI badge.
* **Voiceover:**
  > *"Our economic engine uses the Department of Energy's LBNL ICE standard: we quantify avoided catastrophic outage risk, capital asset life extension, and exact mitigation power costs.*  
  > *For a single heatwave event, Thermal Sentinel Grid delivers $2.79 million in net avoided loss at a 5,952x ROI, saving 846 equivalent aging hours and protecting critical medical feeders."*

---

### 🎬 Scene 6: Outro (2:45 - 3:00)
* **Visual:** Summary slide with Track 06 & Track 02 badges, IEEE compliance badge, and GitHub repository link.
* **Voiceover:**
  > *"By coupling FortyGuard's Temperature AI with first-principles physics and deterministic safety guarantees, Thermal Sentinel Grid makes cities and power grids truly heat-resilient.*  
  > *Thank you, and we invite you to test our live platform!"*

---

## 🏛️ PART 2: 5-Minute Live Presentation Slide Deck & Judge Defense

### Slide 1: The Invisible 2-Meter Hazard
* **Key Takeaway:** Airport weather ($10\text{m}$) has a $+4.5^\circ\mathrm{C}$ blindspot relative to $2\text{m}$ urban asphalt.
* **Talking Points:** Phoenix July 2023 case study; $119^\circ\mathrm{F}$ peak; 31 consecutive days $\ge 110^\circ\mathrm{F}$; why SCADA fails without $2\text{m}$ boundary layer data.

### Slide 2: The Physical-AI Architecture
* **Key Takeaway:** 4-Layer Hybrid Stack (Perception $\to$ Physical Truth $\to$ Agentic Planner $\to$ Safety Barrier).
* **Talking Points:** Why we do NOT use black-box ML; IEEE C57.91 Annex G verification ($<0.0001^\circ\mathrm{C}$ error); LangGraph StateGraph decision flow.

### Slide 3: Eight Asymmetric Scientific & Heavy Computational Moats
* **Key Takeaway:** Unmeasured physical cascades and convex optimization:
  1. IEC 60287 Cable-Soil Dryout ($\rho_{\text{soil}} = 0.95 \to 2.48\text{ K}\cdot\text{m/W}$)
  2. Oke/Evola Canyon Aerodynamics ($-32\%$ cooling derate)
  3. Fickian Virtual Moisture Sensor ($RS_o = 42\%$ arcing warning)
  4. Robust CBF-QP Safety Gate ($0.95 \le V_{\text{pu}} \le 1.05$)
  5. IEEE Std 738-2012 Dynamic Line Rating ($q_c+q_r=q_s+I^2R$, $+22.5\%$ ampacity headroom, sag $S(T_c)$)
  6. Coupled 2-State BESS Thermal ODEs & Arrhenius SEI Capacity Fade ($55^\circ\mathrm{C}$ runaway ceiling)
  7. Arrhenius-Weibull Grid Fragility & Cascading Blackout Risk ($\lambda_i(t,T)$, joint $P_{\text{cascade}}$)
  8. Chance-Constrained SOCP OPF ($95\%/99\%$ Gaussian quantile confidence bounds)

### Slide 4: Multi-Day Compounding & AC Distribution Feeder Network
* **Key Takeaway:** 72-hour continuous heatwave simulation, 4-bus distribution feeder network with OLTC tap tuning, and Chance-Constrained SOCP dispatch.


### Slide 5: Investment-Grade Avoided Loss (LBNL ICE)
* **Key Takeaway:** $\$2,791,338$ Net Avoided Loss; $5,952\text{x}$ ROI; $\$12.50/\text{kWh}$ VoLL.

### Slide 6: Enterprise Zero-Data-Loss Dual-Storage Architecture (16 Tables)
* **Key Takeaway:** 16-table dual-storage persistence (Local SQLite + PostgREST Supabase PostgreSQL) with Row Level Security (RLS) & FortyGuard API query caching.
* **Talking Points:** MD5-hashed query cache saves paid API credits; full auditable legal trails for B2B SCADA work orders, CBF safety proofs, and LBNL ICE filings.

---

## 🛡️ Judge Q&A Defense Cheat-Sheet

| Likely Judge Question | Winning Technical Defense |
| :--- | :--- |
| **"Why didn't you train an ML model to predict temperature?"** | *"FortyGuard already provides state-of-the-art 2m Temperature AI and 12h forecasts. Furthermore, transformer heat rise and Arrhenius aging are governed by exact physical ODEs (IEEE Std C57.91). Training an approximate neural net introduces hallucinations and prevents certification by utilities."* |
| **"How is this different from existing utility SCADA alarms?"** | *"SCADA alarms are reactive - they trip 5 minutes before failure when equipment is already overheated. Thermal Sentinel Grid ingests FortyGuard's 12-hour forecast to proactively pre-cool radiators at 8:00 AM off-peak and schedule BESS peak shaving hours in advance."* |
| **"Why is AI justified here versus simple threshold scripts?"** | *"Deterministic scripts cannot orchestrate multi-asset, cross-feeder trade-offs (e.g. balancing BESS State of Charge, transformer top-oil time constants, and hospital feeder voltage constraints). LangGraph acts as the cognitive planner that evaluates complex multi-step mitigation paths, while CBF-QP acts as the mathematical safety barrier."* |
| **"Would utilities trust an autonomous AI agent with circuit breakers?"** | *"No utility trusts an unconstrained LLM. That is why we designed a non-LLM Control Barrier Function (CBF-QP) as a mathematical firewall. Even if the AI planner proposes an aggressive dispatch, the CBF-QP filter strictly projects actions onto $K_{\text{safe}}$, guaranteeing zero voltage or thermal violations."* |
| **"Are the avoided loss numbers realistic?"** | *"Yes, all financial figures are calculated directly using the Department of Energy's LBNL Interruption Cost Estimate (ICE) standard ($VoLL = \$12.50/\text{kWh}$) and IEEE C57.91 capital replacement formulas over an 180,000-hour asset life."* |
| **"How do you handle data persistence and API cost scaling?"** | *"We built an enterprise 16-table dual-storage persistence layer (SQLite + Supabase PostgreSQL). Every FortyGuard API call is MD5-hashed and cached to prevent duplicate credit billing, while all SCADA orders, CBF certificates, and 72h telemetry are permanently indexed under Row Level Security for regulatory compliance."* |

