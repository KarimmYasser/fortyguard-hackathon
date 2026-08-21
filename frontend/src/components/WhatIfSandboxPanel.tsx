import React, { useState, useEffect } from 'react';
import {
  Sliders,
  Sparkles,
  Flame,
  Battery,
  ShieldCheck,
  Building,
  Wind,
  RotateCcw,
  Zap,
  CheckCircle2,
  AlertTriangle,
  Play,
} from 'lucide-react';
import { API_BASE } from '../utils/api';
import { ReplayDataset } from '../types';
import { BESSDegradationViewer } from './BESSDegradationViewer';

interface WhatIfSandboxPanelProps {
  onSimulateResult: (result: ReplayDataset) => void;
  onResetToDefault: () => void;
}

export const WhatIfSandboxPanel: React.FC<WhatIfSandboxPanelProps> = ({
  onSimulateResult,
  onResetToDefault,
}) => {
  const [deltaC, setDeltaC] = useState<number>(4.5);
  const [heatwaveDay, setHeatwaveDay] = useState<number>(24);
  const [transformerMva, setTransformerMva] = useState<number>(25.0);
  const [bessCapacityMwh, setBessCapacityMwh] = useState<number>(25.0);
  const [canyonHw, setCanyonHw] = useState<number>(1.85);
  const [forcedCooling, setForcedCooling] = useState<boolean>(true);
  const [isSimulating, setIsSimulating] = useState<boolean>(false);
  const [activePreset, setActivePreset] = useState<string>('phoenix_historic');

  const executeSimulation = async (
    d: number,
    day: number,
    mva: number,
    bess: number,
    hw: number,
    cooling: boolean
  ) => {
    setIsSimulating(true);
    try {
      const resp = await fetch(`${API_BASE}/api/v1/sandbox/simulate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          microclimate_delta_c: d,
          heatwave_day: day,
          transformer_mva: mva,
          bess_capacity_mwh: bess,
          canyon_aspect_ratio: hw,
          forced_cooling_enabled: cooling,
        }),
      });

      if (resp.ok) {
        const json = await resp.json();
        onSimulateResult(json);
      }
    } catch (err) {
      console.error('Failed to run live sandbox simulation', err);
    } finally {
      setIsSimulating(false);
    }
  };

  const applyPreset = (preset: string) => {
    setActivePreset(preset);
    let d = 4.5,
      day = 24,
      mva = 25.0,
      bess = 25.0,
      hw = 1.85,
      cooling = true;

    if (preset === 'phoenix_historic') {
      d = 4.5;
      day = 24;
      mva = 25.0;
      bess = 25.0;
      hw = 1.85;
      cooling = true;
    } else if (preset === 'airport_blindspot') {
      d = 0.0; // Blind to local heat
      day = 5;
      mva = 25.0;
      bess = 0.0;
      hw = 0.5;
      cooling = false;
    } else if (preset === 'desertification_31d') {
      d = 5.5;
      day = 31; // Maximum dryout
      mva = 35.0;
      bess = 30.0;
      hw = 2.4;
      cooling = true;
    } else if (preset === 'zero_bess_stress') {
      d = 5.0;
      day = 20;
      mva = 25.0;
      bess = 0.0; // No battery buffer
      hw = 2.0;
      cooling = true;
    }

    setDeltaC(d);
    setHeatwaveDay(day);
    setTransformerMva(mva);
    setBessCapacityMwh(bess);
    setCanyonHw(hw);
    setForcedCooling(cooling);

    executeSimulation(d, day, mva, bess, hw, cooling);
  };

  return (
    <div className="glass-panel rounded-3xl p-6 border border-amber-500/30 bg-gradient-to-b from-[#0F172A] via-[#090E17] to-[#040810] shadow-2xl space-y-6">
      {/* Top Header & Presets */}
      <div className="flex flex-col xl:flex-row items-start xl:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div className="flex items-center gap-3">
          <div className="h-11 w-11 rounded-2xl bg-gradient-to-br from-amber-500 to-orange-500 p-[1px] shadow-lg shadow-amber-500/20">
            <div className="h-full w-full bg-slate-950 rounded-[15px] flex items-center justify-center">
              <Sliders className="h-5 w-5 text-amber-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-base font-black text-white uppercase tracking-wide font-heading">
                Live "What-If" Physics Stress Studio
              </h2>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40 animate-pulse">
                REAL-TIME SOLVER
              </span>
            </div>
            <p className="text-xs text-slate-400 font-mono mt-0.5">
              Modulate boundary layer forcing, multi-day dryout, and BESS reserves; re-solves ODEs in &lt;15ms
            </p>
          </div>
        </div>

        {/* Quick Presets */}
        <div id="tour-sandbox-actions" className="flex items-center gap-1.5 flex-wrap">
          <button
            onClick={() => applyPreset('phoenix_historic')}
            className={`px-3 py-1.5 rounded-xl text-xs font-bold font-mono transition-all flex items-center gap-1.5 ${
              activePreset === 'phoenix_historic'
                ? 'bg-amber-500 text-slate-950 shadow-md shadow-amber-500/30 font-black'
                : 'bg-slate-900/80 text-slate-300 hover:text-white border border-slate-800'
            }`}
          >
            ⚡ Phoenix '23 Peak
          </button>
          <button
            onClick={() => applyPreset('airport_blindspot')}
            className={`px-3 py-1.5 rounded-xl text-xs font-bold font-mono transition-all flex items-center gap-1.5 ${
              activePreset === 'airport_blindspot'
                ? 'bg-rose-600 text-white shadow-md shadow-rose-600/30 font-black'
                : 'bg-slate-900/80 text-slate-300 hover:text-white border border-slate-800'
            }`}
          >
            🚨 Station-Weather Blindspot (0°C)
          </button>
          <button
            onClick={() => applyPreset('desertification_31d')}
            className={`px-3 py-1.5 rounded-xl text-xs font-bold font-mono transition-all flex items-center gap-1.5 ${
              activePreset === 'desertification_31d'
                ? 'bg-purple-600 text-white shadow-md shadow-purple-600/30 font-black'
                : 'bg-slate-900/80 text-slate-300 hover:text-white border border-slate-800'
            }`}
          >
            🏜️ 31-Day Desertification
          </button>
          <button
            onClick={() => applyPreset('zero_bess_stress')}
            className={`px-3 py-1.5 rounded-xl text-xs font-bold font-mono transition-all flex items-center gap-1.5 ${
              activePreset === 'zero_bess_stress'
                ? 'bg-cyan-600 text-white shadow-md shadow-cyan-600/30 font-black'
                : 'bg-slate-900/80 text-slate-300 hover:text-white border border-slate-800'
            }`}
          >
            🔋 Zero-BESS Stress
          </button>
        </div>
      </div>

      {/* 5 Interactive Slider Controls */}
      <div id="tour-sandbox-controls" className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {/* Slider 1: FortyGuard Microclimate Delta */}
        <div className="bg-slate-950/80 p-4 rounded-2xl border border-slate-800 space-y-3">
          <div className="flex items-center justify-between text-xs font-mono">
            <span className="text-slate-300 font-bold flex items-center gap-1.5">
              <Flame className="h-4 w-4 text-rose-400" /> 1. FortyGuard 2m Delta:
            </span>
            <span className="text-rose-400 font-extrabold text-sm">+{deltaC.toFixed(1)}°C</span>
          </div>
          <input
            type="range"
            min="0.0"
            max="6.0"
            step="0.5"
            value={deltaC}
            onChange={(e) => {
              const val = parseFloat(e.target.value);
              setDeltaC(val);
              setActivePreset('custom');
              executeSimulation(val, heatwaveDay, transformerMva, bessCapacityMwh, canyonHw, forcedCooling);
            }}
            className="w-full accent-rose-500 cursor-pointer"
          />
          <div className="flex justify-between text-[10px] font-mono text-slate-500">
            <span>0.0°C (Station Weather)</span>
            <span>+1.1°C (Phoenix 2m, measured)</span>
            <span>+6.0°C (Extreme)</span>
          </div>
        </div>

        {/* Slider 2: Multi-Day Heat Persistence */}
        <div className="bg-slate-950/80 p-4 rounded-2xl border border-slate-800 space-y-3">
          <div className="flex items-center justify-between text-xs font-mono">
            <span className="text-slate-300 font-bold flex items-center gap-1.5">
              <Zap className="h-4 w-4 text-amber-400" /> 2. Heatwave Duration:
            </span>
            <span className="text-amber-400 font-extrabold text-sm">Day {heatwaveDay} / 31</span>
          </div>
          <input
            type="range"
            min="1"
            max="31"
            step="1"
            value={heatwaveDay}
            onChange={(e) => {
              const val = parseInt(e.target.value);
              setHeatwaveDay(val);
              setActivePreset('custom');
              executeSimulation(deltaC, val, transformerMva, bessCapacityMwh, canyonHw, forcedCooling);
            }}
            className="w-full accent-amber-500 cursor-pointer"
          />
          <div className="flex justify-between text-[10px] font-mono text-slate-500">
            <span>Day 1 (Moist Soil)</span>
            <span>Day 24 (Historic)</span>
            <span>Day 31 (Desertified)</span>
          </div>
        </div>

        {/* Slider 3: BESS Peak-Shaving Capacity */}
        <div className="bg-slate-950/80 p-4 rounded-2xl border border-slate-800 space-y-3">
          <div className="flex items-center justify-between text-xs font-mono">
            <span className="text-slate-300 font-bold flex items-center gap-1.5">
              <Battery className="h-4 w-4 text-cyan-400" /> 3. BESS Capacity:
            </span>
            <span className="text-cyan-400 font-extrabold text-sm">{bessCapacityMwh.toFixed(0)} MWh</span>
          </div>
          <input
            type="range"
            min="0"
            max="50"
            step="5"
            value={bessCapacityMwh}
            onChange={(e) => {
              const val = parseFloat(e.target.value);
              setBessCapacityMwh(val);
              setActivePreset('custom');
              executeSimulation(deltaC, heatwaveDay, transformerMva, val, canyonHw, forcedCooling);
            }}
            className="w-full accent-cyan-500 cursor-pointer"
          />
          <div className="flex justify-between text-[10px] font-mono text-slate-500">
            <span>0 MWh (Unbuffered)</span>
            <span>25 MWh (Standard)</span>
            <span>50 MWh (Utility)</span>
          </div>
        </div>

        {/* Slider 4: Transformer Rating MVA */}
        <div className="bg-slate-950/80 p-4 rounded-2xl border border-slate-800 space-y-3">
          <div className="flex items-center justify-between text-xs font-mono">
            <span className="text-slate-300 font-bold flex items-center gap-1.5">
              <ShieldCheck className="h-4 w-4 text-emerald-400" /> 4. Transformer Rating:
            </span>
            <span className="text-emerald-400 font-extrabold text-sm">{transformerMva.toFixed(0)} MVA</span>
          </div>
          <input
            type="range"
            min="15"
            max="50"
            step="5"
            value={transformerMva}
            onChange={(e) => {
              const val = parseFloat(e.target.value);
              setTransformerMva(val);
              setActivePreset('custom');
              executeSimulation(deltaC, heatwaveDay, val, bessCapacityMwh, canyonHw, forcedCooling);
            }}
            className="w-full accent-emerald-500 cursor-pointer"
          />
          <div className="flex justify-between text-[10px] font-mono text-slate-500">
            <span>15 MVA</span>
            <span>25 MVA (Standard)</span>
            <span>50 MVA (Substation)</span>
          </div>
        </div>

        {/* Slider 5: Urban Canyon Aspect Ratio */}
        <div className="bg-slate-950/80 p-4 rounded-2xl border border-slate-800 space-y-3">
          <div className="flex items-center justify-between text-xs font-mono">
            <span className="text-slate-300 font-bold flex items-center gap-1.5">
              <Building className="h-4 w-4 text-purple-400" /> 5. Canyon Geometry (H/W):
            </span>
            <span className="text-purple-400 font-extrabold text-sm">{canyonHw.toFixed(2)}</span>
          </div>
          <input
            type="range"
            min="0.5"
            max="3.0"
            step="0.25"
            value={canyonHw}
            onChange={(e) => {
              const val = parseFloat(e.target.value);
              setCanyonHw(val);
              setActivePreset('custom');
              executeSimulation(deltaC, heatwaveDay, transformerMva, bessCapacityMwh, val, forcedCooling);
            }}
            className="w-full accent-purple-500 cursor-pointer"
          />
          <div className="flex justify-between text-[10px] font-mono text-slate-500">
            <span>0.5 (Open Substation)</span>
            <span>1.85 (Downtown)</span>
            <span>3.0 (Deep Canyon)</span>
          </div>
        </div>

        {/* Toggle 6: Forced Cooling State */}
        <div className="bg-slate-950/80 p-4 rounded-2xl border border-slate-800 flex flex-col justify-between">
          <div className="flex items-center justify-between text-xs font-mono">
            <span className="text-slate-300 font-bold flex items-center gap-1.5">
              <Wind className="h-4 w-4 text-amber-400" /> 6. Forced Cooling Stage 2:
            </span>
            <span className={`font-bold ${forcedCooling ? 'text-emerald-400' : 'text-slate-500'}`}>
              {forcedCooling ? 'ENABLED (+35%)' : 'DISABLED'}
            </span>
          </div>
          <div className="flex items-center gap-3 pt-2">
            <button
              onClick={() => {
                const next = !forcedCooling;
                setForcedCooling(next);
                setActivePreset('custom');
                executeSimulation(deltaC, heatwaveDay, transformerMva, bessCapacityMwh, canyonHw, next);
              }}
              className={`flex-1 py-2 rounded-xl text-xs font-bold font-mono transition-all ${
                forcedCooling
                  ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/30'
                  : 'bg-slate-900 text-slate-400 border border-slate-800'
              }`}
            >
              {forcedCooling ? '✓ Auxiliary Fans Active' : '✕ Fans Inactive'}
            </button>
          </div>
        </div>
      </div>

      {/* BESS Electro-Thermal & SEI Degradation Sub-Engine */}
      <BESSDegradationViewer />
    </div>
  );
};

