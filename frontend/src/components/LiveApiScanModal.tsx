import React, { useState, useEffect } from 'react';
import {
  X,
  Zap,
  Globe,
  Radio,
  Clock,
  ShieldCheck,
  CheckCircle2,
  AlertCircle,
  RefreshCw,
  Sparkles,
  Layers,
  Flame,
  Sun,
  Activity,
} from 'lucide-react';
import { API_BASE } from '../utils/api';

interface LiveApiScanModalProps {
  isOpen: boolean;
  onClose: () => void;
}

interface ApiUsageData {
  status: string;
  api_key_configured: boolean;
  credit_summary?: {
    total_available_credits: number;
    cycle_credits_used: number;
    cycle_remaining_credits: number;
    cycle_usage_percentage: number;
  };
  plan_details?: {
    plan_type: string;
    billing_period?: string;
    active?: boolean;
  };
  data?: any;
}

const PRESET_LOCATIONS = [
  { name: 'Phoenix, AZ (Substation TX-04)', lat: 33.4484, lon: -112.0740, date: '2024-07-15' },
  { name: 'San Jose, CA (Diridon Energy Hub)', lat: 37.3382, lon: -121.8863, date: '2024-07-15' },
  { name: 'Las Vegas, NV (Downtown Feeder)', lat: 36.1699, lon: -115.1398, date: '2024-07-15' },
  { name: 'Houston, TX (Energy Corridor)', lat: 29.7604, lon: -95.3698, date: '2024-07-15' },
];

