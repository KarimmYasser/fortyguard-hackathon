import React from 'react';
import { createPortal } from 'react-dom';
import {
  Zap,
  ShieldCheck,
  AlertTriangle,
  Layers,
  Thermometer,
  Activity,
  BarChart3,
  MapPin,
  Cpu,
  Calculator,
  RefreshCw,
  Sparkles,
  Sliders,
  Award,
  Flame,
  Network,
  Radio,
  BookOpen,
  Database,
  BriefcaseBusiness,
} from 'lucide-react';
import { ScenarioMetadata, SafetyGateVerdict } from '../types';

export type ActiveTab =
  | 'home'
  | 'overview'
  | 'portfolio_operations'
  | 'sandbox'
  | 'multi_day_72h'
  | 'power_flow'
  | 'ieee_annex_g'
  | 'ground_truth'
  | 'academic_provenance'
  | 'gis_map'
  | 'physics_moats'
  | 'agent_graph'
  | 'financial_roi'
  | 'data_science';

interface NavbarProps {
  // Optional: the shell renders before the replay dataset resolves so that
  // first paint is not blocked on the serverless fetch.
  metadata?: ScenarioMetadata | null;
  verdict?: SafetyGateVerdict | null;
  isMitigatedMode: boolean;
  onToggleMode: () => void;
  activeTab: ActiveTab;
  onSelectTab: (tab: ActiveTab) => void;
  onRefresh: () => void;
  onOpenLiveScan?: () => void;
  onOpenDatabaseModal?: () => void;
  onStartTour?: () => void;
  isLoading: boolean;
}


interface TabPreviewInfo {
  badge: string;
  badgeColor: string;
  tagline: string;
  summary: string;
  highlights: string[];
}

