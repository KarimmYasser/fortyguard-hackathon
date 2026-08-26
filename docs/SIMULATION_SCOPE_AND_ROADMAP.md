# Simulation Scope, Evidence Contract, and Deployment Roadmap

## Current operating modes

1. **Demo** — frozen FortyGuard environmental capture plus assumed grid/asset inputs.
2. **Hybrid** — live FortyGuard boundary plus assumed or operator-supplied grid inputs.
3. **Operational** — reserved for a future deployment with authenticated SCADA and calibrated field sensors. The current application does not claim this mode.

Every replay and sandbox result includes a `provenance` object that identifies measured, externally modelled, derived, assumed, simulated, and unvalidated fields.

## What is measured

Depending on the response provenance, FortyGuard supplies or previously supplied the 2 m air-temperature raster, AOI spatial temperatures, humidity, wet bulb, and cloud cover. Persistence and exceedance are calculated from the environmental series. Solar may be derived or externally modelled; wind is an explicit assumption because the current REST endpoint does not expose it.

## What is simulated

Transformer top-oil/hot-spot temperature and aging, canyon cooling derate, soil/cable state, paper-oil moisture state, BESS electro-thermal behavior, demonstration-feeder power flow, overhead-line rating, scenario reliability risk, safety checks, and economic exposure are model outputs. They are not field measurements.

The integrated replay evaluates BESS, power flow, overhead line, and reliability models against one shared indexed timeline. It remains a demonstration 4-bus feeder and does not represent a utility network.

## Claim boundaries

- The safety gate is a **CBF-inspired deterministic bounded-trajectory check with scalar load projection**, not a QP solver and not field certification.
- The uncertainty endpoint is an **analytical quantile-bounded dispatch screen**, not a numerical SOCP or AC-OPF solver.
- Dispatch means a recommendation and auditable work order; no equipment is actuated.
- Failure outputs are uncalibrated scenario risk scores.
- Avoided-loss and ROI outputs are assumption-based estimates, not realized savings.
- Environmental validation does not validate equipment models.

## Completed prototype-hardening work

- Removed duplicate forced-cooling application from replay and agent trajectories.
- Standardized safe-load projection on configured transformer limits.
- Corrected stale DLR and cascading-risk persistence field mappings.
- Corrected baseline/mitigated cascading-hazard sample ordering.
- Preserved arbitrary live-profile lengths and source timestamps in sandbox runs.
- Added a machine-readable provenance contract and UI evidence panel.
- Coupled advanced engines to the canonical replay/sandbox timeline.
- Added cross-engine monotonicity, conservation, provenance, and endpoint regression tests.
- Replaced overstated UI descriptions of QP, formal proof, certification, and realized economics.

## External work required for pilot readiness

These tasks cannot be completed from the repository alone:

1. Obtain utility-approved SCADA exports or API access for timestamped MW, MVAR, voltage, OLTC, and cooling-stage state.
2. Obtain transformer nameplate and factory heat-run parameters for each target asset.
3. Obtain measured top-oil/hot-spot data for calibration and hold-out validation.
4. Obtain cable construction, route, burial, soil type/moisture, and preferably DTS temperature data.
5. Obtain BESS vendor limits, efficiency maps, HVAC consumption, and telemetry.
6. Select an independent feeder reference model (OpenDSS/pandapower) and provide the matching network case.
7. Have a qualified utility protection/control engineer approve limits and operating procedures.
8. Run in read-only shadow mode before any integration capable of actuation.

## Acceptance metrics for a pilot

- Transformer hold-out MAE/RMSE, peak error, and lag error reported per asset.
- Power-flow voltage, current, and loss parity against the chosen reference solver.
- SOC energy-balance error and thermal error reported against BESS telemetry.
- Cable-temperature error reported where field evidence exists.
- Reliability and economic parameters calibrated or explicitly retained as scenario-only outputs.
- Authenticated operator approval, rollback, audit retention, and cybersecurity review completed.
