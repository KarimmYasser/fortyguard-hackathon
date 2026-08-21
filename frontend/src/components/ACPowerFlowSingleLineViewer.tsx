import React, { useState, useEffect } from 'react';
import { Zap, Activity, ShieldCheck, AlertTriangle, Sliders, Battery, Hospital, Building2 } from 'lucide-react';
import { API_BASE } from '../utils/api';

export const ACPowerFlowSingleLineViewer: React.FC = () => {
  const [solution, setSolution] = useState<any>(null);
  const [oltcTap, setOltcTap] = useState<number>(4);
  const [bessP, setBessP] = useState<number>(4.0);
  const [bessQ, setBessQ] = useState<number>(2.0);
  const [loadMultiplier, setLoadMultiplier] = useState<number>(1.18);

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

  useEffect(() => {
    fetchSolution(oltcTap, bessP, bessQ, loadMultiplier);
  }, []);

  if (!solution) {
    return (
      <div className="glass-panel rounded-3xl p-6 text-center text-slate-400 font-mono">
        Solving AC Distribution Feeder Power Flow...
      </div>
    );
  }

  const buses = solution.buses || [];
  const branches = solution.branches || [];

  return (
    <div className="glass-panel rounded-3xl p-6 border border-slate-800/90 shadow-2xl space-y-6">
      {/* Header */}
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
                AC Distribution Feeder Power Flow & Grid Network
              </h2>
              <span
                className={`px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold border ${
                  solution.ansi_c84_envelope_compliant
                    ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30'
                    : 'bg-rose-500/20 text-rose-300 border-rose-800'
                }`}
              >
                {solution.ansi_c84_envelope_compliant ? 'ANSI C84.1 COMPLIANT' : 'VOLTAGE VIOLATION'}
              </span>
            </div>
            <p className="text-xs text-slate-400 font-mono mt-0.5">
              Exact Forward-Backward Sweep AC Solver · On-Load Tap Changer (OLTC) · 4-Quadrant BESS Volt/VAR Support
            </p>
          </div>
        </div>

        {/* Total Losses Badge */}
        <div className="bg-slate-900 border border-slate-800 px-4 py-2 rounded-2xl text-xs font-mono flex items-center gap-3 text-slate-300">
          <span>Grid Losses: <strong className="text-amber-400">{solution.total_grid_losses_kw} kW</strong></span>
          <span>•</span>
          <span>Demand: <strong className="text-cyan-400">{solution.total_grid_demand_mw} MW</strong></span>
        </div>
      </div>

      {/* 4-Bus Single-Line Diagram Topology */}
      <div id="tour-powerflow-diagram" className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 font-mono text-xs">
        {buses.map((bus: any, idx: number) => {
          const isCompliant = bus.voltage_compliant_ansi_c84;
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
                <span className="text-slate-400 text-[10px]">{bus.base_kv} kV Base</span>
              </div>

              <div>
                <div className="text-sm font-bold text-slate-200">{bus.bus_name}</div>
                <div className="flex items-baseline gap-2 mt-1">
                  <span
                    className={`text-2xl font-black ${
                      isCompliant ? 'text-emerald-400' : 'text-rose-400 animate-pulse'
                    }`}
                  >
                    {bus.voltage_magnitude_pu.toFixed(4)} pu
                  </span>
                  <span className="text-[10px] text-slate-400">({bus.voltage_angle_deg}° angle)</span>
                </div>
              </div>

              <div className="pt-2 border-t border-slate-800/80 text-[11px] space-y-1 text-slate-400">
                <div className="flex justify-between">
                  <span>Actual Voltage:</span>
                  <span className="text-slate-200 font-bold">{bus.voltage_actual_kv} kV</span>
                </div>
                {bus.active_power_demand_mw > 0 && (
                  <div className="flex justify-between">
                    <span>Load (P/Q):</span>
                    <span className="text-cyan-300 font-bold">{bus.active_power_demand_mw} MW / {bus.reactive_power_demand_mvar} MVAr</span>
                  </div>
                )}
                {bus.bess_active_injection_mw > 0 && (
                  <div className="flex justify-between text-emerald-400 font-bold">
                    <span>BESS (P/Q):</span>
                    <span>+{bus.bess_active_injection_mw} MW / +{bus.bess_reactive_injection_mvar} MVAr</span>
                  </div>
                )}
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
    </div>
  );
};
