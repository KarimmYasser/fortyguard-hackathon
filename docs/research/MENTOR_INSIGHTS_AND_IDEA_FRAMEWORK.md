# 🧠 Mentor Insights, Idea Selection Framework & Webinar Synthesis
> **FortyGuard Hackathon '26 - *Building the World's Temperature AI***  
> Comprehensive distillation of keynotes, technical workshops, and judging advice from FortyGuard engineers, founders, and industry leaders (*Google Cloud, Autodesk, Inspeerity*).

---

## 🧭 The Winning Hackathon Formula

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   THE WINNING HACKATHON FORMULA                                          │
│                                                                                                          │
│   [Painfully Felt Problem]  +  [FortyGuard 2m/Parcel API]  +  [Multi-Source Data Fusion]                │
│             │                               │                               │                            │
│             ▼                               ▼                               ▼                            │
│   "Deep domain knowledge"      "Persistence/Exceedance"        "OpenStreetMaps / eGrid / Insurance"     │
│                                             │                                                            │
│                                             ▼                                                            │
│                    [Actionable Decision / Mitigation Recommendation Engine]                              │
│                                             │                                                            │
│                                             ▼                                                            │
│                    [Clear Commercial Stakeholder & Measurable ROI / Safety]                              │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. 🎯 Idea Selection & Problem Framing Philosophy

### A. The "Deep Problem Understanding" Advantage
*(Jordana Rosa - Senior Technical Specialist at Autodesk & 4x Hackathon Winner)*

1. **Pick Problems You Deeply Understand:**
   * In the era of AI coding assistants and rapid prototyping, anyone can build a generic dashboard in a few hours. The winning edge comes from finding the non-obvious solution that competitors miss because of your specific domain or engineering background.
