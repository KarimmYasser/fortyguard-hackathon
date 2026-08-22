# Field Notes — Observed API Behaviour During Live Integration

> **Status:** Empirical. Everything here was measured against `api.fortyguard.com`
> while wiring Thermal Sentinel Grid's agent onto the live API, not read out of
> the vendor documentation.
>
> These notes exist because several of them contradict what the field names and
> the official docs imply. Each one cost us a debugging cycle, and two of them
> were silently corrupting our output.

---

## 1. `env_params` does not measure air temperature — it echoes yours back

`POST /v1/env_params` accepts a `location.temperature` value. The response
contains a `location.temperature` field. **They are the same number.** The API
returns whatever you sent it.

Probe:

```jsonc
// request
{ "locations": [ { "latitude": 33.4484, "longitude": -112.0740, "temperature": 12.345 } ] }

// response
{ "locations": [ { "temperature": 12.345, ... } ] }   // <- our own input, unchanged
```

`12.345 °C` in downtown Phoenix in July is physically absurd, and the API
accepted and returned it without complaint.

### Why this matters

`env_params` is an *index* endpoint. It derives comfort and exposure indices
**from a boundary temperature you supply**. It is not a measurement source. The
hourly arrays it returns are genuinely useful and genuinely computed:

| Field | Real? | Notes |
| :--- | :---: | :--- |
| `heat_index_celsius` | ✅ | 24-point hourly array |
| `apparent_temperature_celsius` | ✅ | 24-point hourly array |
| `relative_humidity_percent` | ✅ | 24-point hourly array |
| `wet_bulb_temperature_celsius` | ✅ | 24-point hourly array |
| `cloud_cover_octas` | ✅ | 24-point hourly array — **but see §2** |
| `air_quality_index` | ✅ | |
| `solar_irradiance.clear_sky.ghi` | ✅ | **daily aggregate**, not hourly |
| `location.temperature` | ❌ | echo of the request |

**Measured 2m air temperature is only available from `POST /v1/heatmap` with
`analytic_type: "tcm"`.** If you need real air temperature, that is the only
endpoint that provides it. We had to restructure our whole ingestion path around
this.

---

## 2. `cloud_cover_octas` is reported 0–100, not 0–8

The name says octas. Octas are eighths — the scale caps at 8. The API returns
values up to **100.0**:

```
[2.0, 1.0, 5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
 5.0, 10.0, 24.0, 21.0, 11.0, 2.0, 25.0, 13.0, 3.0, 14.0, 100.0, 100.0]
```

It is a **percentage**.

This is a nasty one because low values are ambiguous — `5.0` is a plausible
reading on either scale, so the bug hides until the sky clouds over. We used it
as octas in a clear-sky attenuation term:

```python
attenuation = 1.0 - 0.75 * (cloud / 8.0)
```

At `cloud = 100`, that evaluates to `-8.375`, and we emitted **negative solar
irradiance** (`-1014 W/m²`) in the middle of the afternoon. Normalise by 100 and
clamp the result:

```python
cloud_fraction = min(max(cloud_raw / 100.0, 0.0), 1.0)
attenuation    = max(0.15, 1.0 - 0.75 * cloud_fraction)
```

---

## 3. "Today" is usually outside the supported window

The documented range is `2019-01-01` → `now + 12h`. In practice this bites
harder than it reads:

- Anything past `now + 12h` is rejected with `400`.
- The archive lags real time, so even *recent* dates can fail.
- **If your host clock is wrong, every live call fails.** Our dev machine's
  clock read 2026; every request was silently out of range and every call fell
  back to a bundled fixture. The system looked like it was working.

Clamp dates into the window explicitly, and pin a known-good benchmark date
rather than defaulting to `date.today()`:

```python
_HISTORICAL_LOWER_BOUND = date(2019, 1, 1)
BENCHMARK_ANALYSIS_DATE = "2023-07-19"
```

---

## 4. Work appears to be serialised per API key — don't fan out blindly

Launching 12 `heatmap` jobs concurrently alongside one `env_params` job caused
the `env_params` activity to sit in `processing` for **over 600 seconds** and
blow its deadline. The exact same `env_params` request completes in **~5s** when
issued on its own.

The heatmap jobs themselves ran fine concurrently — two finished together in
~21s, four in ~32s. The problem was the small job stuck behind the large batch.

Two mitigations, both worth applying:

1. **Issue latency-sensitive calls first and uncontended**, before opening the batch.
2. **Bound fan-out with a semaphore** (we use 6) instead of an unbounded `gather`.

```python
semaphore = asyncio.Semaphore(6)

async def one_hour(hour):
    async with semaphore:
        return await run_heatmap(payload_for(hour))
```

---

## 5. Observed latencies

Measured on the Basic plan, ~1.9 mi² AOI, granularity 100m:

| Call | Cold latency |
| :--- | :--- |
| `env_params`, `filter_type: 3` (uncontended) | ~5 s |
| `heatmap` `tcm`, `filter_type: 1` (single hour) | ~20 s |
| `heatmap` `persistence` + `exceedance` concurrently | ~21 s |
| Full 12-hour forecast scan (12 × `tcm`, semaphore 6) | ~90 s |
| Same scan, served from cache | ~1.2 s |

**Cache aggressively.** A 12-hour scan is ~90s and ~18 credits cold; memoised by
request hash it is ~1.2s and free. This also matters for serverless deployment —
90s exceeds the default function timeout on most platforms.

---

## 6. `persistence` / `exceedance` return a different stats shape than `tcm`

Easy to miss when writing one parser for both.

`analytic_type: "tcm"` nests its statistics:

```jsonc
{ "stats_data": { "temperature_stats": { "minimum": ..., "maximum": ..., "mean": ... } } }
```

