# Ground-Truth Validation Contract

## Status

Implemented. This document is the production acceptance contract for external thermal evidence.

## Current Phoenix replay result

After correcting the Phoenix local-time labels to UTC, the deterministic PHX comparison has 12/12 aligned hours, Pearson $r=0.9609$, RMSE $=3.0877^\circ$C, and mean $\Delta T=-2.1162^\circ$C. Thus the curves track the same diurnal progression, but PHX airport is warmer on average in this window. The result does **not** verify a positive UHI signal; it demonstrates honest external validation and rejects the desired hypothesis when the evidence does not support it.

## Evidence products

1. **Air validation** compares FortyGuard `fortyguard_2m_ambient_c` with hourly `temperature_2m_c`.
   - Primary: IEM-republished ASOS/AWOS physical station observations.
   - Fallback: Open-Meteo historical gridded meteorology.
2. **Surface context** discovers Landsat Collection 2 Level-2 surface-temperature scenes.
   - It is labelled `satellite surface temperature (not 2 m air)`.
   - It cannot enter transformer/BESS ambient-air fields or air-temperature MAE.
3. **Parcel ground truth** requires future co-located, calibrated field sensors. Neither an airport station nor satellite LST proves parcel accuracy.

## Selection and failure policy

- `source=auto`: try IEM, then explicitly report Open-Meteo fallback and the IEM failure.
- `source=iem`: fail closed if station evidence is unavailable.
- `source=open-meteo`: use only gridded evidence.
- Missing values are excluded, never imputed.
- Duplicate timestamps and insufficient aligned pairs fail validation.
- Accepted reports require at least the configured pair count (six by default) and 80% baseline timestamp coverage.
- Gaps are not interpolated; therefore no gap, including one longer than an hour, can be silently bridged.
- Public responses are cache-first and cost zero FortyGuard credits.
- Retries are bounded, honor `Retry-After`, and apply exponential backoff with jitter.

## Provenance

Every report includes provider, evidence class, source-selection decision, exact UTC alignment, retrieval/cache state, and—where available—station coordinates and AOI separation. FortyGuard heatmap request hours are local civil time; the Phoenix fixture and newly generated live profiles retain an explicit ISO-8601 MST offset (UTC−07:00) from `env_params.metadata.timezone_offset_hours`. Comparison code canonicalizes offset-aware timestamps to UTC before any join. Open-Meteo requests pin the ERA5-Land model and report returned grid metadata. Landsat reports native thermal resolution separately from its output grid.

## Metrics

Air reports include aligned count, coverage, MAE, RMSE, bias, peak delta, Pearson and Spearman correlation, paired values, and threshold exposure at 35/40/45 °C: exceedance hours, longest persistence run, and degree-hours. A positive FortyGuard-minus-station ΔT is reported as an **urban–station anomaly**, not proof of UHI. A causal UHI conclusion requires a verified same-time urban/rural reference design (or defensible representative multi-station baseline); PHX is itself an urban airport. Multi-station reports preserve each station independently and summarize median error, minimum coverage, and station peak spread; they are a sparse metro envelope, not a synthetic parcel observation.

Solar uses NLR NSRDB when `NREL_API_KEY` and `NREL_EMAIL` are configured, with Open-Meteo as the no-key modeled fallback. Both are typed as modeled/gridded evidence rather than pyranometer observations.

## Persistence

Live validation runs receive a deterministic SHA-256 identity over baseline, reference, and configuration. Reports are stored in `validation_runs` and listed at `GET /api/v1/db/validation-runs`. Historical API evidence remains cached separately. Existing Supabase projects must apply `docs/supabase_validation_migration.sql`; local SQLite creates the table automatically.

## Configuration

IEM and Open-Meteo need no credentials. Optional provider variables are:

