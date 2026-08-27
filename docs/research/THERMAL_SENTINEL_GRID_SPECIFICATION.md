# ⚡ Thermal Sentinel Grid - Full Implementation Specification
> **FortyGuard Hackathon '26 - Track 06 (Agentic AI) & Track 02 (Future Buildings & Energy)**  
> Physics-Constrained Multi-Agent Decision-Support & Dispatch Engine for Distribution Transformers and Outdoor Energy Assets.

---

## 🧭 Core Architectural Philosophy

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   THE 3 ARCHITECTURAL PILLARS                                            │
│                                                                                                          │
│   1. External Boundary Condition  ──►  FortyGuard 2m Ambient Air + Persistence + Solar Irradiance        │
│   2. Physical State Estimation    ──►  IEEE C57.91 / IEC 60076-7 Differential Thermal & Aging Equations  │
│   3. Deterministic Safety Gate    ──►  Non-LLM Hard Enforcement (Voltage 0.95-1.05pu, N-1, Hotspot <140C)│
└──────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> **Framing Rule:** The system is framed as a **physics-constrained decision-support and dispatch platform**, not as a system claiming to certify equipment loading or predict failure from ambient temperature alone. The LLM orchestrates tools and explains decisions; deterministic code enforces physical safety constraints.

---

## 1. 📐 Mathematical Formulation & Thermal Equations

### 1.1 Variables & Implementation Notation

| Symbol | Definition | Unit / Convention |
| :--- | :--- | :--- |
| $T_a(t)$ | FortyGuard 2-meter ambient air temperature at asset | ${}^\circ\mathrm{C}$ |
| $T_o(t)$ | Absolute top-oil temperature | ${}^\circ\mathrm{C}$ |
| $\theta_o(t)$ | Top-oil temperature rise above ambient ($T_o - T_a$) | ${}^\circ\mathrm{C}$ |
| $\theta_w(t)$ | Winding hot-spot rise over top oil | ${}^\circ\mathrm{C}$ |
| $T_{hs}(t)$ | Absolute winding hot-spot temperature | ${}^\circ\mathrm{C}$ (Kelvin for Arrhenius) |
| $K(t)$ | Per-unit load ratio ($I(t) / I_{\text{rated}}$) | dimensionless ($[0.0, 2.0]$) |
| $R$ | Ratio of load loss to no-load loss at rated load | dimensionless ($\approx 3.0 - 6.0$) |
| $\Delta\theta_{o,r}$ | Rated-load steady-state top-oil rise | ${}^\circ\mathrm{C}$ ($\approx 45 - 55^\circ\mathrm{C}$) |
| $\Delta\theta_{w,r}$ | Rated-load winding hot-spot gradient over top oil | ${}^\circ\mathrm{C}$ ($\approx 20 - 30^\circ\mathrm{C}$) |
| $n, m$ | Top-oil and winding thermal exponents | $n \approx 0.8 - 0.9$, $m \approx 0.8$ |
| $\tau_o, \tau_w$ | Top-oil and winding thermal time constants | $\tau_o \approx 1.5 - 3.0\text{ h}$, $\tau_w \approx 4 - 10\text{ min}$ |
| $S(t)$ | Solar irradiance from FortyGuard endpoint | $\mathrm{W/m^2}$ |

---

### 1.2 Top-Oil Transient Differential Equation (IEC 60076-7)

$$\tau_o \frac{d\theta_o(t)}{dt} + \theta_o(t) = \theta_{o,u}(K(t), S(t))$$

Where the load-dependent steady-state top-oil rise is:
$$\theta_{o,u}(K) = \Delta\theta_{o,r} \left(\frac{1 + R K^2}{1 + R}\right)^n$$

**Absolute Temperature Form (Production API):**
$$\tau_o \frac{dT_o}{dt} + T_o = T_{a,\text{eff}}(t) + \Delta\theta_{o,r} \left(\frac{1 + R K^2}{1 + R}\right)^n$$

---

### 1.3 Winding Hot-Spot Transient Equation

$$\tau_w \frac{d\theta_w(t)}{dt} + \theta_w(t) = \theta_{w,u}(K(t)) = \Delta\theta_{w,r} K(t)^{2m}$$

The absolute winding hot-spot temperature is:
$$T_{hs}(t) = T_{a,\text{eff}}(t) + \theta_o(t) + \theta_w(t)$$

---

### 1.4 Equivalent Solar Ambient Increment

Solar irradiance is mapped into an **equivalent ambient increment**:
$$\Delta T_{\text{solar}}(t) = \frac{\alpha_{\text{abs}} S(t) A_{\text{proj}} F_{\text{view}}}{h_{\text{eff}} A_{\text{surf}}}$$
$$T_{a,\text{eff}}(t) = T_a(t) + \Delta T_{\text{solar}}(t)$$

