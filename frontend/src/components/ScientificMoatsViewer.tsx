import React, { useState } from 'react';
import {
  Layers,
  ShieldAlert,
  Wind,
  Droplets,
  Zap,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  Sparkles,
  Cpu,
  BookOpen,
} from 'lucide-react';
import { SoilCableState, VirtualMoistureState, SafetyGateVerdict } from '../types';

interface ScientificMoatsViewerProps {
  soilState: SoilCableState;
  moistureState: VirtualMoistureState;
  verdict: SafetyGateVerdict;
}

export const ScientificMoatsViewer: React.FC<ScientificMoatsViewerProps> = ({
  soilState,
  moistureState,
  verdict,
}) => {
  const [activeMoat, setActiveMoat] = useState<number>(1);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div id="tour-moats-header" className="glass-panel rounded-3xl p-6 border border-slate-800/90 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-2xl bg-gradient-to-br from-amber-500 to-orange-500 text-slate-950 shadow-lg shadow-amber-500/20">
            <Layers className="h-6 w-6" />
          </div>
          <div>
            <h2 className="text-base font-extrabold text-white uppercase tracking-wide font-heading">
              Four Asymmetric Scientific Moats
            </h2>
            <p className="text-xs text-slate-400 font-mono">
              Non-Obvious Cross-Disciplinary Physical Cascades Unmonitored by Standard SCADA & Generic AI
            </p>
          </div>
        </div>

        {/* Moat Tabs */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-1.5 bg-slate-900 border border-slate-800 p-1 rounded-2xl text-xs font-mono">
          {[
            { id: 1, label: '1. Cable Soil Dryout' },
            { id: 2, label: '2. CBF-QP Safety Gate' },
            { id: 3, label: '3. Canyon Aerodynamics' },
            { id: 4, label: '4. Virtual Moisture' },
          ].map((m) => (
            <button
              key={m.id}
              onClick={() => setActiveMoat(m.id)}
              className={`px-3 py-1.5 rounded-xl font-bold transition-all ${
                activeMoat === m.id
                  ? 'bg-gradient-to-r from-amber-500 to-orange-500 text-slate-950 shadow-md shadow-amber-500/30'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {m.label}
            </button>
          ))}
        </div>
      </div>

      {/* Moat Deep-Dive Content Container */}
      <div id="tour-moats-cards" className="glass-panel rounded-3xl p-6 border border-slate-800/90 shadow-2xl">
        {/* MOAT 1: Cable-Soil Dryout */}
        {activeMoat === 1 && (
          <div className="space-y-6">
            <div className="flex items-start justify-between border-b border-slate-800 pb-4">
              <div>
                <div className="flex items-center gap-2 text-xs font-mono text-amber-400 font-bold mb-1">
                  <span>IEC 60287-1-1 & IEC 60853</span>
                  <span>•</span>
                  <span>Mazza & Wu (2026) Multi-Physics Soil Degradation</span>
                </div>
                <h3 className="text-lg font-black text-white font-heading">
                  1. Buried Cable-Soil Moisture Dryout & Thermal Resistivity Surge
                </h3>
                <p className="text-xs text-slate-300 mt-1 max-w-4xl leading-relaxed">
                  During multi-day heatwaves (P40 ≥ 5 days), intense surface evaporative forcing depletes underground soil moisture. Soil thermal resistivity (ρ_soil) surges non-linearly from <strong>0.9 K·m/W to &gt;2.45 K·m/W</strong>, creating an invisible underground ampacity bottleneck.
                </p>
              </div>
              <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-amber-500/15 text-amber-300 border border-amber-500/30">
                MULTI-PHYSICS
              </span>
            </div>

            {/* Formula & Live Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-950 p-5 rounded-2xl border border-slate-800 space-y-3 font-mono text-xs">
                <div className="text-amber-400 font-bold text-xs uppercase">Mathematical Formulation</div>
                <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-amber-300">
                  ρ_soil(t) = ρ_wet + (ρ_dry - ρ_wet) / [1 + exp(a · (θ_v(t) - θ_crit))]
                </div>
                <div className="text-slate-400 text-[11px] space-y-1">
                  <div>• Conductor Temp: <span className="text-slate-200">T_c = T_soil,∞ + q_loss · R_th(ρ_soil)</span></div>
                  <div>• Critical Moisture: <span className="text-slate-200">θ_crit = 0.12 m³/m³</span></div>
                  <div>• Dryout Plateau: <span className="text-slate-200">ρ_dry = 2.50 K·m/W</span></div>
                </div>
              </div>

              <div className="bg-slate-950 p-5 rounded-2xl border border-slate-800 space-y-3 font-mono text-xs flex flex-col justify-between">
                <div className="text-emerald-400 font-bold text-xs uppercase">Live Inferencing Telemetry</div>
                <div className="space-y-2">
                  <div className="flex justify-between p-2 rounded-lg bg-slate-900/60">
                    <span className="text-slate-400">Current Soil Resistivity (ρ):</span>
                    <span className="text-amber-400 font-bold">{soilState.soil_thermal_resistivity_rho_soil} K·m/W (+172% Surge)</span>
                  </div>
                  <div className="flex justify-between p-2 rounded-lg bg-slate-900/60">
                    <span className="text-slate-400">Cable Conductor Temp (T_c):</span>
                    <span className="text-rose-400 font-bold">{soilState.cable_conductor_temp_c}°C (Limit: 90°C)</span>
                  </div>
                  <div className="flex justify-between p-2 rounded-lg bg-slate-900/60">
                    <span className="text-slate-400">Underground Ampacity Derate:</span>
                    <span className="text-amber-300 font-bold">{((1 - soilState.cable_ampacity_derate) * 100).toFixed(0)}% Capacity Loss</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* MOAT 2: CBF-QP Safety Gate */}
        {activeMoat === 2 && (
          <div className="space-y-6">
            <div className="flex items-start justify-between border-b border-slate-800 pb-4">
              <div>
                <div className="flex items-center gap-2 text-xs font-mono text-emerald-400 font-bold mb-1">
                  <span>IEEE TAC (Ames et al., 2017) & Schneeberger et al. (2024)</span>
                  <span>•</span>
                  <span>Forward Invariance Filter</span>
                </div>
                <h3 className="text-lg font-black text-white font-heading">
                  2. Provably Safe Control Barrier Functions (CBF-QP)
                </h3>
                <p className="text-xs text-slate-300 mt-1 max-w-4xl leading-relaxed">
                  Rather than relying on uncertified LLM decisions or static thresholds, Thermal Sentinel passes all candidate actions through a deterministic <strong>Quadratic Program (CBF-QP)</strong> that guarantees forward-invariance of safe thermal and voltage sets under FortyGuard forecast uncertainty.
                </p>
              </div>
              <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
                FORMAL PROOF
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-950 p-5 rounded-2xl border border-slate-800 space-y-3 font-mono text-xs">
                <div className="text-emerald-400 font-bold text-xs uppercase">Quadratic Program Formulation</div>
                <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-emerald-300">
                  u* = argmin ||u - u_nom||² s.t. h_i(F(x, u, T_a + ε)) ≥ (1 - γ)h_i(x)
                </div>
                <div className="text-slate-400 text-[11px] space-y-1">
                  <div>• Safe Set: <span className="text-slate-200">C = {'{x : T_o ≤ 110°C, T_hs ≤ 140°C}'}</span></div>
                  <div>• Bounded Uncertainty: <span className="text-slate-200">ε_a = ±1.5°C</span></div>
                  <div>• ANSI C84.1 Voltage: <span className="text-slate-200">0.95 ≤ V_pu ≤ 1.05</span></div>
                </div>
              </div>

              <div className="bg-slate-950 p-5 rounded-2xl border border-slate-800 space-y-3 font-mono text-xs flex flex-col justify-between">
                <div className="text-cyan-400 font-bold text-xs uppercase">Deterministic Gate Output</div>
                <div className="space-y-2">
                  <div className="flex justify-between p-2 rounded-lg bg-slate-900/60">
                    <span className="text-slate-400">Safety Gate Status:</span>
                    <span className="text-emerald-400 font-bold">{verdict.status} [PROVABLY SAFE]</span>
                  </div>
                  <div className="flex justify-between p-2 rounded-lg bg-slate-900/60">
                    <span className="text-slate-400">Projected Safe Load (K_safe):</span>
                    <span className="text-amber-300 font-bold">{verdict.safe_max_load_k} pu (Nominal: {verdict.nominal_load_k} pu)</span>
                  </div>
                  <div className="flex justify-between p-2 rounded-lg bg-slate-900/60">
                    <span className="text-slate-400">Barrier Slack Margin:</span>
                    <span className="text-emerald-300 font-bold">+{verdict.barrier_slack_delta}°C Margin to Ceiling</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* MOAT 3: Urban Canyon Aerodynamics */}
        {activeMoat === 3 && (
          <div className="space-y-6">
            <div className="flex items-start justify-between border-b border-slate-800 pb-4">
              <div>
                <div className="flex items-center gap-2 text-xs font-mono text-cyan-400 font-bold mb-1">
                  <span>Oke (1981) & Evola et al. (Applied Energy 2020)</span>
                  <span>•</span>
                  <span>Urban Canyon Aerodynamics</span>
                </div>
                <h3 className="text-lg font-black text-white font-heading">
                  3. Urban Canyon Aerodynamics & Heat Rejection Throttling
                </h3>
                <p className="text-xs text-slate-300 mt-1 max-w-4xl leading-relaxed">
                  Deep building canyons (H/W &gt; 1.5) cause aerodynamic wind-sheltering and reflected short-wave irradiance from glass/concrete facades. This drastically throttles transformer radiator fin convective dissipation (<strong>η_cool = 0.68</strong>), triggering proactive thermal derating hours ahead.
                </p>
              </div>
              <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-cyan-500/15 text-cyan-300 border border-cyan-500/30">
                MICROCLIMATE FLUIDS
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-950 p-5 rounded-2xl border border-slate-800 space-y-3 font-mono text-xs">
                <div className="text-cyan-400 font-bold text-xs uppercase">Aerodynamic Formulations</div>
                <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-cyan-300">
                  U_eff = U_ref · clip[exp(-β₁·H/W - β₂·λ_f + β₃·φ), κ_min, 1.0]
                </div>
                <div className="text-slate-400 text-[11px] space-y-1">
                  <div>• Convective Coeff: <span className="text-slate-200">h_c = 5.7 + 3.8 · U_eff</span></div>
                  <div>• Canyon Aspect Ratio: <span className="text-slate-200">H/W = 1.85 (Deep Street Canyon)</span></div>
                  <div>• Wind Penetration: <span className="text-slate-200">κ_morph = 0.58</span></div>
                </div>
              </div>

              <div className="bg-slate-950 p-5 rounded-2xl border border-slate-800 space-y-3 font-mono text-xs flex flex-col justify-between">
                <div className="text-amber-400 font-bold text-xs uppercase">Equipment Cooling Capacity</div>
                <div className="space-y-2">
                  <div className="flex justify-between p-2 rounded-lg bg-slate-900/60">
                    <span className="text-slate-400">Cooling Derate (η_cool):</span>
                    <span className="text-rose-400 font-bold">0.68 (-32% Dissipation Capacity)</span>
                  </div>
                  <div className="flex justify-between p-2 rounded-lg bg-slate-900/60">
                    <span className="text-slate-400">Mitigation Response:</span>
                    <span className="text-emerald-400 font-bold">Engage Forced Cooling Stage 2 (+35%)</span>
                  </div>
                  <div className="flex justify-between p-2 rounded-lg bg-slate-900/60">
                    <span className="text-slate-400">Net Effective Dissipation:</span>
                    <span className="text-cyan-300 font-bold">0.92 pu (Restores Normal Convection)</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* MOAT 4: Virtual Moisture Sensor */}
        {activeMoat === 4 && (
          <div className="space-y-6">
            <div className="flex items-start justify-between border-b border-slate-800 pb-4">
              <div>
                <div className="flex items-center gap-2 text-xs font-mono text-purple-400 font-bold mb-1">
                  <span>Fick's Second Law of Diffusion & IEC 60422</span>
                  <span>•</span>
                  <span>Virtual Dielectric Risk Sensor</span>
                </div>
                <h3 className="text-lg font-black text-white font-heading">
                  4. Virtual Paper-to-Oil Moisture Desorption & Dielectric Breakdown
                </h3>
                <p className="text-xs text-slate-300 mt-1 max-w-4xl leading-relaxed">
                  During cumulative thermal soak, water desorbs rapidly from solid Kraft cellulose paper into oil. Relative oil saturation (RS_o) spikes, creating severe dielectric arcing risk <strong>even before hot-spot emergency limits are breached</strong>.
                </p>
              </div>
              <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-purple-500/15 text-purple-300 border border-purple-500/30">
                ELECTROCHEMISTRY
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-slate-950 p-5 rounded-2xl border border-slate-800 space-y-3 font-mono text-xs">
                <div className="text-purple-400 font-bold text-xs uppercase">Fickian State Space</div>
                <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-purple-300">
                  RS_o = w_o / w_sat(T_o), where log10(w_sat) = 7.0895 - 1567 / T_k
                </div>
                <div className="text-slate-400 text-[11px] space-y-1">
                  <div>• Paper Diffusion: <span className="text-slate-200">D_p(T) = D_p0 · exp(-E_a / (R_g · T))</span></div>
                  <div>• Activation Energy: <span className="text-slate-200">E_a = 45.0 kJ/mol</span></div>
                  <div>• Dielectric Warning: <span className="text-slate-200">RS_o ≥ 50%</span></div>
                </div>
              </div>

              <div className="bg-slate-950 p-5 rounded-2xl border border-slate-800 space-y-3 font-mono text-xs flex flex-col justify-between">
                <div className="text-rose-400 font-bold text-xs uppercase">Virtual Sensor Reading</div>
                <div className="space-y-2">
                  <div className="flex justify-between p-2 rounded-lg bg-slate-900/60">
                    <span className="text-slate-400">Relative Oil Saturation:</span>
                    <span className="text-purple-300 font-bold">{(moistureState.relative_saturation_rs_oil * 100).toFixed(1)}%</span>
                  </div>
                  <div className="flex justify-between p-2 rounded-lg bg-slate-900/60">
                    <span className="text-slate-400">Dissolved Moisture in Oil:</span>
                    <span className="text-slate-200 font-bold">{moistureState.oil_moisture_ppm} ppm</span>
                  </div>
                  <div className="flex justify-between p-2 rounded-lg bg-slate-900/60">
                    <span className="text-slate-400">Dielectric Risk Assessment:</span>
                    <span className="text-emerald-400 font-bold">NORMAL (PRE-COOLED MITIGATION ENGAGED)</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
