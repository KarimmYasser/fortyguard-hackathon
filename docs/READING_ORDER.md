# 📚 Master Reading Order & Documentation Roadmap
> **Thermal Sentinel Grid — FortyGuard Hackathon '26**  
> *Author:* Karim Y. Azab (Karim Yasser)  
> *Live Application:* [www.thermal-sentinel-grid.live](https://www.thermal-sentinel-grid.live/)  
> *Repository:* [github.com/KarimmYasser/fortyguard-hackathon](https://github.com/KarimmYasser/fortyguard-hackathon)

---

## 🧭 Executive Reading Guide

Thermal Sentinel Grid is backed by extensive research, international engineering standards (IEEE/IEC), physical differential equations, data science pipelines, and 14 keynote webinar masterclasses.

To save your time and eliminate reading duplicate content, this roadmap organizes all project documentation into **3 tiered pathways** based on your role and available time.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       3-TIER READING PATHWAY                                             │
│                                                                                                          │
│   [Tier 1: Executive Foundation]     ──► ~25 min (Vision, SCADA Safety, AI Philosophy & Judging Rubrics)│
│   [Tier 2: Engineering & Science]    ──► ~45 min (Validation Contract, Fleet Triage, IEEE ODEs, Medallion)│
│   [Tier 3: Reference & Deep Dives]   ──► As Needed (307-line Glossary, Keynote Playbook, Math Papers)   │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## ⏱️ Quick Summary of Reading Tiers

| Tier | Target Audience / Goal | Estimated Time | Key Documents Included |
| :--- | :--- | :---: | :--- |
| **Tier 1: Executive Foundation & Strategy** | Judges, evaluators, and engineers wanting the core concept with zero fluff. | **~25 min** | `README.md`, `SCADA_LLM_AND_LANGGRAPH_EXPLAINER.md`, `VALUE_PROPOSITION_AND_AI_PHILOSOPHY.md`, `AGENT_CONTEXT.md`, `HACKATHON_FAQ.md`. |
| **Tier 2: Engineering, Validation & Data Science** | Technical judges and developers auditing math, API calls, ground truth, and ML. | **~45 min** | `GROUND_TRUTH_VALIDATION_CONTRACT.md`, `PORTFOLIO_OPERATIONS_AND_MCP.md`, `14-field-notes-live-integration.md`, `ASYMMETRIC_INNOVATION_AND_PHYSICAL_MECHANISMS.md`, `THERMAL_SENTINEL_GRID_SPECIFICATION.md`, `DATA_SCIENCE_AND_ML_SPECIFICATION.md`, `DATABASE_QUERY_PERFORMANCE.md`, `API_INTEGRATION_AND_REPLAY_ARCHITECTURE.md`. |
| **Tier 3: Advanced Deep Dives & Pitch Assets** | Comprehensive reference for Q&A defense, standards compliance, and citations. | *Reference / As Needed* | `GLOSSARY.md`, `MENTOR_INSIGHTS_AND_IDEA_FRAMEWORK.md`, `sessions-dialogue/README.md`, `PITCH_DECK.md`, `SUBMISSION.md`, `SECURITY_AND_JUDGE_ACCESS.md`, `ADVANCED_PHYSICS_AND_MATHEMATICAL_PAPERS.md`, `IEEE_ANNEX_G_AND_AC_POWER_FLOW_SPECIFICATION.md`, `FORTYGUARD_API_MASTER_REFERENCE.md`. |

---

## 🚀 Tier 1: Executive Foundation & Strategy (~25 min)
*Start here to grasp 90% of the project's vision, architecture, commercial positioning, and hackathon requirements.*

1. **[README.md](../README.md)** *(~5 min)*
   * **Why read it:** The master blueprint. Explains the 3 pillars, the 2-meter boundary layer problem, the 8 scientific moats, Portfolio Operations, external ground-truth validation, and the live production deployment at [www.thermal-sentinel-grid.live](https://www.thermal-sentinel-grid.live/).
2. **[SCADA_LLM_AND_LANGGRAPH_EXPLAINER.md](research/SCADA_LLM_AND_LANGGRAPH_EXPLAINER.md)** *(~5 min)*
   * **Why read it:** Demystifies industrial SCADA (RTUs, PLCs, protocols), establishes the cardinal safety rule (*"LLMs must NEVER be in direct physical control loops"*), and explains why LangGraph is essential for cyclic state machines with human-in-the-loop oversight.
3. **[VALUE_PROPOSITION_AND_AI_PHILOSOPHY.md](research/VALUE_PROPOSITION_AND_AI_PHILOSOPHY.md)** *(~4 min)*
   * **Why read it:** Explains why training a toy black-box neural net is an anti-pattern for critical infrastructure, how the 4-layer Physical-AI stack operates, and the scenario economics (~$2.57M avoided exposure, 5,473x assumption-based ratio).
4. **[AGENT_CONTEXT.md](../AGENT_CONTEXT.md)** *(~5 min)*
   * **Why read it:** Explains the real-world origin story (Egypt & US Sunbelt heatwaves), thermal soak failure mechanics, track alignment (**Track 03 Industrial & Enterprise**, **Track 06 Agentic AI**, & **Track 02 Energy**), and the 4 commercial customer archetypes (Utility Reliability, Data Center Ops, Municipal Infrastructure, InsurTech).
5. **[HACKATHON_FAQ.md](official/HACKATHON_FAQ.md)** *(~6 min - Skim)*
   * **Why read it:** The single consolidated master FAQ compiling all official rules, API limits, deadlines, and the **official judging rubrics** (Impact 40%, Technical Execution 35%, Innovation 15%, Communication 10%).

---

## 🛠️ Tier 2: Core Engineering, Ground Truth & Data Science (~45 min)
*Read these to understand how the system is validated against external ground truth, how physics equations are solved, real API behaviors, and data science methodologies.*

1. **[GROUND_TRUTH_VALIDATION_CONTRACT.md](research/GROUND_TRUTH_VALIDATION_CONTRACT.md)** *(~7 min)*
   * **Why read it:** The production acceptance contract for external thermal evidence: in-situ physical station observations (IEM ASOS/AWOS) vs. gridded meteorology (Open-Meteo ERA5-Land), timezone-aware UTC canonicalization, and honest reporting (e.g. Phoenix airport is warmer in this window, reporting an urban-station anomaly rather than claiming false UHI proof).
2. **[PORTFOLIO_OPERATIONS_AND_MCP.md](research/PORTFOLIO_OPERATIONS_AND_MCP.md)** *(~6 min)*
   * **Why read it:** Details the fleet triage operations engine: deterministic asset risk ranking (`portfolio_rank_v1`), candidate worker intervention windows (`threshold_screen_v1`), SHA-256 content-addressed evidence hashing, and Model Context Protocol (MCP) tool endpoints (`rank_portfolio_risk`, `find_worker_intervention_windows`, `get_mitigation_evidence`).
3. **[14-field-notes-live-integration.md](api-documentation/14-field-notes-live-integration.md)** *(~6 min)*
   * **Why read it:** The empirical reality of integrating `api.fortyguard.com`. Covers 10 crucial findings: why `env_params` echoes your input, percentage vs octas bug, the measured $+1.14^\circ\text{C}$ urban-vs-natural contrast (vs airport heat islands), 12h persistence duration, and live vs replay parity.
4. **[ASYMMETRIC_INNOVATION_AND_PHYSICAL_MECHANISMS.md](research/ASYMMETRIC_INNOVATION_AND_PHYSICAL_MECHANISMS.md)** *(~6 min)*
   * **Why read it:** The 4 unmeasured physical cascades that utility SCADA misses: buried cable-soil dryout, Control Barrier Functions (CBF-QP), urban canyon aerodynamic throttling, and virtual paper-oil moisture diffusion.
5. **[THERMAL_SENTINEL_GRID_SPECIFICATION.md](research/THERMAL_SENTINEL_GRID_SPECIFICATION.md)** *(~8 min)*
   * **Why read it:** Core implementation specification: exact IEEE C57.91 / IEC 60076-7 thermal differential ODEs, discrete exponential updates, and the LangGraph multi-agent schema with structured **Fact vs. Finding** decision synthesis.
6. **[DATA_SCIENCE_AND_ML_SPECIFICATION.md](research/DATA_SCIENCE_AND_ML_SPECIFICATION.md)** *(~6 min)*
   * **Why read it:** Complete IBM Data Science methodology: Bronze $\to$ Silver $\to$ Gold Medallion ETL pipeline (18 features), Moran's I spatial autocorrelation ($I=0.742$), spatial bivariate regression, multi-cadence temporal resampling, Ridge Physics Surrogate ($R^2=0.9987$), Isolation Forest, and Weibull survival analysis.
7. **[DATABASE_QUERY_PERFORMANCE.md](research/DATABASE_QUERY_PERFORMANCE.md)** *(~4 min)*
   * **Why read it:** Architectural review of the 17-table Supabase PostgreSQL data layer: eliminating write amplification on the replay endpoint (ensuring page reloads are read-only and idempotent), narrow `select=response_payload` PostgREST projections, and exact `HEAD` row counting.
8. **[API_INTEGRATION_AND_REPLAY_ARCHITECTURE.md](research/API_INTEGRATION_AND_REPLAY_ARCHITECTURE.md)** *(~2 min)*
   * **Why read it:** Architectural justification for Dual-Mode Ingestion (Live FortyGuard Cloud API vs. Deterministic Phoenix July 2023 Benchmark Replay with $<15\text{ms}$ latency).

---

## 🔬 Tier 3: Advanced Deep Dives, Keynotes, Glossary & Pitch Assets (Reference / As Needed)
*Consult these when preparing for deep judge Q&A, IEEE standards audits, or pitch delivery.*

* **Technical & Scientific Terminology:**
  * **[GLOSSARY.md](GLOSSARY.md)** — Comprehensive 307-line authoritative reference defining microclimate meteorology, transformer physics, grid operations, BESS degradation, human comfort (MRT/UTCI), and financial reliability indices.
* **Pitch & Defense Strategy:**
  * **[PITCH_DECK.md](../PITCH_DECK.md)** — 3-minute video voiceover script, 5-minute slide deck outline, PMF customer discovery brief, and Judge Q&A Defense Cheat Sheet.
  * **[SUBMISSION.md](../SUBMISSION.md)** — Official submission form values, track justification, and verified test metrics (168 passing tests).
* **Mentorship & Product Strategy Master Playbook:**
  * **[MENTOR_INSIGHTS_AND_IDEA_FRAMEWORK.md](research/MENTOR_INSIGHTS_AND_IDEA_FRAMEWORK.md)** — Synthesized master playbook spanning all 14 keynote webinars (*Constantine from NVIDIA on AI for Science & 4 waves of AI, Mike Stelfox on 5-layer cooling priority & human MRT/UTCI, Vikram on VC decision-making, Karel Wiszowaty on engineering execution, Prof. Reichental on Physical AI & Cognitive Cities, Thamir on COCO PMF framework, Snehil on Dashboard masterclass, and Mudethir/Aamir on "Fact vs Finding"*).
  * **[sessions-dialogue/README.md](sessions-dialogue/README.md)** — High-density summary catalog of all 14 official mentorship sessions.
* **Advanced Mathematical Monograph:**
  * **[ADVANCED_PHYSICS_AND_MATHEMATICAL_PAPERS.md](research/ADVANCED_PHYSICS_AND_MATHEMATICAL_PAPERS.md)** — Dynamic Line Rating (IEEE 738), BESS Arrhenius SEI Capacity Fade (IEC 62619), Arrhenius-Weibull Cascading Outage Risk, and Chance-Constrained SOCP OPF.
* **Standards Verification & Power Flow:**
  * **[IEEE_ANNEX_G_AND_AC_POWER_FLOW_SPECIFICATION.md](research/IEEE_ANNEX_G_AND_AC_POWER_FLOW_SPECIFICATION.md)** — Automated verification against IEEE Clause G.2/G.3 ($<0.0001^\circ\text{C}$ error) and 4-bus Forward-Backward Sweep AC flow.
* **Security & Production Compliance:**
  * **[SECURITY_AND_JUDGE_ACCESS.md](SECURITY_AND_JUDGE_ACCESS.md)** — Incognito judge access, edge rate limiting, DDoS protections, and pre-submission checklist.
* **Consolidated API Master Reference:**
  * **[FORTYGUARD_API_MASTER_REFERENCE.md](api-documentation/FORTYGUARD_API_MASTER_REFERENCE.md)** — All 13 endpoint specs in a single document.

---

## 🚫 Documents to Skip (Redundant / Superseded)

To respect your time, avoid reading these files individually as their contents have been merged into the master documents above:

| File / Folder | Why You Can Skip It | What Replaces It |
| :--- | :--- | :--- |
| `docs/api-documentation/01-*.md` through `13-*.md` | 13 separate partial endpoint guides | [FORTYGUARD_API_MASTER_REFERENCE.md](api-documentation/FORTYGUARD_API_MASTER_REFERENCE.md) |
| `docs/sessions-dialogue/1-*.md` through `14-*.md` | Raw verbatim webinar transcripts (1–14) | [sessions-dialogue/README.md](sessions-dialogue/README.md) & [MENTOR_INSIGHTS_AND_IDEA_FRAMEWORK.md](research/MENTOR_INSIGHTS_AND_IDEA_FRAMEWORK.md) |
| `docs/research/RESEARCH_AGENT_SYNTHESIS_*.md` | Early draft superseded by newer specs | [THERMAL_SENTINEL_GRID_SPECIFICATION.md](research/THERMAL_SENTINEL_GRID_SPECIFICATION.md) |
| `docs/official/OFFICIAL_ANNOUNCEMENTS.md` & `SLACK_MESSAGES.md` | Fragmented announcement snippets | [HACKATHON_FAQ.md](official/HACKATHON_FAQ.md) |
| `docs/context/chat-transcripts/*` | Raw LLM debugging logs | [AGENT_CONTEXT.md](../AGENT_CONTEXT.md) |
