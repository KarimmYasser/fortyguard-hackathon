import React, { useState, useEffect } from 'react';
import {
  BarChart3, TrendingUp, AlertTriangle, Brain, Clock,
  Database, Layers, Activity, ShieldCheck, Zap, FlaskConical,
  ChevronDown, ChevronUp, RefreshCw, ArrowRight
} from 'lucide-react';
import { API_BASE } from '../utils/api';

type SubSection = 'eda' | 'correlation' | 'spatial' | 'risk' | 'ml' | 'temporal';

interface FeatureStat {
  feature: string; count: number; mean: number; std: number;
  min: number; q1: number; median: number; q3: number; max: number;
  skewness: number; kurtosis: number; null_pct: number;
}

interface CorrelationPair {
  feature_a: string; feature_b: string; pearson_r: number; spearman_rho: number;
  kind?: 'empirical' | 'derived' | 'structural'; p_value?: number | null;
}

interface RiskTier { tier: string; count: number; percentage: number; }
interface AnomalyRecord { hour_index: number; time_label: string; label: string; anomaly_score: number; }
interface TemporalRecord { hour_index: number; time_label: string; hour_of_day: number; [k: string]: any; }

export const DataScienceStudio: React.FC = () => {
  const [activeSection, setActiveSection] = useState<SubSection>('eda');
  const [edaData, setEdaData] = useState<any>(null);
  const [corrData, setCorrData] = useState<any>(null);
  const [spatialData, setSpatialData] = useState<any>(null);
  const [selectedSpatialModel, setSelectedSpatialModel] = useState<string>('canopy_vs_persistence');
  const [riskData, setRiskData] = useState<any>(null);
  const [mlData, setMlData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchData = async (section: SubSection) => {
    setIsLoading(true);
    try {
      const endpoints: Record<SubSection, string> = {
        eda: '/api/v1/analytics/eda',
        correlation: '/api/v1/analytics/correlation',
        spatial: '/api/v1/analytics/spatial-regression',
        risk: '/api/v1/analytics/risk-distribution',
        ml: '/api/v1/analytics/ml-overview',
        temporal: '/api/v1/analytics/risk-distribution',
      };
      const resp = await fetch(`${API_BASE}${endpoints[section]}`);
      if (resp.ok) {
        const json = await resp.json();
        if (section === 'eda') setEdaData(json);
        else if (section === 'correlation') setCorrData(json);
        else if (section === 'spatial') setSpatialData(json);
        else if (section === 'risk' || section === 'temporal') setRiskData(json);
        else if (section === 'ml') setMlData(json);
      }
    } catch (err) { console.warn('Analytics fetch error:', err); }
    finally { setIsLoading(false); }
  };

  useEffect(() => { fetchData(activeSection); }, [activeSection]);

  const sections: { id: SubSection; label: string; icon: React.ReactNode }[] = [
    { id: 'eda', label: 'EDA & Features', icon: <BarChart3 size={16} /> },
    { id: 'correlation', label: 'Correlation Matrix', icon: <TrendingUp size={16} /> },
    { id: 'spatial', label: 'Spatial Regression (OLS)', icon: <Layers size={16} /> },
    { id: 'risk', label: 'Risk Distribution', icon: <AlertTriangle size={16} /> },
    { id: 'ml', label: 'ML Models', icon: <Brain size={16} /> },
    { id: 'temporal', label: 'Temporal Patterns', icon: <Clock size={16} /> },
  ];


  const riskColor = (tier: string) => {
    if (tier === 'CRITICAL') return '#ef4444';
    if (tier === 'HIGH') return '#f97316';
    if (tier === 'MODERATE') return '#eab308';
    return '#22c55e';
  };

  return (
    <div style={{ padding: '24px', maxWidth: 1400, margin: '0 auto' }}>
      {/* Header */}
      <div id="tour-data-science-header" style={{ marginBottom: 24, display: 'flex', alignItems: 'center', gap: 12 }}>
        <div style={{ width: 48, height: 48, borderRadius: 12, background: 'linear-gradient(135deg, #8b5cf6, #6366f1)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <FlaskConical size={24} color="white" />
        </div>
        <div>
          <h2 style={{ margin: 0, fontSize: 22, fontWeight: 700, color: '#f1f5f9' }}>
            📊 Data Science & Analytics Studio
          </h2>
          <p style={{ margin: 0, fontSize: 13, color: '#94a3b8' }}>
            IBM Data Science Methodology — Bronze→Silver→Gold ETL · EDA · ML · Survival Analysis
          </p>
        </div>
        <div style={{ marginLeft: 'auto', display: 'flex', gap: 8, alignItems: 'center' }}>
          <span style={{ fontSize: 11, color: '#64748b', background: '#1e293b', padding: '4px 10px', borderRadius: 6 }}>
            <Database size={12} style={{ marginRight: 4, verticalAlign: 'middle' }} />
            Medallion Architecture
          </span>
          <span style={{ fontSize: 11, color: '#a78bfa', background: 'rgba(139,92,246,0.15)', padding: '4px 10px', borderRadius: 6 }}>
            <Layers size={12} style={{ marginRight: 4, verticalAlign: 'middle' }} />
            NumPy + pandas + scikit-learn
          </span>
        </div>
      </div>

      {/* Sub-section tabs */}
      <div id="tour-data-science-tabs" style={{ display: 'flex', gap: 4, marginBottom: 20, borderBottom: '1px solid #334155', paddingBottom: 8, flexWrap: 'wrap' }}>
        {sections.map(s => (
          <button
            id={`tour-data-science-tab-${s.id}`}
            key={s.id}
            onClick={() => setActiveSection(s.id)} style={{
            padding: '8px 16px', borderRadius: 8, border: 'none', cursor: 'pointer', fontSize: 13, fontWeight: 600,
            display: 'flex', alignItems: 'center', gap: 6, transition: 'all 0.2s',
            background: activeSection === s.id ? 'linear-gradient(135deg, #8b5cf6, #6366f1)' : '#1e293b',
            color: activeSection === s.id ? '#fff' : '#94a3b8',
          }}>
            {s.icon} {s.label}
          </button>
        ))}
      </div>

      {isLoading && (
        <div style={{ textAlign: 'center', padding: 60, color: '#94a3b8' }}>
          <RefreshCw size={28} style={{ animation: 'spin 1s linear infinite' }} />
          <p style={{ marginTop: 12 }}>Running analytics pipeline...</p>
        </div>
      )}

      {/* ── SECTION 1: EDA ── */}
      {activeSection === 'eda' && edaData && !isLoading && (
        <div id="tour-data-science-eda">
          {/* Pipeline summary cards */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 12, marginBottom: 20 }}>
            {[
              { label: 'Total Records', value: edaData.total_records, color: '#8b5cf6' },
              { label: 'Total Features', value: edaData.total_features, color: '#06b6d4' },
              { label: 'Numeric Features', value: edaData.numeric_features, color: '#22c55e' },
              { label: 'Categorical', value: edaData.categorical_features, color: '#f97316' },
              { label: 'Null %', value: `${edaData.overall_null_pct}%`, color: edaData.overall_null_pct > 0 ? '#ef4444' : '#22c55e' },
            ].map((card, i) => (
              <div key={i} style={{ background: '#0f172a', borderRadius: 12, padding: 16, border: '1px solid #1e293b' }}>
                <p style={{ margin: 0, fontSize: 11, color: '#64748b', textTransform: 'uppercase', letterSpacing: 1 }}>{card.label}</p>
                <p style={{ margin: '4px 0 0', fontSize: 24, fontWeight: 700, color: card.color }}>{card.value}</p>
              </div>
            ))}
          </div>

          {/* Medallion architecture badge */}
          {edaData.pipeline && (
            <div style={{ background: 'linear-gradient(135deg, rgba(139,92,246,0.1), rgba(99,102,241,0.1))', borderRadius: 12, padding: 16, border: '1px solid rgba(139,92,246,0.3)', marginBottom: 20, display: 'flex', alignItems: 'center', gap: 16, flexWrap: 'wrap' }}>
              <span style={{ fontSize: 12, fontWeight: 700, color: '#cd7c34', background: 'rgba(205,124,52,0.15)', padding: '4px 12px', borderRadius: 6 }}>🥉 Bronze</span>
              <ArrowRight size={14} color="#64748b" />
              <span style={{ fontSize: 12, fontWeight: 700, color: '#94a3b8', background: 'rgba(148,163,184,0.15)', padding: '4px 12px', borderRadius: 6 }}>🥈 Silver</span>
              <ArrowRight size={14} color="#64748b" />
              <span style={{ fontSize: 12, fontWeight: 700, color: '#eab308', background: 'rgba(234,179,8,0.15)', padding: '4px 12px', borderRadius: 6 }}>🥇 Gold</span>
              <span style={{ marginLeft: 'auto', fontSize: 11, color: '#64748b' }}>
                {edaData.pipeline.engineered_feature_count} engineered features
              </span>
            </div>
          )}

          {/* Feature statistics table */}
          <div style={{ background: '#0f172a', borderRadius: 12, border: '1px solid #1e293b', overflow: 'auto', maxHeight: 500 }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 12 }}>
              <thead>
                <tr style={{ background: '#1e293b', position: 'sticky', top: 0 }}>
                  {['Feature', 'Mean', 'Std', 'Min', 'Q1', 'Median', 'Q3', 'Max', 'Skew', 'Kurt'].map(h => (
                    <th key={h} style={{ padding: '10px 8px', textAlign: 'left', color: '#94a3b8', fontWeight: 600, fontSize: 11 }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {(edaData.feature_statistics || []).map((f: FeatureStat, i: number) => (
                  <tr key={i} style={{ borderBottom: '1px solid #1e293b' }}>
                    <td style={{ padding: '8px', color: '#a78bfa', fontWeight: 600, fontFamily: 'monospace', fontSize: 11 }}>{f.feature}</td>
                    <td style={{ padding: '8px', color: '#e2e8f0' }}>{f.mean}</td>
                    <td style={{ padding: '8px', color: '#94a3b8' }}>{f.std}</td>
                    <td style={{ padding: '8px', color: '#64748b' }}>{f.min}</td>
                    <td style={{ padding: '8px', color: '#64748b' }}>{f.q1}</td>
                    <td style={{ padding: '8px', color: '#e2e8f0', fontWeight: 600 }}>{f.median}</td>
                    <td style={{ padding: '8px', color: '#64748b' }}>{f.q3}</td>
                    <td style={{ padding: '8px', color: '#64748b' }}>{f.max}</td>
                    <td style={{ padding: '8px', color: Math.abs(f.skewness) > 1 ? '#f97316' : '#94a3b8' }}>{f.skewness}</td>
                    <td style={{ padding: '8px', color: Math.abs(f.kurtosis) > 3 ? '#f97316' : '#94a3b8' }}>{f.kurtosis}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* ── SECTION 2: CORRELATION ── */}
      {activeSection === 'correlation' && corrData && !isLoading && (
        <div id="tour-data-science-correlation">
          <h3 style={{ color: '#f1f5f9', fontSize: 16, marginBottom: 4 }}>🔗 Top 10 Strongest Feature Correlations</h3>
          <p style={{ color: '#64748b', fontSize: 11, marginTop: 0, marginBottom: 12 }}>
            Empirical pairs only — features that are closed-form functions of each other are listed separately below.
            {corrData.n_observations ? ` n = ${corrData.n_observations}.` : ''}
          </p>
          {(corrData.warnings || []).length > 0 && (
            <div style={{ background: '#1c1917', border: '1px solid #78350f', borderRadius: 10, padding: '10px 14px', marginBottom: 14 }}>
              {(corrData.warnings || []).map((w: string, i: number) => (
                <div key={i} style={{ color: '#fbbf24', fontSize: 11.5, lineHeight: 1.6 }}>⚠ {w}</div>
              ))}
            </div>
          )}
          <div style={{ display: 'grid', gap: 8, marginBottom: 20 }}>
            {(corrData.top_10_strongest_pairs || []).map((p: CorrelationPair, i: number) => (
              <div key={i} style={{ background: '#0f172a', borderRadius: 10, padding: 14, border: '1px solid #1e293b', display: 'flex', alignItems: 'center', gap: 12 }}>
                <span style={{ fontSize: 18, fontWeight: 800, color: '#64748b', width: 28 }}>#{i+1}</span>
                <div style={{ flex: 1 }}>
                  <span style={{ color: '#a78bfa', fontFamily: 'monospace', fontSize: 12 }}>{p.feature_a}</span>
                  <span style={{ color: '#475569', margin: '0 8px' }}>↔</span>
                  <span style={{ color: '#06b6d4', fontFamily: 'monospace', fontSize: 12 }}>{p.feature_b}</span>
                </div>
                <div style={{ display: 'flex', gap: 12 }}>
                  <span style={{ fontSize: 13, fontWeight: 700, color: p.pearson_r > 0 ? '#22c55e' : '#ef4444' }}>
                    r = {p.pearson_r > 0 ? '+' : ''}{p.pearson_r}
                  </span>
                  <span style={{ fontSize: 11, color: '#64748b' }}>
                    ρ = {p.spearman_rho > 0 ? '+' : ''}{p.spearman_rho}
                  </span>
                  {p.p_value != null && (
                    <span style={{ fontSize: 11, color: p.p_value < 0.05 ? '#64748b' : '#f97316' }}>
                      p = {p.p_value < 0.001 ? p.p_value.toExponential(1) : p.p_value.toFixed(3)}
                    </span>
                  )}
                </div>
                {/* Visual bar */}
                <div style={{ width: 100, height: 8, background: '#1e293b', borderRadius: 4, overflow: 'hidden' }}>
                  <div style={{ width: `${Math.abs(p.pearson_r) * 100}%`, height: '100%', borderRadius: 4, background: p.pearson_r > 0 ? 'linear-gradient(90deg, #22c55e, #4ade80)' : 'linear-gradient(90deg, #ef4444, #f87171)' }} />
                </div>
              </div>
            ))}
          </div>

          {/* Pairs that are true by construction — shown for transparency, never ranked as findings */}
          {(corrData.tautological_pairs || []).length > 0 && (
            <div style={{ background: '#0f172a', borderRadius: 12, padding: 16, border: '1px dashed #334155', marginBottom: 20 }}>
              <h4 style={{ color: '#94a3b8', fontSize: 13, marginTop: 0, marginBottom: 4 }}>
                Excluded: true by construction
              </h4>
              <p style={{ color: '#64748b', fontSize: 11, marginTop: 0, marginBottom: 10 }}>
                <code style={{ color: '#94a3b8' }}>derived</code> = one feature is computed from the other (or both share a parent);{' '}
                <code style={{ color: '#94a3b8' }}>structural</code> = both come from the same authored scenario curve.
                These report |r| ≈ 1 on any dataset and are not findings.
              </p>
              {(corrData.tautological_pairs || []).map((p: CorrelationPair, i: number) => (
                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '4px 0', fontSize: 11 }}>
                  <span style={{
                    fontFamily: 'monospace', fontSize: 9, textTransform: 'uppercase', letterSpacing: 0.5,
                    color: p.kind === 'derived' ? '#f472b6' : '#fbbf24',
                    border: `1px solid ${p.kind === 'derived' ? '#831843' : '#78350f'}`,
                    borderRadius: 4, padding: '1px 5px', width: 66, textAlign: 'center',
                  }}>{p.kind}</span>
                  <span style={{ color: '#64748b', fontFamily: 'monospace', flex: 1 }}>
                    {p.feature_a} ↔ {p.feature_b}
                  </span>
                  <span style={{ color: '#475569', fontFamily: 'monospace' }}>
                    r = {p.pearson_r > 0 ? '+' : ''}{p.pearson_r}
                  </span>
                </div>
              ))}
            </div>
          )}

          {/* Correlation matrix heatmap (simplified text-based) */}
          <div style={{ background: '#0f172a', borderRadius: 12, padding: 16, border: '1px solid #1e293b' }}>
            <h4 style={{ color: '#94a3b8', fontSize: 13, marginBottom: 12 }}>Pearson Correlation Matrix ({corrData.columns?.length || 0} features)</h4>
            <div style={{ overflowX: 'auto', maxHeight: 400 }}>
              <table style={{ borderCollapse: 'collapse', fontSize: 10 }}>
                <thead>
                  <tr>
                    <th style={{ padding: 4, color: '#64748b' }}></th>
                    {(corrData.columns || []).slice(0, 12).map((c: string, i: number) => (
                      <th key={i} style={{ padding: 4, color: '#64748b', transform: 'rotate(-45deg)', transformOrigin: 'left bottom', whiteSpace: 'nowrap', maxWidth: 30 }}>
                        {c.slice(0, 8)}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {(corrData.pearson_matrix || []).slice(0, 12).map((row: number[], ri: number) => (
                    <tr key={ri}>
                      <td style={{ padding: 4, color: '#94a3b8', fontFamily: 'monospace', fontSize: 9, whiteSpace: 'nowrap' }}>
                        {(corrData.columns || [])[ri]?.slice(0, 12)}
                      </td>
                      {row.slice(0, 12).map((val: number, ci: number) => {
                        const abs = Math.abs(val);
                        const bg = ri === ci ? '#1e293b' : val > 0
                          ? `rgba(34,197,94,${abs * 0.6})` : `rgba(239,68,68,${abs * 0.6})`;
                        return (
                          <td key={ci} style={{ padding: 4, textAlign: 'center', color: abs > 0.5 ? '#fff' : '#94a3b8', background: bg, borderRadius: 2, minWidth: 32, fontSize: 9 }}>
                            {ri === ci ? '1' : val.toFixed(2)}
                          </td>
                        );
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* ── SECTION 3: SPATIAL REGRESSION & MORPHOLOGY ── */}
      {activeSection === 'spatial' && spatialData && !isLoading && (
        <div id="tour-data-science-spatial">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16, flexWrap: 'wrap', gap: 12 }}>
            <div>
              <h3 style={{ color: '#f1f5f9', fontSize: 16, margin: 0 }}>📐 Spatial Bivariate Regression & Urban Morphology</h3>
              <p style={{ color: '#64748b', fontSize: 12, margin: '4px 0 0' }}>
                Empirical Ordinary Least Squares (OLS) regression & Global Moran's I spatial clustering (FortyGuard ML Session 07).
              </p>
            </div>
            <div style={{ display: 'flex', gap: 8 }}>
              {[
                { id: 'canopy_vs_persistence', label: '🌳 Canopy vs P₄₀' },
                { id: 'asphalt_vs_delta_t', label: '🛣️ Asphalt vs ΔT₂ₘ' },
                { id: 'canyon_aspect_vs_cooling_derate', label: '🏙️ Canyon H/W vs Derate' },
              ].map(m => (
                <button
                  key={m.id}
                  onClick={() => setSelectedSpatialModel(m.id)}
                  style={{
                    padding: '6px 12px', borderRadius: 8, fontSize: 12, fontWeight: 600, cursor: 'pointer', border: 'none',
                    background: selectedSpatialModel === m.id ? 'linear-gradient(135deg, #06b6d4, #3b82f6)' : '#1e293b',
                    color: selectedSpatialModel === m.id ? '#fff' : '#94a3b8',
                    transition: 'all 0.2s',
                  }}
                >
                  {m.label}
                </button>
              ))}
            </div>
          </div>

          {spatialData.models && spatialData.models[selectedSpatialModel] && (() => {
            const m = spatialData.models[selectedSpatialModel];
            const pts = m.scatter_points || [];
            const xs = pts.map((p: any) => p.x);
            const ys = pts.map((p: any) => p.y);
            const minX = Math.min(...xs, 0);
            const maxX = Math.max(...xs, 1);
            const minY = Math.min(...ys, 0);
            const maxY = Math.max(...ys, 1);
            const rangeX = maxX - minX || 1;
            const rangeY = maxY - minY || 1;

            const scaleX = (val: number) => 40 + ((val - minX) / rangeX) * 420;
            const scaleY = (val: number) => 220 - ((val - minY) / rangeY) * 180;

            return (
              <div style={{ display: 'grid', gridTemplateColumns: 'minmax(400px, 1.2fr) minmax(300px, 0.8fr)', gap: 20, marginBottom: 20 }}>
                {/* SVG Scatter + Trendline Chart */}
                <div style={{ background: '#0f172a', borderRadius: 12, padding: 16, border: '1px solid #1e293b' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                    <span style={{ fontSize: 13, fontWeight: 700, color: '#f1f5f9' }}>{m.title}</span>
                    <span style={{ fontSize: 11, color: '#06b6d4', background: 'rgba(6,182,212,0.15)', padding: '2px 8px', borderRadius: 4, fontFamily: 'monospace' }}>
                      R² = {m.r_squared} · p = {m.p_value}
                    </span>
                  </div>

                  <svg viewBox="0 0 500 250" style={{ width: '100%', height: 260, overflow: 'visible' }}>
                    {/* Grid lines */}
                    {[0, 0.25, 0.5, 0.75, 1].map((pct, i) => (
                      <g key={i}>
                        <line x1="40" y1={scaleY(minY + pct * rangeY)} x2="470" y2={scaleY(minY + pct * rangeY)} stroke="#1e293b" strokeDasharray="3 3" />
                        <text x="35" y={scaleY(minY + pct * rangeY) + 3} fill="#64748b" fontSize="9" textAnchor="end">
                          {(minY + pct * rangeY).toFixed(1)}
                        </text>
                      </g>
                    ))}

                    {/* Trendline */}
                    {m.trendline_points && m.trendline_points.length > 1 && (
                      <line
                        x1={scaleX(m.trendline_points[0].x)}
                        y1={scaleY(m.trendline_points[0].y)}
                        x2={scaleX(m.trendline_points[m.trendline_points.length - 1].x)}
                        y2={scaleY(m.trendline_points[m.trendline_points.length - 1].y)}
                        stroke="#06b6d4"
                        strokeWidth="2.5"
                        strokeLinecap="round"
                      />
                    )}

                    {/* Scatter Points */}
                    {pts.map((p: any, i: number) => {
                      const cx = scaleX(p.x);
                      const cy = scaleY(p.y);
                      const isHighRisk = Math.abs(p.residual) > 1.0;
                      return (
                        <g key={i}>
                          <circle
                            cx={cx}
                            cy={cy}
                            r={5.5}
                            fill={isHighRisk ? '#f97316' : '#8b5cf6'}
                            stroke="#0f172a"
                            strokeWidth="1.5"
                          >
                            <title>{`${p.label}: (${p.x} ${m.feature_unit}, ${p.y} ${m.target_unit}) residual=${p.residual}`}</title>
                          </circle>
                          <text x={cx + 7} y={cy + 3} fill="#94a3b8" fontSize="8">
                            {p.label.split(' ')[0]}
                          </text>
                        </g>
                      );
                    })}

                    {/* Axis Labels */}
                    <text x="255" y="245" fill="#94a3b8" fontSize="10" textAnchor="middle">
                      {m.feature_name} ({m.feature_unit}) →
                    </text>
                    <text x="15" y="130" fill="#94a3b8" fontSize="10" textAnchor="middle" transform="rotate(-90 15 130)">
                      ↑ {m.target_name} ({m.target_unit})
                    </text>
                  </svg>
                </div>

                {/* Statistical Parameters & Narrative */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                  <div style={{ background: '#0f172a', borderRadius: 12, padding: 16, border: '1px solid #1e293b' }}>
                    <span style={{ fontSize: 11, fontWeight: 700, color: '#64748b', textTransform: 'uppercase', letterSpacing: 0.5 }}>
                      Model Summary Parameters
                    </span>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, marginTop: 10 }}>
                      <div style={{ background: '#1e293b', padding: '10px 12px', borderRadius: 8 }}>
                        <div style={{ fontSize: 10, color: '#64748b' }}>R² Determination</div>
                        <div style={{ fontSize: 18, fontWeight: 700, color: '#06b6d4' }}>{m.r_squared}</div>
                      </div>
                      <div style={{ background: '#1e293b', padding: '10px 12px', borderRadius: 8 }}>
                        <div style={{ fontSize: 10, color: '#64748b' }}>Pearson r</div>
                        <div style={{ fontSize: 18, fontWeight: 700, color: m.pearson_r < 0 ? '#f43f5e' : '#10b981' }}>
                          {m.pearson_r > 0 ? '+' : ''}{m.pearson_r}
                        </div>
                      </div>
                      <div style={{ background: '#1e293b', padding: '10px 12px', borderRadius: 8 }}>
                        <div style={{ fontSize: 10, color: '#64748b' }}>p-value (Significance)</div>
                        <div style={{ fontSize: 14, fontWeight: 700, color: '#a78bfa' }}>{m.p_value}</div>
                      </div>
                      <div style={{ background: '#1e293b', padding: '10px 12px', borderRadius: 8 }}>
                        <div style={{ fontSize: 10, color: '#64748b' }}>Fisher F-Statistic</div>
                        <div style={{ fontSize: 14, fontWeight: 700, color: '#e2e8f0' }}>{m.f_statistic}</div>
                      </div>
                    </div>

                    <div style={{ marginTop: 12, padding: '10px 12px', background: 'rgba(139,92,246,0.1)', border: '1px solid rgba(139,92,246,0.25)', borderRadius: 8 }}>
                      <div style={{ fontSize: 10, color: '#a78bfa', fontWeight: 600 }}>OLS EQUATION & 95% CI:</div>
                      <div style={{ fontSize: 12, color: '#f1f5f9', fontFamily: 'monospace', marginTop: 2 }}>
                        y = {m.slope}x {m.intercept >= 0 ? '+' : ''}{m.intercept}
                      </div>
                      <div style={{ fontSize: 10, color: '#94a3b8', marginTop: 2 }}>
                        Slope 95% CI: [{m.confidence_interval_slope_95[0]}, {m.confidence_interval_slope_95[1]}]
                      </div>
                    </div>
                  </div>

                  {/* Narrative Interpretation */}
                  <div style={{ background: '#0f172a', borderRadius: 12, padding: 14, border: '1px solid #1e293b', flex: 1 }}>
                    <span style={{ fontSize: 11, fontWeight: 700, color: '#10b981', textTransform: 'uppercase', letterSpacing: 0.5 }}>
                      Statistical Inference
                    </span>
                    <p style={{ margin: '6px 0 0', fontSize: 12, color: '#cbd5e1', lineHeight: 1.5 }}>
                      {m.narrative}
                    </p>
                  </div>
                </div>
              </div>
            );
          })()}

          {/* Moran's I and Cadence Doctrine Cards */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
            {spatialData.spatial_autocorrelation && (
              <div style={{ background: '#0f172a', borderRadius: 12, padding: 16, border: '1px solid #1e293b' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
                  <Activity size={18} color="#06b6d4" />
                  <h4 style={{ margin: 0, fontSize: 14, color: '#f1f5f9' }}>Global Moran's I Spatial Autocorrelation</h4>
                  <span style={{ marginLeft: 'auto', fontSize: 10, fontWeight: 700, padding: '2px 8px', borderRadius: 4, background: spatialData.spatial_autocorrelation.is_clustered ? 'rgba(16,185,129,0.2)' : '#1e293b', color: spatialData.spatial_autocorrelation.is_clustered ? '#10b981' : '#94a3b8' }}>
                    {spatialData.spatial_autocorrelation.is_clustered ? 'SPATIALLY CLUSTERED' : 'RANDOM'}
                  </span>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 8, marginBottom: 10 }}>
                  <div style={{ background: '#1e293b', padding: 8, borderRadius: 6, textAlign: 'center' }}>
                    <div style={{ fontSize: 9, color: '#64748b' }}>Moran's I</div>
                    <div style={{ fontSize: 14, fontWeight: 700, color: '#06b6d4' }}>{spatialData.spatial_autocorrelation.morans_i}</div>
                  </div>
                  <div style={{ background: '#1e293b', padding: 8, borderRadius: 6, textAlign: 'center' }}>
                    <div style={{ fontSize: 9, color: '#64748b' }}>Expected I</div>
                    <div style={{ fontSize: 14, fontWeight: 700, color: '#94a3b8' }}>{spatialData.spatial_autocorrelation.expected_i}</div>
                  </div>
                  <div style={{ background: '#1e293b', padding: 8, borderRadius: 6, textAlign: 'center' }}>
                    <div style={{ fontSize: 9, color: '#64748b' }}>z-score</div>
                    <div style={{ fontSize: 14, fontWeight: 700, color: '#a78bfa' }}>{spatialData.spatial_autocorrelation.z_score}</div>
                  </div>
                  <div style={{ background: '#1e293b', padding: 8, borderRadius: 6, textAlign: 'center' }}>
                    <div style={{ fontSize: 9, color: '#64748b' }}>p-value</div>
                    <div style={{ fontSize: 14, fontWeight: 700, color: '#10b981' }}>{spatialData.spatial_autocorrelation.p_value}</div>
                  </div>
                </div>
                <p style={{ margin: 0, fontSize: 11.5, color: '#94a3b8', lineHeight: 1.5 }}>
                  {spatialData.spatial_autocorrelation.interpretation}
                </p>
              </div>
            )}

            <div style={{ background: '#0f172a', borderRadius: 12, padding: 16, border: '1px solid #1e293b' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
                <ShieldCheck size={18} color="#8b5cf6" />
                <h4 style={{ margin: 0, fontSize: 14, color: '#f1f5f9' }}>Multi-Cadence Resampling & Spatial Snapping</h4>
              </div>
              <p style={{ margin: 0, fontSize: 11.5, color: '#cbd5e1', lineHeight: 1.6 }}>
                • <strong>Where / When / What Triad:</strong> Substation coordinates snap to exact 20m/60m raster cells with strict bounding-box validation.<br />
                • <strong>Rate Matching:</strong> 15-minute telemetry is trapezoidally integrated ($\int P(t) dt$) to preserve cumulative thermal soak energy without peak smoothing.<br />
                • <strong>PCHIP Monotonic Spline:</strong> 1-hour forecasts are interpolated to sub-hourly continuous time steps preserving physical derivative continuity.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* ── SECTION 4: RISK DISTRIBUTION ── */}
      {activeSection === 'risk' && riskData && !isLoading && (

        <div id="tour-data-science-risk">
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
            {/* Risk tiers */}
            <div style={{ background: '#0f172a', borderRadius: 12, padding: 20, border: '1px solid #1e293b' }}>
              <h3 style={{ color: '#f1f5f9', fontSize: 15, marginBottom: 16 }}>🎯 Risk Tier Distribution</h3>
              {(riskData.risk_distribution?.risk_tiers || []).map((tier: RiskTier, i: number) => (
                <div key={i} style={{ marginBottom: 12 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                    <span style={{ fontSize: 13, fontWeight: 600, color: riskColor(tier.tier) }}>{tier.tier}</span>
                    <span style={{ fontSize: 13, color: '#94a3b8' }}>{tier.count} hrs ({tier.percentage}%)</span>
                  </div>
                  <div style={{ height: 12, background: '#1e293b', borderRadius: 6, overflow: 'hidden' }}>
                    <div style={{ width: `${tier.percentage}%`, height: '100%', borderRadius: 6, background: riskColor(tier.tier), transition: 'width 0.5s' }} />
                  </div>
                </div>
              ))}
            </div>

            {/* Microclimate divergence */}
            {riskData.microclimate_divergence && !riskData.microclimate_divergence.error && (
              <div style={{ background: '#0f172a', borderRadius: 12, padding: 20, border: '1px solid #1e293b' }}>
                <h3 style={{ color: '#f1f5f9', fontSize: 15, marginBottom: 16 }}>🌡️ Microclimate Divergence</h3>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 16 }}>
                  <div style={{ background: '#1e293b', borderRadius: 8, padding: 12 }}>
                    <p style={{ margin: 0, fontSize: 11, color: '#64748b' }}>Mean Delta</p>
                    <p style={{ margin: 0, fontSize: 22, fontWeight: 700, color: '#ef4444' }}>+{riskData.microclimate_divergence.mean_delta_c}°C</p>
                  </div>
                  <div style={{ background: '#1e293b', borderRadius: 8, padding: 12 }}>
                    <p style={{ margin: 0, fontSize: 11, color: '#64748b' }}>Cohen's d</p>
                    <p style={{ margin: 0, fontSize: 22, fontWeight: 700, color: '#a78bfa' }}>{riskData.microclimate_divergence.cohens_d}</p>
                    <p style={{ margin: 0, fontSize: 10, color: '#64748b' }}>{riskData.microclimate_divergence.effect_size}</p>
                  </div>
                  <div style={{ background: '#1e293b', borderRadius: 8, padding: 12 }}>
                    <p style={{ margin: 0, fontSize: 11, color: '#64748b' }}>p-value</p>
                    <p style={{ margin: 0, fontSize: 18, fontWeight: 700, color: riskData.microclimate_divergence.is_significant ? '#22c55e' : '#f97316' }}>
                      {riskData.microclimate_divergence.p_value < 0.001 ? '<0.001' : riskData.microclimate_divergence.p_value?.toFixed(4)}
                    </p>
                  </div>
                  <div style={{ background: '#1e293b', borderRadius: 8, padding: 12 }}>
                    <p style={{ margin: 0, fontSize: 11, color: '#64748b' }}>Significant?</p>
                    <p style={{ margin: 0, fontSize: 18, fontWeight: 700, color: riskData.microclimate_divergence.is_significant ? '#22c55e' : '#ef4444' }}>
                      {riskData.microclimate_divergence.is_significant ? '✅ YES' : '❌ NO'}
                    </p>
                  </div>
                </div>
                <p style={{ fontSize: 12, color: '#94a3b8', lineHeight: 1.5, margin: 0 }}>
                  {riskData.microclimate_divergence.interpretation}
                </p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ── SECTION 4: ML MODELS ── */}
      {activeSection === 'ml' && mlData && !isLoading && (
        <div id="tour-data-science-ml">
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: 16 }}>
            {/* Physics Surrogate */}
            <div style={{ background: '#0f172a', borderRadius: 12, padding: 20, border: '1px solid #1e293b' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 16 }}>
                <Zap size={18} color="#eab308" />
                <h3 style={{ margin: 0, fontSize: 15, color: '#f1f5f9' }}>Physics Surrogate Regressor</h3>
              </div>
              <p style={{ fontSize: 12, color: '#64748b', marginBottom: 12 }}>{mlData.physics_surrogate?.description}</p>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 8 }}>
                <div style={{ background: '#1e293b', borderRadius: 8, padding: 12, textAlign: 'center' }}>
                  <p style={{ margin: 0, fontSize: 10, color: '#64748b' }}>R² Score</p>
                  <p style={{ margin: 0, fontSize: 24, fontWeight: 800, color: mlData.physics_surrogate?.r2_score == null ? '#64748b' : (mlData.physics_surrogate.r2_score > 0.95 ? '#22c55e' : '#eab308') }}>
                    {mlData.physics_surrogate?.r2_score ?? '—'}
                  </p>
                </div>
                <div style={{ background: '#1e293b', borderRadius: 8, padding: 12, textAlign: 'center' }}>
                  <p style={{ margin: 0, fontSize: 10, color: '#64748b' }}>MAE</p>
                  <p style={{ margin: 0, fontSize: 24, fontWeight: 800, color: mlData.physics_surrogate?.mae_celsius == null ? '#64748b' : '#06b6d4' }}>
                    {mlData.physics_surrogate?.mae_celsius == null ? '—' : `${mlData.physics_surrogate.mae_celsius}°C`}
                  </p>
                </div>
                <div style={{ background: '#1e293b', borderRadius: 8, padding: 12, textAlign: 'center' }}>
                  <p style={{ margin: 0, fontSize: 10, color: '#64748b' }}>Max Error</p>
                  <p style={{ margin: 0, fontSize: 24, fontWeight: 800, color: mlData.physics_surrogate?.max_error_celsius == null ? '#64748b' : '#f97316' }}>
                    {mlData.physics_surrogate?.max_error_celsius == null ? '—' : `${mlData.physics_surrogate.max_error_celsius}°C`}
                  </p>
                </div>
              </div>
              {mlData.physics_surrogate?.status_note ? (
                <p style={{ fontSize: 11, color: '#eab308', marginTop: 8, textAlign: 'center', lineHeight: 1.5 }}>
                  ⚠ {mlData.physics_surrogate.status_note}
                </p>
              ) : (
                <p style={{ fontSize: 11, color: '#22c55e', marginTop: 8, textAlign: 'center' }}>
                  ⚡ {mlData.physics_surrogate?.speedup_factor}
                </p>
              )}
            </div>

            {/* Anomaly Detection */}
            <div style={{ background: '#0f172a', borderRadius: 12, padding: 20, border: '1px solid #1e293b' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 16 }}>
                <AlertTriangle size={18} color="#ef4444" />
                <h3 style={{ margin: 0, fontSize: 15, color: '#f1f5f9' }}>Sensor Anomaly Detector</h3>
              </div>
              <p style={{ fontSize: 12, color: '#64748b', marginBottom: 12 }}>
                {mlData.anomaly_detection?.backend === 'numpy-zscore'
                  ? 'z-score percentile fallback'
                  : 'Isolation Forest'} with {mlData.anomaly_detection?.contamination_threshold} contamination threshold
              </p>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, marginBottom: 12 }}>
                <div style={{ background: '#1e293b', borderRadius: 8, padding: 12 }}>
                  <p style={{ margin: 0, fontSize: 10, color: '#64748b' }}>Anomalies</p>
                  <p style={{ margin: 0, fontSize: 28, fontWeight: 800, color: '#ef4444' }}>{mlData.anomaly_detection?.anomalies_detected}</p>
                </div>
                <div style={{ background: '#1e293b', borderRadius: 8, padding: 12 }}>
                  <p style={{ margin: 0, fontSize: 10, color: '#64748b' }}>Anomaly Rate</p>
                  <p style={{ margin: 0, fontSize: 28, fontWeight: 800, color: '#f97316' }}>{mlData.anomaly_detection?.anomaly_rate_pct}%</p>
                </div>
              </div>
              {/* Anomaly records */}
              <div style={{ maxHeight: 120, overflowY: 'auto' }}>
                {(mlData.anomaly_records || []).map((r: AnomalyRecord, i: number) => (
                  <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '4px 0', borderBottom: '1px solid #1e293b', fontSize: 11 }}>
                    <span style={{ color: '#64748b', width: 70 }}>{r.time_label}</span>
                    <span style={{ fontWeight: 700, color: r.label === 'ANOMALY' ? '#ef4444' : '#22c55e', width: 70 }}>{r.label}</span>
                    <span style={{ color: '#94a3b8' }}>score: {r.anomaly_score}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Survival Analysis */}
            <div style={{ background: '#0f172a', borderRadius: 12, padding: 20, border: '1px solid #1e293b', gridColumn: 'span 2' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 16 }}>
                <Activity size={18} color="#8b5cf6" />
                <h3 style={{ margin: 0, fontSize: 15, color: '#f1f5f9' }}>Remaining Useful Life — Weibull Survival Analysis</h3>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12, marginBottom: 16 }}>
                <div style={{ background: '#1e293b', borderRadius: 8, padding: 12 }}>
                  <p style={{ margin: 0, fontSize: 10, color: '#64748b' }}>Weibull Shape (k)</p>
                  <p style={{ margin: 0, fontSize: 20, fontWeight: 700, color: '#a78bfa' }}>{mlData.survival_analysis?.weibull_shape_k}</p>
                </div>
                <div style={{ background: '#1e293b', borderRadius: 8, padding: 12 }}>
                  <p style={{ margin: 0, fontSize: 10, color: '#64748b' }}>Weibull Scale (λ)</p>
                  <p style={{ margin: 0, fontSize: 20, fontWeight: 700, color: '#06b6d4' }}>{mlData.survival_analysis?.weibull_scale_lambda?.toLocaleString()}</p>
                </div>
                <div style={{ background: '#1e293b', borderRadius: 8, padding: 12 }}>
                  <p style={{ margin: 0, fontSize: 10, color: '#64748b' }}>Median RUL</p>
                  <p style={{ margin: 0, fontSize: 20, fontWeight: 700, color: '#22c55e' }}>{mlData.survival_analysis?.median_rul_years} yrs</p>
                </div>
                <div style={{ background: '#1e293b', borderRadius: 8, padding: 12 }}>
                  <p style={{ margin: 0, fontSize: 10, color: '#64748b' }}>RUL Under Stress</p>
                  <p style={{ margin: 0, fontSize: 20, fontWeight: 700, color: '#ef4444' }}>{mlData.survival_analysis?.rul_under_current_stress_years} yrs</p>
                </div>
              </div>
              {/* Survival curve (text-based) */}
              <div style={{ display: 'flex', gap: 2, alignItems: 'end', height: 80 }}>
                {(mlData.survival_analysis?.survival_curve?.survival_probability || []).slice(0, 40).map((p: number, i: number) => (
                  <div key={i} style={{
                    flex: 1, background: `linear-gradient(to top, rgba(139,92,246,${0.3 + p * 0.7}), rgba(99,102,241,${0.3 + p * 0.7}))`,
                    height: `${p * 100}%`, borderRadius: '2px 2px 0 0', minWidth: 4,
                  }} title={`S(${i * 3600})=${(p * 100).toFixed(1)}%`} />
                ))}
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 10, color: '#64748b', marginTop: 4 }}>
                <span>0 hrs</span>
                <span>← Aging Hours →</span>
                <span>{mlData.survival_analysis?.normal_insulation_life_hours?.toLocaleString()} hrs</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ── SECTION 5: TEMPORAL PATTERNS ── */}
      {activeSection === 'temporal' && riskData?.temporal_patterns && !isLoading && (
        <div id="tour-data-science-temporal">
          <h3 style={{ color: '#f1f5f9', fontSize: 16, marginBottom: 16 }}>📈 Hourly Temporal Pattern Analysis</h3>
          {riskData.temporal_patterns.peak_risk_window && (
            <div style={{ background: 'linear-gradient(135deg, rgba(239,68,68,0.1), rgba(249,115,22,0.1))', borderRadius: 12, padding: 16, border: '1px solid rgba(239,68,68,0.3)', marginBottom: 20, display: 'flex', gap: 20, alignItems: 'center' }}>
              <ShieldCheck size={20} color="#ef4444" />
              <div>
                <p style={{ margin: 0, fontSize: 13, fontWeight: 700, color: '#ef4444' }}>
                  Peak Risk Window: {riskData.temporal_patterns.peak_risk_window.peak_time_label}
                </p>
                <p style={{ margin: 0, fontSize: 12, color: '#94a3b8' }}>
                  T_hs = {riskData.temporal_patterns.peak_risk_window.peak_hot_spot_c}°C · Aging Factor V = {riskData.temporal_patterns.peak_risk_window.peak_aging_factor}×
                </p>
              </div>
            </div>
          )}
          <div style={{ background: '#0f172a', borderRadius: 12, border: '1px solid #1e293b', overflow: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 12 }}>
              <thead>
                <tr style={{ background: '#1e293b' }}>
                  {['Hour', 'Time', 'T_hs (°C)', 'Aging V', 'BESS SoC', 'Ambient 2m', 'Safety Margin', 'Load K'].map(h => (
                    <th key={h} style={{ padding: '10px 8px', textAlign: 'left', color: '#94a3b8', fontSize: 11 }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {(riskData.temporal_patterns.hourly_records || []).map((r: TemporalRecord, i: number) => (
                  <tr key={i} style={{ borderBottom: '1px solid #1e293b' }}>
                    <td style={{ padding: 8, color: '#64748b' }}>{r.hour_of_day}:00</td>
                    <td style={{ padding: 8, color: '#e2e8f0' }}>{r.time_label}</td>
                    <td style={{ padding: 8, fontWeight: 700, color: (r.estimated_hot_spot_c || 0) >= 140 ? '#ef4444' : (r.estimated_hot_spot_c || 0) >= 120 ? '#f97316' : '#22c55e' }}>
                      {r.estimated_hot_spot_c}
                    </td>
                    <td style={{ padding: 8, color: (r.aging_factor_v || 0) >= 4 ? '#ef4444' : '#94a3b8' }}>{r.aging_factor_v}×</td>
                    <td style={{ padding: 8, color: '#06b6d4' }}>{r.bess_soc_pct}%</td>
                    <td style={{ padding: 8, color: '#f97316' }}>{r.fortyguard_2m_ambient_c}°C</td>
                    <td style={{ padding: 8, color: (r.safety_margin_c || 0) < 0 ? '#ef4444' : '#22c55e' }}>{r.safety_margin_c}°C</td>
                    <td style={{ padding: 8, color: '#94a3b8' }}>{r.baseline_load_ratio_k}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
