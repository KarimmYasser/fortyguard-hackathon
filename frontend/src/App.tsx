import React, { useState, useEffect, useCallback, lazy, Suspense } from 'react';
import { SpeedInsights } from '@vercel/speed-insights/react';
import { Analytics } from '@vercel/analytics/react';
import { Navbar, ActiveTab } from './components/Navbar';
import { TabErrorBoundary } from './components/TabErrorBoundary';
import { DataProvenanceBadge } from './components/DataProvenanceBadge';
import { SimulationProvenancePanel } from './components/SimulationProvenancePanel';
import { HomePitchViewer } from './components/HomePitchViewer';
import { ReplayDataset, TimelineStep } from './types';
import { startTourGuide } from './utils/tourGuide';
import { API_BASE } from './utils/api';

/**
 * Everything below the default (home) tab is code-split.
 *
 * ECharts (~1.1 MB) and KaTeX (~256 KB) dominated the entry bundle even though
 * the landing tab renders neither, so the browser had to download, parse, and
 * execute them before the largest element could paint. Lazy boundaries keep
 * them off the LCP critical path and load them on first tab activation.
 */
const named = <K extends string>(key: K) =>
  (mod: Record<K, React.ComponentType<any>>) => ({ default: mod[key] });

const ReplayControlBar = lazy(() => import('./components/ReplayControlBar').then(named('ReplayControlBar')));
const PortfolioOperationsViewer = lazy(() => import('./components/PortfolioOperationsViewer').then(named('PortfolioOperationsViewer')));
const HeroKpiGrid = lazy(() => import('./components/HeroKpiGrid').then(named('HeroKpiGrid')));
const EChartsPhysicsTelemetry = lazy(() => import('./components/EChartsPhysicsTelemetry').then(named('EChartsPhysicsTelemetry')));
const GeospatialMicroclimateViewer = lazy(() => import('./components/GeospatialMicroclimateViewer').then(named('GeospatialMicroclimateViewer')));
const ScientificMoatsViewer = lazy(() => import('./components/ScientificMoatsViewer').then(named('ScientificMoatsViewer')));
const AgentGraphViewer = lazy(() => import('./components/AgentGraphViewer').then(named('AgentGraphViewer')));
const EconomicAuditViewer = lazy(() => import('./components/EconomicAuditViewer').then(named('EconomicAuditViewer')));
const WhatIfSandboxPanel = lazy(() => import('./components/WhatIfSandboxPanel').then(named('WhatIfSandboxPanel')));
const MultiDay72hHeatwaveViewer = lazy(() => import('./components/MultiDay72hHeatwaveViewer').then(named('MultiDay72hHeatwaveViewer')));
const ACPowerFlowSingleLineViewer = lazy(() => import('./components/ACPowerFlowSingleLineViewer').then(named('ACPowerFlowSingleLineViewer')));
const IEEEAnnexGBenchmarkViewer = lazy(() => import('./components/IEEEAnnexGBenchmarkViewer').then(named('IEEEAnnexGBenchmarkViewer')));
const GroundTruthComparisonViewer = lazy(() => import('./components/GroundTruthComparisonViewer').then(named('GroundTruthComparisonViewer')));
const AcademicProvenanceViewer = lazy(() => import('./components/AcademicProvenanceViewer').then(named('AcademicProvenanceViewer')));
const SafetyGateCard = lazy(() => import('./components/SafetyGateCard').then(named('SafetyGateCard')));
const AuditLedger = lazy(() => import('./components/AuditLedger').then(named('AuditLedger')));
const LiveApiScanModal = lazy(() => import('./components/LiveApiScanModal').then(named('LiveApiScanModal')));
const DatabaseAuditModal = lazy(() => import('./components/DatabaseAuditModal').then(named('DatabaseAuditModal')));
const DataScienceStudio = lazy(() => import('./components/DataScienceStudio').then(named('DataScienceStudio')));

