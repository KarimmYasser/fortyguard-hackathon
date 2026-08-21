import React, { useState, useEffect } from 'react';
import { AlertOctagon, ShieldCheck, Flame, Zap, DollarSign, Activity } from 'lucide-react';
import { API_BASE } from '../utils/api';

interface CascadingHazardGaugeProps {
  isMitigatedMode?: boolean;
}

export const CascadingHazardGauge: React.FC<CascadingHazardGaugeProps> = ({ isMitigatedMode = false }) => {
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchHazard = async () => {
    setLoading(true);
    try {
      const resp = await fetch(`${API_BASE}/api/v1/physics/cascading-hazard?is_mitigated=${isMitigatedMode}`);
      if (resp.ok) {
        const json = await resp.json();
        setReport(json);
      }
    } catch (err) {
      console.error('Failed to fetch cascading hazard report', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHazard();
  }, [isMitigatedMode]);

  if (!report) {
    return (
      <div className="glass-panel rounded-3xl p-6 text-center text-slate-400 font-mono">
        Computing Arrhenius-Weibull Grid Fragility...
      </div>
    );
  }

  const riskPct = report.system_cascading_risk_pct;
  const isHighRisk = riskPct >= 10.0;

  return (
    <div id="tour-hazard-gauge" className="glass-panel rounded-3xl p-6 border border-rose-500/30 bg-slate-950/80 shadow-2xl space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div className="flex items-center gap-3.5">
          <div className="h-11 w-11 rounded-2xl bg-gradient-to-br from-rose-500 to-amber-600 p-[1px] shadow-lg shadow-rose-500/20">
            <div className="h-full w-full bg-slate-950 rounded-[15px] flex items-center justify-center">
              <AlertOctagon className="h-5 w-5 text-rose-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2.5">
              <h2 className="text-lg font-bold text-white tracking-wide">
                Arrhenius-Weibull Grid Fragility & Cascading Outage Risk
              </h2>
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono uppercase tracking-wider bg-rose-500/15 text-rose-300 border border-rose-500/30">
                Poisson-Weibull λ(t,T)
              </span>
            </div>
            <p className="text-xs text-slate-400 font-mono mt-0.5">
              Time-dependent thermal failure hazard integration & joint cascading blackout probability
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className={`px-3 py-1.5 rounded-xl text-xs font-mono font-bold flex items-center gap-2 border ${
            isHighRisk
              ? 'bg-rose-500/15 text-rose-300 border-rose-500/30'
              : 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30'
          }`}>
            {isHighRisk ? (
              <Flame className="h-4 w-4 text-rose-400 animate-pulse" />
            ) : (
              <ShieldCheck className="h-4 w-4 text-emerald-400" />
            )}
            <span>CASCADING RISK: {riskPct.toFixed(1)}%</span>
          </div>
        </div>
      </div>

      {/* Main KPI Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
          <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
            Joint Cascading Blackout Risk
          </span>
          <div className="flex items-baseline gap-2 mt-1.5">
            <span className={`text-3xl font-bold font-mono ${isHighRisk ? 'text-rose-400' : 'text-emerald-400'}`}>
              {riskPct.toFixed(1)}%
            </span>
            <span className="text-xs text-slate-500 font-mono">/ 12h heatwave</span>
          </div>
          <div className="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
            <div
              className={`h-full ${isHighRisk ? 'bg-rose-500' : 'bg-emerald-500'}`}
              style={{ width: `${Math.min(riskPct * 4, 100)}%` }}
            />
          </div>
        </div>

        <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
          <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
            N-1 Contingency Reserve Margin
          </span>
          <div className="flex items-baseline gap-2 mt-1.5">
            <span className={`text-2xl font-bold font-mono ${
              report.n_minus_1_reserve_margin_pct < 10 ? 'text-rose-400' : 'text-cyan-300'
            }`}>
              {report.n_minus_1_reserve_margin_pct}%
            </span>
          </div>
          <span className="text-[10px] font-mono text-slate-400 mt-1 block">
            {report.n_minus_1_reserve_margin_pct < 10 ? '⚠️ Critical N-1 Deficit' : '✅ Compliant Reserve'}
          </span>
        </div>

        <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
          <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
            Expected Unserved Energy
          </span>
          <div className="flex items-baseline gap-2 mt-1.5">
            <span className="text-2xl font-bold font-mono text-amber-300">
              {report.expected_unserved_energy_mwh} MWh
            </span>
          </div>
          <span className="text-[10px] font-mono text-slate-400 mt-1 block">
            Customer load at risk
          </span>
        </div>

        <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
          <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
            Value of Lost Load (VoLL) Risk
          </span>
          <div className="flex items-baseline gap-2 mt-1.5">
            <span className={`text-2xl font-bold font-mono ${isHighRisk ? 'text-rose-400' : 'text-emerald-400'}`}>
              ${(report.economic_loss_risk_usd / 1000).toFixed(1)}k
            </span>
          </div>
          <span className="text-[10px] font-mono text-slate-400 mt-1 block">
            @ $18,500/MWh LBNL benchmark
          </span>
        </div>
      </div>

      {/* Asset Breakdown Cards */}
      <div className="space-y-3">
        <h4 className="text-xs font-bold text-slate-300 font-mono uppercase tracking-wider">
          Individual Asset Vulnerability & Arrhenius Acceleration (AF)
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {(report.assets || []).map((asset: any, idx: number) => (
            <div key={idx} className="bg-slate-900/60 p-4 rounded-2xl border border-slate-800 space-y-2">
              <div className="flex justify-between items-start">
                <div>
                  <span className="text-xs font-bold text-white block">{asset.asset_name}</span>
                  <span className="text-[10px] font-mono text-slate-400">{asset.asset_id} ({asset.asset_type})</span>
                </div>
                <span className={`px-2 py-0.5 rounded-full text-[10px] font-mono font-bold ${
                  asset.risk_tier === 'CRITICAL_TRIP'
                    ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                    : asset.risk_tier === 'ELEVATED'
                    ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                    : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                }`}>
                  {asset.risk_tier}
                </span>
              </div>

              <div className="grid grid-cols-2 gap-2 text-xs font-mono pt-1">
                <div>
                  <span className="text-slate-400 text-[10px] block">Hot-Spot Temp:</span>
                  <span className="text-cyan-300 font-bold">{asset.hot_spot_temp_c}°C</span>
                </div>
                <div>
                  <span className="text-slate-400 text-[10px] block">Arrhenius AF:</span>
                  <span className="text-amber-300 font-bold">{asset.arrhenius_acceleration_factor}x</span>
                </div>
                <div>
                  <span className="text-slate-400 text-[10px] block">12h Failure Prob:</span>
                  <span className={`font-bold ${asset.cumulative_failure_probability_pct > 10 ? 'text-rose-400' : 'text-emerald-400'}`}>
                    {asset.cumulative_failure_probability_pct}%
                  </span>
                </div>
                <div>
                  <span className="text-slate-400 text-[10px] block">Hazard λ(t):</span>
                  <span className="text-slate-300 font-bold">{asset.instantaneous_hazard_rate_per_year}/yr</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recommendation Banner */}
      <div className="bg-slate-900/40 p-3.5 rounded-2xl border border-slate-800 flex items-center gap-3">
        <Activity className="h-5 w-5 text-cyan-400 shrink-0" />
        <p className="text-xs text-slate-300 font-mono">
          <span className="text-cyan-300 font-bold uppercase">Dispatcher Directive:</span> {report.recommendation}
        </p>
      </div>
    </div>
  );
};
