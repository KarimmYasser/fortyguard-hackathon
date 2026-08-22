# 🔌 FortyGuard API Integration, Live Ingestion & Simulation Architecture Specification
> **Architecture Decision Record (ADR): Dual-Mode Microclimate Ingestion & System Boundary Specification**  
> **Status:** Accepted & Implemented — *revised after live integration*  
> **Applicable Tracks:** Track 06 (Agentic AI) & Track 02 (Future Buildings & Energy)

---

## ⚠️ Revision Note (post live-integration)

The first version of this ADR described Mode A as implemented. **It was not.**
Both of the agent's data inputs returned fixture data on every code path:

- `get_12h_forecast()` issued a real `env_params` call, discarded the result,
  and returned the bundled Phoenix fixture on the mock, success *and* exception
  branches — spending a credit to produce a hardcoded answer.
- `get_persistence_and_exceedance()` never called the API at all. It derived
  $P_{40}$ from the caller's straight-line distance to downtown Phoenix.

The root cause of the silent fallback was date handling: the client requested
`start_date = today`, which the API rejects (see
[§12 Known Limitations](../api-documentation/12-known-limitations.md) and
[§14 Field Notes](../api-documentation/14-field-notes-live-integration.md)).
Every live attempt failed and fell through to the fixture without surfacing an
error.

Mode A is now genuinely wired. §6 below documents the as-built ingestion path,
and the taxonomy in §2 has been corrected — most importantly, **`env_params`
cannot supply air temperature**, which the original table wrongly implied.

---

## 🧭 1. Executive Summary: Dual-Mode Ingestion Philosophy

