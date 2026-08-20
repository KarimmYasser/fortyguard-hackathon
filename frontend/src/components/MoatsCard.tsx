import React from 'react';
import { Layers, ShieldAlert, Wind, Droplets, ArrowRight } from 'lucide-react';
import { SoilCableState, VirtualMoistureState } from '../types';

interface MoatsCardProps {
  soilState: SoilCableState;
  moistureState: VirtualMoistureState;
}

export const MoatsCard: React.FC<MoatsCardProps> = ({ soilState, moistureState }) => {
  return (
    <div className="glass-panel rounded-2xl p-5 border border-slate-800">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
        <div className="flex items-center gap-2">
          <Layers className="h-5 w-5 text-amber-400" />
          <div>
            <h3 className="text-xs font-bold text-white uppercase tracking-wider font-heading">
              Four Asymmetric Scientific Moats
            </h3>
            <p className="text-[11px] text-slate-400">
              Inferring 4 unmeasured latent physical cascades that utility SCADA and generic AI miss
            </p>
          </div>
        </div>
        <span className="text-[10px] font-mono px-2.5 py-1 rounded bg-slate-900 border border-slate-800 text-slate-400">
          Cross-Disciplinary AI
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
        {/* Moat 1: Soil Dryout */}
        <div className="bg-slate-950/70 p-3.5 rounded-xl border border-slate-800/80 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-[11px] font-mono text-amber-400 mb-1">
              <span className="font-bold">1. Cable–Soil Dryout</span>
              <span className="text-[10px] px-1.5 py-0.2 rounded bg-amber-500/10 border border-amber-500/20">
                IEC 60287
              </span>
            </div>
            <p className="text-xs text-slate-300 font-medium">
              Soil thermal resistivity surge from multi-day persistence
            </p>
          </div>
          <div className="mt-3 pt-2 border-t border-slate-800/60 font-mono text-xs flex items-baseline justify-between">
            <span className="text-slate-400 text-[11px]">Resistivity:</span>
            <span className="text-amber-300 font-bold">
              ρ = {soilState.soil_thermal_resistivity_rho_soil} K·m/W
            </span>
          </div>
        </div>

        {/* Moat 2: Control Barrier Functions */}
        <div className="bg-slate-950/70 p-3.5 rounded-xl border border-slate-800/80 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-[11px] font-mono text-emerald-400 mb-1">
              <span className="font-bold">2. CBF-QP Safety Filter</span>
              <span className="text-[10px] px-1.5 py-0.2 rounded bg-emerald-500/10 border border-emerald-500/20">
                IEEE TAC
              </span>
            </div>
            <p className="text-xs text-slate-300 font-medium">
              Provably safe forward-invariance under 12h forecast error (Ta ± ε)
            </p>
          </div>
          <div className="mt-3 pt-2 border-t border-slate-800/60 font-mono text-xs flex items-baseline justify-between">
            <span className="text-slate-400 text-[11px]">Safe Set:</span>
            <span className="text-emerald-300 font-bold">h(x) ≥ 0 Invariant</span>
          </div>
        </div>

        {/* Moat 3: Urban Canyon Aerodynamics */}
        <div className="bg-slate-950/70 p-3.5 rounded-xl border border-slate-800/80 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-[11px] font-mono text-cyan-400 mb-1">
              <span className="font-bold">3. Canyon Aerodynamics</span>
              <span className="text-[10px] px-1.5 py-0.2 rounded bg-cyan-500/10 border border-cyan-500/20">
                Oke / Evola
              </span>
            </div>
            <p className="text-xs text-slate-300 font-medium">
              Deep street canyon wind-sheltering & radiator cooling derating
            </p>
          </div>
          <div className="mt-3 pt-2 border-t border-slate-800/60 font-mono text-xs flex items-baseline justify-between">
            <span className="text-slate-400 text-[11px]">Cooling Derate:</span>
            <span className="text-cyan-300 font-bold">η_cool = 0.68 (-32%)</span>
          </div>
        </div>

        {/* Moat 4: Virtual Moisture Sensor */}
        <div className="bg-slate-950/70 p-3.5 rounded-xl border border-slate-800/80 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-[11px] font-mono text-purple-400 mb-1">
              <span className="font-bold">4. Virtual Moisture Sensor</span>
              <span className="text-[10px] px-1.5 py-0.2 rounded bg-purple-500/10 border border-purple-500/20">
                Fick's Law
              </span>
            </div>
            <p className="text-xs text-slate-300 font-medium">
              Paper-to-oil desorption & dielectric breakdown warning
            </p>
          </div>
          <div className="mt-3 pt-2 border-t border-slate-800/60 font-mono text-xs flex items-baseline justify-between">
            <span className="text-slate-400 text-[11px]">Oil Saturation:</span>
            <span className="text-purple-300 font-bold">
              RS_oil = {(moistureState.relative_saturation_rs_oil * 100).toFixed(1)}%
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