| Variable | Purpose |
| :--- | :--- |
| `NREL_API_KEY`, `NREL_EMAIL` | NLR NSRDB GOES Aggregated PSM v4 download API. The historical variable names are retained for compatibility. |
| `SYNOPTIC_TOKEN` | Preferred Synoptic generated access token for the multi-provider CLI. |
| `SYNOPTIC_API_KEY` | Compatibility fallback for tooling that already supplies a usable token under this name; an account key may require exchange first. |
| `EIA_API_KEY` | EIA-930 balancing-authority demand context in the multi-provider CLI. |
| `RUN_LIVE_GROUND_TRUTH_TESTS=1` | Enables the three network-dependent pytest checks marked `live`. |

Secrets are never part of NSRDB cache identities or persisted request metadata.

## Endpoints

- `POST /api/v1/validation/air-temperature` (arbitrary capture/AOI/date)
- `POST /api/v1/validation/field-sensor` (calibrated co-located observations)
- `GET /api/v1/validation/phoenix-2023`
- `GET /api/v1/validation/metro/phoenix` (frozen three-station envelope by default; `source=live` refreshes IEM)
- `GET /api/v1/benchmark/ground-truth-comparison` (deterministic replay by default)
- `GET /api/v1/validation/surface-context/landsat` (`summarize_first=true` signs and reads the first scene COG)
- `GET /api/v1/db/validation-runs`

The benchmark route defaults to `source=replay`; `source=iem` refreshes physical
station evidence, `source=open-meteo` forces gridded evidence, and `source=auto`
tries IEM before an explicit fallback. The metro route defaults to frozen
Phoenix PHX/DVT/IWA replay and accepts `source=live` for a fresh envelope.

### General air-temperature request

```json
{
  "scenario_id": "phoenix_custom_capture",
  "latitude": 33.4484,
  "longitude": -112.074,
  "start_date": "2023-07-19",
  "end_date": "2023-07-19",
  "station": "PHX",
  "source": "auto",
  "minimum_pairs": 6,
  "baseline": [
    {
      "timestamp": "2023-07-19T06:00:00-07:00",
      "fortyguard_2m_ambient_c": 36.1,
      "solar_irradiance_w_m2": 0.0
    }
  ]
}
```

`baseline` timestamps must be timezone-aware. The field-sensor route accepts the
same baseline plus a `sensor` object containing `sensor_id`, coordinates,
measurement `height_m` (1.25–2.25 m), calibration reference/date, and a `series`
of UTC or offset-aware `temperature_2m_c` observations.

## Command-line workflows

```bash
# Deterministic station comparison suitable for CI/demos
curl http://localhost:8000/api/v1/benchmark/ground-truth-comparison

# Cache-first physical station or three-station metro validation
python scripts/validate_ground_truth.py --source iem --station PHX
python scripts/validate_ground_truth.py --source iem-metro --metro phoenix

# No-network, labelled multi-provider report plus IEEE thermal solve
python scripts/fetch_ground_truth_comparison.py --offline \
  --start 2024-07-01 --end 2024-07-02 \
  --output data/ground_truth_comparison.json

# Post-deployment route verification; --live additionally calls IEM
python scripts/deployment_smoke_test.py https://www.thermal-sentinel-grid.live
```

The multi-provider CLI uses labelled deterministic mock inputs unless `--strict`
is supplied; `--offline` makes no network calls. Strict mode records optional
provider failures without substituting mocks and continues only if usable
weather and load alternatives remain. Regional EIA/CAISO demand is normalized
as a scenario shape and is never divided by transformer nameplate unless the
input is explicitly classified as `asset_scada`.

## Acceptance gates

- Nearby stations are ranked by valid hourly coverage and then distance; physical station evidence is preferred automatically.
- Fallback evidence is visible and typed.
- LST cannot be returned as `temperature_2m_c`.
- Station separation is disclosed when coordinates exist.
- Historical runs are reproducible from durable cache/replay.
- Positive ΔT against one airport never sets `urban_heat_island.verified=true`.
- Provider failures do not silently change evidence class.
- Unit, route, persistence, parser, and scientific-metric tests pass.