---

### 1.5 Exact Discrete-Time State Updates ($\Delta t = 5\text{ min}$)

For numerical stability and exact integration:
$$\theta_{o,k+1} = \theta_{o,u,k} + \left(\theta_{o,k} - \theta_{o,u,k}\right) e^{-\Delta t / \tau_o}$$
$$\theta_{w,k+1} = \theta_{w,u,k} + \left(\theta_{w,k} - \theta_{w,u,k}\right) e^{-\Delta t / \tau_w}$$
$$T_{hs,k} = T_{a,\text{eff},k} + \theta_{o,k} + \theta_{w,k}$$

---

### 1.6 Insulation Loss-of-Life & Aging Acceleration Factor

IEEE/IEC Arrhenius-style aging acceleration factor $V(T_{hs})$:
$$V(T_{hs}) = \exp\left[\frac{15000}{383} - \frac{15000}{T_{hs} + 273.15}\right]$$
*Where $383\text{ K} = 110^\circ\mathrm{C}$ reference hot-spot temperature ($V = 1.0$ at normal rated life).*

**Cumulative Equivalent Aging Hours ($L_{\text{eq}}$):**
$$L_{\text{eq}} = \sum_{k=0}^{N-1} V(T_{hs,k}) \Delta t_k \quad (\Delta t_k \text{ in hours})$$

---

## 2. ⚡ Proper Parameterization of FortyGuard Persistence & Exceedance

> [!CAUTION]
> **Core Modeling Rule:** Do NOT add persistence ($P_\theta$) or degree-hours ($H_\theta$) directly into physical time constants ($\tau_o, \tau_w$).  
> *Persistence and exceedance shape the forcing trajectory; $\tau_o$ and $\tau_w$ determine the physical response.*

### Event-Response Ratios & Thermal Soak Index
- **Top-Oil Response Ratio:** $\rho_o = 1 - e^{-P_\theta / \tau_o}$ (when $\rho_o \approx 1$, the transformer has spent enough time to reach steady-state thermal saturation).
- **Winding Response Ratio:** $\rho_w = 1 - e^{-P_\theta / \tau_w}$.
- **Thermal Soak Index ($\mathrm{TSI}_\theta$):**
  $$\mathrm{TSI}_\theta = \frac{P_\theta}{\tau_o} + \lambda \frac{H_\theta}{\tau_o \theta_{\text{scale}}}$$

---

## 3. 🌐 Open Data Sources & Asset Mapping

### 3.1 OpenStreetMap Overpass QL Queries (Phoenix Metro Bounding Box)
```text
Bounding Box: south=33.20, west=-112.40, north=33.90, east=-111.80
```

```overpass
[out:json][timeout:180];
(
  // Substations and Transformers
  nwr["power"="substation"](33.20,-112.40,33.90,-111.80);
  nwr["power"="transformer"](33.20,-112.40,33.90,-111.80);
  
  // Power Distribution Lines
  way["power"~"line|minor_line|cable"](33.20,-112.40,33.90,-111.80);
  
  // Commercial / Industrial / Health Footprints
  nwr["building"~"commercial|industrial|warehouse|retail|office|supermarket"](33.20,-112.40,33.90,-111.80);
  nwr["amenity"~"hospital|university|school"](33.20,-112.40,33.90,-111.80);
);
out center tags;
```

### 3.2 Open Datasets Index
1. **NREL End-Use Load Profiles (AWS Public Dataset):** 15-minute building-stock load curves across US climate zones.
2. **EIA Form 861 / 860 / 861M:** Utility sales, customer classes, and generator/BESS registries.
3. **FEMA National Risk Index (NRI):** Census-tract-level heatwave vulnerability and consequence weighting.
4. **Electrical Feeder Topology:** IEEE 13-node / 34-node test feeders or OpenDSS distribution models.

---

## 4. 🛡️ Deterministic Safety Gate Architecture

```mermaid
flowchart TD
    Candidate["Candidate Mitigation Action"] --> Gate{"Deterministic Safety Gate<br>Non-LLM Code"}
    
    Gate --> C1["Check 1: Thermal Ceilings<br>Top-Oil < 110C, Hotspot < 140C"]
    C1 -->|Pass| C2["Check 2: Grid Voltage<br>0.95 <= V_pu <= 1.05"]
    C2 -->|Pass| C3["Check 3: N-1 Redundancy<br>Feeder & Tie Reserve"]
    C3 -->|Pass| C4["Check 4: BESS Energy Reserve<br>SOC >= SOC_min + SOC_reserve"]
    
    C4 -->|All Pass| Accept["ACCEPT: Automated Dispatch"]
    C1 -->|Violation| Modify["MODIFY: Project onto Safe Envelope K_safe"]
    C2 -->|Violation| Modify
    C3 -->|Violation| Reject["REJECT: Escalate to Operator"]
    C4 -->|Violation| Modify
```

