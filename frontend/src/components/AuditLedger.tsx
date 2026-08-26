import { BENCHMARK } from '../constants/benchmark';
import React from 'react';
import { ScrollText, CheckCircle2, AlertCircle, ArrowRight, ShieldCheck } from 'lucide-react';

export interface AuditLogEntry {
  timestamp: string;
  category: 'INGEST' | 'PHYSICS' | 'SAFETY_GATE' | 'DISPATCH' | 'OPERATOR';
  message: string;
  status: 'SUCCESS' | 'WARN' | 'INFO';
}

const DEFAULT_AUDIT_LOG: AuditLogEntry[] = [
  {
    timestamp: '14:05:12 UTC',
    category: 'INGEST',
    message: `FortyGuard 2-meter API: Ingested ${BENCHMARK.persistenceHoursP40}h continuous persistence (>${BENCHMARK.thresholdC}°C) and 12h forward forecast (${BENCHMARK.peak2mC}°C peak, live capture ${BENCHMARK.analysisDate}).`,
    status: 'INFO',
  },
  {
    timestamp: '14:05:15 UTC',
    category: 'PHYSICS',
    message: `IEEE C57.91 Solver: Baseline controller projects ${BENCHMARK.baseline.hotSpotC}°C hot-spot (breaches ${BENCHMARK.hotSpotLimitC}°C emergency ceiling). Aging factor V = ${BENCHMARK.baseline.agingAccelerationX}x.`,
    status: 'WARN',
  },
  {
    timestamp: '14:05:18 UTC',
    category: 'PHYSICS',
    message: 'IEC 60287 multi-physics: Detected soil dryout surge (ρ = 2.45 K·m/W) and urban canyon cooling derate (η_cool = 0.68).',
    status: 'INFO',
  },
  {
    timestamp: '14:05:22 UTC',
    category: 'SAFETY_GATE',
    message: 'Non-LLM trajectory gate: checked candidate plan and projected a safe maximum load against configured model limits.',
    status: 'SUCCESS',
  },
  {
    timestamp: '14:05:25 UTC',
    category: 'DISPATCH',
    message: 'Autonomous Dispatch: Engaged Forced Cooling Stage 2 (+35%) and 5.0 MW BESS peak shaving. Preserved hospital feeder voltage (0.982 pu).',
    status: 'SUCCESS',
  },
  {
    timestamp: '14:05:30 UTC',
    category: 'OPERATOR',
    message: `Economic Audit Ledger: Verified $${BENCHMARK.netAvoidedLossUsd.toLocaleString()} net avoided loss (${BENCHMARK.roiMultiple}x ROI) and ${BENCHMARK.avoidedAgingHours} avoided loss-of-life equivalent hours.`,
    status: 'SUCCESS',
  },
];

export const AuditLedger: React.FC = () => {
  return (
    <div id="tour-audit-ledger" className="glass-panel rounded-2xl p-5 border border-slate-800">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-3">
        <div className="flex items-center gap-2">
          <ScrollText className="h-5 w-5 text-amber-400" />
          <div>
            <h3 className="text-xs font-bold text-white uppercase tracking-wider font-heading">
              Explainable Decision & Safety Audit Ledger
            </h3>
            <p className="text-[11px] text-slate-400 font-mono">
              Immutable physical provenance and action dispatch trail
            </p>
          </div>
        </div>
        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          ALL GATES VERIFIED
        </span>
      </div>

      <div className="space-y-2 font-mono text-xs max-h-48 overflow-y-auto pr-1">
        {DEFAULT_AUDIT_LOG.map((log, index) => (
          <div
            key={index}
            className="flex items-start gap-2.5 p-2 rounded-xl bg-slate-950/60 border border-slate-800/70 hover:border-slate-700 transition-all"
          >
            <span className="text-[10px] text-slate-500 font-mono whitespace-nowrap pt-0.5">
              {log.timestamp}
            </span>
            <span
              className={`text-[9px] px-1.5 py-0.2 rounded font-bold uppercase ${
                log.category === 'SAFETY_GATE'
                  ? 'bg-purple-950 text-purple-300 border border-purple-800'
                  : log.category === 'PHYSICS'
                  ? 'bg-amber-950 text-amber-300 border border-amber-800'
                  : log.category === 'DISPATCH'
                  ? 'bg-emerald-950 text-emerald-300 border border-emerald-800'
                  : 'bg-slate-900 text-slate-400 border border-slate-800'
              }`}
            >
              {log.category}
            </span>
            <span className="text-slate-300 font-sans text-xs flex-1 leading-snug">
              {log.message}
            </span>
            {log.status === 'SUCCESS' && <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400 flex-shrink-0 mt-0.5" />}
            {log.status === 'WARN' && <AlertCircle className="h-3.5 w-3.5 text-rose-400 flex-shrink-0 mt-0.5" />}
          </div>
        ))}
      </div>
    </div>
  );
};
