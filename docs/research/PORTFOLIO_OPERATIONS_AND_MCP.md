# Portfolio Operations, Worker Intervention Screening & MCP

> **Status:** Implemented and production-verified  
> **Production UI:** [Thermal Sentinel Grid](https://www.thermal-sentinel-grid.live) → **Portfolio Ops**  
> **Implementation:** [`src/operations/portfolio.py`](../../src/operations/portfolio.py), [`src/server/routes/operations.py`](../../src/server/routes/operations.py), and [`frontend/src/components/PortfolioOperationsViewer.tsx`](../../frontend/src/components/PortfolioOperationsViewer.tsx)

## 1. Purpose

The Portfolio Operations module extends the canonical single-scenario replay into a fleet-triage workflow. It combines:

1. a common environmental stress scenario;
2. available asset-registry evidence;
3. an explicit worker-intervention screen; and
4. content-addressed decision evidence.

The module is read-only. It does not dispatch equipment, write safety certificates, or create database records merely because an operator views or recalculates the screen.

## 2. Data boundaries and provenance

### Environmental evidence

The current production implementation loads `src/api/fixtures/phoenix_heatwave_2023.json`, a frozen capture generated from live FortyGuard requests for downtown Phoenix on `2023-07-19`. The worker screen uses:

- `fortyguard_2m_ambient_c` — measured 2m air temperature from FortyGuard `tcm` heatmaps;
- `wet_bulb_temp_c` — returned by FortyGuard `env_params`;
- timestamps and per-row source labels from the capture.

### Asset evidence

Portfolio rows come from the durable `grid_assets_registry` when Supabase is available and from the local registry fallback otherwise. The ranking consumes only fields present on each row:

- `current_health_score`;
- `criticality_tier`;
- `current_load_percentage`, when available;
- `max_safe_ambient_temp_c`, when available, otherwise the documented 40°C screening default.

Missing load or health fields are not replaced with plausible values. Instead, the score is normalized over available components and exposes `available_score_weight` as evidence coverage.

### Scope limitation

The current snapshot applies **one common Phoenix scenario boundary to every registered asset**. It demonstrates portfolio prioritization under a shared stress case; it is not a location-specific FortyGuard scan for every asset. A future portfolio scan can replace the common boundary with per-asset cached profiles without changing the ranking contract.

## 3. Transparent portfolio score

`portfolio_rank_v1` is a deterministic triage score from 0 to 100. It is **not a calibrated probability of failure**.

| Component | Maximum weight | Calculation |
| :--- | ---: | :--- |
| Environmental exceedance | 35 | `min(35, max(0, peak_2m − safe_ambient) × 8.75)` |
| Asset loading | 30 | `min(30, max(0, load_pct − 60) × 0.75)` when load is available |
| Asset health | 20 | `min(20, max(0, 100 − health_score) × 0.4)` when health is available |
| Criticality | 15 | Tier 1 = 15, Tier 2 = 9, Tier 3 = 4 |

The final value is:

```text
risk_score = 100 × sum(available component points)
                   / sum(available component weights)
```

Ties are resolved by stable asset ID ordering. Risk labels are `watch` (<25), `elevated` (25–49.9), `high` (50–69.9), and `critical` (≥70).

## 4. Worker intervention screen

`threshold_screen_v1` finds contiguous hourly observations where both conditions hold:

```text
wet_bulb_temp_c <= configured maximum wet bulb
fortyguard_2m_ambient_c <= configured maximum 2m air temperature
```

A sequence is returned only when it meets `min_consecutive_hours`. Defaults are:

- maximum wet bulb: `23°C`;
- maximum 2m air temperature: `40°C`;
- minimum duration: `2` sampled hours.

For the canonical capture, the default candidate window is `06:00–09:00 UTC`, comprising four hourly observations. With `22°C / 39°C / 2h`, it narrows to `06:00–08:00 UTC`.

### Safety disclaimer

This is a **candidate operational screen**, not an occupational-safety certification. It does not calculate compliant WBGT because the available capture lacks globe temperature. It also does not model workload, clothing, acclimatization, hydration, medical status, or jurisdiction-specific work/rest rules. A qualified safety program must evaluate those factors before field deployment.

## 5. Auditable mitigation evidence

The service constructs a canonical JSON body containing:

- schema and decision type;
- scenario and analysis date;
- full ranked portfolio;
- complete worker-screen result and thresholds;
- environmental, asset, and calculation provenance;
- the common-boundary scope limitation.

It serializes the body with sorted keys and compact separators, then calculates SHA-256. The API returns:

- `evidence_id`: the first 16 uppercase hexadecimal characters prefixed by `EVIDENCE-`;
- `sha256`: the full digest;
- `generated_at`: response-generation time, excluded from the digest;
- `immutable_input_digest: true`;
- `read_only: true`.

Therefore, identical evidence inputs produce the same identity even when requested at different times. Changing a threshold changes the evidence identity.

The dashboard can download the evidence payload as JSON.

## 6. REST API

### Default snapshot

```bash
curl https://www.thermal-sentinel-grid.live/api/v1/operations/portfolio
```

### Custom thresholds

```bash
curl -X POST https://www.thermal-sentinel-grid.live/api/v1/operations/portfolio \
  -H 'Content-Type: application/json' \
  -d '{
    "max_wet_bulb_c": 22.0,
    "max_air_temp_c": 39.0,
    "min_consecutive_hours": 2
  }'
```

Request bounds are enforced by Pydantic:

- wet bulb: `0–40°C`;
- 2m air temperature: `−20–60°C`;
- consecutive hours: `1–12`.

## 7. MCP-compatible tool interface

The HTTP endpoint implements the MCP JSON-RPC tool subset needed by this application. It is described as **MCP-compatible**, not as a complete implementation of every MCP transport or capability.

### Discovery

```bash
curl https://www.thermal-sentinel-grid.live/api/v1/mcp
```

### List tools

```bash
curl -X POST https://www.thermal-sentinel-grid.live/api/v1/mcp \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

### Call evidence tool

```bash
curl -X POST https://www.thermal-sentinel-grid.live/api/v1/mcp \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc":"2.0",
    "id":2,
    "method":"tools/call",
    "params":{
      "name":"get_mitigation_evidence",
      "arguments":{
        "max_wet_bulb_c":22.0,
        "max_air_temp_c":39.0,
        "min_consecutive_hours":2
      }
    }
  }'
```

Available tools:

| Tool | Output |
| :--- | :--- |
| `rank_portfolio_risk` | Ranked asset portfolio and score evidence. |
| `find_worker_intervention_windows` | Candidate windows, thresholds, hourly decisions, and limitations. |
| `get_mitigation_evidence` | Complete content-addressed evidence snapshot. |

The web UI and MCP tools call the same `_operations_snapshot()` service. They do not maintain separate formulas.

## 8. Verification

Automated coverage is in [`tests/test_portfolio_operations.py`](../../tests/test_portfolio_operations.py). It verifies:

- measured fields are used by the screen;
- no WBGT/occupational certification is claimed;
- ranking and tie-breaking are deterministic;
- evidence hashes remain stable across generation times;
- REST and MCP return the same evidence identity;
- custom thresholds alter both the candidate window and evidence identity;
- absent asset load values remain `null`.

Production verification on both the custom domain and Vercel alias confirmed:

- HTTP 200 for default and custom REST requests;
- six durable registry assets ranked;
- matching REST/MCP evidence IDs;
- visible threshold controls, evidence export, and MCP-copy action;
- no browser runtime errors.
