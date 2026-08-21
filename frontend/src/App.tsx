import React, { useState, useEffect, useCallback } from 'react';
import { Navbar, ActiveTab } from './components/Navbar';
import { ReplayControlBar } from './components/ReplayControlBar';
import { HeroKpiGrid } from './components/HeroKpiGrid';
import { EChartsPhysicsTelemetry } from './components/EChartsPhysicsTelemetry';
import { GeospatialMicroclimateViewer } from './components/GeospatialMicroclimateViewer';
import { ScientificMoatsViewer } from './components/ScientificMoatsViewer';
import { AgentGraphViewer } from './components/AgentGraphViewer';
import { EconomicAuditViewer } from './components/EconomicAuditViewer';
import { WhatIfSandboxPanel } from './components/WhatIfSandboxPanel';
import { MultiDay72hHeatwaveViewer } from './components/MultiDay72hHeatwaveViewer';
import { ACPowerFlowSingleLineViewer } from './components/ACPowerFlowSingleLineViewer';
import { IEEEAnnexGBenchmarkViewer } from './components/IEEEAnnexGBenchmarkViewer';
import { SafetyGateCard } from './components/SafetyGateCard';
import { AuditLedger } from './components/AuditLedger';
import { LiveApiScanModal } from './components/LiveApiScanModal';
import { HomePitchViewer } from './components/HomePitchViewer';
import { ReplayDataset, TimelineStep } from './types';
import { startTourGuide } from './utils/tourGuide';

export const App: React.FC = () => {
  const [data, setData] = useState<ReplayDataset | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [currentHourIndex, setCurrentHourIndex] = useState<number>(7); // 01:00 PM Peak
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [playbackSpeed, setPlaybackSpeed] = useState<number>(1);
  const [isMitigatedMode, setIsMitigatedMode] = useState<boolean>(true);
  const [activeTab, setActiveTab] = useState<ActiveTab>('home');
  const [isLiveScanOpen, setIsLiveScanOpen] = useState<boolean>(false);

  // Fetch replay dataset from backend
  const fetchReplayData = useCallback(async () => {
    setIsLoading(true);
    try {
      const resp = await fetch('http://127.0.0.1:8000/api/v1/replay/phoenix-2023');
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
    if (data && simResult.timeline_steps) {
      setData({
        ...data,
        timeline_steps: simResult.timeline_steps,
        baseline_summary: simResult.baseline_summary,
        mitigated_summary: simResult.mitigated_summary,
        safety_gate_verdict: simResult.safety_gate_verdict,
        economic_evaluation: simResult.economic_evaluation,
        soil_cable_state: simResult.soil_cable_state,
        virtual_moisture_state: simResult.virtual_moisture_state,
        urban_canyon_state: simResult.urban_canyon_state,
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

  if (!data && isLoading) {
    return (
      <div className="min-h-screen bg-[#080C14] flex flex-col items-center justify-center text-white">
        <div className="h-14 w-14 rounded-full border-4 border-amber-500/20 border-t-amber-500 animate-spin mb-4"></div>
        <h2 className="text-base font-bold font-heading tracking-wide">Initializing Thermal Sentinel Grid...</h2>
        <p className="text-xs text-slate-400 font-mono mt-1">Ingesting IEEE C57.91 & FortyGuard 2m Boundary Engine</p>
      </div>
    );
  }

  const dataset = data;
  if (!dataset) return null;

  const currentStep: TimelineStep = dataset.timeline_steps[currentHourIndex] || dataset.timeline_steps[0];

  return (
    <div className="min-h-screen bg-[#080C14] text-slate-100 flex flex-col selection:bg-amber-500/30 selection:text-amber-200">
      {/* 1. Global Navigation Bar */}
      <Navbar
        metadata={dataset.scenario_metadata}
        verdict={dataset.safety_gate_verdict}
        isMitigatedMode={isMitigatedMode}
        onToggleMode={() => setIsMitigatedMode(!isMitigatedMode)}
        activeTab={activeTab}
        onSelectTab={setActiveTab}
        onRefresh={fetchReplayData}
        onOpenLiveScan={() => setIsLiveScanOpen(true)}
        onStartTour={() =>
          startTourGuide({
            activeTab,
            onNavigateTab: setActiveTab,
            onOpenLiveScan: () => setIsLiveScanOpen(true),
          })
        }
        isLoading={isLoading}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-[1600px] w-full mx-auto px-4 md:px-8 py-6 space-y-6">
        {/* Global Replay Scrub Bar (Visible Across Interactive Simulation Tabs) */}
        {activeTab !== 'home' && (
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

        {/* TAB 0: Executive Home & Video Pitch Showcase */}
        {activeTab === 'home' && (
          <HomePitchViewer
            onNavigateTab={setActiveTab}
            onOpenLiveScan={() => setIsLiveScanOpen(true)}
          />
        )}

        {/* TAB 1: Mission Control Overview */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
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

        {/* TAB 6: Hyperlocal 2m GIS Map */}
        {activeTab === 'gis_map' && (
          <GeospatialMicroclimateViewer
            heatmapData={dataset.heatmap_geojson_tiles}
            currentAmbient2m={currentStep.fortyguard_2m_ambient_c}
            airportAmbient={currentStep.airport_reference_temp_c}
            deltaAmbient={currentStep.microclimate_delta_c}
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
          />
        )}
      </main>

      {/* Live FortyGuard API Cloud Ingestion Modal */}
      <LiveApiScanModal
        isOpen={isLiveScanOpen}
        onClose={() => setIsLiveScanOpen(false)}
      />

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-[#050810] py-4 px-6 text-center text-xs text-slate-500 font-mono flex items-center justify-between max-w-[1600px] mx-auto w-full">
        <span>⚡ Thermal Sentinel Grid · FortyGuard Hackathon '26</span>
        <span>Building the World's Temperature AI · Tracks 06 & 02</span>
        <span>IEEE Std C57.91 & ANSI C84.1 Compliant</span>
      </footer>
    </div>
  );
};

export default App;
