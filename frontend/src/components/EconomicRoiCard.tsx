import React from 'react';
import { DollarSign, TrendingUp, Calculator, ShieldCheck, ArrowUpRight, Scale } from 'lucide-react';
import { EconomicEvaluation } from '../types';

interface EconomicRoiCardProps {
  economic: EconomicEvaluation;
}

export const EconomicRoiCard: React.FC<EconomicRoiCardProps> = ({ economic }) => {
  return (
    <div className="glass-panel rounded-2xl p-5 border border-slate-800 h-full flex flex-col justify-between">
      <div>
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
          <div className="flex items-center gap-2">
            <Calculator className="h-5 w-5 text-amber-400" />
            <div>
              <h3 className="text-xs font-bold text-white uppercase tracking-wider font-heading">
                Investment-Grade Avoided Loss Model
              </h3>
              <p className="text-[11px] text-slate-400 font-mono">
                LBNL ICE Calculator & IEEE C57.91 Replacement Deferral
              </p>
            </div>
          </div>
          <span className="px-2.5 py-1 rounded-full text-xs font-black font-mono bg-amber-500/15 text-amber-300 border border-amber-500/30">
            AUDITABLE ROI
          </span>
        </div>

        {/* Big ROI Highlight Banner */}
        <div className="bg-gradient-to-r from-amber-950/60 via-slate-900 to-slate-950 p-4 rounded-xl border border-amber-500/30 mb-4 flex items-center justify-between">
          <div>
            <div className="text-[11px] font-mono text-amber-400 uppercase tracking-wider">
              NET AVOIDED LOSS (PER HEAT EVENT)
            </div>
            <div className="text-3xl font-black font-mono text-white mt-0.5">
              ${economic.net_avoided_loss_usd.toLocaleString()}
            </div>
          </div>
          <div className="text-right">
            <div className="text-[11px] font-mono text-slate-400 uppercase">
              ROI MULTIPLE
            </div>
            <div className="text-2xl font-black font-mono text-amber-400 flex items-center gap-0.5 justify-end">
              {economic.roi_multiple}x <ArrowUpRight className="h-5 w-5" />
            </div>
          </div>
        </div>

        {/* 3-Bucket Mathematical Decomposition */}
        <div className="space-y-2 text-xs font-mono">
          {/* Bucket 1: Outage Risk */}
          <div className="flex items-center justify-between p-2 rounded-lg bg-slate-950/60 border border-slate-800/80">
            <div className="flex items-center gap-1.5 text-slate-300">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400"></span>
              <span>1. Avoided Outage Risk [Δp_f · C_consequence]:</span>
            </div>
            <span className="text-emerald-400 font-bold">
              +${economic.avoided_outage_risk_usd.toLocaleString()}
            </span>
          </div>

          {/* Bucket 2: Capital Aging Deferral */}
          <div className="flex items-center justify-between p-2 rounded-lg bg-slate-950/60 border border-slate-800/80">
            <div className="flex items-center gap-1.5 text-slate-300">
              <span className="h-1.5 w-1.5 rounded-full bg-amber-400"></span>
              <span>2. Asset Replacement Deferral [ΔPV_aging]:</span>
            </div>
            <span className="text-amber-400 font-bold">
              +${economic.capital_aging_deferral_usd.toLocaleString()}
            </span>
          </div>

          {/* Bucket 3: Mitigation Cost */}
          <div className="flex items-center justify-between p-2 rounded-lg bg-slate-950/60 border border-slate-800/80">
            <div className="flex items-center gap-1.5 text-slate-300">
              <span className="h-1.5 w-1.5 rounded-full bg-rose-400"></span>
              <span>3. Mitigation Dispatch Cost [BESS + Fans]:</span>
            </div>
            <span className="text-rose-400 font-bold">
              -${economic.mitigation_cost_usd.toLocaleString()}
            </span>
          </div>
        </div>
      </div>

      {/* Formula Footer */}
      <div className="mt-3 pt-2.5 border-t border-slate-800/80 text-[10px] text-slate-400 font-mono flex items-center justify-between">
        <span>VoLL: $12.50/kWh (Hospital/Commercial)</span>
        <span>Transformer Life: 180,000h</span>
      </div>
    </div>
  );
};
