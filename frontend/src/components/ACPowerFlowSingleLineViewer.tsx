import React, { useState, useEffect } from 'react';
import { Zap, Activity, ShieldCheck, AlertTriangle, Sliders, Battery, Hospital, Building2, Layers, Wind, AlertOctagon } from 'lucide-react';
import { API_BASE } from '../utils/api';
import { DynamicLineRatingViewer } from './DynamicLineRatingViewer';
import { CascadingHazardGauge } from './CascadingHazardGauge';

export const ACPowerFlowSingleLineViewer: React.FC = () => {
  const [solution, setSolution] = useState<any>(null);
  const [ccOpfSolution, setCcOpfSolution] = useState<any>(null);
  const [isCcOpfMode, setIsCcOpfMode] = useState<boolean>(false);
  const [confidenceLevel, setConfidenceLevel] = useState<number>(95.0);
  const [oltcTap, setOltcTap] = useState<number>(4);
  const [bessP, setBessP] = useState<number>(4.0);
  const [bessQ, setBessQ] = useState<number>(2.0);
  const [loadMultiplier, setLoadMultiplier] = useState<number>(1.18);
  const [activeSubView, setActiveSubView] = useState<'topology' | 'dlr' | 'hazard'>('topology');

  const fetchSolution = async (tap: number, p: number, q: number, k: number) => {
    try {
      const resp = await fetch(`${API_BASE}/api/v1/power-flow/solve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          substation_slack_v_pu: 1.03,
          tx_load_multiplier_k: k,
          bess_discharge_mw: p,
          bess_volt_var_q_mvar: q,
          oltc_tap_position: tap,
          soil_resistivity_rho: 1.85,
        }),
      });
      if (resp.ok) {
        const json = await resp.json();
        setSolution(json);
      }
    } catch (err) {
      console.error('Failed to solve AC power flow', err);
    }
  };

  const fetchCcOpf = async (conf: number) => {
    try {
      const resp = await fetch(`${API_BASE}/api/v1/physics/cc-opf-solve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          base_ambient_temp_c: 42.7,
          forecast_std_dev_c: 1.85,
          confidence_level_pct: conf,
          total_grid_load_mw: 22.8 * loadMultiplier,
          total_grid_load_mvar: 6.8 * loadMultiplier,
          bess_max_power_mw: 8.0,
          bess_max_mvar: 4.0,
        }),
      });
      if (resp.ok) {
        const json = await resp.json();
        setCcOpfSolution(json);
      }
    } catch (err) {
      console.error('Failed to solve Chance-Constrained OPF', err);
    }
  };

  useEffect(() => {
    fetchSolution(oltcTap, bessP, bessQ, loadMultiplier);
    fetchCcOpf(confidenceLevel);
  }, [oltcTap, bessP, bessQ, loadMultiplier, confidenceLevel]);

  if (!solution) {
    return (
      <div className="glass-panel rounded-3xl p-6 text-center text-slate-400 font-mono">
        Solving AC Distribution Feeder Power Flow & Chance-Constrained OPF...
      </div>
    );
  }

  const buses = isCcOpfMode && ccOpfSolution ? ccOpfSolution.buses : solution.buses || [];
  const branches = isCcOpfMode && ccOpfSolution ? ccOpfSolution.branches : solution.branches || [];

  return (
    <div className="glass-panel rounded-3xl p-6 border border-slate-800/90 shadow-2xl space-y-6">
      {/* Header with Sub-View Navigation & Mode Switcher */}
      <div id="tour-powerflow-header" className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div className="flex items-center gap-3.5">
          <div className="h-11 w-11 rounded-2xl bg-gradient-to-br from-emerald-500 to-cyan-600 p-[1px] shadow-lg shadow-emerald-500/20">
            <div className="h-full w-full bg-slate-950 rounded-[15px] flex items-center justify-center">
              <Zap className="h-5 w-5 text-emerald-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2.5">
              <h2 className="text-base font-black text-white uppercase tracking-wide font-heading">
                AC Distribution Feeder Power Flow & Optimal Dispatch
              </h2>
              <span
                className={`px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold border ${
                  isCcOpfMode
                    ? 'bg-purple-500/15 text-purple-300 border-purple-500/30'
                    : solution.ansi_c84_envelope_compliant
                    ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30'
                    : 'bg-rose-500/20 text-rose-300 border-rose-800'
                }`}
              >
                {isCcOpfMode ? `CHANCE-CONSTRAINED (${confidenceLevel}% CONFIDENCE)` : solution.ansi_c84_envelope_compliant ? 'ANSI C84.1 COMPLIANT' : 'VOLTAGE VIOLATION'}
              </span>
            </div>
            <p className="text-xs text-slate-400 font-mono mt-0.5">
              Exact Forward-Backward Sweep · Second-Order Cone CC-OPF · Dynamic Line Rating · Volt/VAR
            </p>
          </div>
        </div>

        {/* View Switcher Tabs */}
        <div id="tour-powerflow-subviews" className="flex items-center gap-2 bg-slate-900/80 p-1.5 rounded-2xl border border-slate-800">
          <button
            id="tour-powerflow-tab-topology"
            onClick={() => setActiveSubView('topology')}
            className={`px-3 py-1.5 rounded-xl text-xs font-mono font-bold transition-all flex items-center gap-1.5 ${
              activeSubView === 'topology'
                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Layers className="h-3.5 w-3.5" /> 4-Bus Feeder
          </button>
          <button
            id="tour-powerflow-tab-dlr"
            onClick={() => setActiveSubView('dlr')}
            className={`px-3 py-1.5 rounded-xl text-xs font-mono font-bold transition-all flex items-center gap-1.5 ${
              activeSubView === 'dlr'
                ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Wind className="h-3.5 w-3.5" /> IEEE 738 DLR
          </button>
          <button
            id="tour-powerflow-tab-hazard"
            onClick={() => setActiveSubView('hazard')}
            className={`px-3 py-1.5 rounded-xl text-xs font-mono font-bold transition-all flex items-center gap-1.5 ${
              activeSubView === 'hazard'
                ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40 shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <AlertOctagon className="h-3.5 w-3.5" /> Cascading Hazard
          </button>
        </div>
      </div>

      {activeSubView === 'dlr' && <DynamicLineRatingViewer />}
      {activeSubView === 'hazard' && <CascadingHazardGauge isMitigatedMode={bessP > 2.0} />}

      {activeSubView === 'topology' && (
        <>
          {/* Chance-Constrained Mode Toggle Bar */}
          <div id="tour-cc-opf-controls" className="bg-slate-900/60 p-3.5 rounded-2xl border border-slate-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-3 text-xs font-mono">
            <div className="flex items-center gap-3">
              <span className="text-slate-400 font-bold">Optimization Formulation:</span>
              <button
                onClick={() => setIsCcOpfMode(false)}
                className={`px-3 py-1 rounded-xl font-bold transition-all ${
                  !isCcOpfMode
                    ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                    : 'text-slate-500 hover:text-slate-300'
                }`}
              >
                Deterministic AC Flow
              </button>
              <button
                onClick={() => setIsCcOpfMode(true)}
                className={`px-3 py-1 rounded-xl font-bold transition-all ${
                  isCcOpfMode
                    ? 'bg-purple-500/20 text-purple-300 border border-purple-500/40'
                    : 'text-slate-500 hover:text-slate-300'
                }`}
              >
                Uncertainty-Bounded Dispatch Screen
              </button>
            </div>

            {isCcOpfMode && (
              <div className="flex items-center gap-2">
                <span className="text-slate-400">Confidence:</span>
                {[90, 95, 99].map((lvl) => (
                  <button
                    key={lvl}
                    onClick={() => setConfidenceLevel(lvl)}
                    className={`px-2.5 py-0.5 rounded-lg text-[11px] font-bold ${
                      confidenceLevel === lvl
                        ? 'bg-purple-500 text-white shadow-md'
                        : 'bg-slate-800 text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    {lvl}%
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* 4-Bus Single-Line Diagram Topology */}
          <div id="tour-powerflow-diagram" className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 font-mono text-xs">
            {buses.map((bus: any, idx: number) => {
              const isCompliant = bus.voltage_compliant_ansi_c84 ?? bus.voltage_compliant;
              return (
                <div
                  key={bus.bus_id}
                  className={`p-4 rounded-2xl border space-y-3 relative ${
                    isCompliant
                      ? 'bg-slate-950/80 border-slate-800 hover:border-slate-700'
                      : 'bg-rose-950/40 border-rose-600 shadow-lg shadow-rose-950/40'
                  }`}
                >
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="font-bold text-white flex items-center gap-1.5">
                      {idx === 0 && <Zap className="h-3.5 w-3.5 text-blue-400" />}
                      {idx === 1 && <Sliders className="h-3.5 w-3.5 text-purple-400" />}
                      {idx === 2 && <Battery className="h-3.5 w-3.5 text-cyan-400" />}
                      {idx === 3 && <Hospital className="h-3.5 w-3.5 text-emerald-400" />}
                      {bus.bus_id}
                    </span>
                    <span className="text-slate-400 text-[10px]">{bus.base_kv || '13.8'} kV Base</span>
                  </div>

                  <div>
                    <div className="text-sm font-bold text-slate-200">{bus.bus_name}</div>
                    <div className="flex items-baseline gap-2 mt-1">
                      <span
                        className={`text-2xl font-black ${
                          isCompliant ? 'text-emerald-400' : 'text-rose-400 animate-pulse'
                        }`}
                      >
                        {bus.voltage_magnitude_pu != null
                          ? `${bus.voltage_magnitude_pu.toFixed(3)} pu`
                          : bus.voltage_mean_pu != null ? `${bus.voltage_mean_pu} pu` : '—'}
                      </span>
                      <span className="text-slate-500 text-[11px]">
                        {bus.voltage_angle_deg != null
                          ? `${bus.voltage_angle_deg.toFixed(1)}°`
                          : bus.voltage_lower_bound_pu != null && bus.voltage_upper_bound_pu != null
                            ? `[${bus.voltage_lower_bound_pu} - ${bus.voltage_upper_bound_pu}]`
                            : ''}
                      </span>
                    </div>
                  </div>

                  <div className="pt-2 border-t border-slate-800/80 space-y-1 text-[11px] text-slate-400">
                    <div className="flex justify-between">
                      <span>P Load / Inj:</span>
                      <span className="text-cyan-300 font-bold">
                        {bus.active_power_demand_mw != null
                          ? `${bus.active_power_demand_mw.toFixed(2)} MW`
                          : bus.bess_active_injection_mw != null
                            ? `${bus.bess_active_injection_mw.toFixed(2)} MW`
                            : '—'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span>Q Load / Inj:</span>
                      <span className="text-purple-300 font-bold">
                        {bus.reactive_power_demand_mvar != null
                          ? `${bus.reactive_power_demand_mvar.toFixed(2)} MVAr`
                          : bus.bess_reactive_injection_mvar != null
                            ? `${bus.bess_reactive_injection_mvar.toFixed(2)} MVAr`
                            : '—'}
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Interactive Power Flow Grid Controls */}
          <div id="tour-powerflow-voltvar" className="p-4 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-4 font-mono text-xs">
            <div className="text-slate-300 font-bold text-xs uppercase border-b border-slate-800 pb-2 flex items-center justify-between">
              <span>Interactive Grid Control & Volt/VAR Optimization</span>
              <span className="text-amber-400">ANSI C84.1 Envelope [0.95 - 1.05 pu]</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* OLTC Slider */}
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-slate-400">OLTC Tap Position:</span>
                  <span className="text-purple-400 font-bold">{oltcTap > 0 ? `+${oltcTap}` : oltcTap} ({solution.oltc_voltage_boost_pct > 0 ? `+${solution.oltc_voltage_boost_pct}%` : `${solution.oltc_voltage_boost_pct}%`})</span>
                </div>
                <input
                  type="range"
                  min="-8"
                  max="12"
                  step="1"
                  value={oltcTap}
                  onChange={(e) => {
                    const val = parseInt(e.target.value);
                    setOltcTap(val);
                    fetchSolution(val, bessP, bessQ, loadMultiplier);
                  }}
                  className="w-full accent-purple-500 cursor-pointer"
                />
                <div className="flex justify-between text-[10px] text-slate-500">
                  <span>-5.0% Boost</span>
                  <span>Nominal (0)</span>
                  <span>+7.5% Boost</span>
                </div>
              </div>

              {/* BESS Active Discharge */}
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-slate-400">BESS Active Discharge (P):</span>
                  <span className="text-cyan-400 font-bold">{bessP.toFixed(1)} MW</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="10"
                  step="0.5"
                  value={bessP}
                  onChange={(e) => {
                    const val = parseFloat(e.target.value);
                    setBessP(val);
                    fetchSolution(oltcTap, val, bessQ, loadMultiplier);
                  }}
                  className="w-full accent-cyan-500 cursor-pointer"
                />
                <div className="flex justify-between text-[10px] text-slate-500">
                  <span>0 MW</span>
                  <span>5.0 MW</span>
                  <span>10.0 MW</span>
                </div>
              </div>

              {/* BESS Reactive Volt/VAR */}
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-slate-400">BESS Volt/VAR Reactive (Q):</span>
                  <span className="text-emerald-400 font-bold">+{bessQ.toFixed(1)} MVAr</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="6"
                  step="0.5"
                  value={bessQ}
                  onChange={(e) => {
                    const val = parseFloat(e.target.value);
                    setBessQ(val);
                    fetchSolution(oltcTap, bessP, val, loadMultiplier);
                  }}
                  className="w-full accent-emerald-500 cursor-pointer"
                />
                <div className="flex justify-between text-[10px] text-slate-500">
                  <span>0 MVAr</span>
                  <span>3.0 MVAr</span>
                  <span>6.0 MVAr (Max Support)</span>
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};
