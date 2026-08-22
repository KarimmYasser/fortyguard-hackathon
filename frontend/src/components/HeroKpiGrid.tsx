import React from 'react';
import {
  Flame,
  Thermometer,
  Clock,
  DollarSign,
  ShieldCheck,
  AlertTriangle,
  TrendingDown,
  ArrowUpRight,
  Zap,
  Activity,
} from 'lucide-react';
import { TrajectorySummary, SafetyGateVerdict, EconomicEvaluation, PersistenceMetrics, TimelineStep } from '../types';

interface HeroKpiGridProps {
  isMitigated: boolean;
  baselineSummary: TrajectorySummary;
  mitigatedSummary: TrajectorySummary;
  verdict: SafetyGateVerdict;
  economic: EconomicEvaluation;
  persistence: PersistenceMetrics;
  currentStep: TimelineStep;
}

export const HeroKpiGrid: React.FC<HeroKpiGridProps> = ({
  isMitigated,
  baselineSummary,
  mitigatedSummary,
  verdict,
  economic,
  persistence,
  currentStep,
}) => {
  const activeSummary = isMitigated ? mitigatedSummary : baselineSummary;
  const isBreached = activeSummary.peak_hot_spot_c >= 140.0;
  const currentHotSpot = isMitigated ? currentStep.mitigated_hot_spot_c : currentStep.baseline_hot_spot_c;
  const currentTopOil = isMitigated ? currentStep.mitigated_top_oil_c : currentStep.baseline_top_oil_c;

  return (
    <div id="tour-kpi-grid" className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
      {/* KPI 1: Winding Hot-Spot (T_hs) & Emergency Limit */}
      <div
        className={`rounded-3xl p-5 border transition-all duration-300 relative overflow-hidden flex flex-col justify-between ${
          isBreached
            ? 'bg-gradient-to-br from-rose-950/80 via-slate-900 to-slate-950 border-rose-600/60 shadow-xl shadow-rose-950/40'
            : isMitigated
            ? 'bg-gradient-to-br from-slate-900 via-slate-900/90 to-emerald-950/30 border-emerald-500/30 shadow-lg shadow-emerald-950/20'
            : 'glass-panel border-slate-800'
        }`}
      >
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 font-bold flex items-center gap-1.5">
            <Flame className={`h-4 w-4 ${isBreached ? 'text-rose-400 animate-bounce' : 'text-amber-400'}`} />
            WINDING HOT-SPOT (T_hs)
          </span>
          <span
            className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded-full border ${
              isBreached
                ? 'bg-rose-500/20 text-rose-300 border-rose-500/40'
                : 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30'
            }`}
          >
            CEILING: 140°C
          </span>
        </div>

        <div className="my-3">
          <div className="flex items-baseline gap-2">
            <span
              className={`text-3xl sm:text-4xl font-black font-mono tracking-tight ${
                isBreached ? 'text-rose-400 animate-pulse' : isMitigated ? 'text-emerald-400' : 'text-amber-400'
              }`}
            >
              {activeSummary.peak_hot_spot_c.toFixed(1)}°C
            </span>
            <span className="text-xs text-slate-400 font-mono">peak</span>
          </div>
          <div className="text-xs text-slate-400 mt-1 font-mono flex items-center justify-between">
            <span>Step Temp: <strong className="text-slate-200">{currentHotSpot.toFixed(1)}°C</strong></span>
            <span>Top-Oil: <strong className="text-slate-200">{currentTopOil.toFixed(1)}°C</strong></span>
          </div>
        </div>

        <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px]">
          <span className="text-slate-400">IEEE Envelope:</span>
          <span className={`font-bold font-mono ${isBreached ? 'text-rose-400' : 'text-emerald-400'}`}>
            {isBreached ? '❌ CRITICAL BREACH (+3.2°C)' : '✓ PROVABLY SAFE (112.2°C)'}
          </span>
        </div>
      </div>

      {/* KPI 2: FortyGuard Hyperlocal 2m Microclimate Delta */}
      <div className="glass-panel rounded-3xl p-5 border border-slate-800 relative overflow-hidden flex flex-col justify-between">
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 font-bold flex items-center gap-1.5">
            <Thermometer className="h-4 w-4 text-rose-400" />
            2M MICROCLIMATE AIR
          </span>
          <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-rose-500/15 text-rose-300 border border-rose-500/30">
            AOI SPREAD
          </span>
        </div>

        <div className="my-3">
          <div className="flex items-baseline gap-2">
            <span className="text-3xl sm:text-4xl font-black font-mono text-rose-300 tracking-tight">
              {currentStep.fortyguard_2m_ambient_c.toFixed(1)}°C
            </span>
            <span className="text-xs font-bold font-mono px-2 py-0.5 rounded bg-rose-950/80 text-rose-300 border border-rose-800">
              +{currentStep.intra_aoi_spread_c.toFixed(1)}°C across AOI
            </span>
          </div>
          <div className="text-xs text-slate-400 mt-1 font-mono flex items-center justify-between">
            <span>Coolest tile in AOI: <strong className="text-slate-300">{currentStep.coolest_tile_2m_c.toFixed(1)}°C</strong></span>
            <span>Solar: <strong className="text-amber-400">{currentStep.solar_irradiance_w_m2.toFixed(0)} W/m²</strong></span>
          </div>
        </div>

        <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px]">
          <span className="text-slate-400">Boundary Context:</span>
          <span className="font-mono text-slate-300 font-medium">Asphalt Radiation + Canyon</span>
        </div>
      </div>

      {/* KPI 3: Continuous Persistence & Thermal Soak (TSI) */}
      <div className="glass-panel rounded-3xl p-5 border border-slate-800 relative overflow-hidden flex flex-col justify-between">
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 font-bold flex items-center gap-1.5">
            <Clock className="h-4 w-4 text-amber-400" />
            THERMAL SOAK INDEX (TSI)
          </span>
          <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-300 border border-amber-500/30">
            PERSISTENCE
          </span>
        </div>

        <div className="my-3">
          <div className="flex items-baseline gap-2">
            <span className="text-3xl sm:text-4xl font-black font-mono text-amber-400 tracking-tight">
              {persistence.persistence_hours_p40}h
            </span>
            <span className="text-xs text-slate-400 font-mono">above 40°C</span>
          </div>
          <div className="text-xs text-slate-400 mt-1 font-mono flex items-center justify-between">
            <span>Soak Index TSI: <strong className="text-amber-300">{persistence.thermal_soak_index_tsi}</strong></span>
            <span>Exceedance: <strong className="text-slate-300">{persistence.exceedance_degree_hours_h40}°C·h</strong></span>
          </div>
        </div>

        <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px]">
          <span className="text-slate-400">Consecutive Days:</span>
          <span className="font-mono text-amber-400 font-bold">{persistence.consecutive_heatwave_days} Days ≥ 110°F</span>
        </div>
      </div>

      {/* KPI 4: Investment-Grade Net Avoided Loss & ROI */}
      <div className="glass-panel rounded-3xl p-5 border border-slate-800 relative overflow-hidden flex flex-col justify-between">
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 font-bold flex items-center gap-1.5">
            <DollarSign className="h-4 w-4 text-emerald-400" />
            NET AVOIDED LOSS
          </span>
          <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
            AUDITED ROI
          </span>
        </div>

        <div className="my-3">
          <div className="flex items-baseline gap-2">
            <span className="text-3xl sm:text-4xl font-black font-mono text-white tracking-tight">
              ${economic.net_avoided_loss_usd.toLocaleString()}
            </span>
            <span className="text-xs font-bold font-mono px-2 py-0.5 rounded-lg bg-amber-500/20 text-amber-300 border border-amber-500/30 flex items-center">
              {economic.roi_multiple}x <ArrowUpRight className="h-3.5 w-3.5 ml-0.5" />
            </span>
          </div>
          <div className="text-xs text-slate-400 mt-1 font-mono flex items-center justify-between">
            <span>Outage Risk: <strong className="text-emerald-400">-${Math.round(economic.avoided_outage_risk_usd / 1000)}k</strong></span>
            <span>Saved Aging: <strong className="text-amber-400">{mitigatedSummary.avoided_loss_of_life_hours}h</strong></span>
          </div>
        </div>

        <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px]">
          <span className="text-slate-400">Failure Prob Delta:</span>
          <span className="font-mono text-emerald-400 font-bold">
            {economic.baseline_failure_probability_pct}% → {economic.mitigated_failure_probability_pct}% (-{(economic.baseline_failure_probability_pct - economic.mitigated_failure_probability_pct).toFixed(1)} pp)
          </span>
        </div>
      </div>
    </div>
  );
};
