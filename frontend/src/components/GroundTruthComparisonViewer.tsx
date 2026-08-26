import React, { useEffect, useMemo, useState } from 'react';
import ReactECharts from 'echarts-for-react';
import { AlertTriangle, CheckCircle2, RefreshCw, Thermometer } from 'lucide-react';
import { API_BASE } from '../utils/api';

interface Pair {
  timestamp: string;
  fortyguard_2m_c: number;
  station_ground_truth_c: number;
  delta_t_c: number;
}

export const GroundTruthComparisonViewer: React.FC = () => {
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [mode, setMode] = useState<'replay' | 'iem'>('replay');

  const load = async (selected = mode) => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`${API_BASE}/api/v1/benchmark/ground-truth-comparison?source=${selected}`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      setReport(await response.json());
    } catch (err: any) {
      setError(err?.message || 'Comparison unavailable');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(mode); }, [mode]);
  const metrics = report?.metrics?.temperature_2m;
  const series: Pair[] = metrics?.paired_series || [];
  const chart = useMemo(() => ({
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis', valueFormatter: (value: number) => `${Number(value).toFixed(2)} °C` },
    legend: { data: ['FortyGuard urban 2m', 'PHX ASOS station', 'ΔT'], textStyle: { color: '#94a3b8' } },
    grid: { left: 48, right: 55, top: 48, bottom: 42 },
    xAxis: {
      type: 'category',
      data: series.map(p => new Date(p.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', timeZone: 'America/Phoenix' })),
      axisLabel: { color: '#64748b' }, name: 'Phoenix local time', nameTextStyle: { color: '#64748b' },
    },
    yAxis: [
      { type: 'value', name: 'Temperature °C', min: (v: any) => Math.floor(v.min - 1), axisLabel: { color: '#64748b' }, nameTextStyle: { color: '#64748b' }, splitLine: { lineStyle: { color: '#1e293b' } } },
      { type: 'value', name: 'ΔT °C', axisLabel: { color: '#f59e0b' }, nameTextStyle: { color: '#f59e0b' }, splitLine: { show: false } },
    ],
    series: [
      { name: 'FortyGuard urban 2m', type: 'line', smooth: true, data: series.map(p => p.fortyguard_2m_c), lineStyle: { width: 3, color: '#f59e0b' }, itemStyle: { color: '#f59e0b' } },
      { name: 'PHX ASOS station', type: 'line', smooth: true, data: series.map(p => p.station_ground_truth_c), lineStyle: { width: 3, color: '#22d3ee' }, itemStyle: { color: '#22d3ee' } },
      { name: 'ΔT', type: 'bar', yAxisIndex: 1, data: series.map(p => ({ value: p.delta_t_c, itemStyle: { color: p.delta_t_c >= 0 ? '#a78bfa99' : '#ef444499' } })) },
    ],
  }), [series]);

  if (loading) return <div id="tour-ground-truth-header" className="rounded-2xl border border-slate-800 bg-slate-900/40 p-16 text-center text-slate-400"><RefreshCw className="inline h-6 w-6 animate-spin mr-2" />Loading independent station evidence…</div>;
  if (error || !metrics) return <div id="tour-ground-truth-header" className="rounded-2xl border border-red-900 bg-red-950/20 p-8 text-red-300">Ground-truth comparison failed: {error}</div>;

  const anomaly = metrics.urban_station_anomaly;
  const cards = [
    ['Mean urban − station ΔT', `${metrics.mean_delta_t_c > 0 ? '+' : ''}${metrics.mean_delta_t_c.toFixed(2)} °C`],
    ['Pearson correlation', metrics.pearson_r == null ? 'N/A' : metrics.pearson_r.toFixed(3)],
    ['RMSE', `${metrics.rmse.toFixed(2)} °C`],
    ['Positive ΔT hours', `${metrics.positive_delta_hours}/${metrics.n_pairs}`],
  ];

  return <div className="space-y-5">
    <div id="tour-ground-truth-header" className="flex flex-wrap items-center gap-4">
      <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-amber-500 to-violet-600 flex items-center justify-center"><Thermometer /></div>
      <div>
        <h2 className="text-xl font-bold">Ground Truth vs FortyGuard</h2>
        <p className="text-xs text-slate-400">Independent PHX ASOS station · local-to-UTC normalization · ΔT = FortyGuard urban 2m − station</p>
      </div>
      <div className="ml-auto flex gap-2">
        <select value={mode} onChange={e => setMode(e.target.value as 'replay' | 'iem')} className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-xs text-slate-300">
          <option value="replay">Frozen station replay</option>
          <option value="iem">Refresh IEM live</option>
        </select>
        <button onClick={() => load()} className="rounded-lg border border-slate-700 px-3 py-2 text-xs text-slate-300 hover:bg-slate-800"><RefreshCw className="inline h-3 w-3 mr-1" />Refresh</button>
      </div>
    </div>

    <div id="tour-ground-truth-interpretation" className={`rounded-xl border p-4 flex gap-3 ${anomaly?.observed ? 'border-cyan-500/40 bg-cyan-500/10' : 'border-slate-700 bg-slate-900/40'}`}>
      {anomaly?.observed ? <CheckCircle2 className="text-cyan-400 shrink-0" /> : <AlertTriangle className="text-amber-400 shrink-0" />}
      <div><div className="font-bold">{anomaly?.interpretation}</div><div className="text-xs text-slate-400 mt-1">Observed comparison result—not a causal UHI claim. Phoenix Sky Harbor is an urban airport, not a rural control.</div></div>
    </div>

    <div id="tour-ground-truth-metrics" className="grid grid-cols-2 lg:grid-cols-4 gap-3">{cards.map(([label, value]) => <div key={label} className="rounded-xl border border-slate-800 bg-slate-900/60 p-4"><div className="text-[10px] uppercase tracking-wider text-slate-500">{label}</div><div className="text-xl font-bold text-white mt-1">{value}</div></div>)}</div>

    <div id="tour-ground-truth-chart" className="rounded-2xl border border-slate-800 bg-[#0b1220] p-4"><ReactECharts option={chart} style={{ height: 430 }} notMerge /></div>

    <div id="tour-ground-truth-uhi" className="rounded-xl border border-amber-800/50 bg-amber-950/10 p-4 flex gap-3 text-xs text-amber-100">
      <AlertTriangle className="h-5 w-5 text-amber-400 shrink-0" />
      <div><strong>UHI status: not established by this comparison.</strong><p className="text-slate-400 mt-1">{metrics.urban_heat_island.criterion} This chart tests temporal agreement and quantifies a location-specific contrast.</p></div>
    </div>

    <div id="tour-ground-truth-provenance" className="rounded-xl border border-slate-800 bg-slate-900/40 p-4 text-xs text-slate-400 grid md:grid-cols-3 gap-3">
      <div><span className="text-slate-500">Evidence</span><br/><strong className="text-cyan-300">{report.provenance.evidence_class}</strong></div>
      <div><span className="text-slate-500">Station / separation</span><br/><strong className="text-white">{report.provenance.station} · {report.provenance.distance_to_aoi_km} km</strong></div>
      <div><span className="text-slate-500">Mode / coverage</span><br/><strong className="text-violet-300">{report.selection.selected_source} · {metrics.coverage_pct}%</strong></div>
      <p className="md:col-span-3 border-t border-slate-800 pt-3">Time alignment: {report.comparison.time_alignment.conversion}. This validates the environmental 2 m boundary only; it does not claim proprietary distribution SCADA or feeder telemetry.</p>
    </div>
  </div>;
};