`analytic_type: "persistence"` / `"exceedance"` are flat, and carry `units`:

```jsonc
{ "activity_id": "...", "analytic_type": "persistence", "units": "hour",
  "n_cells": 497, "min": ..., "max": ..., "mean": 8.0 }
```

Per-tile values live in `map_data.features[].properties = { tile_id, value }`.

Also note: `overall_temperature_distribution` is a **5-point quantile summary**,
not one entry per cell. Use `n_cells` for the actual tile count.

---

## 7. Spatial contrast at 100m granularity is smaller than expected

We had assumed a `+4.5 °C` urban-vs-reference microclimate delta. The API does
not support that at this granularity. Measured, all at 15:00 on 2023-07-19:

| Location | Mean 2m (°C) |
| :--- | ---: |
| Downtown core | 42.74 |
| Industrial west Phoenix | 42.73 |
| Encanto Park (green space) | 42.71 |
| **Sky Harbor airport** | **42.78** |
| **South Mountain (natural desert)** | **41.60** |

Two findings worth internalising:

- **Intra-AOI spread is tiny.** A ~1.9 mi² downtown AOI spans only `0.06 °C`
  min-to-max; widening to ~7.7 mi² only reaches `0.31 °C`. Taking the AOI
  minimum as a "cool reference" yields a near-zero delta.
- **An airport is not a cool reference.** Sky Harbor came back *warmer* than
  downtown. It is ringed by asphalt runways — it is itself a heat island. The
  common "distant airport station under-reads urban heat" framing did not hold
  here.

The real, defensible contrast is **urban core vs natural land cover**:
`42.74 − 41.60 = +1.14 °C`. Smaller than the folklore figure, but measured.

---

## 8. AOI must be a closed ring

`polygon_aoi` must be a GeoJSON `FeatureCollection` whose polygon's first and
last coordinate are **identical**. An unclosed ring is rejected. Granularity must
be exactly `60`, `80`, or `100`.

```python
def build_aoi(lat, lon, d=0.011):
    ring = [[lon-d, lat-d], [lon+d, lat-d], [lon+d, lat+d], [lon-d, lat+d], [lon-d, lat-d]]
    return {"type": "FeatureCollection", "features": [
        {"type": "Feature", "properties": {},
         "geometry": {"type": "Polygon", "coordinates": [ring]}}]}
```

---

## 9. Failure-handling advice: don't let a fallback look like a success

Our own bug, but it generalises. Our `environmental_parameters()` wrapper caught
its own exceptions and returned the offline fixture. Callers therefore received
a well-formed dict on failure and could not distinguish live data from fallback
— so the system reported healthy while serving synthetic numbers.

Two rules we now follow:

- **Decide provenance from response content, not from the absence of an
  exception.** We check for the `locations` key, which only a real response has.
- **Propagate provenance to the caller.** Every response carries
  `data_source: "fortyguard_live" | "fortyguard_live_partial" | "phoenix_fixture"`.

A `mock_mode: false` health flag only reports *configuration*. It does not tell
you whether the last response actually came from the API.

---

## Summary table

| # | Finding | Impact if missed |
| :--- | :--- | :--- |
| 1 | `env_params.temperature` echoes your input | Silent fabricated temperatures |
| 2 | `cloud_cover_octas` is 0–100 percent | Negative solar irradiance |
| 3 | `today` often out of range; clock skew kills calls | Silent fixture fallback |
| 4 | Work serialises per key | 600s timeouts on small calls |
| 5 | 12h scan ≈ 90s cold | Serverless timeout |
| 6 | Two different stats shapes | Parser returns `None` |
| 7 | Spatial contrast ≈ 1 °C, airports are hot | Overstated claims |
| 8 | AOI ring must be closed | `400 Bad Request` |
| 9 | Fallbacks that mimic success | Undetectable synthetic data |

## Finding 10 — replay and the live agent disagreed on identical inputs

Comparing `GET /api/v1/replay/phoenix-2023` against `POST
/api/v1/dispatch/run-mitigation` for the same pinned date showed matching
ambient, persistence and solar series but a ~1.3 % gap in net avoided loss.
Three separate causes, all in our own code rather than the API:

1. `phoenix_heatwave_replay.py` computed the urban-canyon derate from a
   hardcoded `47.6 °C` — the superseded synthetic peak — while the live path
   resolved the real hottest hour (42.74 °C).
2. The replay never forwarded `persistence_hours_p40` /
   `exceedance_degree_hours_h40` into `simulate_trajectory`, so it silently fell
   back to the retired `7.17 h` / `34.25 °C·h` literals.
3. `physics_node` and the replay disagreed on wind and solar for the derate:
   one used the signature defaults (3.0 m/s, 850 W/m²), the other the captured
   series.

A fourth, unrelated defect surfaced while tracing it: `multi_day_heatwave.py`
called `calculate_cooling_derate_factor(45.0, 980.0)` positionally, placing a
solar-irradiance figure into `reference_wind_speed_m_s` and modelling a 980 m/s
wind — roughly Mach 3 — which grossly over-estimated convective heat rejection.

Both paths now derive the derate from the peak hour of the capture and forward
the measured persistence metrics. The baseline trajectory is byte-identical
across replay and live dispatch (peak hot-spot 159.53 °C, top-oil 128.26 °C,
loss-of-life 377.77 h). The mitigated trajectories still differ, correctly:
replay applies a scripted BESS shave, while the live path applies the actions
admitted by the deterministic safety-envelope gate.

**This lowered the headline figures.** Net avoided loss moved from $2,736,106 to
$2,576,849 and ROI from 5,834.9× to 5,495.3×, because the inflated 47.6 °C
ambient and the stale persistence literals had been overstating baseline
degradation. The corrected numbers are the ones now reproducible from the API.
