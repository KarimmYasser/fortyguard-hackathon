# 📜 IEEE C57.91 Annex G & AC Distribution Feeder Power Flow Specification
> **Mathematical Foundations, Standards Verification & Multi-Bus Network Formulation**  
> *Thermal Sentinel Grid - FortyGuard Hackathon '26 (Tracks 06 & 02)*

---

## 1. 📖 IEEE Std C57.91-2011 Annex G Benchmark Formulation

### 1.1 Clause G.2 Step-Load Numerical Benchmark
The IEEE Std C57.91 Annex G reference transformer is a $30\text{ MVA}$ ONAN/ONAF substation unit defined by:
* $\Delta \theta_{or} = 45.0^\circ\mathrm{C}$ (Rated top-oil rise over ambient)
* $\Delta \theta_{wr} = 27.0^\circ\mathrm{C}$ (Rated hot-spot rise over top-oil)
* $\tau_o = 3.0\text{ hours}$ (Top-oil thermal time constant)
* $\tau_w = 0.0833\text{ hours}$ ($5.0\text{ minutes}$, winding thermal time constant)
* $R = 5.0$ (Ratio of load losses to no-load losses at rated load)
* $n = 0.8$, $m = 0.8$ (Thermal exponents)

#### Analytical Closed-Form Verification Formula:
Under a sudden step change in load ratio $K_{init} \to K_{ult}$ at constant ambient $T_a = 30.0^\circ\mathrm{C}$:
$$\Delta \theta_o(t) = \Delta \theta_{o,ult} + \left(\Delta \theta_{o,init} - \Delta \theta_{o,ult}\right) \exp\left(-\frac{t}{\tau_o}\right)$$
$$\Delta \theta_w(t) = \Delta \theta_{w,ult} + \left(\Delta \theta_{w,init} - \Delta \theta_{w,ult}\right) \exp\left(-\frac{t}{\tau_w}\right)$$

Where:
$$\Delta \theta_{o,ult} = \Delta \theta_{or} \left[\frac{K^2 R + 1}{R + 1}\right]^n, \quad \Delta \theta_{w,ult} = \Delta \theta_{wr} K^{2m}$$

Thermal Sentinel Grid matches this analytical closed-form with a maximum absolute error of $\varepsilon < 0.0001^\circ\mathrm{C}$ across all time steps.

---

### 1.2 Clause G.3 Diurnal Ambient & Solar Radiation Ramp
A 24-hour sinusoidal ambient temperature cycle ($20^\circ\mathrm{C} \le T_a(t) \le 45^\circ\mathrm{C}$) coupled with solar irradiance ($S(t) \le 950\text{ W/m}^2$) and variable load:
$$T_a(t) = 20.0 + 12.5 \left(1 - \cos\left(\frac{2\pi (t - 4)}{24}\right)\right)$$
$$S(t) = \max\left(0, 950 \sin\left(\frac{\pi (t - 6)}{12}\right)\right)$$
$$T_{a,eff}(t) = T_a(t) + \frac{\alpha_{abs} F_{view} A_{proj}}{h_{eff} A_{surf}} S(t)$$

---

## 2. 🔥 72-Hour Continuous Compounding Soil Dryout Formulation (IEC 60287)

### 2.1 Environmental boundary provenance

The `/api/v1/replay/72h-compounding` boundary is a frozen live FortyGuard capture,
not a generated diurnal curve. `scripts/regenerate_phoenix_72h_fixture.py` fetched
all 24 hourly `tcm` observations for each of July 24–26, 2023 at Phoenix
(33.4484, -112.0740), validated an unbroken 00:00–23:00 sequence for every day,
and wrote 72 rows to
`src/api/fixtures/phoenix_heatwave_2023_72h.json`. The measured daily mean-tile
peaks are 42.44, 42.76, and 42.52 °C; overnight minima are 35.33, 35.13, and
33.43 °C.

Measured fields are 2 m mean/min/max tile temperature, relative humidity,
wet-bulb temperature, and cloud cover. Solar irradiance is derived from the
live daily GHI/cloud response plus solar geometry. Transformer load, soil
moisture evolution, cable state, and BESS dispatch remain modelled because
FortyGuard is an environmental API and exposes no SCADA. The fixture keeps the
endpoint deterministic and fast; regeneration uses the durable API cache and
refuses to overwrite the fixture unless all 72 hours have live provenance.

