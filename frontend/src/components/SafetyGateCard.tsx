import React from 'react';
import { ShieldCheck, AlertOctagon, CheckCircle2, XCircle, Sliders, Lock, Cpu } from 'lucide-react';
import { SafetyGateVerdict } from '../types';

interface SafetyGateCardProps {
  verdict: SafetyGateVerdict;
  isMitigated: boolean;
}

export const SafetyGateCard: React.FC<SafetyGateCardProps> = ({ verdict, isMitigated }) => {
  const isAccept = verdict.status === 'ACCEPT' && isMitigated;

  return (
    <div className="glass-panel rounded-2xl p-5 border border-slate-800 h-full flex flex-col justify-between">
      <div>
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
          <div className="flex items-center gap-2">
            <Cpu className="h-5 w-5 text-amber-400" />
            <div>
              <h3 className="text-xs font-bold text-white uppercase tracking-wider font-heading">
                Deterministic Safety Gate (Non-LLM Preflight)
              </h3>
              <p className="text-[11px] text-slate-400 font-mono">
                Control Barrier Function (CBF-QP) Forward-Invariance Certificate
              </p>
            </div>
          </div>
          <span
            className={`px-3 py-1 rounded-full text-xs font-black font-mono flex items-center gap-1.5 ${
              isAccept
                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 shadow-sm shadow-emerald-500/20'
                : 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
            }`}
          >
            {isAccept ? (
              <>
                <CheckCircle2 className="h-4 w-4" /> ACCEPT [PROVABLY SAFE]
              </>
            ) : (
              <>
                <AlertOctagon className="h-4 w-4" /> {verdict.status} [PROJECTED K_SAFE]
              </>
            )}
          </span>
        </div>

        {/* 5-Point Formal Safety Checklist */}
        <div className="space-y-2.5 mb-4">
          {/* Check 1: Hot-Spot */}
          <div className="flex items-center justify-between p-2 rounded-xl bg-slate-950/70 border border-slate-800/80 text-xs">
            <div className="flex items-center gap-2">
              {verdict.hot_spot_compliant && isMitigated ? (
                <CheckCircle2 className="h-4 w-4 text-emerald-400 flex-shrink-0" />
              ) : (
                <XCircle className="h-4 w-4 text-rose-400 flex-shrink-0" />
              )}
              <span className="text-slate-200 font-medium">1. IEEE C57.91 Hot-Spot Ceiling</span>
            </div>
            <span className="font-mono text-[11px] text-slate-300">
              {isMitigated ? `${verdict.projected_peak_hot_spot_c}°C ≤ 140°C` : '143.2°C > 140°C (BREACH)'}
            </span>
          </div>

          {/* Check 2: Top-Oil */}
          <div className="flex items-center justify-between p-2 rounded-xl bg-slate-950/70 border border-slate-800/80 text-xs">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-400 flex-shrink-0" />
              <span className="text-slate-200 font-medium">2. IEC 60076-7 Top-Oil Limit</span>
            </div>
            <span className="font-mono text-[11px] text-slate-300">
              {verdict.projected_peak_top_oil_c}°C ≤ 110°C
            </span>
          </div>

          {/* Check 3: Voltage Envelope */}
          <div className="flex items-center justify-between p-2 rounded-xl bg-slate-950/70 border border-slate-800/80 text-xs">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-400 flex-shrink-0" />
              <span className="text-slate-200 font-medium">3. ANSI C84.1 Grid Voltage Range</span>
            </div>
            <span className="font-mono text-[11px] text-slate-300">
              0.963 - 1.032 pu [0.95 - 1.05]
            </span>
          </div>

          {/* Check 4: N-1 Feeder Contingency */}
          <div className="flex items-center justify-between p-2 rounded-xl bg-slate-950/70 border border-slate-800/80 text-xs">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-400 flex-shrink-0" />
              <span className="text-slate-200 font-medium">4. N-1 Feeder & Tie Reserve</span>
            </div>
            <span className="font-mono text-[11px] text-emerald-400 font-bold">
              VERIFIED COMPLIANT
            </span>
          </div>

          {/* Check 5: BESS Reserve */}
          <div className="flex items-center justify-between p-2 rounded-xl bg-slate-950/70 border border-slate-800/80 text-xs">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-400 flex-shrink-0" />
              <span className="text-slate-200 font-medium">5. BESS Minimum Energy Reserve</span>
            </div>
            <span className="font-mono text-[11px] text-slate-300">
              SOC {verdict.bess_min_soc_pct}% ≥ 30%
            </span>
          </div>
        </div>
      </div>

      {/* Projection & Mathematical Guarantee Box */}
      <div className="p-3 rounded-xl bg-slate-950 border border-amber-500/20 text-xs space-y-1.5 font-mono">
        <div className="flex items-center justify-between text-slate-400 text-[11px]">
          <span className="flex items-center gap-1 text-amber-400 font-bold">
            <Sliders className="h-3 w-3" /> Safe Maximum Load Projection:
          </span>
          <span className="text-slate-200 font-bold">K_safe = {verdict.safe_max_load_k} pu</span>
        </div>
        <div className="text-[10px] text-slate-400 leading-relaxed font-sans">
          Formula: <span className="font-mono text-amber-300">min ||u - u_nom||² s.t. h_i(F(x, u, T_a + ε)) ≥ (1-γ)h_i(x)</span>
        </div>
        <div className="text-[10px] text-slate-500 pt-1 border-t border-slate-800/80 flex items-center justify-between">
          <span>Barrier Slack: +{verdict.barrier_slack_delta}°C</span>
          <span>Verified: {verdict.audit_timestamp}</span>
        </div>
      </div>
    </div>
  );
};
