import React from 'react';
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
} from 'lucide-react';
import { ScenarioMetadata, SafetyGateVerdict } from '../types';

export type ActiveTab =
  | 'overview'
  | 'sandbox'
  | 'multi_day_72h'
  | 'power_flow'
  | 'ieee_annex_g'
  | 'gis_map'
  | 'physics_moats'
  | 'agent_graph'
  | 'financial_roi';

interface NavbarProps {
  metadata: ScenarioMetadata;
  verdict: SafetyGateVerdict;
  isMitigatedMode: boolean;
  onToggleMode: () => void;
  activeTab: ActiveTab;
  onSelectTab: (tab: ActiveTab) => void;
  onRefresh: () => void;
  isLoading: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  metadata,
  verdict,
  isMitigatedMode,
  onToggleMode,
  activeTab,
  onSelectTab,
  onRefresh,
  isLoading,
}) => {
  const tabs = [
    { id: 'overview', label: 'Mission Control', icon: Activity },
    { id: 'sandbox', label: '⚡ What-If Studio', icon: Sliders },
    { id: 'multi_day_72h', label: '🔥 72h Compounding', icon: Flame },
    { id: 'power_flow', label: '⚡ AC Power Flow', icon: Network },
    { id: 'ieee_annex_g', label: '📜 IEEE Annex G', icon: Award },
    { id: 'gis_map', label: 'Hyperlocal 2m GIS', icon: MapPin },
    { id: 'physics_moats', label: '4 Scientific Moats', icon: Layers },
    { id: 'agent_graph', label: 'LangGraph Engine', icon: Cpu },
    { id: 'financial_roi', label: 'Avoided Loss ROI', icon: Calculator },
  ] as const;

  return (
    <header className="border-b border-slate-800/90 bg-[#080C14]/90 backdrop-blur-2xl sticky top-0 z-50 transition-all">
      {/* Top Banner / Pulse Bar */}
      <div className="bg-gradient-to-r from-amber-950/40 via-slate-900/60 to-cyan-950/40 px-6 py-1.5 border-b border-slate-800/40 flex items-center justify-between text-[11px] font-mono">
        <div className="flex items-center gap-3">
          <span className="flex items-center gap-1.5 text-emerald-400 font-bold">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            SYSTEM OPERATIONAL · CBF-QP SAFETY GATE ARMED
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
            Track 06: Agentic AI
          </span>
          <span className="px-2 py-0.5 rounded bg-orange-500/10 text-orange-400 border border-orange-500/20 font-medium hidden md:inline">
            Track 02: Future Buildings
          </span>
        </div>
      </div>

      {/* Main Navigation Bar */}
      <div className="max-w-[1600px] mx-auto px-6 py-3 flex flex-col xl:flex-row items-start xl:items-center justify-between gap-4">
        {/* Brand & Logo */}
        <div className="flex items-center gap-3.5">
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

        {/* Center Tab Navigation */}
        <nav className="flex items-center gap-1 p-1 bg-slate-900/90 border border-slate-800 rounded-2xl shadow-inner overflow-x-auto max-w-full">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => onSelectTab(tab.id as ActiveTab)}
                className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all duration-200 flex items-center gap-1.5 whitespace-nowrap ${
                  isActive
                    ? 'bg-gradient-to-r from-amber-500 to-orange-500 text-slate-950 font-bold shadow-lg shadow-amber-500/25 ring-1 ring-amber-300/40'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`}
              >
                <Icon className={`h-3.5 w-3.5 ${isActive ? 'text-slate-950' : 'text-slate-400'}`} />
                {tab.label}
              </button>
            );
          })}
        </nav>

        {/* Right Controller Mode Switcher */}
        <div className="flex items-center gap-3 w-full xl:w-auto justify-between xl:justify-end">
          <div className="bg-slate-900/95 border border-slate-800 p-1 rounded-2xl flex items-center shadow-lg">
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
    </header>
  );
};
