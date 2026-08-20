import React from 'react';
import {
  AlertTriangle,
  CheckCircle2,
  TrendingDown,
  DollarSign,
  Clock,
  Zap,
  BatteryCharging,
  Fan,
  Car,
  ShieldAlert,
} from 'lucide-react';
import { TrajectorySummary, SafetyGateVerdict, EconomicEvaluation, PersistenceMetrics } from '../types';

interface CommandPanelProps {
  isMitigated: boolean;
  baselineSummary: TrajectorySummary;
  mitigatedSummary: TrajectorySummary;
  verdict: SafetyGateVerdict;
  economic: EconomicEvaluation;
  persistence: PersistenceMetrics;
  currentHotSpot: number;
  currentTopOil: number;
}

export const CommandPanel: React.FC<CommandPanelProps> = ({
  isMitigated,
  baselineSummary,
  mitigatedSummary,
  verdict,
  economic,
  persistence,
  currentHotSpot,
  currentTopOil,
}) => {
  const activeSummary = isMitigated ? mitigatedSummary : baselineSummary;
  const isBreached = activeSummary.peak_hot_spot_c >= 140.0;

  return (
    <div
      className={`rounded-2xl p-5 border transition-all ${
        isBreached
          ? 'glass-panel-danger'
          : isMitigated
          ? 'glass-panel-glow'
          : 'glass-panel'
      }`}
    >
      {/* Header Status */}
      <div className="flex items-center justify-between border-b border-slate-800/80 pb-3 mb-4">
        <div className="flex items-center gap-2.5">
          <div
            className={`p-2 rounded-xl flex items-center justify-center ${
              isBreached
                ? 'bg-rose-500/20 text-rose-400 ring-1 ring-rose-500/30'
                : 'bg-emerald-500/20 text-emerald-400 ring-1 ring-emerald-500/30'
            }`}
          >
            {isBreached ? <AlertTriangle className="h-5 w-5" /> : <CheckCircle2 className="h-5 w-5" />}
          </div>
          <div>
            <div className="text-[11px] font-mono uppercase tracking-wider text-slate-400">
              PHYSICAL RESILIENCE STATE
            </div>
            <div
              className={`text-sm font-extrabold font-heading ${
                isBreached ? 'text-rose-400 animate-pulse' : 'text-emerald-400'
              }`}
            >
              {isBreached
                ? 'CRITICAL THERMAL CEILING BREACH DETECTED'
                : 'FORWARD-INVARIANT SAFE OPERATION ENFORCED'}
            </div>
          </div>
        </div>

        <span
          className={`text-xs font-mono font-bold px-3 py-1 rounded-full border ${
            isMitigated
              ? 'bg-amber-500/15 text-amber-300 border-amber-500/30'
              : 'bg-rose-500/15 text-rose-300 border-rose-500/30'
          }`}
        >
          {isMitigated ? 'SAFETY GATE ACTIVE [CBF-QP]' : 'UNGUARDED BASELINE'}
        </span>
      </div>

      {/* Grid of Key Metrics */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-4">
        {/* Metric 1: Peak Winding Hot-Spot */}
        <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800/80">
          <div className="text-[11px] text-slate-400 font-medium flex items-center justify-between">
            <span>Peak Hot-Spot (T_hs)</span>
            <span className="text-[10px] font-mono text-slate-500">Max: 140°C</span>
          </div>
          <div className="flex items-baseline gap-1.5 mt-1">
            <span
              className={`text-2xl font-black font-mono ${
                activeSummary.peak_hot_spot_c >= 140.0
                  ? 'text-rose-400'
                  : activeSummary.peak_hot_spot_c >= 130.0
                  ? 'text-amber-400'
                  : 'text-emerald-400'
              }`}
            >
              {activeSummary.peak_hot_spot_c.toFixed(1)}°C
            </span>
            <span className="text-xs text-slate-400 font-mono">
              (Current: {currentHotSpot.toFixed(1)}°)
            </span>
          </div>
          <div className="text-[10px] text-slate-400 mt-1">
            {isMitigated ? '✓ Capped safely below ceiling' : '⚠️ Breaches emergency limit'}
          </div>
        </div>

        {/* Metric 2: Persistence & Thermal Soak */}
        <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800/80">
          <div className="text-[11px] text-slate-400 font-medium flex items-center justify-between">
            <span>Continuous Persistence</span>
            <Clock className="h-3.5 w-3.5 text-amber-400" />
          </div>
          <div className="flex items-baseline gap-1.5 mt-1">
            <span className="text-2xl font-black font-mono text-amber-400">
              {persistence.persistence_hours_p40}h
            </span>
            <span className="text-xs text-slate-400 font-mono">above 40°C</span>
          </div>
          <div className="text-[10px] text-slate-400 mt-1 font-mono">
            TSI: <strong className="text-slate-200">{persistence.thermal_soak_index_tsi}</strong> · Exceedance: {persistence.exceedance_degree_hours_h40}°C·h
          </div>
        </div>

        {/* Metric 3: Failure Probability Reduction */}
        <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800/80">
          <div className="text-[11px] text-slate-400 font-medium flex items-center justify-between">
            <span>Failure Risk Delta</span>
            <TrendingDown className="h-3.5 w-3.5 text-emerald-400" />
          </div>
          <div className="flex items-baseline gap-1.5 mt-1">
            <span className="text-2xl font-black font-mono text-emerald-400">
              -{(economic.baseline_failure_probability_pct - economic.mitigated_failure_probability_pct).toFixed(1)}%
            </span>
            <span className="text-xs text-slate-400 font-mono">
              ({economic.baseline_failure_probability_pct}% → {economic.mitigated_failure_probability_pct}%)
            </span>
          </div>
          <div className="text-[10px] text-emerald-400/90 mt-1 font-medium">
            Avoided Outage Risk: ${Math.round(economic.avoided_outage_risk_usd / 1000)}k
          </div>
        </div>

        {/* Metric 4: Net Avoided Loss */}
        <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800/80">
          <div className="text-[11px] text-slate-400 font-medium flex items-center justify-between">
            <span>Net Avoided Loss (ROI)</span>
            <DollarSign className="h-3.5 w-3.5 text-amber-400" />
          </div>
          <div className="flex items-baseline gap-1.5 mt-1">
            <span className="text-2xl font-black font-mono text-amber-400">
              ${economic.net_avoided_loss_usd.toLocaleString()}
            </span>
            <span className="text-xs font-bold font-mono px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300">
              {economic.roi_multiple}x
            </span>
          </div>
          <div className="text-[10px] text-slate-400 mt-1">
            Saved <strong>{mitigatedSummary.avoided_loss_of_life_hours}h</strong> equivalent aging life
          </div>
        </div>
      </div>

      {/* Autonomous Mitigation Action Triggers */}
      {isMitigated && (
        <div className="bg-slate-950/80 p-3 rounded-xl border border-amber-500/20 flex flex-wrap items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-2 text-slate-300 font-medium">
            <Zap className="h-4 w-4 text-amber-400" />
            <span>Autonomous Mitigation Package Engaged:</span>
          </div>
          <div className="flex items-center gap-2 flex-wrap font-mono text-[11px]">
            <span className="px-2.5 py-1 rounded-lg bg-cyan-950/80 text-cyan-300 border border-cyan-800/50 flex items-center gap-1">
              <Fan className="h-3 w-3" /> Forced Cooling Stage 2 (+35%)
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-emerald-950/80 text-emerald-300 border border-emerald-800/50 flex items-center gap-1">
              <BatteryCharging className="h-3 w-3" /> BESS Peak Shaving (5.0 MW)
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-purple-950/80 text-purple-300 border border-purple-800/50 flex items-center gap-1">
              <Car className="h-3 w-3" /> EV Smart Curtailment (-0.08 pu)
            </span>
          </div>
        </div>
      )}
    </div>
  );
};
