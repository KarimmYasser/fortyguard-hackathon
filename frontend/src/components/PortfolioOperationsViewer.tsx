import React, { useEffect, useState } from 'react';
import { AlertTriangle, Check, CheckCircle2, Clock3, Copy, Download, FileCheck2, Network, RefreshCw, ShieldCheck, SlidersHorizontal } from 'lucide-react';
import { API_BASE } from '../utils/api';

type Thresholds = { max_wet_bulb_c: number; max_air_temp_c: number; min_consecutive_hours: number };
type Ranking = {
  rank: number; asset_id: string; asset_name: string; asset_type: string; risk_score: number; risk_level: string; action: string;
  inputs: { peak_air_temp_2m_c: number; current_load_percentage: number | null; current_health_score: number | null; criticality_tier: number | null; available_score_weight: number };
  rank_components: Record<string, number | null>;
};
type OperationsPayload = {
  portfolio: { asset_count: number; ranking_method: string; rankings: Ranking[] };
  worker_intervention_screen: {
    occupational_safety_certification: boolean; limitations: string; thresholds: Thresholds;
    windows: Array<{ start_timestamp: string; end_timestamp: string; duration_hours: number; peak_air_temp_2m_c: number; peak_wet_bulb_temp_c: number }>;
  };
  mitigation_evidence: {
    evidence_id: string; sha256: string; analysis_date: string; generated_at: string;
    provenance: Record<string, string>; read_only: boolean;
  };
};

const DEFAULT_THRESHOLDS: Thresholds = { max_wet_bulb_c: 23, max_air_temp_c: 40, min_consecutive_hours: 2 };
const riskTone = (level: string) => level === 'critical' ? 'text-rose-300 bg-rose-500/10 border-rose-500/30' : level === 'high' ? 'text-orange-300 bg-orange-500/10 border-orange-500/30' : level === 'elevated' ? 'text-amber-300 bg-amber-500/10 border-amber-500/30' : 'text-cyan-300 bg-cyan-500/10 border-cyan-500/30';
const utcTime = (value: string) => new Date(value).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', timeZone: 'UTC' });

