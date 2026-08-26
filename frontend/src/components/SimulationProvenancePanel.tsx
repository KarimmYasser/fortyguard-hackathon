import React from 'react';
import { AlertTriangle, Database, Gauge, Radio, Sigma } from 'lucide-react';
import type { EvidenceKind, SimulationProvenance } from '../types';

const styles: Record<EvidenceKind, string> = {
  measured: 'border-emerald-500/30 bg-emerald-500/10 text-emerald-300',
  externally_modelled: 'border-sky-500/30 bg-sky-500/10 text-sky-300',
  derived: 'border-cyan-500/30 bg-cyan-500/10 text-cyan-300',
  assumed: 'border-amber-500/30 bg-amber-500/10 text-amber-300',
  simulated: 'border-violet-500/30 bg-violet-500/10 text-violet-300',
  validated: 'border-teal-500/30 bg-teal-500/10 text-teal-300',
  unvalidated: 'border-rose-500/30 bg-rose-500/10 text-rose-300',
};

export const SimulationProvenancePanel: React.FC<{ provenance: SimulationProvenance }> = ({ provenance }) => (
  <details id="tour-provenance-panel" className="rounded-2xl border border-slate-800 bg-slate-950/70 px-4 py-3 font-mono text-xs">
    <summary className="cursor-pointer list-none flex flex-wrap items-center gap-3 text-slate-200">
      <Database className="h-4 w-4 text-cyan-400" />
      <strong>Evidence contract</strong>
      <span className="rounded border border-slate-700 px-2 py-0.5 text-slate-400">{provenance.operating_mode.toUpperCase()}</span>
      <span className="text-slate-500">Environmental boundary validated; equipment outputs modelled</span>
    </summary>
    <div className="mt-4 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
      {provenance.evidence.map((item) => (
        <div key={item.field} className={`rounded-xl border p-3 ${styles[item.kind]}`}>
          <div className="flex items-center gap-2 font-bold uppercase text-[10px] tracking-wider">
            {item.kind === 'measured' ? <Radio className="h-3.5 w-3.5" /> : item.kind === 'simulated' ? <Gauge className="h-3.5 w-3.5" /> : <Sigma className="h-3.5 w-3.5" />}
            {item.kind.replace('_', ' ')}
          </div>
          <div className="mt-1 text-slate-100">{item.field}</div>
          <div className="mt-1 text-[10px] opacity-70">{item.source}{item.note ? ` · ${item.note}` : ''}</div>
        </div>
      ))}
    </div>
    <div className="mt-4 rounded-xl border border-amber-500/20 bg-amber-500/5 p-3 text-slate-400">
      <div className="mb-2 flex items-center gap-2 font-bold text-amber-300"><AlertTriangle className="h-4 w-4" /> Model limitations</div>
      <ul className="space-y-1 list-disc pl-5">{provenance.limitations.map((item) => <li key={item}>{item}</li>)}</ul>
    </div>
  </details>
);
