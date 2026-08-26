# 📚 Documentation & Reference Hub

Welcome to the PyreShield AI / FortyGuard Hackathon documentation hub.

---

## 🗂️ Documentation Sections

### 1. 📘 [Participant Handbook](handbook/FortyGuard_Hackathon_Participant_Handbook.md)
* **[Complete PDF (High-Res 20 Pages)](handbook/FortyGuard_Hackathon_Participant_Handbook.pdf)**
* **[Markdown Handbook Text](handbook/FortyGuard_Hackathon_Participant_Handbook.md)**
* **[High-Resolution Page Scans](handbook/pages)**
* Covers rules, key dates, 7 tracks, judging criteria, scoring rubrics, and submission requirements.

---

### 2. ⚡ [FortyGuard API Reference & Guides](api-documentation/README.md)
* **[Consolidated Master Reference](api-documentation/FORTYGUARD_API_MASTER_REFERENCE.md)**
* **[OpenAPI 3.1 Schema](api-documentation/openapi.json)**
* Individual Guides:
  * `01-introduction.md` - Physics model, 2m altitude layer, spatial resolution.
  * `02-quickstart.md` - Submit-and-poll async lifecycle.
  * `03-authentication.md` - Header conventions & API keys.
  * `04-create-heatmap.md` - Heatmap generation (Snapshot, Exceedance, Persistence).
  * `05-satellite-view-segmentation.md` - Satellite land-cover computer vision.
  * `06-street-view-segmentation.md` - Street-level facade & canopy segmentation.
  * `07-heat-intelligence.md` - Multi-dimensional diagnostic reports.
  * `08-environmental-parameters.md` - AQI, wet bulb, solar radiation parameters.
  * `09-check-status.md` - Async activity polling.
  * `10-credits-usage.md` - Quota management.
  * `11-error-handling.md` - Retry & status code handling.
  * `12-known-limitations.md` - Bounding box limits & temporal constraints.
  * `13-release-notes.md` - v1.0.0 changelog.

---

### 3. 🏛️ [Official Hackathon Rules & FAQs](official)
* **[Security & Judge Access](SECURITY_AND_JUDGE_ACCESS.md):** Current edge and application safeguards, private-repository judge access, and the pre-submission availability checklist.
* **[Official Announcements & Rules](official/OFFICIAL_ANNOUNCEMENTS.md):** Verbatim dates (18-30 Aug 2026), hard deadline (30 Aug 11:59 PM GST), prizes ($6,000 + 3x Jetson kits), rubrics, and 4 required deliverables.
* **[Frequently Asked Questions (FAQ)](official/HACKATHON_FAQ.md):** Comprehensive Master FAQ compiling official rules, credit quotas, API schemas, and production gotchas.
* **[Tracks & Mentors](official/HACKATHON_TRACKS_AND_MENTORS.md):** Detailed breakdown of all 7 tracks and keynote mentor/judge advice.
* **[Slack Onboarding Posts](official/SLACK_MESSAGES.md):** Pinned Slack announcements regarding API launch & Quickstart.

---