### 4.1 Hard Constraint Ceilings
- **Upper Bound Hot-Spot Ceiling:** $T_{hs}^{U}(t) < 140^\circ\mathrm{C}$
- **Upper Bound Top-Oil Ceiling:** $T_o^{U}(t) < 110^\circ\mathrm{C}$
- **Voltage Envelope:** $0.95 \le V_i^{\text{pu}} \le 1.05$ across all monitored buses.
- **BESS Operating Envelope:** $SOC_{k+1} \ge SOC_{\min} + SOC_{\text{reserve}}$ (e.g., $20\% + 10\% = 30\%$).

### 4.2 Constraint Projection Logic (`MODIFY`)
If requested loading $K_{\text{proposed}}$ violates thermal limits, the gate solves for safe maximum capacity $K_{\text{safe}}$:
$$K_{\text{safe}} = \max K \quad \text{s.t. } T_{hs}^{U}(K) \le T_{hs,\max}, \; T_o^{U}(K) \le T_{o,\max}, \; V_i(K) \in [0.95, 1.05]$$

---

## 5. ☀️ Historical Replay Demonstration: Phoenix, July 2023

```
                                  PHOENIX HEATWAVE REPLAY EPISODE
   ┌───────────────────────────────────┐     ┌───────────────────────────────────┐
   │ Live Capture: July 24-26, 2023   │ ──► │ Target Asset: Generic 25 MVA Twin │
   │ 72 hourly FortyGuard boundaries  │     │ • Transformer + MV Cable Model    │
   │ Daily peaks: 42.44/42.76/42.52°C │     │ • BESS + Modelled Grid Load       │
   └───────────────────────────────────┘     └─────────────────┬─────────────────┘
                                                               │
                                                               ▼
   ┌───────────────────────────────────┐     ┌───────────────────────────────────┐
   │ Baseline (No proactive dispatch) │ vs. │ Thermal Sentinel (Measured 2m +   │
   │ over 72 measured weather hours:   │     │ modelled pre-cooling / BESS):     │
   │ • Daily peak hot-spot: 165.1°C    │     │ • Daily peak hot-spot: 138.5°C    │
   │ • 2,088.5 equivalent aging hours  │     │ • 181.0 equivalent aging hours    │
   │ • Emergency load tripping         │     │ • Zero voltage/N-1 violations     │
   └───────────────────────────────────┘     └───────────────────────────────────┘
```

---

## 6. 🤖 LangGraph StateGraph Architecture

### 6.1 State Schema (`src/models/state.py`)
```python
from datetime import datetime
from typing import TypedDict, List, Dict, Any, Optional

class ThermalSentinelState(TypedDict):
    timestamp: datetime
    asset_id: str
    location: Dict[str, float]  # {"lat": float, "lon": float}
    fortyguard_forecast: Dict[str, Any]  # 12h 2m temp, irradiance, wet bulb
    persistence_metrics: Dict[str, float]  # P_40, H_40, TSI
    asset_parameters: Dict[str, Any]  # rating, tau_o, tau_w, loss ratio
    load_forecast: List[float]  # 12h load profile
    thermal_trajectory: Dict[str, List[float]]  # T_o, T_hs over 12h
    aging_summary: Dict[str, float]  # V_max, L_eq
    safety_gate_result: Dict[str, Any]  # status: ACCEPT | MODIFY | REJECT
    mitigation_plan: Optional[Dict[str, Any]]
    operator_approval_required: bool
    audit_trail: List[Dict[str, Any]]
```

### 6.2 StateGraph Flow
```
[Ingest & Validate] ──► [FortyGuard 12h Forecast & Persistence Node]
                                    │
                                    ▼
[Asset & Grid Mapping Node] ──► [IEEE/IEC Physics Simulation Node]
                                    │
                                    ▼
[Insulation Aging Evaluator] ──► [Mitigation Planner Node]
                                    │
                                    ▼
                        [Deterministic Safety Gate]
                               ┌────┴────┐
                      (Pass)   │         │  (Violation)
                               ▼         ▼
                    [Approved Dispatch] [Project Safe K_safe]
                               │         │
                               └────┬────┘
                                    ▼
                    [Audit Logger & Webhook Dispatcher]
```

---

## 7. ⚡ Advanced Heavy Computational Physics Engines
For complete mathematical monographs, LaTeX formulations, and standards proofs, see **[`ADVANCED_PHYSICS_AND_MATHEMATICAL_PAPERS.md`](ADVANCED_PHYSICS_AND_MATHEMATICAL_PAPERS.md)**:


