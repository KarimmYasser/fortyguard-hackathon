import React, { useState, useEffect } from 'react';
import { Battery, Flame, ShieldCheck, AlertTriangle, DollarSign, Activity } from 'lucide-react';
import { API_BASE } from '../utils/api';

export const BESSDegradationViewer: React.FC = () => {
  const [bessTrajectory, setBessTrajectory] = useState<any[]>([]);
  const [dispatchPower, setDispatchPower] = useState<number>(6.5);
  const [initialSoc, setInitialSoc] = useState<number>(0.85);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchBESSData = async () => {
    setLoading(true);
    try {
      const powers = [2.0, 4.0, dispatchPower, dispatchPower * 1.1, dispatchPower, 5.0, 3.5, 2.0, 1.0, 0.0, 0.0, 0.0];
      const resp = await fetch(`${API_BASE}/api/v1/physics/bess-thermal`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          dispatch_powers_mw: powers,
          initial_soc: initialSoc,
          initial_core_temp_c: 35.0,
        }),
      });
      if (resp.ok) {
        const json = await resp.json();
        setBessTrajectory(json);
      }
    } catch (err) {
      console.error('Failed to simulate BESS thermal degradation', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBESSData();
  }, [dispatchPower, initialSoc]);

  const latest = bessTrajectory[bessTrajectory.length - 1] || {};
  const peakCoreTemp = Math.max(...bessTrajectory.map((t) => t.core_temp_c), 35.0);

  return (
    <div id="tour-bess-panel" className="glass-panel rounded-3xl p-6 border border-emerald-500/30 bg-slate-950/80 shadow-2xl space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div className="flex items-center gap-3.5">
          <div className="h-11 w-11 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 p-[1px] shadow-lg shadow-emerald-500/20">
            <div className="h-full w-full bg-slate-950 rounded-[15px] flex items-center justify-center">
              <Battery className="h-5 w-5 text-emerald-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2.5">
              <h2 className="text-lg font-bold text-white tracking-wide">
                BESS Electro-Thermal & Arrhenius SEI Degradation
              </h2>
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono uppercase tracking-wider bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
                2-State Lumped ODEs
              </span>
            </div>
            <p className="text-xs text-slate-400 font-mono mt-0.5">
              Core (Tc) vs. Surface (Ts) coupled ODEs, continuous SEI film growth & $55°C thermal runaway barrier
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className={`px-3 py-1.5 rounded-xl text-xs font-mono font-bold flex items-center gap-2 border ${
            peakCoreTemp >= 55.0
              ? 'bg-rose-500/15 text-rose-300 border-rose-500/30'
              : peakCoreTemp >= 45.0
              ? 'bg-amber-500/15 text-amber-300 border-amber-500/30'
              : 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30'
          }`}>
            {peakCoreTemp < 55.0 ? (
              <ShieldCheck className="h-4 w-4 text-emerald-400" />
            ) : (
              <Flame className="h-4 w-4 text-rose-400 animate-pulse" />
            )}
            <span>CBF BARRIER: {peakCoreTemp < 55.0 ? 'SAFE (Tc < 55°C)' : 'RUNAWAY CEILING BREACH'}</span>
          </div>
        </div>
      </div>

      {/* Sliders */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-slate-900/60 p-4 rounded-2xl border border-slate-800/80">
        <div>
          <div className="flex justify-between text-xs font-mono mb-1">
            <span className="text-slate-400">Peak BESS Discharge Power:</span>
            <span className="text-emerald-300 font-bold">{dispatchPower} MW</span>
          </div>
          <input
            type="range"
            min="0"
            max="10"
            step="0.5"
            value={dispatchPower}
            onChange={(e) => setDispatchPower(parseFloat(e.target.value))}
            className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-400"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs font-mono mb-1">
            <span className="text-slate-400">Initial State of Charge (SOC):</span>
            <span className="text-cyan-300 font-bold">{Math.round(initialSoc * 100)}%</span>
          </div>
          <input
            type="range"
            min="0.2"
            max="1.0"
            step="0.05"
            value={initialSoc}
            onChange={(e) => setInitialSoc(parseFloat(e.target.value))}
            className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-400"
          />
        </div>
      </div>

      {/* Real-time KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
          <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
            Peak Core Temperature (Tc)
          </span>
          <div className="flex items-baseline gap-2 mt-1.5">
            <span className={`text-2xl font-bold font-mono ${
              peakCoreTemp >= 55 ? 'text-rose-400' : peakCoreTemp >= 45 ? 'text-amber-300' : 'text-emerald-400'
            }`}>
              {peakCoreTemp.toFixed(1)}°C
            </span>
            <span className="text-xs text-slate-500 font-mono">/ 55°C limit</span>
          </div>
          <div className="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
            <div
              className={`h-full ${peakCoreTemp >= 55 ? 'bg-rose-500' : 'bg-emerald-500'}`}
              style={{ width: `${Math.min((peakCoreTemp / 55) * 100, 100)}%` }}
            />
          </div>
        </div>

        <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
          <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
            State of Health (SOH)
          </span>
          <div className="flex items-baseline gap-2 mt-1.5">
            <span className="text-2xl font-bold font-mono text-cyan-300">
              {latest.state_of_health_pct != null ? `${latest.state_of_health_pct}%` : '—'}
            </span>
          </div>
          <span className="text-[10px] font-mono text-slate-400 mt-1 block">
            Loss: {latest.cumulative_capacity_loss_pct != null ? `${latest.cumulative_capacity_loss_pct}%` : '—'}
          </span>
        </div>

        <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
          <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
            SEI Degradation Rate
          </span>
          <div className="flex items-baseline gap-2 mt-1.5">
            <span className="text-2xl font-bold font-mono text-amber-300">
              {latest.sei_degradation_rate_pct_per_hr ? `${(latest.sei_degradation_rate_pct_per_hr * 1000).toFixed(3)}e-3` : '0.012%'}
            </span>
            <span className="text-xs text-slate-500 font-mono">%/hr</span>
          </div>
          <span className="text-[10px] font-mono text-slate-400 mt-1 block">
            Arrhenius kinetic rate
          </span>
        </div>

        <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
          <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
            Hourly Degradation Cost
          </span>
          <div className="flex items-baseline gap-2 mt-1.5">
            <span className="text-2xl font-bold font-mono text-emerald-400">
              ${latest.hourly_degradation_cost_usd ? latest.hourly_degradation_cost_usd.toFixed(2) : '18.50'}
            </span>
            <span className="text-xs text-slate-500 font-mono">/ hour</span>
          </div>
          <span className="text-[10px] font-mono text-emerald-300/80 mt-1 block">
            Stack CAPEX: $2.50M
          </span>
        </div>
      </div>

      {/* Trajectory Table Mini Preview */}
      <div className="bg-slate-900/40 p-4 rounded-2xl border border-slate-800 overflow-x-auto">
        <h4 className="text-xs font-bold text-slate-300 font-mono uppercase tracking-wider mb-3">
          12-Hour BESS Electro-Thermal Progression Timeline
        </h4>
        <div className="grid grid-cols-6 gap-2 text-center text-xs font-mono">
          {bessTrajectory.slice(0, 6).map((step, idx) => (
            <div key={idx} className="p-2.5 rounded-xl bg-slate-950/70 border border-slate-800/80">
              <span className="text-[10px] text-slate-400 block">Hour {idx + 1} ({step.ambient_temp_c}°C)</span>
              <span className="text-cyan-300 font-bold block mt-1">{step.discharge_power_mw} MW</span>
              <span className={`text-xs block mt-0.5 ${step.core_temp_c >= 50 ? 'text-rose-400' : 'text-slate-300'}`}>
                Tc: {step.core_temp_c}°C
              </span>
              <span className="text-[10px] text-emerald-400 block mt-0.5">SOC: {step.state_of_charge_pct}%</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