### 4. 🔬 [Research, Specifications & System Blueprints](research/README.md)
* **[Simulation Scope, Evidence Contract & Deployment Roadmap](SIMULATION_SCOPE_AND_ROADMAP.md):** Canonical boundary between measured inputs, assumptions, model outputs, unvalidated scores, and future operational requirements.
* **[Technical & Scientific Glossary](GLOSSARY.md):** Authoritative, mathematically rigorous definitions for all physics, meteorology, IEEE/IEC standards, power flow, CBF safety filters, and economic reliability terms across the project.
* **[Data Science, Engineering & ML Specification](research/DATA_SCIENCE_AND_ML_SPECIFICATION.md):** Complete IBM Data Science lifecycle specification covering Bronze→Silver→Gold ETL Medallion architecture (18 features), Ridge Physics Surrogate ($R^2=0.9987$), Isolation Forest anomaly detection, Weibull RUL survival analysis, and paired $t$-test hypothesis proofs.
* **[Advanced Mathematical & Physical Moats](research/ADVANCED_PHYSICS_AND_MATHEMATICAL_PAPERS.md):** Academic monograph on Dynamic Line Rating (IEEE 738), BESS electro-thermal degradation (IEC 62619), Arrhenius-Weibull cascading risk, and the SOCP research basis for the prototype's analytical uncertainty screen.
* **[Scientific Research & alphaXiv Academic Corpus Report](research/SCIENTIFIC_RESEARCH_REPORT.md):** 22-record production academic index grounding PINNs, cool pavements, urban microclimates, cable soil physics, and control-barrier-function research.
* **[Thermal Sentinel Grid - Implementation Specification](research/THERMAL_SENTINEL_GRID_SPECIFICATION.md):** Full mathematical formulation, IEEE C57.91 / IEC 60076-7 equations, Overpass QL / EIA dataset queries, deterministic Safety Gate rules, Phoenix July 2023 replay scenario, and LangGraph schema.
* **[IEEE Annex G & AC Power Flow Specification](research/IEEE_ANNEX_G_AND_AC_POWER_FLOW_SPECIFICATION.md):** Standards verification benchmarks (Clause G.2 & G.3), 72-hour continuous compounding soil dryout ODEs, and 4-bus Forward-Backward Sweep AC power flow with OLTC and BESS Volt/VAR support.
* **[Value Proposition & AI Philosophy](research/VALUE_PROPOSITION_AND_AI_PHILOSOPHY.md):** Why physics-constrained Agentic AI outperforms black-box ML training, the 4-layer value matrix (~$2.57M modeled avoided exposure, 5,472.6× assumption-based ratio), and keynote mentorship insights.
* **[Asymmetric Innovation & Advanced Physical Mechanisms](research/ASYMMETRIC_INNOVATION_AND_PHYSICAL_MECHANISMS.md):** 4 non-obvious literature intersections (cable-soil moisture dry-out, CBF-inspired deterministic safety filtering, urban canyon aerodynamic throttling, and virtual paper-oil moisture diffusion).
* **[Economic Model, UI Architecture & Video Pitch Script](research/ECONOMIC_MODEL_DASHBOARD_AND_PITCH_SCRIPT.md):** Assumption-based avoided-exposure formulation, customer interruption ($VoLL$), React/Vite operator dashboard wireframe, and second-by-second 3-minute video pitch script.
* **[Mentor Insights & Idea Selection Framework](research/MENTOR_INSIGHTS_AND_IDEA_FRAMEWORK.md):** Comprehensive synthesized distillation of keynotes (*Google, Autodesk, FortyGuard*), idea selection philosophy, 6 demonstrated industry blueprints, and winning hackathon strategies.
* **[API Integration & Replay Architecture](research/API_INTEGRATION_AND_REPLAY_ARCHITECTURE.md):** Architecture Decision Record (ADR) justifying Dual-Mode Ingestion (Live Cloud Ingestion vs. Deterministic Phoenix Benchmark Replay), sub-15ms operator latency, and IEEE ground truth reproducibility.
* **[Portfolio Operations, Worker Intervention Screening & MCP](research/PORTFOLIO_OPERATIONS_AND_MCP.md):** As-built deterministic portfolio ranking, evidence coverage, explicit worker-screen limits, content-addressed audit evidence, REST contracts, and the MCP-compatible tool surface.
* **[Database Query Performance & Replay Persistence](research/DATABASE_QUERY_PERFORMANCE.md):** Application-side analysis of the Supabase performance report, the read-only replay contract, narrow PostgREST projections, persistence boundaries, regression tests, and production verification checklist.
* **[Ground-Truth Validation Contract](research/GROUND_TRUTH_VALIDATION_CONTRACT.md):** Evidence taxonomy and acceptance gates for IEM/ASOS station observations, Open-Meteo fallback, NSRDB solar context, Landsat surface context, calibrated field sensors, UTC alignment, persistence, and public validation routes.
* **[Supabase Validation Migration](supabase_validation_migration.sql):** Idempotent SQL migration adding the `validation_runs` audit table and index to existing Supabase projects.
* **[Physical-AI Research & Standards Synthesis](research/RESEARCH_AGENT_SYNTHESIS_AND_PHYSICAL_MODELS.md):** Academic literature foundation, IEEE/IEC/UL standards equations, multi-agent control architecture, and comparative concept benchmarks.
* **[SCADA, LLM Safety & LangGraph Architecture Guide](research/SCADA_LLM_AND_LANGGRAPH_EXPLAINER.md):** Architecture Decision Record (ADR) detailing SCADA telemetry, why LLMs are strictly forbidden from direct grid control loops, and when LangGraph is vs. is not overengineering.


---