1. **Dynamic Line Rating & Conductor Catenary Sag (IEEE Std 738-2012):**
   Iterative Newton-Raphson convective, radiative, and solar heat equilibrium ($q_c + q_r = q_s + I^2R$) unlocking $+22.5\%$ dynamic ampacity headroom while preventing ground flashover sag ($S(T_c)$).
2. **Coupled 2-State BESS Electro-Thermal & Arrhenius SEI Capacity Fade:**
   2-state lumped core ($T_c$) vs. surface ($T_s$) differential thermal equations with continuous electrochemical SEI growth ($dQ_{\text{loss}}/dt$), tracking real-time degradation cost (\$/MWh) and enforcing the $55^\circ\mathrm{C}$ thermal runaway ceiling.
3. **Arrhenius-Weibull Grid Fragility & Cascading Blackout Risk:**
   Time-dependent non-homogeneous Poisson-Weibull failure hazard model $\lambda_i(t, T)$ with Arrhenius acceleration $A_F(T)$ integrated across substation assets to output joint cascading failure probability ($P_{\text{cascade}}$).
4. **Analytical Uncertainty-Bounded Dispatch Screen:**
   Applies Gaussian 90%/95%/99% quantiles to a simplified four-bus feeder approximation and heuristically selects BESS, OLTC, and load-shedding actions. The implementation does not invoke a numerical SOCP optimizer.

---

## 8. 🗄️ Durable Hybrid Database Layer (17 Tables)

Thermal Sentinel Grid incorporates a **Dual-Storage Persistence Engine** (Local SQLite + PostgREST Supabase Cloud PostgreSQL) across 17 application tables. Supabase is authoritative in production; SQLite is a local/offline fallback and is ephemeral on Vercel:

1. **`api_call_cache`:** Raw FortyGuard responses indexed by MD5 request identity plus full simulation results indexed by `sim:` SHA-256 identity. Prevents duplicate billing and replays identical solves without expiry.
2. **`dispatch_work_orders`:** Historical prototype dispatch recommendations ($K_{\text{safe}}$, BESS MW, OLTC tap steps).
3. **`credit_accounting_ledger`:** Audit trail of FortyGuard API credit deductions and remaining balances.
4. **`academic_research_papers`:** 22 indexed research records with LaTeX equations and alphaXiv links.
5. **`substation_telemetry_logs`:** 12-hour synchronized modelled asset telemetry steps ($\theta_o, \theta_w, V(t)$).
6. **`simulation_runs`:** What-If input and scalar-output audit summaries; the full trajectory is persisted in `api_call_cache`.
7. **`multi_day_heatwave_logs`:** Per-step model audit records for 72h soil and aging progression; environmental forcing is the frozen 72-row live capture.
8. **`dlr_catenary_telemetry`:** Dynamic Line Rating heat balance ($q_c, q_r, q_s, I^2R$) and catenary sag.
9. **`agent_execution_traces`:** Multi-agent LangGraph StateGraph DAG execution logs and GPT narratives.
10. **`financial_audit_snapshots`:** VoLL-informed scenario snapshots (~$2.57M modeled avoided exposure and a 5,472.6× assumption-based cost ratio in the canonical replay); not realized savings or actuarially calibrated forecasts.
11. **`microclimate_parcel_store`:** Saved parcel geometry and measured peak/spread with city, coordinates, and catalog date in GeoJSON properties. Cloud DB can select a row and rebase the dashboard onto its persisted or newly computed solve.
12. **`bess_degradation_logs`:** 2-state core/surface thermal ODEs & continuous Arrhenius SEI capacity fade (\$/hr).
13. **`cascading_risk_snapshots`:** Uncalibrated Poisson-Weibull cascading-risk scenario score ($P_{\text{cascade}}$) and modeled $VoLL$ exposure.
14. **`chance_constrained_opf_logs`:** Analytical quantile-bounded dispatch results under Gaussian uncertainty ($z_{1-\alpha}$).
15. **`cbf_safety_certificates`:** Deterministic safety-envelope checks, slack, and pass/modify/reject verdicts.
16. **`grid_assets_registry`:** Digital twin asset catalog (transformers, substations, BESS units, health scores).
17. **`validation_runs`:** Content-addressed external-validation reports with immutable baseline/reference identities, evidence class, configuration, and complete metrics. SQLite creates this table automatically; existing Supabase deployments apply [`../supabase_validation_migration.sql`](../supabase_validation_migration.sql).

External air validation prefers physical IEM/ASOS observations, explicitly falls
back to Open-Meteo gridded meteorology only in `auto` mode, and keeps Landsat LST
as surface context. See the [Ground-Truth Validation Contract](GROUND_TRUTH_VALIDATION_CONTRACT.md).


