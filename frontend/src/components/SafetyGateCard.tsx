import React from 'react';
import { ShieldCheck, AlertOctagon, CheckCircle2, XCircle, Sliders, Lock, Cpu } from 'lucide-react';
import { SafetyGateVerdict } from '../types';
import { MathView } from './MathView';

interface SafetyGateCardProps {
  verdict: SafetyGateVerdict;
  isMitigated: boolean;
}

export const SafetyGateCard: React.FC<SafetyGateCardProps> = ({ verdict, isMitigated }) => {
  const isAccept = verdict.status === 'ACCEPT' && isMitigated;

  return (
    <div id="tour-safety-gate" className="glass-panel rounded-2xl p-5 border border-slate-800 h-full flex flex-col justify-between">
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
                CBF-inspired bounded-trajectory model check · no field certification
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
                <CheckCircle2 className="h-4 w-4" /> ACCEPT [MODEL LIMITS]
              </>
            ) : (
              <>
                <AlertOctagon className="h-4 w-4" /> REJECT [OVERRIDE ACTIVE]
              </>
            )}
          </span>
        </div>

        {/* 5-Point Safety Checks */}
        <div className="space-y-2 mb-4">
          {/* Check 1: Top-Oil */}
          <div className="flex items-center justify-between p-2 rounded-xl bg-slate-950/70 border border-slate-800/80 text-xs">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-400 flex-shrink-0" />
              <span className="text-slate-200 font-medium">1. Top-Oil Temperature Margin</span>
            </div>
            <span className="font-mono text-[11px] text-slate-300">
              {verdict.projected_peak_top_oil_c}°C ≤ 110°C
            </span>
          </div>

          {/* Check 2: Winding Hot-Spot */}
          <div className="flex items-center justify-between p-2 rounded-xl bg-slate-950/70 border border-slate-800/80 text-xs">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-400 flex-shrink-0" />
              <span className="text-slate-200 font-medium">2. Hot-Spot Thermal Limit</span>
            </div>
            <span className="font-mono text-[11px] text-slate-300">
              {verdict.projected_peak_hot_spot_c}°C ≤ 140°C
            </span>
          </div>

          {/* Check 3: Voltage Band */}
          <div className="flex items-center justify-between p-2 rounded-xl bg-slate-950/70 border border-slate-800/80 text-xs">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-400 flex-shrink-0" />
              <span className="text-slate-200 font-medium">3. ANSI C84.1 Voltage Band</span>
            </div>
            <span className="font-mono text-[11px] text-slate-300">
              {verdict.voltage_pu_min}–{verdict.voltage_pu_max} pu [0.95–1.05]
            </span>
          </div>

          {/* Check 4: Transformer MVA Loading */}
          <div className="flex items-center justify-between p-2 rounded-xl bg-slate-950/70 border border-slate-800/80 text-xs">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-400 flex-shrink-0" />
              <span className="text-slate-200 font-medium">4. Dynamic Loading Ceiling</span>
            </div>
            <span className="font-mono text-[11px] text-slate-300">
              K = {verdict.nominal_load_k} pu ≤ {verdict.safe_max_load_k} pu
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

      {/* Projection and model-constraint box */}
      <div className="p-3 rounded-xl bg-slate-950 border border-amber-500/20 text-xs space-y-2 font-mono">
        <div className="flex items-center justify-between text-slate-400 text-[11px]">
          <span className="flex items-center gap-1.5 text-amber-400 font-bold">
            <Sliders className="h-3.5 w-3.5" /> Safe Maximum Load Projection:
          </span>
          <span className="text-slate-200 font-bold bg-slate-900 px-2 py-0.5 rounded border border-slate-800">
            <MathView math={`K_{\\text{safe}} = ${verdict.safe_max_load_k}\\,\\text{pu}`} displayMode={false} className="text-amber-300 font-bold" />
          </span>
        </div>
        
        <div className="p-2.5 rounded-lg bg-slate-900/90 border border-slate-800/80 text-center overflow-hidden text-amber-200 flex items-center justify-center min-h-[48px] w-full">
          <MathView math="K_{\text{safe}} = \max\{K : T_o(K) \le T_{o,\max},\; T_{hs}(K) \le T_{hs,\max},\; 0.95 \le V(K) \le 1.05\}" scale="sm" />
        </div>


        <div className="text-[10px] text-slate-500 pt-1 border-t border-slate-800/80 flex items-center justify-between">
          <span>Barrier Slack: +{verdict.barrier_slack_delta}°C</span>
          <span>Verified: {verdict.audit_timestamp}</span>
        </div>
      </div>
    </div>
  );
};