### 5. 🎙️ [Mentorship & Webinar Session Dialogues](sessions-dialogue/README.md)
* **[Sessions Dialogue Index](sessions-dialogue/README.md):** Full master catalog of official webinar recordings, speakers, timestamps, and key technical takeaways.
* **[01. Onboarding & Kickoff Session](sessions-dialogue/1-onboarding-kickoff-session.md):** Hackathon launch rules, team format, US 2m data coverage, $6,000 + NVIDIA Jetson AI prizes, and submission criteria.
* **[02. Building on FortyGuard Temperature API®](sessions-dialogue/2-building-fortyguard-temperature-api.md):** Technical deep-dive by Fawad Shah (Head of Software Engineering) covering asynchronous polling architecture, 6 core endpoints, Quickstart Python SDK walkthrough, and Agentic AI track ideas.
* **[03. Heat Intelligence Cloud: What You Can Build](sessions-dialogue/3-heat-cloud-webinar-session.md):** Exploration of FortyGuard's 4 data layers and live product demonstrations across 6 major target industries (PropTech, InsurTech, Logistics, Worker Safety, Urban Planning, Utilities).
* **[04. Breaking Silos with Autodesk: Data to Design](sessions-dialogue/4-autodesk-webinar-session.md):** Mentorship by Jordana Rosa (Autodesk Forma specialist & 4x Hackathon Winner) on bridging microclimate intelligence with AEC design and winning hackathon strategies.
* **[05. Escaping the Builder's Trap: Building MLPs with Google Cloud](sessions-dialogue/5-builders-trap-webinar-session.md):** Mentorship by Ahmed Abdelkhalek (Head of Startups, Google Cloud & Judge) on MLP validation, Google Cardboard speed, the 15-minute pre-build decision checklist, and critical AI justification.
* **[06. Headlines to Impact: Mastering PR & Storytelling](sessions-dialogue/6-headlines-to-impact-session.md):** Keynote by Tarek (Founder & CEO, Narrative One) on the 3 P's engine (Perception → Presence → Partnerships), 80/20 headline rule, and winning 3-minute pitch storytelling.
* **[07. From Heat Data to Real Signal: Data Correlation Analysis](sessions-dialogue/7-data-correlation-webinar-session.md):** Technical deep-dive by Mudethir (ML Lead) & Aamir (Cloud/Data Architect, FortyGuard) on the Where/When/What triad, preventing spurious correlations, 2m air temp vs LST/ERA5, "Fact vs. Finding" rule, and cadence matching.
* **[08. Finding Product-Market Fit: Validating Idea, Customer, and Message](sessions-dialogue/8-product-market-fit-webinar.md):** Commercial masterclass by Thamir (Partner @ Cultivators; early operator at BreezoMeter $\to$ Google acquisition; Google Solar API) on the COCO discovery framework, early adopters vs enterprise ICP, willingness to pay, and the space pen vs pencil test.
* **[09. Mastering the Temperature Dashboard: Microclimate Intelligence & Live Walkthrough](sessions-dialogue/9-temperature-dashboard-webinar.md):** Technical walkthrough by Snehil Ahuja (Product Lead) & Aamir on the FortyGuard Temperature Dashboard (granularity, heat flow simulation, environmental parameters, persistence vs exceedance, segmentation, 5-pillar heat intelligence report), API key management (2M credits), public voting feature, and the 4 official judging rubrics (Impact 40%, Technical Execution 35%, Innovation 15%, Communication 10%).
* **[10. Physical AI and the Future of Smart Cities](sessions-dialogue/10-physical-ai-webinar-session.md):** Keynote by Professor Jonathan Reichental (Founder of Human Future, former CIO City of Palo Alto, Advisor @ FortyGuard, Mentor + Judge) on the Cognitive Industrial Revolution, the 4 pillars of Physical AI, autonomous urban infrastructure (aviation mini-cities, solar maintenance robotics, AV urban redesign), and deterministic safety boundaries for critical infrastructure.

---

### 6. 📝 [Project Registration & Motivation](project-registration)
* **[Registration Details & Motivation](project-registration/REGISTRATION_FIELDS.md):** Submitted form values, webhook endpoint, and exact **PyreShield AI** motivation pitch under Tracks 6 & 2.
* **[Conversation History & Strategy](project-registration/CONVERSATION_HISTORY.md):** Ideation journey, strategy iterations, Nile University research alignment, and Egypt local hazard pivot.

---

### 7. 📜 [Chat Transcripts & Context](context/README.md)
* **[Context Index](context/README.md):** Overview of transcript logs and historical context files.
* **[Full Chat Log](context/chat-transcripts/FULL_CHAT_LOG.md):** Human-readable markdown transcript of brainstorming sessions.
* **[Compact JSONL Transcript](context/chat-transcripts/transcript.jsonl):** Fast token-efficient JSONL action log.
* **[Full JSONL Transcript](context/chat-transcripts/transcript_full.jsonl):** Complete untruncated action log.


