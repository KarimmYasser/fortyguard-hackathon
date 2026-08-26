import React, { useState, useEffect } from 'react';
import { Flame, Clock, TrendingUp, AlertTriangle, ShieldCheck, Zap, Droplets, ArrowRight } from 'lucide-react';
import { API_BASE } from '../utils/api';

export const MultiDay72hHeatwaveViewer: React.FC = () => {
  const [data72h, setData72h] = useState<any>(null);
  const [selectedDay, setSelectedDay] = useState<number>(1);

  useEffect(() => {
    fetch(`${API_BASE}/api/v1/replay/72h-compounding`)
      .then((res) => res.json())
      .then((data) => setData72h(data))
      .catch((err) => console.error('Failed to load 72h data', err));
  }, []);

  if (!data72h) {
    return (
      <div className="glass-panel rounded-3xl p-6 text-center text-slate-400 font-mono">
        Loading 72-Hour Compounding Heatwave Simulation...
      </div>
    );
  }

  const days = data72h.days_summary || [];
  const currentDaySteps = (data72h.timeline_72h || []).filter(
    (s: any) => s.day_number === selectedDay
  );
  const provenance = data72h.scenario_metadata?.provenance;

  return (
    <div className="glass-panel rounded-3xl p-6 border border-slate-800/90 shadow-2xl space-y-6">
      {/* Header */}
      <div id="tour-72h-header" className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div className="flex items-center gap-3.5">
          <div className="h-11 w-11 rounded-2xl bg-gradient-to-br from-rose-500 to-orange-600 p-[1px] shadow-lg shadow-rose-500/20">
            <div className="h-full w-full bg-slate-950 rounded-[15px] flex items-center justify-center">
              <Flame className="h-5 w-5 text-rose-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2.5">
              <h2 className="text-base font-black text-white uppercase tracking-wide font-heading">
                72-Hour Compounding Heatwave · Live Capture Replay
              </h2>
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-rose-500/20 text-rose-300 border border-rose-800 animate-pulse">
                FORTYGUARD 24×3
              </span>
            </div>
            <p className="text-xs text-slate-400 font-mono mt-0.5">
              Every hourly weather boundary measured July 24–26, 2023 · grid load, soil evolution, and mitigation explicitly modelled
            </p>
          </div>
        </div>

        {/* Day Switcher */}
        <div id="tour-72h-day-selector" className="flex items-center gap-2 bg-slate-900 border border-slate-800 p-1 rounded-2xl text-xs font-mono">
          {days.map((day: any) => (
            <button
              key={day.day_number}
              onClick={() => setSelectedDay(day.day_number)}
              className={`px-3.5 py-1.5 rounded-xl font-bold transition-all ${
                selectedDay === day.day_number
                  ? 'bg-gradient-to-r from-rose-500 to-orange-500 text-white shadow-md shadow-rose-500/30'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Day {day.day_number} ({day.date})
            </button>
          ))}
        </div>
      </div>

      {/* 3-Day Progressive Cards */}
      <div id="tour-72h-metrics" className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs">
        {days.map((day: any) => {
          const isSelected = day.day_number === selectedDay;
          return (
            <div
              key={day.day_number}
              onClick={() => setSelectedDay(day.day_number)}
              className={`cursor-pointer p-4 rounded-2xl border transition-all ${
                isSelected
                  ? 'bg-gradient-to-b from-rose-950/40 via-slate-900 to-slate-950 border-rose-500 shadow-xl shadow-rose-500/20 ring-2 ring-rose-400/30'
                  : 'bg-slate-950/70 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between text-slate-400 text-[11px] mb-2">
                <span className="font-bold text-white">Day 0{day.day_number} · {day.date}</span>
                <span className="text-rose-400 font-bold">Peak {day.peak_ambient_2m_c}°C</span>
              </div>

              <div className="space-y-2 text-[11px] border-t border-slate-800/80 pt-2">
                <div className="flex justify-between">
                  <span className="text-slate-400">Coolest tile @ peak:</span>
                  <span className="text-cyan-300 font-bold">{day.coolest_tile_at_peak_c}°C</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Measured AOI spread:</span>
                  <span className="text-cyan-300 font-bold">{day.intra_aoi_spread_c}°C</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Soil Resistivity (ρ):</span>
                  <span className="text-amber-400 font-bold">{day.end_of_day_soil_resistivity_rho} K·m/W</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Cable Peak Temp:</span>
                  <span className="text-rose-300 font-bold">{day.cable_conductor_peak_c}°C</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Baseline Hot-Spot:</span>
                  <span className="text-rose-400 font-bold">{day.baseline_peak_hot_spot_c}°C (BREACH)</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Mitigated Hot-Spot:</span>
                  <span className="text-emerald-400 font-bold">{day.mitigated_peak_hot_spot_c}°C (SAFE)</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div id="tour-72h-provenance" className="flex flex-wrap items-center gap-x-4 gap-y-1 rounded-xl border border-cyan-900/60 bg-cyan-950/20 px-4 py-2 text-[10px] font-mono text-cyan-200">
        <span className="font-bold">ENVIRONMENT: {provenance?.data_source ?? '—'}</span>
        <span>72 hourly tcm rows</span>
        <span>Solar: live GHI/cloud + geometry</span>
        <span>Load/soil/dispatch: modelled</span>
      </div>

      {/* 24-Hour Timeline of Selected Day */}
      <div id="tour-72h-timeline" className="p-4 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-3 font-mono text-xs">
        <div className="flex items-center justify-between text-xs text-slate-300 font-bold border-b border-slate-800 pb-2">
          <span>Day {selectedDay} Hourly Progression (24 Steps)</span>
          <span className="text-amber-400">Underground Cable + Transformer Co-Simulation</span>
        </div>

        <div className="grid grid-cols-4 sm:grid-cols-8 md:grid-cols-12 gap-2 overflow-x-auto">
          {currentDaySteps.map((step: any, idx: number) => (
            <div
              key={idx}
              className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-center space-y-1"
            >
              <div className="text-[10px] text-slate-500">{step.hour_of_day}:00</div>
              <div className="text-xs font-black text-rose-300">{step.fortyguard_2m_ambient_c}°</div>
              <div className="text-[9px] text-amber-400">ρ:{step.soil_resistivity_rho}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
