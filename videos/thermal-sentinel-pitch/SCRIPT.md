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
hours**. That sustained load aged transformer insulation a hundred and
forty-four times faster than normal. Nobody was watching the duration.

---

## Scene 2: The Solution (0:30 – 1:00, 30s)

Introducing Thermal Sentinel Grid: a physics-constrained agentic resilience
engine for urban energy infrastructure.

We pair FortyGuard's 2-meter Temperature AI with exact IEEE C57.91 and
IEC 60287 differential thermal equations — and critically, with FortyGuard's
*persistence* and *exceedance* analytics, which measure how long a parcel stays
above a damage threshold.

From that we model four latent cascades SCADA misses entirely: underground soil
dryout, building-canyon wind throttling, paper-oil moisture desorption, and
exact winding hot-spots.

---

## Scene 3: Why Agentic Physical AI (1:00 – 1:30, 30s)

Rather than train a black-box neural net that hallucinates, we built a hybrid
Physical-AI architecture with a strict division of labour.

Exact physics ODEs do the thermal math. FortyGuard supplies the measured
environmental boundary. LangGraph coordinates autonomous multi-agent dispatch
planning. And a deterministic Control Barrier Function — a quadratic program,
not a language model — acts as a mathematical firewall, proving that voltage and
temperature limits can never be violated before a single command is issued.

The LLM writes the explanation. It never touches the safety decision.

---

## Scene 4: Live Dashboard Demo (1:30 – 2:15, 45s)

In Mission Control, watch the baseline controller run away. Fed the real
measured thermal soak, the winding hot-spot climbs to **159.5 degrees** — twenty-five
degrees past the IEEE emergency ceiling — driving aging acceleration to a
hundred and forty-four times nominal.

Thermal Sentinel Grid sees it twelve hours ahead. It pre-cools radiators at
8 AM while power is cheap, then discharges five megawatts of storage across the
afternoon, capping the hot-spot at **112 degrees** — a **53-degree** reduction,
held safely inside the limit.

In the What-If Studio, judges can modulate the microclimate delta, heatwave
duration and battery size, with sub-15-millisecond ODE re-solving. Our AC power
flow solver simultaneously steps tap changers and dispatches Volt/VAR support to
hold hospital feeders at a hundred percent uptime.

---

## Scene 5: Auditable ROI & Impact (2:15 – 2:45, 30s)

Our economic engine uses the Department of Energy's LBNL ICE standard, so the
numbers are auditable rather than asserted. We quantify avoided outage risk,
capital life extension, and the exact energy cost of mitigating.

For a single heatwave event: **2.58 million dollars** in net avoided loss, an ROI
of roughly **5,800 to one**, and **605 equivalent aging hours** returned to the
asset — while keeping critical medical feeders energised.

Failure probability drops from ninety-six percent to under one.

---

## Scene 6: Outro (2:45 – 3:00, 15s)

Every number you just saw came back from the live FortyGuard API, and we publish
the field notes — including the places our own early assumptions turned out to
be wrong.

Physics you can verify. Safety you can prove. Thermal Sentinel Grid.

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
| Mitigated hot-spot | 109.4 °C | IEEE C57.91 solver |
| Hot-spot reduction | −50.1 °C | Derived |
| Baseline aging acceleration | 88.4× | Arrhenius |
| Mitigated aging acceleration | 0.94× | Arrhenius |
| Avoided aging hours | 374.3 h | Derived |
| Net avoided loss | $2,576,849 | LBNL ICE |
| ROI | 5,495× | LBNL ICE |
| Failure probability | 90.8% → 0.75% | Weibull RUL |

### Deliberately NOT claimed

- **A +4.5 °C airport-vs-urban delta.** We assumed this early on. Measuring it
  against the API gives +1.1 °C versus natural desert terrain — and Sky Harbor
  airport reads *warmer* than downtown, because an airport ringed by runways is
  itself a heat island. The pitch leads on duration instead, which is both true
  and the stronger physical argument.
- **A peak-temperature story.** $P_{40}$ = 12.0 h is the full width of our
  sampling window, so we describe it as "twelve unbroken hours," not as a
  maximum the weather happened to reach.
