import React from 'react';
import { Play, Pause, RotateCcw, FastForward, Clock, MapPin, AlertCircle } from 'lucide-react';
import { ScenarioMetadata, TimelineStep } from '../types';

interface ReplayScrubberProps {
  metadata: ScenarioMetadata;
  steps: TimelineStep[];
  currentHourIndex: number;
  onSelectHour: (index: number) => void;
  isPlaying: boolean;
  onTogglePlay: () => void;
  onReset: () => void;
}

export const ReplayScrubber: React.FC<ReplayScrubberProps> = ({
  metadata,
  steps,
  currentHourIndex,
  onSelectHour,
  isPlaying,
  onTogglePlay,
  onReset,
}) => {
  const currentStep = steps[currentHourIndex] || steps[0];

  return (
    <div className="glass-panel rounded-2xl p-4 border border-slate-800 shadow-xl">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-3">
        {/* Scenario Metadata & Clock */}
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400">
            <Clock className="h-5 w-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-sm font-bold text-white tracking-wide uppercase font-heading">
                {metadata.name}
              </h2>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30">
                119°F PEAK RECORD
              </span>
            </div>
            <div className="flex items-center gap-2 text-xs text-slate-400 mt-0.5">
              <span className="flex items-center gap-1 font-medium text-slate-300">
                <MapPin className="h-3 w-3 text-amber-400" />
                {metadata.location.substation_name} ({metadata.location.city}, {metadata.location.state})
              </span>
              <span>•</span>
              <span className="font-mono text-amber-400 font-bold">
                Hour {currentStep.hour_index + 1}/12 ({currentStep.time_label})
              </span>
            </div>
          </div>
        </div>

        {/* Playback Controls */}
        <div className="flex items-center gap-2 self-end md:self-auto">
          <button
            onClick={onReset}
            className="p-2 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-400 hover:text-slate-200 transition-all"
            title="Reset to 06:00 AM"
          >
            <RotateCcw className="h-4 w-4" />
          </button>
          <button
            onClick={onTogglePlay}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 shadow-lg ${
              isPlaying
                ? 'bg-amber-500 text-slate-950 shadow-amber-500/30 hover:bg-amber-400'
                : 'bg-gradient-to-r from-amber-500 to-orange-500 text-white shadow-amber-500/20 hover:from-amber-400 hover:to-orange-400'
            }`}
          >
            {isPlaying ? (
              <>
                <Pause className="h-4 w-4 fill-current" /> Pause Replay
              </>
            ) : (
              <>
                <Play className="h-4 w-4 fill-current" /> Play Episode
              </>
            )}
          </button>
        </div>
      </div>

      {/* Scrubber Timeline Bar */}
      <div className="space-y-1.5">
        <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 px-1">
          <span>06:00 AM (Sunrise)</span>
          <span className="text-rose-400 font-bold flex items-center gap-1">
            <AlertCircle className="h-3 w-3" /> 01:00 PM Peak (42.7°C / 108.9°F)
          </span>
          <span>05:00 PM (Evening)</span>
        </div>

        {/* Step Buttons Track */}
        <div className="grid grid-cols-12 gap-1.5 bg-slate-950/60 p-1.5 rounded-xl border border-slate-800/80">
          {steps.map((step, idx) => {
            const isSelected = idx === currentHourIndex;
            const isPeak = idx >= 6 && idx <= 8;
            return (
              <button
                key={step.timestamp}
                onClick={() => onSelectHour(idx)}
                className={`relative py-2 rounded-lg text-center font-mono text-xs transition-all ${
                  isSelected
                    ? 'bg-amber-500 text-slate-950 font-bold shadow-md shadow-amber-500/40 ring-2 ring-amber-300'
                    : isPeak
                    ? 'bg-rose-950/40 hover:bg-rose-900/60 text-rose-300 border border-rose-800/40'
                    : 'bg-slate-900/80 hover:bg-slate-800 text-slate-400 hover:text-slate-200'
                }`}
              >
                <div className="text-[10px] opacity-80">{step.time_label.split(' ')[0]}</div>
                <div className="text-[11px] font-bold mt-0.5">
                  {step.fortyguard_2m_ambient_c.toFixed(0)}°
                </div>
                {isPeak && !isSelected && (
                  <span className="absolute -top-1 -right-1 flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-rose-500"></span>
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