export const PortfolioOperationsViewer: React.FC = () => {
  const [data, setData] = useState<OperationsPayload | null>(null);
  const [thresholds, setThresholds] = useState<Thresholds>(DEFAULT_THRESHOLDS);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const load = async (next: Thresholds = thresholds) => {
    setLoading(true); setError(null);
    try {
      const response = await fetch(`${API_BASE}/api/v1/operations/portfolio`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(next),
      });
      if (!response.ok) throw new Error(`Operations API returned ${response.status}`);
      setData(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to load operations portfolio');
    } finally { setLoading(false); }
  };

  useEffect(() => { void load(DEFAULT_THRESHOLDS); }, []);

  const exportEvidence = () => {
    if (!data) return;
    const blob = new Blob([JSON.stringify(data.mitigation_evidence, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url; link.download = `${data.mitigation_evidence.evidence_id}.json`; link.click();
    URL.revokeObjectURL(url);
  };

  const copyMcp = async () => {
    const command = `curl -X POST ${window.location.origin}/api/v1/mcp -H 'Content-Type: application/json' -d '${JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'tools/call', params: { name: 'get_mitigation_evidence', arguments: thresholds } })}'`;
    await navigator.clipboard.writeText(command);
    setCopied(true); window.setTimeout(() => setCopied(false), 1800);
  };

  if (loading && !data) return <div className="py-24 text-center font-mono text-slate-400">Loading deterministic operations evidence…</div>;
  if (error && !data) return <div className="rounded-2xl border border-rose-500/30 bg-rose-500/10 p-8 text-center"><AlertTriangle className="mx-auto mb-3 text-rose-400" /><p className="text-rose-200">{error}</p><button onClick={() => void load()} className="mt-4 rounded-lg border border-rose-400/30 px-4 py-2 text-xs font-bold">Retry</button></div>;
  if (!data) return null;

  const firstWindow = data.worker_intervention_screen.windows[0];
  return (
    <div className="space-y-6">
      <section id="tour-operations-header" className="rounded-3xl border border-cyan-500/20 bg-gradient-to-r from-cyan-950/30 via-slate-900/80 to-emerald-950/20 p-6 md:p-8">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
          <div><div className="mb-3 flex items-center gap-2 text-xs font-mono font-bold uppercase tracking-[0.18em] text-cyan-300"><Network className="h-4 w-4" /> Portfolio Operations</div><h2 className="text-3xl font-black text-white font-heading">Risk-ranked intervention command</h2><p className="mt-2 max-w-3xl text-sm leading-relaxed text-slate-300">Registered grid assets are ranked against one frozen live-captured Phoenix FortyGuard boundary. Candidate crew windows and content-addressed evidence come from the same deterministic service exposed to operators and MCP clients.</p></div>
          <button onClick={() => void load()} disabled={loading} className="flex items-center justify-center gap-2 rounded-xl border border-cyan-500/30 bg-cyan-500/10 px-4 py-2 text-xs font-bold text-cyan-200 hover:bg-cyan-500/20 disabled:opacity-50"><RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} /> Refresh evidence</button>
        </div>
      </section>

      <section id="tour-operations-controls" className="glass-panel rounded-2xl border border-slate-800 p-5">
        <div className="mb-4 flex items-center gap-2"><SlidersHorizontal className="h-4 w-4 text-cyan-400" /><h3 className="text-sm font-bold text-white">Explicit worker-screen thresholds</h3></div>
        <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
          <label className="text-xs text-slate-400">Maximum wet bulb °C<input aria-label="Maximum wet bulb temperature" type="number" step="0.5" min="0" max="40" value={thresholds.max_wet_bulb_c} onChange={(e) => setThresholds({ ...thresholds, max_wet_bulb_c: Number(e.target.value) })} className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 font-mono text-white" /></label>
          <label className="text-xs text-slate-400">Maximum 2m air °C<input aria-label="Maximum 2 metre air temperature" type="number" step="0.5" min="-20" max="60" value={thresholds.max_air_temp_c} onChange={(e) => setThresholds({ ...thresholds, max_air_temp_c: Number(e.target.value) })} className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 font-mono text-white" /></label>
          <label className="text-xs text-slate-400">Minimum consecutive hours<input aria-label="Minimum consecutive hours" type="number" min="1" max="12" value={thresholds.min_consecutive_hours} onChange={(e) => setThresholds({ ...thresholds, min_consecutive_hours: Number(e.target.value) })} className="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 font-mono text-white" /></label>
          <button onClick={() => void load(thresholds)} disabled={loading} className="self-end rounded-lg bg-cyan-500 px-4 py-2 text-xs font-black text-slate-950 hover:bg-cyan-400 disabled:opacity-50">{loading ? 'Recalculating…' : 'Recalculate evidence'}</button>
        </div>
      </section>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <div className="glass-panel rounded-2xl border border-slate-800 p-5"><div className="text-[10px] font-mono uppercase tracking-wider text-slate-500">Assets ranked</div><div className="mt-2 text-3xl font-black text-white">{data.portfolio.asset_count}</div><div className="mt-1 text-xs text-slate-400">Method: {data.portfolio.ranking_method}</div></div>
        <div className="glass-panel rounded-2xl border border-slate-800 p-5"><div className="text-[10px] font-mono uppercase tracking-wider text-slate-500">Next candidate field window</div><div className="mt-2 text-xl font-black text-emerald-300">{firstWindow ? `${utcTime(firstWindow.start_timestamp)}–${utcTime(firstWindow.end_timestamp)} UTC` : 'No qualifying window'}</div><div className="mt-1 text-xs text-slate-400">{firstWindow ? `${firstWindow.duration_hours} hourly observations` : 'Adjust explicit screen thresholds'}</div></div>
        <div className="glass-panel rounded-2xl border border-slate-800 p-5"><div className="text-[10px] font-mono uppercase tracking-wider text-slate-500">Evidence snapshot</div><div className="mt-2 truncate text-sm font-bold text-amber-300">{data.mitigation_evidence.evidence_id}</div><div className="mt-1 flex items-center gap-1 text-xs text-slate-400"><FileCheck2 className="h-3.5 w-3.5" /> SHA-256 content addressed</div></div>
      </div>

      <section id="tour-operations-ranking" className="glass-panel overflow-hidden rounded-2xl border border-slate-800">
        <div className="border-b border-slate-800 p-5"><h3 className="font-bold text-white">Portfolio risk ranking</h3><p className="mt-1 text-xs text-slate-400">A transparent triage score—not a failure probability. Missing registry fields are excluded from normalization instead of imputed.</p></div>
        <div className="overflow-x-auto"><table className="w-full min-w-[820px] text-left text-xs"><thead className="bg-slate-950/50 font-mono uppercase tracking-wider text-slate-500"><tr><th className="p-4">Rank</th><th className="p-4">Asset</th><th className="p-4">Score</th><th className="p-4">Evidence coverage</th><th className="p-4">Peak 2m</th><th className="p-4">Health</th><th className="p-4">Tier</th><th className="p-4">Decision</th></tr></thead><tbody className="divide-y divide-slate-800/70">{data.portfolio.rankings.map((row) => <tr key={row.asset_id} className="hover:bg-slate-800/30"><td className="p-4 text-lg font-black text-slate-300">#{row.rank}</td><td className="p-4"><div className="font-bold text-white">{row.asset_name}</div><div className="mt-1 font-mono text-[10px] text-slate-500">{row.asset_id}</div></td><td className="p-4"><span className={`rounded-full border px-2.5 py-1 font-bold ${riskTone(row.risk_level)}`}>{row.risk_score} · {row.risk_level}</span></td><td className="p-4 font-mono text-slate-300">{row.inputs.available_score_weight}%</td><td className="p-4 font-mono text-amber-300">{row.inputs.peak_air_temp_2m_c.toFixed(2)}°C</td><td className="p-4 font-mono text-slate-300">{row.inputs.current_health_score ?? '—'}</td><td className="p-4 font-mono text-slate-300">{row.inputs.criticality_tier ?? '—'}</td><td className="p-4"><span className={row.action === 'prioritize_intervention' ? 'text-orange-300' : 'text-cyan-300'}>{row.action.replaceAll('_', ' ')}</span></td></tr>)}</tbody></table></div>
      </section>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <section id="tour-worker-window" className="glass-panel rounded-2xl border border-slate-800 p-5"><div className="mb-4 flex items-center gap-2"><Clock3 className="h-5 w-5 text-emerald-400" /><h3 className="font-bold text-white">Worker intervention screen</h3></div><div className="space-y-3">{data.worker_intervention_screen.windows.length ? data.worker_intervention_screen.windows.map((window) => <div key={window.start_timestamp} className="rounded-xl border border-emerald-500/20 bg-emerald-500/5 p-4"><div className="font-bold text-emerald-300">{utcTime(window.start_timestamp)}–{utcTime(window.end_timestamp)} UTC · {window.duration_hours}h</div><div className="mt-1 text-xs text-slate-400">Peak 2m air {window.peak_air_temp_2m_c}°C · peak wet bulb {window.peak_wet_bulb_temp_c}°C</div></div>) : <div className="rounded-xl border border-slate-700 p-4 text-sm text-slate-400">No consecutive hours satisfy the selected screen.</div>}</div><div className="mt-4 rounded-xl border border-amber-500/20 bg-amber-500/5 p-3 text-xs leading-relaxed text-amber-100/80"><strong>Screen only:</strong> {data.worker_intervention_screen.limitations}</div></section>

        <section id="tour-operations-evidence" className="glass-panel rounded-2xl border border-slate-800 p-5"><div className="mb-4 flex items-center gap-2"><ShieldCheck className="h-5 w-5 text-cyan-400" /><h3 className="font-bold text-white">Auditable mitigation evidence</h3></div><dl className="space-y-3 text-xs"><div><dt className="font-mono uppercase text-slate-500">Evidence ID</dt><dd className="mt-1 break-all text-amber-300">{data.mitigation_evidence.evidence_id}</dd></div><div><dt className="font-mono uppercase text-slate-500">SHA-256</dt><dd className="mt-1 break-all text-slate-300">{data.mitigation_evidence.sha256}</dd></div><div><dt className="font-mono uppercase text-slate-500">Environmental source</dt><dd className="mt-1 text-slate-300">{data.mitigation_evidence.provenance.environmental_inputs}</dd></div><div><dt className="font-mono uppercase text-slate-500">Scope</dt><dd className="mt-1 text-slate-300">{data.mitigation_evidence.provenance.scope_limitation}</dd></div></dl><div className="mt-4 flex flex-wrap gap-2"><button onClick={exportEvidence} className="flex items-center gap-2 rounded-lg border border-amber-500/30 bg-amber-500/10 px-3 py-2 text-xs font-bold text-amber-300"><Download className="h-4 w-4" /> Export JSON evidence</button><button onClick={() => void copyMcp()} className="flex items-center gap-2 rounded-lg border border-cyan-500/30 bg-cyan-500/10 px-3 py-2 text-xs font-bold text-cyan-300">{copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}{copied ? 'Copied MCP call' : 'Copy MCP call'}</button></div><div className="mt-4 flex items-center gap-2 text-xs font-bold text-emerald-300"><CheckCircle2 className="h-4 w-4" /> Read-only deterministic snapshot · MCP-accessible</div></section>
      </div>
    </div>
  );
};