const TAB_PREVIEWS: Record<ActiveTab, TabPreviewInfo> = {
  home: {
    badge: 'HYPERFRAMES STUDIO',
    badgeColor: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
    tagline: 'Executive Presentation & Pitch',
    summary: '3-minute synchronized video pitch and interactive 5-minute slide deck with embedded audio narration and full screenplay transcripts.',
    highlights: ['3-Minute Video Pitch (1080p)', '5-Minute Presenter Slide Deck', 'Interactive Screenplay & Controls'],
  },
  overview: {
    badge: 'MISSION CRITICAL',
    badgeColor: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
    tagline: 'Real-Time 12h Telemetry & Dispatch',
    summary: 'Synchronized Phoenix July 2023 heatwave timeline scrubber with 3-axis Apache ECharts physics telemetry and real-time mitigation dispatch.',
    highlights: ['12-Hour Timeline Scrubber', 'Top-Oil & Hot-Spot Dynamic Rises', 'Real-Time Dispatch Actuation'],
  },
  portfolio_operations: {
    badge: 'OPERATIONS COMMAND',
    badgeColor: 'bg-cyan-500/15 text-cyan-300 border-cyan-500/30',
    tagline: 'Portfolio Triage & Field Intervention',
    summary: 'Ranks registered grid assets, screens candidate crew intervention windows, and emits content-addressed mitigation evidence through the same MCP-accessible deterministic core.',
    highlights: ['Transparent Portfolio Ranking', 'Worker Intervention Windows', 'MCP + SHA-256 Evidence'],
  },
  sandbox: {
    badge: 'INTERACTIVE LAB',
    badgeColor: 'bg-purple-500/15 text-purple-300 border-purple-500/30',
    tagline: 'Live Physics Stress Studio',
    summary: 'Modulate FortyGuard 2m delta (0 to +6°C), heatwave dryout days (1–31), and BESS capacity with sub-15ms live ODE recalculation.',
    highlights: ['FortyGuard 2m Delta Slider', 'Multi-Day Persistence Sweep', 'Sub-15ms ODE Solvers'],
  },
  multi_day_72h: {
    badge: 'HEATWAVE ACCUMULATION',
    badgeColor: 'bg-orange-500/15 text-orange-300 border-orange-500/30',
    tagline: 'Multi-Day Thermal Ratcheting',
    summary: 'Tracks cumulative 3-day diurnal heat cycles, nocturnal recovery deficit, and compounding Kraft paper insulation loss of life.',
    highlights: ['72h Continuous ODE Timeline', 'Nightly Recovery Deficit Debt', 'Compounded Aging Multipliers'],
  },
  power_flow: {
    badge: 'GRID VOLTAGE STABILITY',
    badgeColor: 'bg-cyan-500/15 text-cyan-300 border-cyan-500/30',
    tagline: '4-Bus Forward-Backward Sweep',
    summary: 'Full AC power flow solver calculating line thermal I²R losses, OLTC transformer tap changes, and BESS Volt/VAR reactive support.',
    highlights: ['4-Bus Radial Distribution', 'ANSI C84.1 Voltage Envelope', 'BESS Volt/VAR Injection'],
  },
  ground_truth: {
    badge: 'INDEPENDENT VALIDATION',
    badgeColor: 'bg-cyan-500/15 text-cyan-300 border-cyan-500/30',
    tagline: 'Station Ground Truth vs FortyGuard',
    summary: 'Timestamp-aligned PHX ASOS observations quantify the urban microclimate delta and correlation against FortyGuard 2m telemetry.',
    highlights: ['Independent In-Situ Station', 'Hourly ΔT & Correlation', 'Explicit UHI Guardrails'],
  },
  ieee_annex_g: {
    badge: 'STANDARDS BENCHMARK',
    badgeColor: 'bg-blue-500/15 text-blue-300 border-blue-500/30',
    tagline: 'IEEE Std C57.91-2011 Verification',
    summary: 'Step-by-step numerical verification comparing Thermal Sentinel continuous ODE solver directly against IEEE Standard reference tables.',
    highlights: ['Clause G.2 & G.3 Compliance', 'Top-Oil Time Constant τ_TO', 'Zero-Drift Benchmark Match'],
  },
  academic_provenance: {
    badge: 'ALPHAXIV DISCOVERY',
    badgeColor: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
    tagline: 'Peer-Reviewed Literature Grounding',
    summary: 'Curated repository of peer-reviewed papers discovered via alphaXiv, covering PINNs, cool pavements, and CBF safety filters.',
    highlights: ['Live alphaXiv Discussion Links', 'IEEE/BibTeX Formatted Citations', 'Publication-Grade LaTeX Proofs'],
  },
  gis_map: {
    badge: 'MICROCLIMATE TILES',
    badgeColor: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
    tagline: '60m Urban Parcel Resolution',
    summary: 'Spatial boundary layer temperature heatmaps mapped to Phoenix substation coordinates, street canyons, and building footprints.',
    highlights: ['2m Convective Heat Map', 'Land-Cover Albedo Overlay', 'Substation Asset Inspector'],
  },
  physics_moats: {
    badge: 'ASYMMETRIC IP',
    badgeColor: 'bg-indigo-500/15 text-indigo-300 border-indigo-500/30',
    tagline: 'First-Principles Physics Engines',
    summary: 'Deep dives into Cable-Soil Dryout (IEC 60287), deterministic trajectory safety checks, Canyon Aerodynamics, and Virtual Moisture Sensor.',
    highlights: ['Non-Linear Soil Resistivity', 'Control Barrier Functions', 'Fickian Paper-Oil Diffusion'],
  },
  agent_graph: {
    badge: 'AUTONOMOUS ORCHESTRATION',
    badgeColor: 'bg-rose-500/15 text-rose-300 border-rose-500/30',
    tagline: 'StateGraph Multi-Agent Harness',
    summary: 'Live visualization of LangGraph state execution: Sensor validation, Thermal forecasting, Risk audit, and deterministic Safety Gate.',
    highlights: ['Live Node State Inspector', 'Deterministic Non-LLM Gate', 'Autonomous Work Orders'],
  },
  financial_roi: {
    badge: 'FINANCIAL AUDIT',
    badgeColor: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
    tagline: 'LBNL ICE Avoided Loss Calculator',
    summary: 'Auditable financial impact quantifying customer interruption savings (VoLL), asset capital deferral, and net operational ROI.',
    highlights: ['Customer Interruption Costs', 'Capital Replacement Deferral', '>24x Operational ROI Multiple'],
  },
  data_science: {
    badge: 'DATA SCIENCE & AI/ML',
    badgeColor: 'bg-violet-500/15 text-violet-300 border-violet-500/30',
    tagline: 'IBM Data Science Methodology',
    summary: 'Bronze→Silver→Gold ETL pipeline, physics-surrogate ML, Isolation Forest anomaly detection, and Weibull survival analysis.',
    highlights: ['Medallion ETL Architecture', 'Ridge Surrogate R²>0.99', 'Weibull RUL Forecasting'],
  },
};