2. **The "Elevator & Mirrors" Mental Model:**
   * When building tenants complain about slow elevators, the obvious logical answer is *"make the elevator faster"* (expensive, slow, brute-force).
   * The psychological / structural answer is *"install mirrors in the lobby"* (occupying passengers' attention eliminates complaints at near-zero cost).
   * In your hackathon project, look for the unique physical, operational, or algorithmic lever rather than just plotting temperature numbers on a generic map.
3. **Make Decisions Earlier (AEC & Infrastructure ROI):**
   * Early-stage site planning decisions have the highest leverage and are 10x to 100x cheaper than late-stage retrofits or post-disaster insurance payouts. A winning product shifts thermal analysis to the *beginning* of the decision cycle.

---

### B. Escaping the "Builder's Trap" & Prioritizing Commercial Value
*(Ashan Javed - Lead Solutions Architect / FortyGuard AI Team & Ahmed Abdelkhalek - Head of Digital Natives & Startups, Google Cloud)*

1. **Engineering Perfection vs. Commercial Clarity:**
   * *"If you do great engineering, but your product doesn't answer a clear commercial question or show measurable value, it will score poorly with judges."*
2. **Identify the Exact Paying Customer:**
   * Never pitch a generic *"everyone in the city"* tool. Specify the exact buyer: Commercial Facility Managers, Data Center Operators, Property Underwriters, Electric Utilities, General Contractors, or Municipal Heat Officers.
3. **Outcome over Tech Stack *(Karol Wiszowaty - COO, Inspeerity)*:**
   * Sell the **catastrophe prevented, downtime eliminated, or operational dollar savings**, not just the list of LLM models or API endpoints.

---

### C. The Data Science & Spatial Rigor Playbook: "Fact vs. Finding"
*(Mudethir - Lead ML Engineer & Aamir - Cloud/Data Architect, FortyGuard - Session 7)*

1. **The "Fact vs. Finding" Doctrine:**
   * Reporting *"Substation A hit 43°C on July 19"* is merely a static **fact**—it offers zero basis for an operational decision.
   * A true **finding** provides context, comparison, and consequence: *"Substation A spent 3.2x more continuous hours above 40°C than ambient baseline due to 0% canopy and 72% asphalt cover, driving a 58% increase in transformer loss of life."*
2. **Preventing Spurious Correlations (Where, When, What):**
   * **Where (Geometry):** Explicitly match vector asset points/polygons to the 20m/60m raster grid cells without coordinate skew.
   * **When (Cadence):** When fusing multi-rate datasets (e.g. 15-minute SCADA vs. hourly FortyGuard forecasts), match to the slower cadence or compute continuous moving integrations. Always align time zones (UTC vs local).
   * **What (Physical Variable):** Distinguish 2-meter convective air temperature (what assets/humans experience) from satellite Land Surface Temperature (LST skin temperature) and coarse ERA5 reanalysis (25 km cells).

---

### D. Product-Market Fit & The BreezoMeter / Google Solar Precedent
*(Thamir - Partner @ Cultivators; early operator at BreezoMeter $\to$ Google acquisition; Google Solar API validation lead - Session 8)*

1. **The COCO Customer Discovery Framework:**
   * **Context:** Deeply characterize the operational environment (e.g. extreme multi-day heatwaves in Sunbelt/MENA).
   * **Outcomes:** Quantify how the buyer measures success ($0 unforced outages, extended equipment life, lower insurance premiums).
   * **Constraints:** Understand inertia, legacy workarounds (e.g., reactive maintenance, coarse weather apps), and switching costs.
   * **Options:** Validate willingness to pay via interactive mockups before building excessive features.
2. **Early Adopters vs. Ideal Customer Profile (ICP):**
   * Do not start by pitching conservative utilities with multi-year RFP cycles.
   * Target agile **early adopters** who feel acute financial pain today (private solar operators, high-density data centers, cold storage managers). Use early wins as the bridge to enterprise utility ICPs.
3. **The "Space Pen vs. Pencil" Test:**
   * Avoid engineering 50 complex features nobody asked for. Focus relentlessly on the core catastrophic failure mechanism and its automated mitigation.

---

### E. Temperature Dashboard Masterclass: Microclimate Intelligence & Physical Indicators
*(Snehil Ahuja - Product Lead at FortyGuard & Aamir - Cloud/Data Architect, FortyGuard - Session 9)*

1. **Granularity Isolation ($60\text{m}$ vs. $100\text{m}$):**
   * Use $100\text{m}$ for macro city-wide overviews, but switch to $60\text{m}$ for hyperlocal asset-level analysis (substations, industrial transformers, data center chiller yards, individual park segments).
2. **Exceedance ($H_{\text{threshold}}$) vs. Persistence ($P_{\text{threshold}}$):**
   * **Exceedance Layer:** Cumulative total hours spent above a safety threshold (e.g., $>35^\circ\text{C}$ / $>66^\circ\text{F}$).
   * **Persistence Layer:** The longest uninterrupted, continuous stretch of hours without cooling relief. Continuous thermal soak is what destroys equipment insulation and triggers physiological heat stress.
3. **Diurnal Heat Peak & Forward AI Forecasts:**
   * Microclimate heat systematically peaks between **1:00 PM and 5:00 PM (13:00 – 17:00)**. 12-hour predictive dispatch engines must initiate pre-cooling and battery peak-shaving hours ahead of this peak.
4. **Physical & Environmental Parameters ($T_{\text{wb}}$, Solar Irradiance, AQI):**
   * **Wet-Bulb Temperature ($T_{\text{wb}}$):** The thermodynamic ceiling for human/evaporative cooling; essential for outdoor worker safety shifts and HVAC/data center cooling intake optimization.
   * **Solar Irradiance ($W/m^2$):** Direct driver of asphalt/concrete thermal retention and Dynamic Line Rating (DLR) conductor sag equilibrium.
   * **Multi-Gas Air Quality Suite:** Ozone ($O_3$), Sulfur Dioxide ($SO_2$), Nitrogen Dioxide ($NO_2$), and $PM_{2.5}$ for comprehensive environmental risk indexing.
5. **Dual-Perspective Computer Vision Segmentation:**
   * **Satellite (Macro Land Cover):** Explains ground heat absorption (e.g., 82% asphalt/concrete absorbing heat vs. 7% canopy).
   * **Street View (Human/Asset 2m Level):** Panoramic 2m perspective (with sky masked out) measuring exact local shade and canopy relief.
6. **Seasonal & Baseline Analysis:**
   * Comparing peak summer heatwaves against baseline months (e.g., January vs. July) isolates permanent structural Urban Heat Islands (UHIs) from transient synoptic weather anomalies.

---

### F. Physical AI, Cognitive Cities & Autonomous Infrastructure Safety
*(Prof. Jonathan Reichental - Founder of Human Future, former CIO of City of Palo Alto, Advisor @ FortyGuard, Mentor + Judge - Session 10)*

1. **The 5th Industrial (Cognitive) Revolution:**
   * Transitioning from Smart Cities (sensors + human intervention) to **Cognitive Cities** (Perceive $\to$ Reason $\to$ Learn $\to$ Act). Systems automate the *mind* and compound knowledge monotonically over time.
2. **The 4 Pillars of Physical AI:**
   * **Generative & Reasoning AI:** Cognitive graph orchestration, agentic planning, multi-step tool use.
   * **Sensors & Perception Hardware:** High-resolution spatial/temporal telemetry (FortyGuard 2m rasters, thermal cameras, grid SCADA).
   * **Robotics & Physical Actuation:** Autonomous dispatch, DER switches, drone inspections, robotic cooling systems.
   * **Data Infrastructure & Quality:** Clean, synchronized, accessible spatial truth. *"Data is the #1 asset of modern organizations outside human talent."*
3. **Inseparability of Temperature & Physical AI:**
   * Microclimate temperature is an indispensable operating layer for physical infrastructure. Extreme heat directly dictates electric grid stability, battery degradation rates, cooling overhead, and labor safety.
4. **Autonomous AI vs. Deterministic Safety Guardrails:**
   * Where human safety, life, or critical electrical infrastructure is at risk, **AI autonomy must be bounded by deterministic physics-based guardrails** (e.g., IEEE C57.91 thermal limits, IEC 60287 ampacity constraints) and maintain human-in-the-loop oversight.
5. **Why Smart City Initiatives Fail:**
   * Underestimating execution effort/time, poor-quality/fragmented data, and the absence of a bold, context-aligned vision.
6. **The Winning Hackathon Mindset:**
   * Build solutions that **anticipate the future, articulate why it matters, solve high-consequence pain points, and deliver certifiable, real-world utility**.

---

### G. Bridging Engineering to Business Value & Multi-Stakeholder Influence
*(Karel Wiszowaty - Partner @ developX, ex-COO & Delivery Director @ Inspirity - Session 11)*

1. **The Whiteboard Trap:**
   * The whiteboard is the safest place in the world for an idea because it faces zero user resistance or economic friction. Ideas die when leaving the whiteboard not from being technically wrong, but from failing to make stakeholders care.
2. **Builders Are in Sales:**
   * Engineering leadership is influencing without authority, translating technical choices into business value, and aligning architecture with strategic goals.
3. **The Multi-Stakeholder Currency Matrix:**
   * Never pitch a single technical message to an entire room. Match the message to each stakeholder's native currency:
     - **Executives:** ROI, capital preservation, risk mitigation, and top-line growth.
     - **Product Owners:** Sprint velocity, rapid iteration, and low coordination overhead.
     - **Developers:** Tooling autonomy, modular independence, and developer experience.
     - **Judges (40% Impact Score):** Measurable real-world consequence averted (e.g. cutting emergency heat response from days to hours).
     - **Investors:** TAM expansion potential and scalable unit economics.
4. **Selling the "Quarter-Inch Hole" (Theodore Levitt):**
   * Buyers don't buy database queries or raster grids; they buy the equipment saved from thermal explosion, the blackout prevented, or the regulatory fine avoided.
5. **Evolutionary Architecture vs. Day-1 Over-Engineering:**
   * Stage 1 (MVP / Hackathon $\to$ Validate speed/value) $\longrightarrow$ Stage 2 (PMF $\to$ Modular reliability) $\longrightarrow$ Stage 3 (Scale $\to$ Microservices & cost optimization) $\longrightarrow$ Stage 4 (Enterprise $\to$ SOC2/ISO compliance & governance).
6. **Pain is the Ultimate Salesman (Amazon / Netflix / Twitter Lessons):**
   * Frame technical investments around risk mitigation before catastrophic failure forces reactive, expensive refactors.

---

### H. Inside the VC Decision: Commercial Moats, Painkillers & Compounding Defensibility
*(Vikram - Principal @ Kota Capital, ex-Rocketship.vc, Jump Capital, BCG, Hackathon Judge - Session 12)*

1. **The Core VC & Judge Evaluation Filter:**
   * When founders leave the room, investors evaluate: *Burning Problem $\to$ Market Size & Expansion $\to$ Defensible Product Moat $\to$ Founder-Market Fit $\to$ Stickiness & Real Traction*.
2. **The "Painkiller vs. Vitamin" Test:**
   * Vitamins offer optional convenience; painkillers eliminate acute, intolerable bleeding. In climate tech, position microclimate intelligence as a catastrophic failure prevention engine rather than a passive weather map.
3. **Market Expansion & Customer Concentration:**
   * Seek ideas that expand the total addressable market (similar to how AI coding agents democratized software creation). Avoid reliance on 3–5 dominant enterprise buyers where customer bargaining power destroys pricing leverage.
4. **Defensibility: Why Execution is Never a Moat:**
   * GTM speed, marketing, and pricing advantages are easily copied. True defensibility comes from:
     - **Proprietary sensor/telemetry ingress** (FortyGuard 2m ground truth).
     - **Domain-specific physical modeling** (IEEE ODEs, IEC soil dynamics).
     - **Compounding data flywheels** (systems where operational telemetry and user interactions make the AI continuously more accurate and sticky).
5. **Founder-Market Fit & Self-Awareness:**
   * Show deep domain credibility and articulate exactly why your team has the right to win in this specific vertical, while demonstrating self-awareness of organizational and technical gaps.

---

### I. Human-Centric Urban Design & The Multiplicative Vulnerability Rule
*(Mike Stelfox - Founder @ Stelfox Design Studio, Virginia Sea Grant Fellow, Hackathon Mentor - Session 13)*

1. **The 5-Layer Cooling Priority Model:**
   * Systematically prioritize microclimate interventions across:
     - **Conditions:** 2m ambient temperature, duration/persistence, diurnal peaks.
     - **Causes:** Impervious ratio, surface albedo, canyon wind-sheltering.
     - **Exposure:** Pedestrian foot traffic, transit waiting times, bus stops, school zones.
     - **Vulnerability:** Demographic sensitivity (asthma rates, elderly, poverty, night-time heat).
     - **Opportunity:** Plantable ground area %, right-of-way permissions, municipal budget feasibility.
2. **The "Empty Parking Lot vs. School Bus Stop" Paradox:**
   * Never chase raw temperature peaks on heat maps without human context. An empty asphalt parking lot may be the hottest pixel, but has zero human exposure. 
   * True intervention priority is multiplicative: $\text{Priority} = \text{Hazard} \times \text{Exposure} \times \text{Vulnerability} \times \text{Opportunity}$.
3. **Convective 2m Air Temp vs. Mean Radiant Temperature (MRT):**
   * While FortyGuard measures 2m ambient air temperature, human physiological thermal strain (and outdoor worker safety) is dominated by Mean Radiant Temperature (MRT) and solar irradiance ($W/m^2$). Adding tree canopy or shade structures cuts radiant heat flux by hundreds of watts per square meter, slashing perceived thermal strain (UTCI / WBGT / PET) by multiple degrees.
4. **Historic Hydrology & Nocturnal Thermal Drainage:**
   * Buried 1861 streams and paved-over storm sewer channels continue to act as natural cold-air pooling conduits at 3:00 AM due to low-lying topography. Planners can exploit historic hydrology to identify natural urban cooling corridors.
5. **Actionable Microclimate UX for Decision-Makers:**
   * Translate complex spatial data into intuitive trade-off models and parcel-level opportunity screening rather than raw raster maps.

---

### J. AI for Science, Digital Twins & The Winning Judge Doctrine
*(Constantine - Senior Solutions Architect & AI for Science Lead @ NVIDIA, Hackathon Judge - Session 14)*

1. **Software-First Acceleration Philosophy:**
   * Generational speedups ($10\times$ to $100\times$) are driven by algorithmic co-design, specialized core pipelines (Tensor Cores), and CUDA-X libraries rather than CPU transistor scaling.
2. **AI for Science & Climate Digital Twins (NVIDIA Earth-2):**
   * Digital twins of natural and physical infrastructure (**FourCastNet** for instantaneous global weather, **CorrDiff** for generative downscaling to 25m street microclimates) enable real-time risk simulation for power grids and urban resilience.
3. **The 4 Waves of AI (Perception $\to$ Generative $\to$ Agentic $\to$ Physical AI):**
   * Moving beyond chatbots: Agentic AI connects reasoning models (Nemotron, LangGraph) into autonomous tool-calling loops. Physical AI applies these models to autonomous robots and grid hardware to execute high-stakes, dangerous tasks.
4. **The Winning Judge Rule ("Simplicity of Explanation"):**
   * The backend code and mathematical physics can be deeply complex, but the problem, engineering logic, and real-world impact must be explainable in intuitive, crystal-clear terms where the judge's *"lightbulb immediately goes on."*
5. **Solving Real High-Stakes Human & Infrastructure Problems:**
   * Judges reward solutions that tackle burning crises: preventing catastrophic power grid failure during extreme heatwaves, protecting outdoor workers, and stabilizing public infrastructure.

---

## 2. ⚡ What FortyGuard's Temperature API Uniquely Offers

Mentors repeatedly emphasized that conventional weather APIs (Apple Weather, OpenWeather, NOAA) and orbital satellites (MODIS/Landsat) fail during extreme urban heatwaves. FortyGuard provides 4 proprietary capabilities that must form the foundation of any submission:

| Dimension | Conventional Weather APIs / Orbital Satellites | FortyGuard Temperature AI |
| :--- | :--- | :--- |
| **Spatial Resolution** | Regional zip-code or city averages (~10-30 km) | **Parcel & street level** (60m, 80m, 100m tiles down to building footprints) |
| **Atmospheric Boundary** | 10-30m tower height or open airport grass | **Exact 2-meter ground/street layer** (where humans, building facades, and electrical equipment operate) |
| **Heat Duration Analysis** | Single snapshot max temperature only | **Exceedance & Persistence layers** (continuous hours spent above critical safety thresholds) |
| **Context & Causality** | Raw temperature number only | **Land Cover & Computer Vision** (explains *why* it's hot: building %, asphalt %, tree canopy %, facade reflectance) |
| **Temporal Horizon** | Macroscopic synoptic forecast | **12-Hour Hyperlocal Street Forecast** (updated hourly) + Historical back to 2021 |

> [!IMPORTANT]
> **Core Mentor Rule:** Never build an application that merely displays raw temperatures. Always extract **actionable context** (Land Cover + Environmental Parameters) and generate an **automated decision, mitigation schedule, or intervention**.

---

## 3. 🏭 6 Core Industry Blueprints & Live Product Demos

During the technical webinars, FortyGuard demonstrated 6 production-grade web applications built with the Temperature API combined with open-source data:

```
                                    FORTYGUARD API USE CASE SPECTRUM
   ┌───────────────────────┬───────────────────────┬───────────────────────┬───────────────────────┐
   │ 1. PropTech / AEC     │ 2. Energy & Utilities │ 3. Insurance & Risk   │ 4. Logistics & Health │
   ├───────────────────────┼───────────────────────┼───────────────────────┼───────────────────────┤
   │ • CoolScope           │ • Grid Peak           │ • Thermal Underwrite  │ • CoolRoute           │
   │ • UHI Retrofit ROI    │ • Transformer Thermal │ • LA Fire Hazard Risk │ • Wet-Bulb Worker     │
   │ • Shading Simulation  │ • Feeder Peak Alert   │ • Extreme Heat Claim  │   Safety Shifts       │
   │ • Autodesk Forma Sync │ • Demand Response     │   Predictor           │ • Cold-Chain Cargo    │
   └───────────────────────┴───────────────────────┴───────────────────────┴───────────────────────┘
```

### 1. Real Estate & PropTech (`CoolScope`)
* **Core Endpoints:** Heatmap + Satellite Land Cover + Environmental Parameters.
* **Mechanism:** Ingests 2m temperature and segmentation masks (e.g., 72.7% building, 0% canopy). Simulates the exact cooling delta from adding cool roofs, facade reflectance, or shade trees.
* **Commercial Value:** Quantifies HVAC energy savings, heatwave penalty days, and property valuation uplift for developers and municipal planning boards.

### 2. Electric Grid & Utilities (`Grid Peak`)
* **Core Endpoints:** Heatmap + Solar Irradiance + 12h Hyperlocal Forecast.
* **Third-Party Data Fusion:** Open electrical grid datasets (`eGrid`), substation coordinates, and dynamic energy pricing.
* **Mechanism:** Predicts transformer thermal overload and feeder peak demand hours before equipment blowouts occur.
* **Commercial Value:** Triggers automated industrial demand-response and pre-cooling cycles, preventing multi-million dollar substation burnouts.

### 3. High-Density Compute & Data Centers (`Thermal Grid`)
* **Core Endpoints:** Heatmap + Apparent Temperature + 12h Forecast.
* **Mechanism:** Monitors outdoor ambient microclimate enveloping data center chiller yards and cooling towers.
* **Commercial Value:** Dynamically optimizes Power Usage Effectiveness (PUE) and schedules carbon-aware compute workloads during cooler microclimate windows.

### 4. Insurance & Underwriting Risk Modeling
* **Core Endpoints:** Historical Time-Series (2021-present) + Exceedance / Persistence + Satellite Segmentation.
* **Mechanism:** Correlates multi-year heatwave duration with structural fire claims, electrical panel failures, and wildfire ignition zones (e.g., Los Angeles heatwave fire risks).
* **Commercial Value:** Enables parametric heat insurance products and dynamic property risk premiums.

### 5. Cold-Chain Logistics & Worker Safety (`CoolRoute`)
* **Core Endpoints:** Environmental Parameters (**Wet-Bulb Temperature**, Humidity, Solar Irradiance) + Heatmap.
* **Third-Party Data Fusion:** OpenStreetMap routing algorithms.
* **Mechanism:** Computes dynamic "cool corridors" and safe work shifts for delivery couriers and outdoor construction crews based on OSHA/NIOSH thermal stress limits. Applies specialized thresholds for sensitive cargo (vaccines, dairy, produce).
* **Commercial Value:** Prevents heatstroke liabilities and cargo spoilage.

### 6. ESG & Urban Environmental Planning (`Carbon Lens`)
* **Core Endpoints:** Environmental Parameters (AQI, PM2.5, CO2, Methane) + Heatmap.
* **Mechanism:** Correlates hyper-local heat pockets with stagnant air pollution traps across urban street canyons.
* **Commercial Value:** Informs municipal policy on climate resilience zones, bus shelter shading, and clean-air corridors.

---

## 4. 🤖 Engineering Guide for Track 06: Agentic AI
*(Fawad Shah - Head of Software Engineering)*

1. **Expose APIs as Structured Agent Tools:**
   Wrap the 6 core FortyGuard endpoints (Heatmap, Exceedance, Persistence, Environmental Parameters, Satellite Segmentation, Heat Intelligence) as typed tool functions for LangGraph / LangChain agents.
2. **Handle Asynchronous Polling Gracefully:**
   Geospatial polygon computations are non-blocking. The agent must submit the query, extract the `activity_id`, and poll the `/v1/status` endpoint every 3-5 seconds without hanging the pipeline.
3. **Contextual Multi-Step Reasoning:**
   The agent should not stop at fetching temperature; it must:
 - Identify *why* the heat anomaly exists (Land Cover segmentation).
 - Evaluate cumulative thermal soak (Persistence / Exceedance).
 - Formulate and dispatch actionable mitigation instructions (load-shedding, HVAC cycling, resident push alerts).

---

## 5. 📊 Official 4 Judging Criteria & Percentage Rubrics
*(Officially confirmed by FortyGuard Leadership in Session 9)*

| Weight | Official Criterion | What Judges Evaluate | Thermal Sentinel Grid Alignment |
| :-: | :--- | :--- | :--- |
| **40%** | **Impact & Relevance** | Does the project solve a real-world, high-stakes urban heat problem with measurable, defensible outcomes? Is it a production-grade utility rather than a toy demo? | **~$2.57M modeled avoided exposure** under disclosed VoLL assumptions, 365.4 equivalent aging hours avoided, and a clear path to reducing thermal risk for utilities and data centers; not realized savings. |
| **35%** | **Technical Execution** | Architectural rigor, robust utilization of FortyGuard API data, code quality, security, and live deployment stability. | **168 passing pytest tests plus 3 opt-in live checks skipped by default**, IEEE Std C57.91 Annex G verification ($<0.0001^\circ\mathrm{C}$ error), dual-storage Supabase persistence, deterministic safety filter. |
| **15%** | **Innovation** | Novel concept, non-obvious multi-source data coupling, creative synthesis across tracks. | **Physical-AI Hybrid Stack:** FortyGuard 2m microclimate coupled with IEEE ODEs, IEC 60287 soil dryout physics, and LangGraph StateGraph. |
| **10%** | **Communication** | Clarity of demo pitch, written documentation, value proposition, and communicating the core "Why". | **3-minute screen demo** of live UI, second-by-second pitch script, complete academic documentation suite. |

---

## 🚨 Mandatory Submission Checklist & Rules
*(Hard Deadline: **August 30, 2026, at 11:59 PM GST**)*

- [ ] **Working Live Application URL:** Publicly deployed web app (e.g. `https://www.thermal-sentinel-grid.live`) with zero authentication barrier and full incognito compatibility.
- [ ] **3 to 5 Minute Demo Video (English):** Must feature a direct screen recording of the **actual working software UI** (pure AI-generated avatar/marketing videos are strictly disqualified). Hosted on YouTube (unlisted/public) or Vimeo.
- [ ] **GitHub Repository & Collaborator Access:** Clean codebase with **`Hackathon FG`** (`Hackathon@fortyguard.com`) invited as a collaborator. All API keys kept strictly in server-side environment variables.
- [ ] **Official Google Form Submission:** Submitted by the team lead via **[https://forms.gle/jLgBzVTG1NhJ3gNe6](https://forms.gle/jLgBzVTG1NhJ3gNe6)** under **Track 03: Industrial & Enterprise** (with **Track 06: Agentic AI** & **Track 02: Future Buildings & Energy** secondary tags). (New submissions overwrite prior ones).
- [ ] **API Quota Management:** 2,000,000 credits allocated. If exhausted during testing, create a secondary account and include both API keys in the submission notes.
- [ ] **Public Community Voting Campaign:** Activate network voting when the "Cast Your Vote" tab launches on the Temperature Dashboard (1 verified vote per account for public visibility and social proof).
- [ ] **Prizes:** Top 3 overall winners receive cash prizes from the $6,000 pool + **1 NVIDIA GPU / Jetson kit per team** (presented by Constantine from NVIDIA). Winners announced on **September 16, 2026**.

