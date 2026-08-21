import React from 'react';
import {
  Play,
  Pause,
  RotateCcw,
  SkipBack,
  SkipForward,
  Clock,
  MapPin,
  Flame,
  Gauge,
  Sun,
  Layers,
} from 'lucide-react';
import { ScenarioMetadata, TimelineStep } from '../types';

interface ReplayControlBarProps {
  metadata: ScenarioMetadata;
  steps: TimelineStep[];
  currentHourIndex: number;
  onSelectHour: (index: number) => void;
  isPlaying: boolean;
  onTogglePlay: () => void;
  onReset: () => void;
  speed: number;
  onChangeSpeed: (speed: number) => void;
}

export const ReplayControlBar: React.FC<ReplayControlBarProps> = ({
  metadata,
  steps,
  currentHourIndex,
  onSelectHour,
  isPlaying,
  onTogglePlay,
  onReset,
  speed,
  onChangeSpeed,
}) => {
  const currentStep = steps[currentHourIndex] || steps[0];

  const handlePrev = () => {
    onSelectHour(Math.max(0, currentHourIndex - 1));
  };

  const handleNext = () => {
    onSelectHour(Math.min(steps.length - 1, currentHourIndex + 1));
  };

  return (
    <div id="tour-replay-bar" className="glass-panel rounded-3xl p-5 border border-slate-800/90 shadow-2xl relative overflow-hidden">
      {/* Subtle background glow based on peak */}
      <div className="absolute top-0 right-1/4 w-96 h-32 bg-amber-500/5 rounded-full blur-3xl pointer-events-none"></div>

      {/* Top Row: Replay Header, Incident Badge, & Playback Controls */}
      <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 mb-4">
        {/* Left: Replay Scenario Information */}
        <div className="flex items-center gap-3.5">
          <div className="h-12 w-12 rounded-2xl bg-gradient-to-br from-amber-500/20 to-orange-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 shadow-inner">
            <Clock className="h-6 w-6 text-amber-400" />
          </div>
          <div>
            <div className="flex items-center gap-2.5 flex-wrap">
              <h2 className="text-sm font-extrabold text-white tracking-wide uppercase font-heading">
                {metadata.name}
              </h2>
              <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-md bg-rose-950/80 text-rose-300 border border-rose-800/60 flex items-center gap-1">
                <Flame className="h-3 w-3 text-rose-400" /> 119°F / 48.3°C HISTORIC PEAK
              </span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded-md bg-slate-900 text-slate-400 border border-slate-800">
                July 24, 2023 · Phoenix AZ
              </span>
            </div>
            <div className="flex items-center gap-2 text-xs text-slate-400 mt-1">
              <span className="flex items-center gap-1 font-medium text-slate-300">
                <MapPin className="h-3 w-3 text-amber-400" />
                {metadata.location.substation_name}
              </span>
              <span>•</span>
              <span className="font-mono text-amber-400 font-bold bg-amber-500/10 px-2 py-0.5 rounded">
                Active Step: {currentStep.time_label} (Hour {currentStep.hour_index + 1}/12)
              </span>
            </div>
          </div>
        </div>

        {/* Right: Studio Playback Controls & Speed Toggle */}
        <div className="flex items-center gap-2.5 self-end lg:self-auto flex-wrap">
          {/* Speed Pills */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-1 flex items-center gap-1 text-[11px] font-mono">
            {[1, 2, 5].map((s) => (
              <button
                key={s}
                onClick={() => onChangeSpeed(s)}
                className={`px-2 py-0.5 rounded-lg font-bold transition-all ${
                  speed === s
                    ? 'bg-amber-500 text-slate-950 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {s}x
              </button>
            ))}
          </div>

          {/* Transport Controls */}
          <div className="flex items-center gap-1.5 bg-slate-900 border border-slate-800 p-1 rounded-2xl">
            <button
              onClick={onReset}
              className="p-2 rounded-xl text-slate-400 hover:text-slate-200 hover:bg-slate-800/80 transition-all"
              title="Reset to 06:00 AM"
            >
              <RotateCcw className="h-4 w-4" />
            </button>
            <button
              onClick={handlePrev}
              disabled={currentHourIndex === 0}
              className="p-2 rounded-xl text-slate-400 hover:text-slate-200 hover:bg-slate-800/80 transition-all disabled:opacity-40"
              title="Step Backward (1 Hour)"
            >
              <SkipBack className="h-4 w-4" />
            </button>
            <button
              onClick={onTogglePlay}
              className={`px-4 py-2 rounded-xl text-xs font-extrabold transition-all flex items-center gap-2 shadow-lg ${
                isPlaying
                  ? 'bg-amber-500 text-slate-950 shadow-amber-500/30 hover:bg-amber-400'
                  : 'bg-gradient-to-r from-amber-500 via-orange-500 to-rose-500 text-white shadow-amber-500/25 hover:opacity-90'
              }`}
            >
              {isPlaying ? (
                <>
                  <Pause className="h-4 w-4 fill-current" /> Pause
                </>
              ) : (
                <>
                  <Play className="h-4 w-4 fill-current" /> Play Episode
                </>
              )}
            </button>
            <button
              onClick={handleNext}
              disabled={currentHourIndex === steps.length - 1}
              className="p-2 rounded-xl text-slate-400 hover:text-slate-200 hover:bg-slate-800/80 transition-all disabled:opacity-40"
              title="Step Forward (1 Hour)"
            >
              <SkipForward className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Interactive 12-Hour Thermal Gradient Scrubber */}
      <div className="space-y-2">
        {/* Track Label Bar */}
        <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 px-1">
          <span className="flex items-center gap-1.5">
            <Sun className="h-3.5 w-3.5 text-amber-400" /> 06:00 AM (Sunrise · 34.2°C)
          </span>
          <span className="text-rose-400 font-bold flex items-center gap-1 bg-rose-950/40 px-2 py-0.5 rounded border border-rose-800/40 animate-pulse">
            <Flame className="h-3.5 w-3.5" /> 01:00 PM Peak Forcing (42.7°C / 108.9°F)
          </span>
          <span className="flex items-center gap-1.5">
            <Clock className="h-3.5 w-3.5 text-slate-500" /> 05:00 PM (Evening · 44.1°C)
          </span>
        </div>

        {/* 12-Step Button Cards */}
        <div className="grid grid-cols-6 sm:grid-cols-12 gap-2 bg-[#040810]/80 p-2 rounded-2xl border border-slate-800/80 shadow-inner">
          {steps.map((step, idx) => {
            const isSelected = idx === currentHourIndex;
            const isPeak = idx >= 6 && idx <= 8;
            const temp = step.fortyguard_2m_ambient_c;

            return (
              <button
                key={step.timestamp}
                onClick={() => onSelectHour(idx)}
                className={`relative py-2.5 px-1.5 rounded-xl text-center font-mono transition-all duration-150 flex flex-col items-center justify-between border ${
                  isSelected
                    ? 'bg-gradient-to-b from-amber-500 to-orange-600 text-slate-950 font-black shadow-xl shadow-amber-500/40 ring-2 ring-amber-300 border-amber-300'
                    : isPeak
                    ? 'bg-rose-950/50 hover:bg-rose-900/70 text-rose-200 border-rose-800/60'
                    : 'bg-slate-900/80 hover:bg-slate-800/90 text-slate-400 hover:text-slate-200 border-slate-800'
                }`}
              >
                <div className={`text-[10px] font-bold ${isSelected ? 'text-slate-950' : 'text-slate-400'}`}>
                  {step.time_label.split(' ')[0]}
                </div>
                <div className={`text-xs font-extrabold mt-1 ${isSelected ? 'text-slate-950' : isPeak ? 'text-rose-400' : 'text-slate-200'}`}>
                  {temp.toFixed(0)}°C
                </div>
                <div className={`text-[9px] mt-0.5 opacity-80 ${isSelected ? 'text-slate-900 font-bold' : 'text-slate-500'}`}>
                  +{(step.microclimate_delta_c).toFixed(1)}°
                </div>

                {isPeak && !isSelected && (
                  <span className="absolute -top-1 -right-1 flex h-2.5 w-2.5">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-rose-500"></span>
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};
