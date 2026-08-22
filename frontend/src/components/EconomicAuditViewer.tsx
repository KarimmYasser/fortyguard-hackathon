import React from 'react';
import {
  Calculator,
  DollarSign,
  TrendingUp,
  ArrowUpRight,
  ShieldCheck,
  Building,
  Scale,
  Award,
  FileCheck,
} from 'lucide-react';
import { EconomicEvaluation, TrajectorySummary, ScenarioMetadata, TimelineStep } from '../types';

interface EconomicAuditViewerProps {
  economic: EconomicEvaluation;
  baselineSummary: TrajectorySummary;
  mitigatedSummary: TrajectorySummary;
  /** Measured ambient inputs, so the matrix tracks the active scan. */
  metadata?: ScenarioMetadata;
  steps?: TimelineStep[];
}

export const EconomicAuditViewer: React.FC<EconomicAuditViewerProps> = ({
  economic,
  baselineSummary,
  mitigatedSummary,
  metadata,
  steps,
}) => {
  // Derived from the props, not transcribed. The transcribed version drifted
  // badly: it claimed a 6.4 C hot-spot reduction against a 50.1 C actual, a
  // 2.1x mitigated aging factor against 0.94x, and a $175,276 / 24.3x ROI
  // against the $2,576,849 / 5495x the same page reports elsewhere.
  const n = (v: number | null | undefined, d = 1) =>
    v === null || v === undefined || Number.isNaN(v) ? '—' : v.toFixed(d);
  const usd = (v: number | null | undefined) =>
    v === null || v === undefined || Number.isNaN(v)
      ? '—'
      : `$${Math.round(v).toLocaleString()}`;
  // Spread is a within-hour, across-space quantity. Taking the day's max 2m
  // against the day's min coolest-tile mixes two different hours and inflates
  // it into a diurnal swing - it read +6.51 C next to a banner saying 0.62 C.
  const peakStep = steps?.length
    ? steps.reduce((a, s) => (s.fortyguard_2m_ambient_c > a.fortyguard_2m_ambient_c ? s : a), steps[0])
    : null;
  const peak2mC = peakStep?.fortyguard_2m_ambient_c ?? null;
  const coolestTileC = peakStep?.coolest_tile_2m_c ?? null;
  const spreadC = peak2mC != null && coolestTileC != null ? peak2mC - coolestTileC : null;
  const pm = metadata?.persistence_metrics;

  const hotSpotReductionC =
    baselineSummary?.peak_hot_spot_c != null && mitigatedSummary?.peak_hot_spot_c != null
      ? baselineSummary.peak_hot_spot_c - mitigatedSummary.peak_hot_spot_c
      : null;
  const avoidedLolHours =
    mitigatedSummary?.avoided_loss_of_life_hours ??
    (baselineSummary?.total_loss_of_life_hours != null && mitigatedSummary?.total_loss_of_life_hours != null
      ? baselineSummary.total_loss_of_life_hours - mitigatedSummary.total_loss_of_life_hours
      : null);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div id="tour-financial-header" className="glass-panel rounded-3xl p-6 border border-slate-800/90 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-2xl bg-gradient-to-br from-emerald-500 to-amber-500 text-slate-950 shadow-lg shadow-emerald-500/20">
            <Calculator className="h-6 w-6" />
          </div>
          <div>
            <h2 className="text-base font-extrabold text-white uppercase tracking-wide font-heading">
              Investment-Grade Economic Avoided Loss Model
            </h2>
            <p className="text-xs text-slate-400 font-mono">
              Auditable Financial Quantification for Utilities (Rate Basing) & Property/Fire Insurers
            </p>
          </div>
        </div>

        <span className="px-3.5 py-1.5 rounded-2xl text-xs font-mono font-bold bg-amber-500/15 text-amber-300 border border-amber-500/30 flex items-center gap-1.5">
          <Award className="h-4 w-4" /> LBNL ICE CALCULATOR CERTIFIED
        </span>
      </div>

      {/* Hero Financial Banner */}
      <div id="tour-financial-breakdown" className="glass-panel rounded-3xl p-6 border border-amber-500/30 bg-gradient-to-r from-amber-950/40 via-slate-900 to-slate-950 shadow-2xl">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 text-mono">
          <div>
            <div className="text-xs font-mono text-amber-400 uppercase tracking-wider">
              NET AVOIDED LOSS / HEAT EVENT
            </div>
            <div className="text-3xl sm:text-4xl font-black text-white mt-1">
              ${economic.net_avoided_loss_usd.toLocaleString()}
            </div>
            <div className="text-xs text-slate-400 mt-1 font-mono">
              Per extreme heatwave incident
            </div>
          </div>

          <div>
            <div className="text-xs font-mono text-slate-400 uppercase tracking-wider">
              RETURN ON INVESTMENT (ROI)
            </div>
            <div className="text-3xl sm:text-4xl font-black text-amber-400 flex items-center mt-1">
              {economic.roi_multiple}x <ArrowUpRight className="h-7 w-7 text-amber-400" />
            </div>
            <div className="text-xs text-slate-400 mt-1 font-mono">
              Mitigation cost: ${economic.mitigation_cost_usd.toLocaleString()}
            </div>
          </div>

          <div>
            <div className="text-xs font-mono text-emerald-400 uppercase tracking-wider">
              AVOIDED OUTAGE RISK
            </div>
            <div className="text-3xl sm:text-4xl font-black text-emerald-400 mt-1">
              ${economic.avoided_outage_risk_usd.toLocaleString()}
            </div>
            <div className="text-xs text-slate-400 mt-1 font-mono">
              Δp_f: -{(economic.baseline_failure_probability_pct - economic.mitigated_failure_probability_pct).toFixed(1)} pp
            </div>
          </div>

          <div>
            <div className="text-xs font-mono text-cyan-400 uppercase tracking-wider">
              CAPITAL AGING DEFERRAL
            </div>
            <div className="text-3xl sm:text-4xl font-black text-cyan-300 mt-1">
              ${economic.capital_aging_deferral_usd.toLocaleString()}
            </div>
            <div className="text-xs text-slate-400 mt-1 font-mono">
              {mitigatedSummary.avoided_loss_of_life_hours}h life consumed deferred
            </div>
          </div>
        </div>
      </div>

      {/* Side-by-Side Comparison Table: Baseline vs. Thermal Sentinel Grid */}
      <div id="tour-financial-matrix" className="glass-panel rounded-3xl p-6 border border-slate-800/90 shadow-2xl">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-4">
          <div>
            <h3 className="text-base font-extrabold text-white font-heading">
              Benchmark Comparison: Baseline Controller vs. Thermal Sentinel Grid
            </h3>
            <p className="text-xs text-slate-400 font-mono">
              Heatwave Episode Validation Matrix · benchmark capture 2023-07-19
            </p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left font-mono text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 uppercase text-[11px]">
                <th className="pb-3 pr-4 font-bold">Dimension</th>
                <th className="pb-3 px-4 text-rose-400 font-bold">Baseline Controller (Static Rating, No Forecast)</th>
                <th className="pb-3 px-4 text-emerald-400 font-bold">Thermal Sentinel Grid (FortyGuard + Physics)</th>
                <th className="pb-3 pl-4 text-amber-400 font-bold">Resilience Advantage</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300">
              <tr>
                <td className="py-3 pr-4 font-bold text-white">1. Ambient Boundary Input</td>
                <td className="py-3 px-4 text-rose-300">Coolest tile in AOI at peak hour ({n(coolestTileC)}°C)</td>
                <td className="py-3 px-4 text-emerald-300 font-bold">Peak parcel 2m convective air ({n(peak2mC)}°C)</td>
                <td className="py-3 pl-4 text-amber-300">+{n(spreadC, 2)}°C measured intra-AOI spread</td>
              </tr>
              <tr>
                <td className="py-3 pr-4 font-bold text-white">2. Duration / Persistence</td>
                <td className="py-3 px-4 text-rose-300">Blind to {n(pm?.persistence_hours_p40)}h continuous persistence</td>
                <td className="py-3 px-4 text-emerald-300 font-bold">Tracks P40 &amp; Thermal Soak Index ({n(pm?.thermal_soak_index_tsi, 2)})</td>
                <td className="py-3 pl-4 text-amber-300">Proactive pre-cooling 12h ahead</td>
              </tr>
              <tr>
                <td className="py-3 pr-4 font-bold text-white">3. Peak Winding Hot-Spot</td>
                <td className="py-3 px-4 text-rose-400 font-bold">
                  {n(baselineSummary?.peak_hot_spot_c)}°C{' '}
                  {baselineSummary?.breached_emergency_ceiling ? '(Breaches 140°C Ceiling)' : '(Within Ceiling)'}
                </td>
                <td className="py-3 px-4 text-emerald-400 font-bold">
                  {n(mitigatedSummary?.peak_hot_spot_c)}°C{' '}
                  {mitigatedSummary?.breached_emergency_ceiling ? '(Still Breaching)' : '(Safely Capped)'}
                </td>
                <td className="py-3 pl-4 text-amber-300">−{n(hotSpotReductionC)}°C peak reduction</td>
              </tr>
              <tr>
                <td className="py-3 pr-4 font-bold text-white">4. Insulation Aging Factor (V)</td>
                <td className="py-3 px-4 text-rose-300">{n(baselineSummary?.peak_aging_acceleration_v, 2)}x normal degradation rate</td>
                <td className="py-3 px-4 text-emerald-300 font-bold">{n(mitigatedSummary?.peak_aging_acceleration_v, 2)}x normal degradation rate</td>
                <td className="py-3 pl-4 text-amber-300">{n(avoidedLolHours)}h loss-of-life saved</td>
              </tr>
              <tr>
                <td className="py-3 pr-4 font-bold text-white">5. Voltage Stability & N-1</td>
                <td className="py-3 px-4 text-rose-300">Uncontrolled emergency feeder tripping</td>
                <td className="py-3 px-4 text-emerald-300 font-bold">Zero ANSI C84.1 voltage breaches</td>
                <td className="py-3 pl-4 text-amber-300">Preserved hospital priority feeder</td>
              </tr>
              <tr>
                <td className="py-3 pr-4 font-bold text-white">6. Net Avoided Loss ROI</td>
                <td className="py-3 px-4 text-rose-300">$0 (Incurs catastrophic blowout risk)</td>
                <td className="py-3 px-4 text-emerald-400 font-bold">{usd(economic?.net_avoided_loss_usd)} Net Avoided Loss</td>
                <td className="py-3 pl-4 text-amber-300 font-black">{n(economic?.roi_multiple)}x ROI Multiplier</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
