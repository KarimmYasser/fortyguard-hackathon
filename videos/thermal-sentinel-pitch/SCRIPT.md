# Thermal Sentinel Grid — Official 3-Minute Video Pitch Script (180s)

> **Every figure in this script is reproducible.** Run
> `GET /api/v1/replay/phoenix-2023` or `python scripts/regenerate_phoenix_fixture.py`.
> Measured values come from the live FortyGuard API for downtown Phoenix on
> 2023-07-19; physics values are solved from that data by our IEEE C57.91 engine.
> See `docs/api-documentation/14-field-notes-live-integration.md`.

---

## Scene 1: The Hook & Market Blindspot (0:00 – 0:30, 30s)

During extreme heatwaves, utilities manage hundreds of millions of dollars of
infrastructure using weather stations that report a *peak*. SCADA systems from
Siemens, GE and Schneider only react when an alarm trips at 135 degrees — when
the failure is already locked in.

But transformers don't fail from a peak. They fail from a soak.

In Phoenix, on July nineteenth 2023, FortyGuard measured the air two meters
above downtown asphalt holding above forty degrees for **twelve unbroken
hours**. Under the benchmark load profile, that sustained boundary drove peak
transformer aging acceleration to **88.4 times nominal**. Nobody was watching
the duration.

---

## Scene 2: The Solution (0:30 – 1:00, 30s)

Introducing Thermal Sentinel Grid: a physics-constrained agentic resilience
engine for urban energy infrastructure.

We pair FortyGuard's 2-meter Temperature AI with transparent, standards-based
IEEE C57.91 and IEC 60287 thermal models — and critically, with FortyGuard's
*persistence* and *exceedance* analytics, which measure how long a parcel stays
above a damage threshold.

From that we model four latent cascades SCADA misses entirely: underground soil
dryout, building-canyon wind throttling, paper-oil moisture desorption, and
exact winding hot-spots.

---

## Scene 3: Why Agentic Physical AI (1:00 – 1:30, 30s)

Rather than train a black-box neural net that hallucinates, we built a hybrid
Physical-AI architecture with a strict division of labour.

Transparent standards-based ODEs do the thermal math. FortyGuard supplies the measured
environmental boundary. LangGraph coordinates multi-agent recommendation
planning. And a deterministic, CBF-inspired safety gate — not a language model —
rejects or modifies proposals outside the configured modelled voltage and
temperature envelope before a work order can be proposed.

The LLM writes the explanation. It never touches the safety decision.

---

## Scene 4: Live Dashboard Demo (1:30 – 2:15, 45s)

In Mission Control, watch the baseline controller run away. Fed the real
measured thermal soak, the winding hot-spot climbs to **159.5 degrees** — twenty-five
degrees past the IEEE emergency ceiling — driving peak aging acceleration to
**88.4 times nominal**.

Thermal Sentinel Grid sees it twelve hours ahead. It pre-cools radiators at
8 AM while power is cheap, then discharges five megawatts of storage across the
afternoon, reducing the modelled hot-spot to **122.5 degrees** — a **37-degree**
reduction, held inside the configured limit.

In the What-If Studio, judges can modulate the microclimate delta, heatwave
duration and battery size, with sub-15-millisecond ODE re-solving. Our AC power
flow solver simultaneously evaluates tap changers and Volt/VAR support on the
modelled four-bus hospital feeder while checking its configured limits.

---

## Scene 5: Auditable Scenario Economics & Impact (2:15 – 2:45, 30s)

Our scenario economic engine uses a disclosed value-of-lost-load assumption
informed by LBNL interruption-cost research. It separates avoided consequence
exposure, capital-aging deferral, and assumed mitigation cost.

For this benchmark: approximately **2.57 million dollars** in modeled avoided
exposure, a **5,472.6-to-one** assumption-based cost ratio, and **365.4 equivalent
aging hours** avoided. These are scenario outputs, not realized savings.

The uncalibrated scenario risk score drops from **90.84 percent to 1.13 percent**.

---

## Scene 6: Outro (2:45 – 3:00, 15s)

Every environmental boundary you just saw came from the live FortyGuard API;
the grid, asset, dispatch, and financial values were derived by our documented
models. We publish the field notes — including where early assumptions were
wrong.

Physics you can inspect. Decisions you can audit. Thermal Sentinel Grid.

---

## Figure Reference (for on-screen graphics)

| On-screen figure | Value | Origin |
| :--- | ---: | :--- |
| Peak 2m air temperature | 42.7 °C | Measured — `heatmap` `tcm` |
| Natural-terrain reference | 41.6 °C | Measured — South Mountain AOI |
| Land-cover delta | +1.1 °C | Derived from the two above |
| Persistence $P_{40}$ | 12.0 h | Measured — `persistence` analytic |
| Exceedance $H_{40}$ | 17.48 °C·h | Integrated from measured curve |
| Thermal Soak Index | 3.68 | Computed |
| Baseline hot-spot | 159.5 °C | IEEE C57.91 solver |
| Mitigated hot-spot | 122.5 °C | IEEE C57.91-based solver |
| Hot-spot reduction | −37.0 °C | Derived |
| Baseline aging acceleration | 88.4× | Arrhenius |
| Mitigated aging acceleration | 3.45× | Arrhenius |
| Avoided aging hours | 365.4 h | Derived |
| Modeled avoided exposure | $2,566,192.66 | VoLL-informed scenario model |
| Assumption-based cost ratio | 5,472.6× | Scenario model |
| Scenario risk score | 90.84% → 1.13% | Uncalibrated logistic model |

### Deliberately NOT claimed

- **A +4.5 °C airport-vs-urban delta.** We assumed this early on. Measuring it
  against the API gives +1.1 °C versus natural desert terrain — and Sky Harbor
  airport reads *warmer* than downtown, because an airport ringed by runways is
  itself a heat island. The pitch leads on duration instead, which is both true
  and the stronger physical argument.
- **A peak-temperature story.** $P_{40}$ = 12.0 h is the full width of our
  sampling window, so we describe it as "twelve unbroken hours," not as a
  maximum the weather happened to reach.