const PanelFallback: React.FC<{ label?: string }> = ({ label = 'Loading module' }) => (
  <div className="rounded-2xl border border-slate-800 bg-slate-900/40 px-6 py-10 flex items-center justify-center gap-3">
    <div className="h-4 w-4 rounded-full border-2 border-amber-500/20 border-t-amber-500 animate-spin" />
    <span className="text-xs font-mono text-slate-400">{label}...</span>
  </div>
);

/** Data-backed tabs cannot render until the replay dataset arrives. */
const DataPending: React.FC = () => (
  <div className="rounded-2xl border border-slate-800 bg-slate-900/40 px-6 py-16 flex flex-col items-center justify-center gap-3">
    <div className="h-10 w-10 rounded-full border-4 border-amber-500/20 border-t-amber-500 animate-spin" />
    <h2 className="text-sm font-bold font-heading tracking-wide">Ingesting replay dataset...</h2>
    <p className="text-xs text-slate-400 font-mono">IEEE C57.91 &amp; FortyGuard 2m Boundary Engine</p>
  </div>
);


export const App: React.FC = () => {
  const [data, setData] = useState<ReplayDataset | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [currentHourIndex, setCurrentHourIndex] = useState<number>(7); // 01:00 PM Peak
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [playbackSpeed, setPlaybackSpeed] = useState<number>(1);
  const [isMitigatedMode, setIsMitigatedMode] = useState<boolean>(true);
  const [activeTab, setActiveTab] = useState<ActiveTab>('home');
  const [isLiveScanOpen, setIsLiveScanOpen] = useState<boolean>(false);
  const [isDbModalOpen, setIsDbModalOpen] = useState<boolean>(false);
  // Which dataset the dashboard is currently showing. Null = Phoenix benchmark.
  const [activeBinding, setActiveBinding] = useState<any>(null);


  // Fetch replay dataset from backend
  const fetchReplayData = useCallback(async () => {
    setIsLoading(true);
    try {
      const resp = await fetch(`${API_BASE}/api/v1/replay/phoenix-2023`);
      if (resp.ok) {
        const json = await resp.json();
        setData(json);
      } else {
        console.warn('Backend returned non-200');
      }
    } catch (err) {
      console.warn('Failed to fetch from backend; using fallback', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchReplayData();
  }, [fetchReplayData]);

  // Handle dynamic sandbox results
  const handleSandboxSimulateResult = (simResult: any) => {
    if (simResult?.scan_binding?.mode === 'live_scan') {
      setActiveBinding({ ...simResult.scan_binding, cache_hit: simResult.cache?.hit === true });
    }
    if (data && simResult.timeline_steps) {
      const patch = simResult?.scan_binding?.scenario_metadata_patch;
      // Merge rather than replace: the patch only carries what the scan can
      // actually speak to, so canyon/soil metrics keep their existing values.
      const mergedMetadata = patch
        ? {
            ...data.scenario_metadata,
            name: `${patch.location?.city ?? 'Live scan'} — live FortyGuard capture`,
            location: { ...data.scenario_metadata.location, ...patch.location },
            date_range: { ...data.scenario_metadata.date_range, ...patch.date_range },
            persistence_metrics:
              patch.persistence_metrics ?? data.scenario_metadata.persistence_metrics,
          }
        : data.scenario_metadata;
      setData({
        ...data,
        scenario_metadata: mergedMetadata,
        provenance: simResult.provenance ?? data.provenance,
        timeline_steps: simResult.timeline_steps,
        baseline_summary: simResult.baseline_summary,
        mitigated_summary: simResult.mitigated_summary,
        safety_gate_verdict: simResult.safety_gate_verdict,
        economic_evaluation: simResult.economic_evaluation,
        soil_cable_state: simResult.soil_cable_state,
        virtual_moisture_state: simResult.virtual_moisture_state,
        urban_canyon_state: simResult.urban_canyon_state,
        sensitivity_analysis: simResult.sensitivity_analysis,
        integrated_grid_evaluation: simResult.integrated_grid_evaluation,
      });
    }
  };

  // Playback timer loop with dynamic speed
  useEffect(() => {
    let interval: any = null;
    if (isPlaying && data?.timeline_steps) {
      const delay = Math.round(1500 / playbackSpeed);
      interval = setInterval(() => {
        setCurrentHourIndex((prev) => (prev + 1) % data.timeline_steps.length);
      }, delay);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isPlaying, playbackSpeed, data]);

  /**
   * The shell is NOT gated on the replay fetch.
   *
   * That request is a Python serverless function with a multi-second cold
   * start, and blocking the whole tree on it pushed Largest Contentful Paint
   * past 4s. The default (home) tab needs no dataset at all, so it paints
   * immediately and only data-backed tabs wait.
   */
  const dataset = data;
  const currentStep: TimelineStep | null = dataset
    ? dataset.timeline_steps[currentHourIndex] || dataset.timeline_steps[0]
    : null;

  return (
    <div className="min-h-screen bg-[#080C14] text-slate-100 flex flex-col selection:bg-amber-500/30 selection:text-amber-200">
      {/* 1. Global Navigation Bar */}
      <Navbar
        metadata={dataset?.scenario_metadata}
        verdict={dataset?.safety_gate_verdict}
        isMitigatedMode={isMitigatedMode}
        onToggleMode={() => setIsMitigatedMode(!isMitigatedMode)}
        activeTab={activeTab}
        onSelectTab={setActiveTab}
        onRefresh={fetchReplayData}
        onOpenLiveScan={() => setIsLiveScanOpen(true)}
        onOpenDatabaseModal={() => setIsDbModalOpen(true)}
        onStartTour={() =>
          startTourGuide({
            activeTab,
            onNavigateTab: setActiveTab,
            onOpenLiveScan: () => setIsLiveScanOpen(true),
            onOpenDatabaseModal: () => setIsDbModalOpen(true),
          })
        }
        isLoading={isLoading}
      />


      {/* Main Content Area */}
      <main className="flex-1 max-w-[1600px] w-full mx-auto px-4 md:px-8 py-6 space-y-6">
        {/* Every tab's copy is written around the Phoenix benchmark, so say
            plainly when the numbers on screen came from somewhere else. */}
        {activeBinding && (
          <div className="flex flex-wrap items-center gap-3 px-4 py-3 rounded-2xl bg-amber-500/10 border border-amber-500/40 text-[11px] font-mono">
            <span className="px-2 py-0.5 rounded-lg bg-amber-500/20 text-amber-300 font-bold">LIVE SCAN</span>
            <span className="text-slate-300">
              Showing <strong className="text-amber-300">{activeBinding.city}</strong>
              {activeBinding.analysis_date ? ` · ${activeBinding.analysis_date}` : ''}
              {' '}· peak 2m {activeBinding.peak_2m_ambient_c}°C · measured spread{' '}
              {activeBinding.measured_intra_aoi_spread_c}°C · {activeBinding.n_hours}h solved
            </span>
            {activeBinding.cache_hit && (
              <span
                className="px-2 py-0.5 rounded-lg bg-emerald-500/20 text-emerald-300 font-bold"
                title="Identical inputs, so this is the stored solve rather than a recomputation."
              >
                REPLAYED FROM STORE
              </span>
            )}
            <span className="text-slate-500">Not the Phoenix 2023 benchmark.</span>
            <button
              onClick={() => { setActiveBinding(null); fetchReplayData(); }}
              className="ml-auto px-3 py-1 rounded-lg bg-slate-800 border border-slate-600 text-slate-300 hover:bg-slate-700 transition"
            >
              Reset to Phoenix benchmark
            </button>
          </div>
        )}
        {dataset?.provenance && activeTab !== 'home' && (
          <SimulationProvenancePanel provenance={dataset.provenance} />
        )}
        <TabErrorBoundary name={activeTab}>
          {/* TAB 0: Executive Home & Video Pitch Showcase - renders instantly */}
          {activeTab === 'home' && (
            <HomePitchViewer
              onNavigateTab={setActiveTab}
              onOpenLiveScan={() => setIsLiveScanOpen(true)}
              onOpenDatabaseModal={() => setIsDbModalOpen(true)}
            />
          )}

          {activeTab === 'portfolio_operations' && (
            <Suspense fallback={<PanelFallback label="Loading portfolio operations" />}>
              <PortfolioOperationsViewer />
            </Suspense>
          )}

          {activeTab !== 'home' && activeTab !== 'portfolio_operations' && (!dataset || !currentStep ? (
            <DataPending />
          ) : (
          <Suspense fallback={<PanelFallback />}>
          {/* Global Replay Scrub Bar (Visible Across Interactive Simulation Tabs) */}
          {(
            <ReplayControlBar
              metadata={dataset.scenario_metadata}
              steps={dataset.timeline_steps}
              currentHourIndex={currentHourIndex}
              onSelectHour={setCurrentHourIndex}
              isPlaying={isPlaying}
              onTogglePlay={() => setIsPlaying(!isPlaying)}
              onReset={() => {
                setIsPlaying(false);
                setCurrentHourIndex(0);
              }}
              speed={playbackSpeed}
              onChangeSpeed={setPlaybackSpeed}
            />
          )}

          {/* TAB 1: Mission Control Overview */}
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {/* State the data's origin up front, rather than letting a
                  fixture-backed replay read as though it were a live feed. */}
              <div className="flex items-center justify-end">
                <DataProvenanceBadge
                  source={dataset.scenario_metadata.persistence_metrics.data_source}
                  analysisDate={dataset.scenario_metadata.persistence_metrics.analysis_date}
                />
              </div>

              <HeroKpiGrid
                isMitigated={isMitigatedMode}
                baselineSummary={dataset.baseline_summary}
                mitigatedSummary={dataset.mitigated_summary}
                verdict={dataset.safety_gate_verdict}
                economic={dataset.economic_evaluation}
                persistence={dataset.scenario_metadata.persistence_metrics}
                currentStep={currentStep}
              />

              <EChartsPhysicsTelemetry
                steps={dataset.timeline_steps}
                currentHourIndex={currentHourIndex}
                isMitigated={isMitigatedMode}
                onSelectHour={setCurrentHourIndex}
              />

              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <div className="lg:col-span-6">
                  <SafetyGateCard
                    verdict={dataset.safety_gate_verdict}
                    isMitigated={isMitigatedMode}
                  />
                </div>
                <div className="lg:col-span-6">
                  <AuditLedger />
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: Live What-If Stress Studio Sandbox */}
          {activeTab === 'sandbox' && (
            <div className="space-y-6">
              <WhatIfSandboxPanel
                onSimulateResult={handleSandboxSimulateResult}
                onResetToDefault={fetchReplayData}
              />

              <HeroKpiGrid
                isMitigated={isMitigatedMode}
                baselineSummary={dataset.baseline_summary}
                mitigatedSummary={dataset.mitigated_summary}
                verdict={dataset.safety_gate_verdict}
                economic={dataset.economic_evaluation}
                persistence={dataset.scenario_metadata.persistence_metrics}
                currentStep={currentStep}
              />

              <EChartsPhysicsTelemetry
                steps={dataset.timeline_steps}
                currentHourIndex={currentHourIndex}
                isMitigated={isMitigatedMode}
                onSelectHour={setCurrentHourIndex}
              />
            </div>
          )}

          {/* TAB 3: 72-Hour Compounding Heatwave */}
          {activeTab === 'multi_day_72h' && (
            <MultiDay72hHeatwaveViewer />
          )}

          {/* TAB 4: AC Distribution Feeder Power Flow */}
          {activeTab === 'power_flow' && (
            <ACPowerFlowSingleLineViewer />
          )}

          {/* TAB 5: IEEE Annex G Standards Benchmark */}
          {activeTab === 'ieee_annex_g' && (
            <IEEEAnnexGBenchmarkViewer />
          )}

          {/* Independent station validation */}
          {activeTab === 'ground_truth' && (
            <GroundTruthComparisonViewer />
          )}

          {/* TAB 6: Academic Provenance & alphaXiv Literature */}
          {activeTab === 'academic_provenance' && (
            <AcademicProvenanceViewer />
          )}

          {/* TAB 7: Hyperlocal 2m GIS Map */}
          {activeTab === 'gis_map' && (
            <GeospatialMicroclimateViewer

              heatmapData={dataset.heatmap_geojson_tiles}
              currentAmbient2m={currentStep.fortyguard_2m_ambient_c}
              coolestTile2m={currentStep.coolest_tile_2m_c}
              deltaAmbient={currentStep.intra_aoi_spread_c}
              onOpenLiveScan={() => setIsLiveScanOpen(true)}
            />
          )}

          {/* TAB 7: Four Scientific Moats */}
          {activeTab === 'physics_moats' && (
            <ScientificMoatsViewer
              soilState={dataset.soil_cable_state}
              moistureState={dataset.virtual_moisture_state}
              verdict={dataset.safety_gate_verdict}
            />
          )}

          {/* TAB 8: LangGraph Engine */}
          {activeTab === 'agent_graph' && (
            <AgentGraphViewer
              verdict={dataset.safety_gate_verdict}
              economic={dataset.economic_evaluation}
            />
          )}

          {/* TAB 9: Avoided Loss & ROI */}
          {activeTab === 'financial_roi' && (
            <EconomicAuditViewer
              economic={dataset.economic_evaluation}
              baselineSummary={dataset.baseline_summary}
              mitigatedSummary={dataset.mitigated_summary}
              metadata={dataset.scenario_metadata}
              steps={dataset.timeline_steps}
            />
          )}

          {/* TAB 12: Data Science & Analytics Studio */}
          {activeTab === 'data_science' && (
            <DataScienceStudio />
          )}
          </Suspense>
          ))}
        </TabErrorBoundary>
      </main>

      {/* Live FortyGuard API Cloud Ingestion Modal (chunk fetched on open) */}
      {isLiveScanOpen && (
        <Suspense fallback={null}>
          <LiveApiScanModal
            isOpen={isLiveScanOpen}
            onClose={() => setIsLiveScanOpen(false)}
            onSimulationResult={handleSandboxSimulateResult}
          />
        </Suspense>
      )}

      {/* Enterprise Database Hub & Audit Modal (chunk fetched on open) */}
      {isDbModalOpen && (
        <Suspense fallback={null}>
          <DatabaseAuditModal
            isOpen={isDbModalOpen}
            onClose={() => setIsDbModalOpen(false)}
            onSimulationResult={handleSandboxSimulateResult}
          />
        </Suspense>
      )}


      {/* Footer */}
      <footer className="border-t border-slate-900 bg-[#050810] py-4 px-6 text-center text-xs text-slate-500 font-mono flex items-center justify-between max-w-[1600px] mx-auto w-full">
        <span>⚡ Thermal Sentinel Grid · FortyGuard Hackathon '26</span>
        <span>Building the World's Temperature AI · Track 03: Industrial & Enterprise (Tracks 06 & 02)</span>
        <span>IEEE Std C57.91 & ANSI C84.1 Compliant</span>
      </footer>

      {/* Vercel Speed Insights */}
      <SpeedInsights />
      
      {/* Vercel Web Analytics */}
      <Analytics />
    </div>
  );
};

export default App;
