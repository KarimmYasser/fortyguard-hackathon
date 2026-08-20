# 🛡️ PyreShield AI — FortyGuard Hackathon'26
> **Autonomous 2-Meter Thermal Hazard & Electrical Asset Fire Prevention Agent**  
> *Building the World's Temperature AI · Global AI Hackathon (August 18–30, 2026)*

[![Track: Agentic AI](https://img.shields.io/badge/Track%2006-Agentic%20AI-0e9ec4?style=for-the-badge)](https://www.fortyguard.com/hackathon26)
[![Track: Future Buildings](https://img.shields.io/badge/Track%2002-Future%20Buildings%20%26%20Energy-e8762d?style=for-the-badge)](https://www.fortyguard.com/hackathon26)
[![Track: Resilient Cities](https://img.shields.io/badge/Track%2001-Resilient%20Cities-1769b0?style=for-the-badge)](https://www.fortyguard.com/hackathon26)

---

## 📌 Executive Summary

During extreme urban heatwaves, standard weather forecasts report broad, city-wide temperatures (e.g., 38°C–40°C) measured high above open fields or at airports. However, critical building and urban electrical infrastructure—**outdoor AC compressor units, balcony battery storage, rooftop solar inverters, and street-level utility transformer boxes**—operates directly within the **2-meter boundary layer** above radiating asphalt and concrete, where ambient temperatures regularly reach **48°C–52°C**.

This localized microclimate heat trap creates massive **cumulative thermal soak**, pushing capacitors, lithium-ion battery cells, and refrigerant loops into violent thermal runaway. In dense urban centers (such as recent record-breaking heatwaves in Egypt and the Middle East), this exact blind spot has triggered a deadly wave of **appliance explosions, electrical panel blowouts, and structural building fires**.

**PyreShield AI** solves this critical safety failure by combining **FortyGuard’s 2-meter street-level Temperature API** with an autonomous **LangGraph-driven multi-agent harness**.

---

## 🎯 Dual Market Architecture (B2B + B2C)

```
                              ┌────────────────────────────────────────────────────────┐
                              │              FortyGuard Temperature API                │
                              │  (2m Ambient, 20m Spatial, Persistence, Exceedance)    │
                              └──────────────────────────┬─────────────────────────────┘
                                                         │
                                                         ▼
                              ┌────────────────────────────────────────────────────────┐
                              │             PyreShield Agent Pipeline                  │
                              │    (LangGraph StateGraph + Physical Constraint Gate)   │
                              └────────────┬───────────────────────────────┬───────────┘
                                           │                               │
                                           ▼                               ▼
                 ┌───────────────────────────────────┐   ┌───────────────────────────────────┐
                 │        B2B Enterprise Engine      │   │        B2C Resident Early-Warning │
                 ├───────────────────────────────────┤   ├───────────────────────────────────┤
                 │ • Commercial Facility Managers    │   │ • Tenant / Homeowner Alerts       │
                 │ • Property & Fire Insurers        │   │ • Facade & Balcony Heat Traps     │
                 │ • Automated Electrical Load Shed  │   │ • Safe Appliance Duty-Cycling     │
                 │ • HVAC Compressor Pre-Cooling     │   │ • Battery Overheating Warnings    │
                 │ • Transformer Blowout Prevention  │   │ • Real-time Risk Level & Advice   │
                 └───────────────────────────────────┘   └───────────────────────────────────┘
```

---

## 🔑 Why FortyGuard's 2-Meter Layer is the Missing Link

| Dimension | Standard Weather Forecasts / Satellite LST | FortyGuard Temperature AI |
| :--- | :--- | :--- |
| **Measurement Height** | 10m–30m altitude / Airport grass / Orbital surface skin | **Exact 2-meter human & infrastructure boundary layer** |
| **Microclimate Sensitivity** | Misses street canyons, unshaded asphalt, and building reflections | **Captures true convective ambient heat surrounding assets** |
| **Duration Analysis** | Snapshot only (single max temp) | **Thermal Persistence Layer** (hours of continuous heat soak) |
| **Predictive Horizon** | Macroscopic 7-day model | **12-Hour Hyperlocal Street Forecast** for proactive intervention |
| **Impact on Explosions** | *"39°C today — status normal"* ❌ (Explosions still occur) | *"49°C ambient at transformer pad with 5h soak"* ⚠️ (Triggers mitigation) |

---

## 🏗️ System Architecture & Workflow

1. **Async Polling Client:** Interfaces with FortyGuard's REST endpoints (`/v1/heat-intelligence`, persistence, exceedance, and forecasts) using a robust submit-and-poll async worker.
2. **Physical-Envelope Asset Registry:** Maps assets (transformers, HVAC condensers, inverters, batteries) with their rated thermal tolerances (e.g., UL 40°C/45°C limits).
3. **LangGraph Agent Harness:**
   - **Spatial Thermal Scanner Node:** Ingests 2m street microclimate tiles across the target urban grid.
   - **Thermal Soak & Exceedance Evaluator Node:** Calculates cumulative degree-hours above rated equipment limits.
   - **3-Level Risk Preflight Gate:** Evaluates whether risk is *Normal*, *Elevated*, *Critical*, or *Thermal Runaway Imminent*.
   - **Mitigation & Load-Shedding Planner Node:** Formulates automated HVAC duty-cycling and electrical load-shedding schedules.
   - **Dispatcher Node:** Pushes structured alerts to B2B facility dashboards and B2C mobile notifications.

---

## 📁 Repository Structure

```
fortyguard-hackathon/
├── README.md                           # Main Project Overview & Architecture
├── AGENT_CONTEXT.md                    # Master Knowledge Reservoir (All Ideas, Background, Research)
├── docs/                               # Comprehensive Documentation & Reference Hub
│   ├── README.md                       # Master Documentation Index
│   ├── research/                       # Physical AI Specs, Equations, Standards & Pitch Script
│   ├── sessions-dialogue/              # Full Webinar & Mentorship Transcripts (Fawad, Jordana, Aashan, Onboarding)
│   ├── api-documentation/              # OpenAPI Schemas & FortyGuard Endpoint Guides
│   ├── handbook/                       # Participant Handbook & Official Scoring Rubrics
│   ├── official/                       # Rules, FAQs, Tracks, and Mentor Keynotes
│   ├── project-registration/           # PyreShield Registration Pitch & Strategy History
│   └── context/                        # Chat Transcripts & Brainstorming Action Logs

├── temperature-api-quickstart/         # Official FortyGuard Quickstart SDK & Notebooks
│   ├── fortyguard/                     # Quickstart client module
│   ├── notebooks/                      # Exploration notebooks
│   └── docs/                           # API documentation
├── src/                                # PyreShield Core Application
│   ├── api/                            # FortyGuard Async Client & Tool Adapters
│   ├── models/                         # Asset, Risk, and Thermal Pydantic Schemas
│   ├── agent/                          # LangGraph StateGraph, Tools, and Preflight Gates
│   └── server/                         # FastAPI Application & Webhook Handlers
└── tests/                              # Automated Pytest Suite
```


---

## 👨‍💻 Author & Research Background

**Karim Yasser** — *Computer Engineering, Cairo University Faculty of Engineering*  
* AI Research Intern at Nile University SESC Research Center (Architected autonomous multi-agent OpenFOAM CFD/thermal pipeline; co-authoring upcoming research paper).
* Software Engineering Intern at Siemens Digital Industries Software (High-performance CAT RTS engine, 54.5x speedup, large-scale data ingestion).
* Portfolio: [karim-yasser.vercel.app](https://karim-yasser.vercel.app) · GitHub: [@KarimmYasser](https://github.com/KarimmYasser)