export const LiveApiScanModal: React.FC<LiveApiScanModalProps> = ({ isOpen, onClose }) => {
  const [usage, setUsage] = useState<ApiUsageData | null>(null);
  const [isFetchingUsage, setIsFetchingUsage] = useState<boolean>(false);

  // Scan Form State
  const [city, setCity] = useState<string>('Phoenix, AZ (Substation TX-04)');
  const [latitude, setLatitude] = useState<number>(33.4484);
  const [longitude, setLongitude] = useState<number>(-112.0740);
  const [startDate, setStartDate] = useState<string>('2024-07-15');
  const [analyticType, setAnalyticType] = useState<string>('tcm');
  const [thresholdC, setThresholdC] = useState<number>(40.0);

  // Execution State
  const [isScanning, setIsScanning] = useState<boolean>(false);
  const [scanResult, setScanResult] = useState<any>(null);
  const [scanError, setScanError] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [analysis, setAnalysis] = useState<any>(null);
  const [analysisError, setAnalysisError] = useState<string | null>(null);

  // Fetch usage on open
  const fetchUsage = async () => {
    setIsFetchingUsage(true);
    try {
      const resp = await fetch(`${API_BASE}/api/v1/scan/usage`);
      if (resp.ok) {
        const json = await resp.json();
        setUsage(json);
      }
    } catch (e) {
      console.warn('Failed to fetch API usage', e);
    } finally {
      setIsFetchingUsage(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchUsage();
    }
  }, [isOpen]);

  const handleSelectPreset = (preset: typeof PRESET_LOCATIONS[0]) => {
    setCity(preset.name);
    setLatitude(preset.lat);
    setLongitude(preset.lon);
    setStartDate(preset.date);
  };

  // Runs the full multi-physics + CBF + economics stack against the coordinates
  // that were just scanned, instead of the frozen Phoenix benchmark curve.
  // 0.0 is a legitimate measurement (Houston genuinely logs P40 = 0.0h), so
  // this must test for null, not falsiness. The previous panel used
  // `value || '12.0'` and therefore relabelled a real zero as Phoenix's 12.0h.
  const fmt = (v: any, unit = '') =>
    v === null || v === undefined || Number.isNaN(v) ? '—' : `${v}${unit}`;

  const handleAnalyzeScan = async () => {
    setIsAnalyzing(true);
    setAnalysis(null);
    setAnalysisError(null);
    try {
      const resp = await fetch(`${API_BASE}/api/v1/sandbox/simulate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          latitude: Number(latitude),
          longitude: Number(longitude),
          analysis_date: startDate,
          city,
        }),
      });
      if (!resp.ok) {
        const errJson = await resp.json().catch(() => ({}));
        throw new Error(errJson.detail || `Analysis failed with HTTP ${resp.status}`);
      }
      setAnalysis(await resp.json());
    } catch (err: any) {
      setAnalysisError(err.message || 'Analysis failed');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleExecuteScan = async () => {
    setIsScanning(true);
    setScanResult(null);
    setScanError(null);
    setAnalysis(null);
    setAnalysisError(null);

    try {
      const resp = await fetch(`${API_BASE}/api/v1/scan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          city,
          latitude: Number(latitude),
          longitude: Number(longitude),
          start_date: startDate,
          analytic_type: analyticType,
          threshold_c: Number(thresholdC),
        }),
      });

      if (!resp.ok) {
        const errJson = await resp.json().catch(() => ({}));
        throw new Error(errJson.detail || `Scan request failed with HTTP ${resp.status}`);
      }

      const json = await resp.json();
      setScanResult(json);
      // Refresh credit usage after call
      fetchUsage();
    } catch (err: any) {
      setScanError(err.message || 'Scan execution failed');
    } finally {
      setIsScanning(false);
    }
  };

  if (!isOpen) return null;

  const creditSummary = usage?.data?.credit_summary || usage?.credit_summary || {
    total_available_credits: 2000000,
    cycle_credits_used: 0,
    cycle_remaining_credits: 2000000,
    cycle_usage_percentage: 0.0,
  };

  const planDetails = usage?.data?.plan_details || usage?.plan_details || {
    plan_type: 'Hackathon',
    active: true,
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-in fade-in duration-200">
      <div className="relative w-full max-w-3xl glass-panel rounded-3xl border border-slate-700/80 bg-[#0B0F19] p-6 shadow-2xl overflow-hidden max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-2xl bg-amber-500/15 text-amber-400 border border-amber-500/30">
              <Radio className="h-6 w-6 animate-pulse" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-base font-extrabold text-white font-heading tracking-wide">
                  FORTYGUARD LIVE CLOUD INGESTION & QUOTA HUB
                </h2>
                <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 flex items-center gap-1">
                  <span className="h-1.5 w-1.5 rounded-full bg-emerald-400"></span>
                  LIVE API
                </span>
              </div>
              <p className="text-xs text-slate-400 font-mono mt-0.5">
                Trigger ad-hoc 2-meter microclimate scans against FortyGuard tOS Enterprise API
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-400 hover:text-white transition-all"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Scrollable Content */}
        <div className="flex-1 overflow-y-auto py-4 space-y-5 pr-1 font-mono text-xs">
          {/* Real-Time Credit Balance Card */}
          <div className="p-4 rounded-2xl bg-slate-950/90 border border-slate-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-slate-400">Subscription Plan:</span>
                <span className="text-amber-400 font-bold">{planDetails.plan_type || 'Hackathon Active'}</span>
                <span className="text-slate-600">|</span>
                <span className="text-slate-400">Endpoint:</span>
                <span className="text-cyan-400">https://api.fortyguard.com/v1</span>
              </div>
              <div className="text-[11px] text-slate-500">
                Billing Cycle: {planDetails.billing_period || 'Aug 20 - Sep 24, 2026'} · Deducts credits on completed tasks
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="text-right">
                <div className="text-[10px] text-slate-500 uppercase">Available Credits</div>
                <div className="text-base font-black text-emerald-400">
                  {creditSummary.cycle_remaining_credits?.toLocaleString()} / {creditSummary.total_available_credits?.toLocaleString()}
                </div>
              </div>
              <button
                onClick={fetchUsage}
                disabled={isFetchingUsage}
                className="p-2 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-400 hover:text-white transition-all"
                title="Refresh Credit Quota"
              >
                <RefreshCw className={`h-4 w-4 ${isFetchingUsage ? 'animate-spin text-amber-400' : ''}`} />
              </button>
            </div>
          </div>

          {/* Quick Presets */}
          <div>
            <label className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-2">
              Select Preset Target Corridor:
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {PRESET_LOCATIONS.map((preset) => (
                <button
                  key={preset.name}
                  type="button"
                  onClick={() => handleSelectPreset(preset)}
                  className={`p-2.5 rounded-xl border text-left transition-all ${
                    latitude === preset.lat && longitude === preset.lon
                      ? 'border-amber-400 bg-amber-500/10 text-amber-300 shadow-md shadow-amber-500/20'
                      : 'border-slate-800 bg-slate-900/60 text-slate-300 hover:border-slate-700 hover:bg-slate-900'
                  }`}
                >
                  <div className="font-bold flex items-center gap-1.5">
                    <Globe className="h-3.5 w-3.5 text-amber-400" />
                    {preset.name}
                  </div>
                  <div className="text-[10px] text-slate-500 mt-0.5">
                    ({preset.lat.toFixed(4)}°, {preset.lon.toFixed(4)}°) · {preset.date}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Custom Coordinates & Date Form */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 p-4 rounded-2xl bg-slate-950/70 border border-slate-800/80">
            <div>
              <label className="text-[11px] text-slate-400 block mb-1">Latitude (°N)</label>
              <input
                type="number"
                step="0.0001"
                value={latitude}
                onChange={(e) => setLatitude(parseFloat(e.target.value))}
                className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-white font-mono text-xs focus:ring-1 focus:ring-amber-400 outline-none"
              />
            </div>
            <div>
              <label className="text-[11px] text-slate-400 block mb-1">Longitude (°W)</label>
              <input
                type="number"
                step="0.0001"
                value={longitude}
                onChange={(e) => setLongitude(parseFloat(e.target.value))}
                className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-white font-mono text-xs focus:ring-1 focus:ring-amber-400 outline-none"
              />
            </div>
            <div>
              <label className="text-[11px] text-slate-400 block mb-1">Catalog Date (YYYY-MM-DD)</label>
              <input
                type="text"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-white font-mono text-xs focus:ring-1 focus:ring-amber-400 outline-none"
              />
            </div>
          </div>

          {/* Scan Layer & Threshold */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="text-[11px] text-slate-400 block mb-1">Analytic Heat Layer</label>
              <select
                value={analyticType}
                onChange={(e) => setAnalyticType(e.target.value)}
                className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-white font-mono text-xs focus:ring-1 focus:ring-amber-400 outline-none"
              >
                <option value="tcm">tcm - 2m Snapshot Temperature</option>
                <option value="persistence">persistence - Continuous Heat Run (P40)</option>
                <option value="exceedance">exceedance - Degree-Hour Threshold</option>
              </select>
            </div>
            <div>
              <label className="text-[11px] text-slate-400 block mb-1">Heat Threshold (°C)</label>
              <input
                type="number"
                value={thresholdC}
                onChange={(e) => setThresholdC(parseFloat(e.target.value))}
                className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-white font-mono text-xs focus:ring-1 focus:ring-amber-400 outline-none"
              />
            </div>
          </div>

          {/* Results Box */}
          {scanResult && (
            <div className="p-4 rounded-2xl bg-emerald-950/30 border border-emerald-500/40 text-xs font-mono space-y-2 animate-in fade-in">
              <div className="flex items-center gap-2 text-emerald-400 font-bold">
                <CheckCircle2 className="h-4 w-4" />
                Live FortyGuard Cloud Ingestion Succeeded!
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-2 border-t border-emerald-500/20 text-[11px]">
                <div className="p-2 rounded-xl bg-slate-950/80">
                  <div className="text-slate-500">Peak 2m Air:</div>
                  <div className="text-sm font-bold text-rose-400">
                    {fmt(scanResult?.metrics?.peak_2m_ambient_c, '°C')}
                  </div>
                </div>
                <div className="p-2 rounded-xl bg-slate-950/80">
                  <div className="text-slate-500">Solar Irradiance:</div>
                  <div className="text-sm font-bold text-amber-400">
                    {fmt(scanResult?.metrics?.solar_irradiance_w_m2, ' W/m²')}
                  </div>
                </div>
                <div className="p-2 rounded-xl bg-slate-950/80">
                  <div className="text-slate-500">Wet Bulb:</div>
                  <div className="text-sm font-bold text-cyan-400">
                    {fmt(scanResult?.metrics?.wet_bulb_temp_c, '°C')}
                  </div>
                </div>
                <div className="p-2 rounded-xl bg-slate-950/80">
                  <div className="text-slate-500">Persistence (P40):</div>
                  <div className="text-sm font-bold text-emerald-400">
                    {fmt(scanResult?.metrics?.persistence_hours_p40, 'h')}
                  </div>
                </div>
              </div>

              <div className="pt-2 border-t border-emerald-500/20 space-y-2">
                <div className="text-[10px] text-slate-400 leading-relaxed">
                  {scanResult?.metrics?.n_hours ?? 0}h 2m profile ·{' '}
                  {scanResult?.metrics?.analysis_date ?? '—'} · source{' '}
                  <span className="text-slate-300">{scanResult?.metrics?.data_source ?? '—'}</span>
                  {scanResult?.parcel_id && (
                    <> · stored as <span className="text-emerald-300">{scanResult.parcel_id}</span> in <span className="text-emerald-300">microclimate_parcel_store</span></>
                  )}
                </div>

                <button
                  onClick={handleAnalyzeScan}
                  disabled={isAnalyzing}
                  className="w-full py-2 rounded-xl bg-amber-500/20 border border-amber-500/50 text-amber-300 font-bold text-[11px] hover:bg-amber-500/30 disabled:opacity-50 transition"
                >
                  {isAnalyzing ? 'Running multi-physics on this scan…' : 'Run Physics + Economics on This Scan'}
                </button>

                {analysisError && (
                  <div className="text-[10px] text-rose-300 font-mono">{analysisError}</div>
                )}

                {analysis && (
                  <div className="grid grid-cols-2 gap-2 text-[11px]">
                    <div className="p-2 rounded-xl bg-slate-950/80">
                      <div className="text-slate-500">Baseline hot-spot:</div>
                      <div className="text-sm font-bold text-rose-400">
                        {fmt(analysis?.baseline_summary?.peak_hot_spot_c, '°C')}
                      </div>
                    </div>
                    <div className="p-2 rounded-xl bg-slate-950/80">
                      <div className="text-slate-500">Mitigated hot-spot:</div>
                      <div className="text-sm font-bold text-emerald-400">
                        {fmt(analysis?.mitigated_summary?.peak_hot_spot_c, '°C')}
                      </div>
                    </div>
                    <div className="p-2 rounded-xl bg-slate-950/80">
                      <div className="text-slate-500">Net avoided loss:</div>
                      <div className="text-sm font-bold text-amber-400">
                        {analysis?.economic_evaluation?.net_avoided_loss_usd == null
                          ? '—'
                          : `$${Number(analysis.economic_evaluation.net_avoided_loss_usd).toLocaleString()}`}
                      </div>
                    </div>
                    <div className="p-2 rounded-xl bg-slate-950/80">
                      <div className="text-slate-500">ROI multiple:</div>
                      <div className="text-sm font-bold text-cyan-400">
                        {fmt(analysis?.economic_evaluation?.roi_multiple, '×')}
                      </div>
                    </div>
                    <div className="col-span-2 text-[10px] text-slate-400">
                      Mode <span className="text-slate-300">{analysis?.scan_binding?.mode ?? '—'}</span> ·
                      measured spread {fmt(analysis?.scan_binding?.measured_intra_aoi_spread_c, '°C')} ·
                      {' '}{analysis?.scan_binding?.n_hours ?? '—'}h solved
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Error Box */}
          {scanError && (
            <div className="p-4 rounded-2xl bg-rose-950/40 border border-rose-500/50 text-rose-300 text-xs font-mono flex items-start gap-2">
              <AlertCircle className="h-4 w-4 text-rose-400 flex-shrink-0 mt-0.5" />
              <div>
                <strong className="block font-bold">Cloud Scan Failed:</strong>
                {scanError}
              </div>
            </div>
          )}
        </div>

        {/* Footer Actions */}
        <div className="pt-4 border-t border-slate-800 flex items-center justify-between">
          <div className="text-[11px] text-slate-500 font-mono">
            Calls <code className="text-slate-300 font-bold">POST /api/v1/scan</code> → FortyGuard Async Task Pipeline
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={onClose}
              className="px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white text-xs font-bold transition-all"
            >
              Close
            </button>

            <button
              onClick={handleExecuteScan}
              disabled={isScanning}
              className="px-5 py-2 rounded-xl bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-400 hover:to-orange-400 text-slate-950 font-bold text-xs shadow-lg shadow-amber-500/25 flex items-center gap-2 transition-all disabled:opacity-50"
            >
              {isScanning ? (
                <>
                  <RefreshCw className="h-4 w-4 animate-spin" />
                  Polling FortyGuard Cloud...
                </>
              ) : (
                <>
                  <Zap className="h-4 w-4 fill-current" />
                  Execute Live Cloud Scan
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
