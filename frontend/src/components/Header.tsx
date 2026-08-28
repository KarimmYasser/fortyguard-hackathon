import React from 'react';
import { Activity, ShieldCheck, Zap, AlertTriangle, Thermometer, Layers, RefreshCw } from 'lucide-react';
import { ScenarioMetadata, SafetyGateVerdict } from '../types';

interface HeaderProps {
  metadata: ScenarioMetadata;
  verdict: SafetyGateVerdict;
  isMitigatedMode: boolean;
  onToggleMode: () => void;
  onRefresh: () => void;
  isLoading: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  metadata,
  verdict,
  isMitigatedMode,
  onToggleMode,
  onRefresh,
  isLoading,
}) => {
  return (
    <header className="border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-xl sticky top-0 z-50 px-6 py-3.5">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        {/* Left Title & Track Badges */}
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-amber-600 to-orange-500 flex items-center justify-center shadow-lg shadow-amber-500/20 ring-1 ring-amber-400/30">
            <Zap className="h-5 w-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2.5 flex-wrap">
              <h1 className="text-lg font-bold tracking-tight text-white flex items-center gap-2">
                THERMAL SENTINEL GRID
                <span className="text-xs px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20 font-mono font-medium">
                  v1.0-PROD
                </span>
              </h1>
            </div>
            <p className="text-xs text-slate-400 font-medium">
              Physics-Constrained Industrial Thermal Resilience Engine · Track 03: Industrial & Enterprise (Tracks 06 & 02)
            </p>
          </div>
        </div>

        {/* Middle Track / Standards Badges */}
        <div className="hidden lg:flex items-center gap-2">
          <span className="text-[11px] px-2.5 py-1 rounded-md bg-cyan-950/60 text-cyan-400 border border-cyan-800/50 font-medium flex items-center gap-1.5">
            <Layers className="h-3 w-3" /> Track 03: Industrial & Enterprise
          </span>
          <span className="text-[11px] px-2.5 py-1 rounded-md bg-purple-950/60 text-purple-400 border border-purple-800/50 font-medium flex items-center gap-1.5">
            <Activity className="h-3 w-3" /> Track 06: Agentic AI
          </span>
          <span className="text-[11px] px-2.5 py-1 rounded-md bg-orange-950/60 text-orange-400 border border-orange-800/50 font-medium flex items-center gap-1.5">
            <Thermometer className="h-3 w-3" /> Track 02: Energy
          </span>
          <span className="text-[11px] px-2.5 py-1 rounded-md bg-blue-950/60 text-blue-400 border border-blue-800/50 font-mono">
            IEEE C57.91 | IEC 60076-7
          </span>
        </div>

        {/* Right Controller Mode Switch & Safety Status */}
        <div className="flex items-center gap-3 w-full md:w-auto justify-between md:justify-end">
          {/* Mode Switcher */}
          <div className="bg-slate-900/90 border border-slate-800 p-1 rounded-xl flex items-center shadow-inner">
            <button
              onClick={() => isMitigatedMode && onToggleMode()}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 ${
                !isMitigatedMode
                  ? 'bg-rose-950/80 text-rose-300 border border-rose-800/60 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <AlertTriangle className="h-3.5 w-3.5" />
              Baseline (Static Rating)
            </button>
            <button
              onClick={() => !isMitigatedMode && onToggleMode()}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 ${
                isMitigatedMode
                  ? 'bg-gradient-to-r from-amber-500 to-orange-500 text-white shadow-md shadow-amber-500/25 ring-1 ring-amber-300/30'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <ShieldCheck className="h-3.5 w-3.5" />
              Thermal Sentinel (Mitigated)
            </button>
          </div>

          {/* Refresh Button */}
          <button
            onClick={onRefresh}
            disabled={isLoading}
            className="p-2 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 hover:text-white transition-all disabled:opacity-50"
            title="Refresh Replay Data"
          >
            <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin text-amber-400' : ''}`} />
          </button>
        </div>
      </div>
    </header>
  );
};