Thermal Sentinel Grid implements an industry-standard, production-grade **Dual-Mode Microclimate Ingestion Architecture**. The system operates across two complementary ingestion pathways:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              DUAL-MODE MICROCLIMATE INGESTION ARCHITECTURE                             │
│                                                                                                        │
│   ┌──────────────────────────────────────────────┐    ┌────────────────────────────────────────────┐   │
│   │       MODE A: LIVE CLOUD API INGESTION       │    │   MODE B: DETERMINISTIC BENCHMARK REPLAY   │   │
│   │       (Async submit-and-poll lifecycle)      │    │   (Zero-latency IEEE standards validation) │   │
│   ├──────────────────────────────────────────────┤    ├────────────────────────────────────────────┤   │
│   │ • Route: POST /api/v1/scan                   │    │ • Route: GET /api/v1/replay/phoenix-2023   │   │
│   │ • Target: api.fortyguard.com/v1/*            │    │ • Source: phoenix_heatwave_2023.json       │   │
│   │ • Purpose: Hyperlocal ad-hoc parcel scanning │    │ • Purpose: Interactive Mission Control     │   │
│   │ • Latency: 3-15 seconds (Cloud Task Worker)  │    │ • Latency: < 10 ms (Sub-second physics ODE)│   │
│   │ • Billing: Real credit deduction (live)      │    │ • Billing: 0 credits (Cached baseline)     │   │
│   └──────────────────────────────────────────────┘    └────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔍 2. Comprehensive System Taxonomy: Live vs. Physics vs. Simulated

To maintain full transparency for hackathon judging and production validation, the entire codebase is categorized into three distinct operational layers:

### 🟢 Layer 1: Live Cloud Integrations (Real External APIs)
These components communicate with real external cloud services and update remote ledgers in real time:

| Component | Endpoint / Service | Live Behavior |
| :--- | :--- | :--- |
| **FortyGuard Quota Hub** | `POST /v1/system/fetch-api-key-usage` | Fetches real-time billing cycles, plan status, and remaining credit balances. |
| **Derived Index Layer** | `POST /v1/env_params` | Returns live 24-point hourly arrays for Heat Index, Apparent Temp, Relative Humidity, Wet Bulb, Cloud Cover and AQI, plus a **daily-aggregate** Clear-Sky $GHI$. ⚠️ **Does not measure air temperature** — the `location.temperature` field echoes back the value supplied in the request (verified: sent `12.345`, received `12.345`). Deducts live credits. |
| **2m Air Temperature** | `POST /v1/heatmap` (`analytic_type: tcm`) | The **only** source of measured 2-meter convective air temperature. One job per forecast hour (`filter_type: 1`). Returns `stats_data.temperature_stats` (min/max/mean) plus per-tile GeoJSON. Deducts live credits. |
| **Persistence & Exceedance** | `POST /v1/heatmap` (`analytic_type: persistence` \| `exceedance`) | Native analytics returning hours above a threshold, in `units: "hour"`, over the AOI (`filter_type: 2`, 00:00–23:00). Flat stats shape — *not* the nested `tcm` shape. Deducts live credits. |
| **Siemens SDC LLM Gateway** | `https://llm.sdc.siemens.cloud/v1` | Routes LangGraph agent reasoning through GPT-5 / Claude Sonnet models when API keys are configured. |

---

### ⚡ Layer 2: Real Physics Solvers (Calculated Live via Differential Equations)
These are **not static mocks or hardcoded tables**. Every value is computed in real time by continuous numerical ODE solvers and IEEE standard equations:

| Physics Engine | Standard / Formulation | Exact Mathematical Implementation |
| :--- | :--- | :--- |
| **Transformer Thermal Dynamics** | **IEEE Std C57.91-2011 Annex G** | 2nd-order non-linear differential equations: $\tau_{TO} \frac{d\Theta_{TO}}{dt} = [\Delta\Theta_{TO,U} - \Delta\Theta_{TO}]$ and $\tau_W \frac{d\Delta\Theta_H}{dt} = [\Delta\Theta_{H,U} - \Delta\Theta_H]$. |
| **Arrhenius Insulation Aging** | **Arrhenius Loss of Life** | Exact Arrhenius aging acceleration factor: $F_{AA} = \exp\left(\frac{15000}{383.15} - \frac{15000}{\Theta_H + 273.15}\right)$ and equivalent aging $F_{EQ} = \frac{1}{T} \int_0^T F_{AA}(t) dt$. |
| **Underground Cable Soil Dryout** | **IEC 60287-2-1** | 3-zone transient soil thermal resistivity solver with critical moisture threshold ($\psi_{\text{crit}}$) and thermal runaway boundary. |
| **AC Power Flow & Voltage Stability** | **4-Bus Forward-Backward Sweep** | Iterative complex radial-feeder power flow calculating active/reactive flow, bus-voltage magnitudes, losses, and OLTC stepping. |
| **Safety Envelope Filter** | **CBF-inspired deterministic validator** | Simulates the bounded-uncertainty trajectory, checks thermal/voltage/BESS/N-1 limits, and uses bisection to find a safe maximum load. The current implementation does not solve a quadratic program. |
| **Avoided Loss Financial Model** | **LBNL ICE Calculator** | Quantifies avoided capital loss ($\text{Asset Value} \times \Delta L$) minus BESS cycling wear and auxiliary fan kWh costs. |

---

### 📦 Layer 3: Simulated, Modeled & Cached Elements

| Item | Source Location | Status | Architectural Justification |
| :--- | :--- | :---: | :--- |
| **Phoenix July 2023 Replay Dataset** | [`src/api/fixtures/phoenix_heatwave_2023.json`](../../src/api/fixtures/phoenix_heatwave_2023.json) | **Cached Fixture** | Pre-ingested benchmark ground truth. Enables sub-10ms scrubbing on the interactive 12-hour replay bar and offline judging tests without burning API credits on every slider tick. Now reached only via an **explicitly labelled** replay path (`data_source: "phoenix_fixture"`), never as a silent fallback masquerading as live data. |
| **Grid-Side Telemetry** | `hourly_forecast[].wind_speed_m_s`, `baseline_load_ratio_k`, `hospital_critical_load_mw`, `bess_soc_pct` | **Modelled** | FortyGuard is an environmental API and exposes no SCADA telemetry. These four fields are modelled from the diurnal load profile and are labelled as modelled in every response. |
| **Utility Substation Assets** | [`src/server/routes/assets.py`](../../src/server/routes/assets.py) | **Synthetic Asset Registry** | 3 representative transformer nameplate profiles (Phoenix TX-04 50 MVA, San Jose Diridon 35 MVA, Las Vegas Strip 60 MVA) parameterized per IEEE standards. |
| **Baseline Grid Load Curve** | [`src/physics/transformer_thermal.py`](../../src/physics/transformer_thermal.py) | **Simulated Profile** | Diurnal load curve ($0.75\,\text{pu}$ morning ramp to $1.18\,\text{pu}$ afternoon peak) modeling desert urban summer air conditioning demand. |
| **Hardware Actuator Signals** | [`src/models/safety.py`](../../src/models/safety.py) | **Simulated Actuation** | Generates schema-validated dispatch commands (`COOLING_STAGE_2`, `BESS_PEAK_SHAVING`, `EV_SMART_CURTAIL`, `FEEDER_TRANSFER`) for software state machines rather than physical substation SCADA RTUs. |

---

### 🧭 Layer 4: Deterministic Portfolio Operations

The Portfolio Ops module consumes the frozen Phoenix environmental profile and the durable grid asset registry to produce a transparent fleet-triage view. It adds no new vendor calls and performs no writes when viewed or recalculated.

| Capability | Route | Contract |
| :--- | :--- | :--- |
| Portfolio ranking | `GET/POST /api/v1/operations/portfolio` | Deterministic 0–100 triage score normalized over available asset evidence; not a failure probability. |
| Worker intervention screen | Included in portfolio response | Explicit wet-bulb, 2m air-temperature, and consecutive-hour thresholds; not OSHA/WBGT certification. |
| Mitigation evidence | Included in portfolio response | SHA-256 content identity over rankings, thresholds, provenance, and limitations. |
| MCP-compatible tools | `GET/POST /api/v1/mcp` | JSON-RPC `initialize`, `tools/list`, and `tools/call` for three read-only deterministic tools. |

The present version uses one common Phoenix scenario boundary across all registry assets. It does not imply that each asset received its own location-specific scan. See [Portfolio Operations, Worker Intervention Screening & MCP](PORTFOLIO_OPERATIONS_AND_MCP.md) for formulas, examples, and verification.

---

## 🏛️ 3. Why the Simulated Elements Must NOT Be Changed

A common question is whether the simulated elements should be connected to "live" feeds. **The engineering answer is an emphatic NO.** Modifying these elements would degrade the system, introduce unneeded fragility, and violate core software engineering principles:

### 1. Phoenix July 2023 Dataset (`phoenix_heatwave_2023.json`)
* **Sub-10ms UI Responsiveness:** Scrubbing the 12-hour replay timeline or adjusting the **What-If Studio** sliders requires instantaneous ODE recalculation ($<10\text{ ms}$). Waiting 30–90 seconds for a cloud API roundtrip on every tick would destroy real-time operator usability.
* **Scientific Ground Truth & IEEE Annex G Reproducibility:** Evaluating transformer hot-spot change ($159.53^\circ\mathrm{C} \to 109.43^\circ\mathrm{C}$) and Arrhenius life extension ($374.3\text{ h saved}$) requires an **immutable, standardized weather boundary condition** that judges and automated test suites (`pytest tests/`) can verify identically every time.
* **Credit Conservation:** Running continuous automated integration tests or live presentations against FortyGuard's billing endpoints on every page reload would rapidly exhaust the 2,000,000 credit quota.

### 2. Utility Substation Assets (`assets.py`)
* Nameplate parameters (50 MVA rating, $\tau_{TO} = 180\text{ min}$, $\tau_W = 4.8\text{ min}$, $R = 5.0$, exponents $m = 0.8, n = 0.8$) are **physical hardware constants from IEEE C57.91-2011 Table 1 / Annex G**.
* In real-world utility Energy Management Systems (EMS), these reside in static asset registries (CIM/GIS databases). Defining standardized profiles for Phoenix, San Jose, and Las Vegas is the industry-standard methodology for digital twins.

### 3. Baseline Grid Load Curve (`transformer_thermal.py`)
* The $0.75\,\text{pu} \to 1.18\,\text{pu}$ diurnal load shape models peak heatwave cooling demand. In a digital twin, using a calibrated diurnal load shape is standard practice to test whether mitigation agents successfully shave peak load ($1.18\,\text{pu} \to 0.98\,\text{pu}$).

### 4. Hardware Actuator Signals (`safety.py`)
* A hackathon software system cannot physically trip real high-voltage $69\,\text{kV}$ substation circuit breakers, discharge physical utility battery banks, or spin physical radiator fans. Emitting structured, schema-validated dispatch payloads with deterministic **model-envelope checks** is the prototype objective for **Track 06 (Agentic AI)** and **Track 02 (Future Buildings & Energy)**.

---

## 📊 4. FortyGuard Billing & Credit Consumption Rules

| Endpoint | Type | Billable? | Credit Behavior |
| :--- | :--- | :--- | :--- |
| `POST /v1/system/fetch-api-key-usage` | System Status | ❌ **Free (0 credits)** | Returns remaining balance & active plan details |
| `POST /v1/system/fetch-api-key-custom-usage` | System Status | ❌ **Free (0 credits)** | Queries historical credit consumption window |
| `POST /v1/heatmap` (`tcm` / `persistence`) | Analysis Engine | ✅ **Billable** | Deducts credits only upon task status = `"succeeded"` |
| `POST /v1/satellite` | Computer Vision | ✅ **Billable** | Deducts credits upon completion |
| `POST /v1/env_params` | Microclimate Index | ✅ **Billable** | Deducts credits upon completion |
| `POST /v1/heat_intelligence` | Synthesis Report | ✅ **Billable** | Deducts credits upon PDF report generation |

---

## 🧪 5. How to Trigger Live API Calls & Verify Credits

### A. Programmatic Credit Verification (Python)
```python
from src.api.fortyguard_client import FortyGuardClient

client = FortyGuardClient()
usage = client.fetch_api_key_usage()
print("Plan:", usage["plan_details"]["plan_type"])
print("Remaining Credits:", usage["credit_summary"]["cycle_remaining_credits"])
print("Credits Used This Cycle:", usage["credit_summary"]["cycle_credits_used"])
```

### B. Live Spatial Scan Execution (cURL)
```bash
# Cloud Deployment:
curl -X POST "https://www.thermal-sentinel-grid.live/api/v1/scan" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "San Jose, CA (Diridon Energy Hub)",
    "latitude": 37.3382,
    "longitude": -121.8863,
    "start_date": "2024-07-15",
    "analytic_type": "tcm",
    "threshold_c": 35.0
  }'

# Or Local Server (http://localhost:8000/api/v1/scan)
```

### C. Live Quickstart Notebooks
Navigate to [`temperature-api-quickstart/notebooks/`](../../temperature-api-quickstart/notebooks) and execute any notebook (e.g. `01_create_heatmap.ipynb`, `02_environmental_parameters.ipynb`) with `REFRESH = True` to run live cloud queries against FortyGuard's infrastructure.

---

## 🔧 6. As-Built Live Ingestion Path

### A. Request topology per scan

```
                        ┌──────────────────────────────────────────┐
                        │  get_12h_forecast(lat, lon)              │
                        └────────────────────┬─────────────────────┘
                                             │
              ① uncontended, first           │
        ┌────────────────────────────────────▼─────────────────────────────────┐
        │  POST /v1/env_params   filter_type 3   (~5 s)                        │
        │  → hourly RH, wet-bulb, heat index, cloud cover; daily GHI           │
        │  Runs ALONE: batched behind ② it starved >600 s in 'processing'.     │
        └────────────────────────────────────┬─────────────────────────────────┘
                                             │
              ② bounded fan-out              │  asyncio.Semaphore(6)
        ┌────────────────────────────────────▼─────────────────────────────────┐
        │  POST /v1/heatmap  analytic_type=tcm  filter_type 1   × 12 hours     │
        │  → measured 2m air temperature, hours 06:00–17:00     (~90 s cold)   │
        └────────────────────────────────────┬─────────────────────────────────┘
                                             │
        ┌────────────────────────────────────▼─────────────────────────────────┐
        │  POST /v1/heatmap  persistence + exceedance  filter_type 2 (~21 s)   │
        │  → P₄₀ (units: hour); H₄₀ integrated from the measured 2m curve      │
        └──────────────────────────────────────────────────────────────────────┘
```

Every response is memoised by deterministic MD5 request identity in the durable
`api_call_cache` (Supabase-backed), so a repeat scan of the same AOI/date costs
**0 credits** and returns in **~1.2 s** instead of ~90 s. The same table also
stores complete deterministic simulation payloads under a `sim:` SHA-256
identity. Those solve records have no expiry: identical coordinates, catalog
date, city, and physics parameters replay the prior trajectory across serverless
cold starts instead of recomputing and discarding it.

### B. Persisted scan → persisted solve lifecycle

`POST /api/v1/scan` writes the measured parcel to
`microclimate_parcel_store`. Its GeoJSON properties carry `city`,
`analysis_date`, coordinates, measured peak, persistence and provenance, so the
record remains re-runnable without changing the existing Supabase schema.
`GET /api/v1/scan/parcels` exposes those rows newest-first in the Cloud DB
**Saved Scans** tab. Choosing **Use for calculations** posts the stored
coordinates/date to `/api/v1/sandbox/simulate` and rebases the dashboard.

The sandbox result is itself persisted as a complete payload in
`api_call_cache`, keyed as `sim:` plus a SHA-256 digest of every request field.
`simulation_runs` remains the compact scalar audit table; it is not sufficient
to reconstruct the timeline. Solve entries have `expires_at = NULL` because the
physics is deterministic for identical inputs. A repeat request therefore
returns the stored trajectory and carries `cache.hit=true`; the dashboard marks
it **REPLAYED FROM STORE**. Supabase is authoritative in production, while local
SQLite is only a warm/offline fallback and is ephemeral on Vercel.

Rows written before GeoJSON properties were introduced were repaired from
stored evidence rather than guessed or deleted: a backfill matched each parcel's
coordinates and measured peak to a unique full 12-hour group in
`api_call_cache`, tagged the result `backfilled_from: api_call_cache`, and left
all measured columns untouched.

The canonical `GET /api/v1/replay/phoenix-2023` is intentionally outside this
write lifecycle. Viewing a fixed replay does not create a new measurement or
operator decision, so the route neither appends its 12 modelled telemetry steps
nor persists a fresh safety certificate. Cache retrieval selects only
`response_payload`; database-health counts use exact PostgREST count headers and
primary-key projections rather than selecting JSON-heavy rows. See
[Database Query Performance & Replay Persistence](DATABASE_QUERY_PERFORMANCE.md)
for the query-report analysis and verification procedure.

### C. Why the hour loop exists

There is **no time-series endpoint** in the OpenAPI surface — the paths are
`/v1/heatmap`, `/v1/satellite`, `/v1/streetview`, `/v1/heat_intelligence`,
`/v1/env_params`, `/v1/status/{id}` and two usage endpoints. An hourly 2m
temperature curve must therefore be assembled from **N single-hour `tcm` calls**.
This is the single largest cost and latency driver in the system, and the reason
caching is not optional.

### D. Field provenance

Scope: this is the **ingestion schema** — the per-hour record assembled from the
API and frozen into `src/api/fixtures/phoenix_heatwave_2023.json`. The replay
response projects a subset of it into `timeline_steps`; fields such as
`relative_humidity_pct`, `wet_bulb_temp_c`, `heat_index_c`, `cloud_cover_pct`
and `tile_peak_2m_c` live in the fixture and the gold dataset rather than in
that projection.

| Field | Source | Kind |
| :--- | :--- | :--- |
| `fortyguard_2m_ambient_c` | `tcm` `temperature_stats.mean` | 🟢 Measured |
| `tile_peak_2m_c` | `tcm` `temperature_stats.maximum` | 🟢 Measured |
| `coolest_tile_2m_c` | `tcm` `temperature_stats.minimum` | 🟢 Measured — coolest tile in the AOI |
| `intra_aoi_spread_c` | `mean − min` within AOI | 🟡 Derived (small; see §7) |
| `relative_humidity_pct`, `wet_bulb_temp_c`, `heat_index_c`, `cloud_cover_pct` | `env_params` hourly arrays | 🟢 Measured |
| `solar_irradiance_w_m2` | daily GHI × solar-geometry shape × cloud attenuation | 🟡 Modelled magnitude, measured attenuation |
| `persistence_hours_p40` | `persistence` analytic | 🟢 Measured |
| `exceedance_degree_hours_h40` | integrated from measured 2m curve | 🟢 Derived from measured |
| `wind_speed_m_s`, `baseline_load_ratio_k`, `hospital_critical_load_mw`, `bess_soc_pct` | diurnal load model | 🔴 Modelled |

> **Why `coolest_tile_2m_c` and not an airport reference:** these fields were
> once named `airport_reference_temp_c` and `microclimate_delta_c`, which
> implied a comparison we never actually made. The series is the AOI's coolest
> **tile**. We measured Sky Harbor directly and it came back *warmer* than
> downtown (42.78 vs 42.74 °C) — an airport ringed by runways is itself a heat
> island. The fields were renamed to describe what is measured, and the spread
> they express is small: **+0.06 °C mean, +0.19 °C max**, a *negligible* effect
> size (Cohen's d = 0.024). The damage in this scenario comes from **duration**,
> not spatial gradient.

### E. Provenance contract

| `data_source` | Meaning |
| :--- | :--- |
| `fortyguard_live` | 2m temperature, persistence, exceedance and hourly humidity all live. |
| `fortyguard_live_partial` | Live 2m temperature and persistence; `env_params` unavailable, humidity/solar from benchmark. |
| `phoenix_fixture` | Fully offline labelled replay. |

Provenance is decided by **response content** (presence of the `locations` key),
not by the absence of an exception — the client wrapper returns a fixture on
failure, so a well-formed dict does not imply live data.

### F. Configuration

| Variable | Default | Purpose |
| :--- | :--- | :--- |
| `FORTYGUARD_ANALYSIS_DATE` | `2023-07-19` | Pinned reproducible benchmark date inside the supported window. |
| `FORTYGUARD_MAX_CONCURRENCY` | `6` | Semaphore bound on heatmap fan-out. |
| `FORTYGUARD_ENV_TIMEOUT_S` | `180` | Poll deadline for `env_params`. |
| `MOCK_FORTYGUARD_API` | `false` | Forces labelled fixture mode (used by the test suite). |

---

## 📈 7. Verified Live Results

End-to-end through the deployed agent, benchmark date `2023-07-19`:

| City | Peak 2m | $P_{40}$ | $H_{40}$ | TSI |
| :--- | ---: | ---: | ---: | ---: |
| Phoenix, AZ | 42.74 °C | 12.00 h | 17.48 °C·h | 3.68 |
| Seattle, WA | 30.41 °C | **0.00 h** | 0.00 °C·h | 0.00 |

Seattle correctly reports **zero** hours above 40 °C. Under the previous
synthetic path both cities returned Phoenix's 47.6 °C, because persistence was a
function of distance from Phoenix rather than of weather. This divergence is the
clearest single proof that the ingestion path is live.

Two honest caveats, also recorded in `SUBMISSION.md`:

- $P_{40} = 12.0\,\text{h}$ is the **full width of the sampling window**
  (06:00–17:00). The temperature stayed above 40 °C for every sampled hour, so
  the metric is bounded by our window, not by the weather.
- The measured land-cover delta is $+1.14\,^\circ\mathrm{C}$ (downtown 42.74 vs
  South Mountain natural desert 41.60), **not** the $+4.5\,^\circ\mathrm{C}$
  originally assumed.

---

### G. 72-hour capture and replay

The multi-day endpoint does not invent a sinusoidal weather curve and does not
issue 75 paid jobs on every page load. `scripts/regenerate_phoenix_72h_fixture.py`
requests all 24 `tcm` hours plus `env_params` for each of July 24–26, validates
an exact 00:00–23:00 sequence and live provenance, then freezes the 72 rows in
`src/api/fixtures/phoenix_heatwave_2023_72h.json`. Daily measured 2m peaks are
**42.44 / 42.76 / 42.52 °C** and minima are **35.33 / 35.13 / 33.43 °C**.
Temperature, humidity, wet bulb and cloud cover are measured; solar is derived
from live GHI/cloud plus geometry; load, soil, transformer and dispatch state
are modelled. The replay API returns this distinction under
`scenario_metadata.provenance`.

## 🧾 8. Regression Guards

The failure mode here was not a crash — it was a system that looked healthy
while serving synthetic data. Guards now in place:

1. **Provenance on every response.** No caller can consume a metric without
   being able to see where it came from.
2. **Cross-city divergence check.** Phoenix and Seattle must not return
   identical temperatures; identical output means the synthetic path is back.
3. **No hardcoded physics constants.** `simulate_trajectory()` previously pinned
   `p_40 = 7.17` / `h_40 = 34.25` internally, overriding the live layer even
   when it was working. These are now parameters.
4. **No fixed-length forecast assumptions.** `forecast[7]` assumed the fixture's
   12-entry shape and raised `IndexError` on shorter live series. Consumers now
   resolve the peak hour by search.
5. **Hermetic tests.** `tests/conftest.py` forces `MOCK_FORTYGUARD_API=true` and
   blanks Supabase credentials, so the suite exercises our own physics and
   persistence logic deterministically and never bills credits.