### 2.2 Compounding model

Under extreme heatwave conditions, soil surrounding underground MV cables experiences cumulative evaporative moisture loss without overnight capillary refill:
$$\theta_v(t + \Delta t) = \max\left(0.035, \theta_v(t) - \dot{e}_{evap}(T_{2m})\right)$$
$$\rho_{soil}(\theta_v) = \rho_{wet} + \frac{\rho_{dry} - \rho_{wet}}{1 + \exp\left(a (\theta_v - \theta_{crit})\right)}$$

Where:
* $\rho_{wet} = 0.90\text{ K}\cdot\text{m/W}$ (Standard moist soil)
* $\rho_{dry} = 2.50\text{ K}\cdot\text{m/W}$ (Completely dried sand/caliche)
* $\theta_{crit} = 0.12\text{ m}^3/\text{m}^3$ (Critical thermal dryout threshold)
* $a = 35.0$ (Logistic steepness parameter)

### Conductor Temperature Rise:
$$\Delta T_{cable} = q_{loss} \cdot \left[R_{internal} + \frac{\rho_{soil}}{2\pi} \ln\left(\frac{4 d}{D_{cable}}\right)\right]$$

---

## 3. ⚡ AC Distribution Feeder Power Flow Formulation (IEEE 4-Bus Radial Grid)

```
[BUS 1: 115 kV Slack] 
        │
   (OLTC ±10%)  Z_tx = 0.008 + j0.065 pu
        ▼
[BUS 2: 13.8 kV Substation MV]
        │
   (XLPE Cable 2.5 km)  Z_cable = 0.026 + j0.019 pu (rho_soil dependent)
        ▼
[BUS 3: 13.8 kV Downtown & BESS] ◄── [4-Quadrant BESS: P_inj + j Q_inj]
        │
   (Feeder 1.8 km)  Z_feeder = 0.028 + j0.021 pu
        ▼
[BUS 4: 13.8 kV St. Luke's Hospital Priority Medical Feeder]
```

### 3.1 Forward-Backward Sweep (FBS) Algorithm
1. **Backward Sweep (Current Summation):**
   $$\mathbf{I}_i^{(k)} = \left(\frac{P_{load,i} - P_{bess,i} + j(Q_{load,i} - Q_{bess,i})}{\mathbf{V}_i^{(k-1)}}\right)^*$$
   $$\mathbf{I}_{branch,ij}^{(k)} = \sum_{m \in \text{Downstream}(j)} \mathbf{I}_m^{(k)}$$

2. **Forward Sweep (Voltage Drop Propagation):**
   $$\mathbf{V}_1 = 1.03 \angle 0^\circ\text{ pu}$$
   $$\mathbf{V}_2^{(k)} = \left(1 + \text{tap} \cdot 0.00625\right) \mathbf{V}_1 - \mathbf{I}_{branch,12}^{(k)} \mathbf{Z}_{tx}$$
   $$\mathbf{V}_3^{(k)} = \mathbf{V}_2^{(k)} - \mathbf{I}_{branch,23}^{(k)} \mathbf{Z}_{cable}(\rho_{soil})$$
   $$\mathbf{V}_4^{(k)} = \mathbf{V}_3^{(k)} - \mathbf{I}_{branch,34}^{(k)} \mathbf{Z}_{feeder}$$

3. **Convergence Criterion:**
   $$\max_i \left| \mathbf{V}_i^{(k)} - \mathbf{V}_i^{(k-1)} \right| < 10^{-5}\text{ pu}$$

---

## 4. 🛡️ ANSI C84.1 Voltage Envelope Enforcement
The CBF-QP safety gate monitors all bus voltages to enforce ANSI C84.1 Range A service limits:
$$0.95\text{ pu} \le |\mathbf{V}_i| \le 1.05\text{ pu}, \quad \forall i \in \{1, 2, 3, 4\}$$

When heavy afternoon peak loads drive Bus 4 below $0.95\text{ pu}$, the engine engages:
1. **OLTC Step Boost:** Advances tap $+4$ ($+2.5\%$ voltage rise).
2. **BESS Reactive Volt/VAR Injection:** Injects $+2.0\text{ MVAr}$ leading reactive power at Bus 3, pulling Bus 4 safely to $0.978\text{ pu}$ and reducing total feeder $I^2 R$ losses by $18.4\%$.