export const Navbar: React.FC<NavbarProps> = ({
  metadata,
  verdict,
  isMitigatedMode,
  onToggleMode,
  activeTab,
  onSelectTab,
  onRefresh,
  onOpenLiveScan,
  onOpenDatabaseModal,
  onStartTour,
  isLoading,
}) => {

  const [hoveredTab, setHoveredTab] = React.useState<ActiveTab | null>(null);
  const [previewPosition, setPreviewPosition] = React.useState<{ top: number; left: number } | null>(null);

  const showTabPreview = (tab: ActiveTab, anchor: HTMLElement) => {
    const rect = anchor.getBoundingClientRect();
    const previewWidth = window.innerWidth < 640 ? 288 : 320;
    const gutter = 12;
    setHoveredTab(tab);
    setPreviewPosition({
      top: rect.bottom + 8,
      left: Math.min(
        window.innerWidth - previewWidth - gutter,
        Math.max(gutter, rect.left + rect.width / 2 - previewWidth / 2),
      ),
    });
  };

  const hideTabPreview = () => {
    setHoveredTab(null);
    setPreviewPosition(null);
  };

  const tabs = [
    { id: 'home', label: 'Pitch & Video', icon: Sparkles },
    { id: 'overview', label: 'Mission Control', icon: Activity },
    { id: 'portfolio_operations', label: 'Portfolio Ops', icon: BriefcaseBusiness },
    { id: 'sandbox', label: 'What-If Studio', icon: Sliders },
    { id: 'multi_day_72h', label: '72h Compounding', icon: Flame },
    { id: 'power_flow', label: 'AC Power Flow', icon: Network },
    { id: 'ieee_annex_g', label: 'IEEE Annex G', icon: Award },
    { id: 'ground_truth', label: 'Ground Truth', icon: Thermometer },
    { id: 'academic_provenance', label: 'Academic Provenance', icon: BookOpen },
    { id: 'gis_map', label: 'Hyperlocal 2m GIS', icon: MapPin },
    { id: 'physics_moats', label: '4 Scientific Moats', icon: Layers },
    { id: 'agent_graph', label: 'LangGraph Engine', icon: Cpu },
    { id: 'financial_roi', label: 'Avoided Loss ROI', icon: Calculator },
    { id: 'data_science', label: 'Data Science Studio', icon: BarChart3 },
  ] as const;

  return (
    <header className="border-b border-slate-800/90 bg-[#080C14]/95 backdrop-blur-2xl sticky top-0 z-50 transition-all">
      {/* Top Banner / Pulse Bar */}
      <div className="bg-gradient-to-r from-amber-950/40 via-slate-900/60 to-cyan-950/40 px-6 py-1.5 border-b border-slate-800/40 flex items-center justify-between text-[11px] font-mono">
        <div className="flex items-center gap-3">
          <span className="flex items-center gap-1.5 text-emerald-400 font-bold">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            DEMO SYSTEM · MODEL SAFETY PREFLIGHT ACTIVE
          </span>
          <span className="text-slate-600">|</span>
          <span className="text-slate-400 hidden sm:inline">
            FortyGuard tOS 2m Boundary Engine: Active (60m Resolution)
          </span>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-amber-400 font-bold flex items-center gap-1">
            <Sparkles className="h-3 w-3" /> FortyGuard Hackathon '26
          </span>
          <span className="text-slate-600">|</span>
          <span className="px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-medium">
            Track 03: Industrial & Enterprise
          </span>
          <span className="px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 border border-purple-500/20 font-medium hidden md:inline">
            Track 06: Agentic AI
          </span>
          <span className="px-2 py-0.5 rounded bg-orange-500/10 text-orange-400 border border-orange-500/20 font-medium hidden lg:inline">
            Track 02: Energy
          </span>
        </div>
      </div>

      {/* Main Header Bar (Logo & Controls) */}
      <div className="max-w-[1600px] mx-auto px-6 py-3.5 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        {/* Brand & Logo */}
        <div id="tour-navbar-brand" className="flex items-center gap-3.5">
          <div className="relative group">
            <div className="absolute -inset-1 bg-gradient-to-r from-amber-500 to-orange-500 rounded-2xl blur opacity-30 group-hover:opacity-60 transition duration-500"></div>
            <div className="relative h-11 w-11 rounded-xl bg-gradient-to-tr from-amber-500 via-orange-500 to-rose-500 p-[1px]">
              <div className="h-full w-full bg-slate-950 rounded-[11px] flex items-center justify-center">
                <Zap className="h-6 w-6 text-amber-400 fill-amber-400/20" />
              </div>
            </div>
          </div>

          <div>
            <div className="flex items-center gap-2.5">
              <h1 className="text-xl font-extrabold tracking-tight text-white font-heading flex items-center gap-2">
                THERMAL SENTINEL GRID
              </h1>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-300 border border-amber-500/30 font-bold">
                PHYSICS-AI v1.0
              </span>
            </div>
            <p className="text-xs text-slate-400 font-medium mt-0.5">
              IEEE C57.91 & IEC 60076-7 Multi-Agent Thermal Resilience & Dispatch Engine
            </p>
          </div>
        </div>

        {/* Right Controller Mode Switcher & Quick Actions */}
        <div className="flex items-center gap-3 w-full md:w-auto justify-between md:justify-end flex-wrap">
          {/* Baseline vs Mitigated Toggle */}
          <div id="tour-navbar-mode-toggle" className="bg-slate-900/95 border border-slate-800 p-1 rounded-2xl flex items-center shadow-lg">
            <button
              onClick={() => isMitigatedMode && onToggleMode()}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
                !isMitigatedMode
                  ? 'bg-rose-950 text-rose-300 border border-rose-700/80 shadow-md shadow-rose-900/30'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <AlertTriangle className="h-3.5 w-3.5 text-rose-400" />
              Baseline
            </button>
            <button
              onClick={() => !isMitigatedMode && onToggleMode()}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
                isMitigatedMode
                  ? 'bg-gradient-to-r from-amber-500 to-orange-500 text-slate-950 shadow-md shadow-amber-500/30 ring-1 ring-amber-300'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <ShieldCheck className="h-4 w-4 text-slate-950" />
              Mitigated
            </button>
          </div>

          {/* Universal Tour Guide Button */}
          {onStartTour && (
            <button
              id="tour-navbar-tour-btn"
              onClick={onStartTour}
              className="px-3.5 py-2 rounded-xl bg-gradient-to-r from-indigo-500/15 via-purple-500/15 to-pink-500/15 hover:from-indigo-500/25 hover:via-purple-500/25 hover:to-pink-500/25 border border-indigo-500/40 hover:border-indigo-400 text-indigo-300 hover:text-white font-bold text-xs flex items-center gap-1.5 transition-all shadow-sm shadow-indigo-500/15 hover:shadow-indigo-500/30"
              title="Start Interactive Spotlight Tour for Active Tab"
            >
              <Sparkles className="h-3.5 w-3.5 text-indigo-400 animate-pulse" />
              <span>Tour Guide</span>
            </button>
          )}

          {onOpenLiveScan && (
            <button
              id="tour-navbar-live-scan"
              onClick={onOpenLiveScan}
              className="px-3.5 py-2 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/30 text-amber-300 font-bold text-xs flex items-center gap-1.5 transition-all shadow-sm shadow-amber-500/10 hover:shadow-amber-500/20 font-mono"
              title="Open FortyGuard Live Cloud Ingestion & Quota Hub"
            >
              <Radio className="h-3.5 w-3.5 text-amber-400 animate-pulse" />
              <span className="hidden sm:inline">Live Cloud Scan</span>
            </button>
          )}

          {onOpenDatabaseModal && (
            <button
              id="tour-navbar-db-modal"
              onClick={onOpenDatabaseModal}
              className="px-3.5 py-2 rounded-xl bg-cyan-500/10 hover:bg-cyan-500/20 border border-cyan-500/30 text-cyan-300 font-bold text-xs flex items-center gap-1.5 transition-all shadow-sm shadow-cyan-500/10 hover:shadow-cyan-500/20 font-mono"
              title="Open Supabase & SQLite Enterprise 16-Table Database Hub"
            >
              <Database className="h-3.5 w-3.5 text-cyan-400 animate-pulse" />
              <span className="hidden sm:inline">Cloud DB (17 Tables)</span>
            </button>
          )}


          <button
            onClick={onRefresh}
            disabled={isLoading}
            className="p-2.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 hover:text-white transition-all disabled:opacity-50 shadow-sm"
            title="Reload Scenario Telemetry"
          >
            <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin text-amber-400' : ''}`} />
          </button>
        </div>
      </div>

      {/* Dedicated Expanded Navigation Bar (Directly Under Header) */}
      <div className="w-full border-t border-slate-800/80 bg-[#060a12]/95 px-3 md:px-6 py-2 shadow-inner relative overflow-x-auto no-scrollbar">
        <nav id="tour-navbar-tabs" className="max-w-[1600px] min-w-[980px] lg:min-w-0 mx-auto grid grid-cols-7 gap-1.5 w-full">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;

            return (
              <div
                key={tab.id}
                className="relative min-w-0"
                onMouseEnter={(event) => showTabPreview(tab.id as ActiveTab, event.currentTarget)}
                onMouseLeave={hideTabPreview}
              >
                <button
                  id={`tour-navbar-tab-${tab.id}`}
                  onClick={() => onSelectTab(tab.id as ActiveTab)}
                  className={`w-full px-2.5 sm:px-3 py-2 rounded-xl text-[11px] sm:text-xs font-semibold transition-all duration-200 flex items-center justify-center gap-1.5 whitespace-nowrap ${
                    isActive
                      ? 'bg-gradient-to-r from-amber-500 to-orange-500 text-slate-950 font-bold shadow-lg shadow-amber-500/25 ring-1 ring-amber-300/50 scale-[1.02]'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/70 bg-slate-900/50 border border-slate-800/70'
                  }`}
                >
                  <Icon className={`h-3.5 w-3.5 shrink-0 ${isActive ? 'text-slate-950' : 'text-slate-400'}`} />
                  <span className="truncate">{tab.label}</span>
                </button>

              </div>
            );
          })}
        </nav>
      </div>

      {hoveredTab && previewPosition && typeof document !== 'undefined' && createPortal((() => {
        const preview = TAB_PREVIEWS[hoveredTab];
        const tab = tabs.find((item) => item.id === hoveredTab);
        if (!tab) return null;
        const Icon = tab.icon;
        const isActive = activeTab === hoveredTab;

        return (
          <div
            className="navbar-tab-preview fixed z-[100] w-72 sm:w-80 pointer-events-none p-4 rounded-2xl border border-slate-700/80 shadow-2xl shadow-black/80 space-y-2.5 animate-in fade-in zoom-in-95"
            style={{ top: previewPosition.top, left: previewPosition.left }}
            role="tooltip"
          >
            <div className="flex items-center justify-between gap-2">
              <span className={`px-2 py-0.5 rounded-full text-[9px] font-mono font-bold border ${preview.badgeColor}`}>
                {preview.badge}
              </span>
              <span className="text-[10px] text-slate-500 font-mono">
                {isActive ? 'ACTIVE VIEW' : 'CLICK TO VIEW'}
              </span>
            </div>

            <div>
              <h4 className="text-xs font-bold text-white font-heading flex items-center gap-1.5">
                <Icon className="h-3.5 w-3.5 text-amber-400" />
                {tab.label}
              </h4>
              <p className="text-[11px] text-amber-300/90 font-medium mt-0.5">
                {preview.tagline}
              </p>
            </div>

            <p className="text-[11px] text-slate-300 leading-relaxed font-sans border-t border-slate-800/80 pt-2">
              {preview.summary}
            </p>

            <div className="bg-slate-900/90 rounded-xl p-2 border border-slate-800 space-y-1">
              <div className="text-[10px] uppercase font-mono text-slate-400 font-bold">Key Capabilities:</div>
              <ul className="space-y-0.5">
                {preview.highlights.map((highlight, index) => (
                  <li key={index} className="text-[10.5px] text-slate-300 flex items-center gap-1.5 font-mono">
                    <span className="h-1 w-1 rounded-full bg-amber-400" />
                    {highlight}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        );
      })(), document.body)}
    </header>
  );
};

