import React from 'react';
import { Activity, Flame, Shield, TrendingUp, AlertCircle, Sun, Battery, Gauge } from 'lucide-react';
import { TimelineStep } from '../types';

interface PhysicsTelemetryChartsProps {
  steps: TimelineStep[];
  currentHourIndex: number;
  isMitigated: boolean;
}

export const PhysicsTelemetryCharts: React.FC<PhysicsTelemetryChartsProps> = ({
  steps,
  currentHourIndex,
  isMitigated,
}) => {
  // Chart dimensions & scaling
  const width = 600;
  const height = 140;
  const padding = { top: 15, right: 20, bottom: 25, left: 45 };

  const plotWidth = width - padding.left - padding.right;
  const plotHeight = height - padding.top - padding.bottom;

  // Helper to map (hour_index, value) to SVG (x, y)
  const getX = (idx: number) => padding.left + (idx / (steps.length - 1)) * plotWidth;
  const getY = (val: number, minVal: number, maxVal: number) =>
    padding.top + plotHeight - ((val - minVal) / (maxVal - minVal)) * plotHeight;

  // 1. Boundary Ambient Range: 30°C to 55°C
  const minTempA = 30;
  const maxTempA = 55;
  const pathCoolest = steps.map((s, i) => `${i === 0 ? 'M' : 'L'} ${getX(i)} ${getY(s.coolest_tile_2m_c, minTempA, maxTempA)}`).join(' ');
  const pathFortyGuard = steps.map((s, i) => `${i === 0 ? 'M' : 'L'} ${getX(i)} ${getY(s.fortyguard_2m_ambient_c, minTempA, maxTempA)}`).join(' ');

  // 2. Internal State Range: 60°C to 155°C
  const minTempB = 60;
  const maxTempB = 155;
  const pathBaseTopOil = steps.map((s, i) => `${i === 0 ? 'M' : 'L'} ${getX(i)} ${getY(s.baseline_top_oil_c, minTempB, maxTempB)}`).join(' ');
  const pathBaseHotSpot = steps.map((s, i) => `${i === 0 ? 'M' : 'L'} ${getX(i)} ${getY(s.baseline_hot_spot_c, minTempB, maxTempB)}`).join(' ');
  const pathMitTopOil = steps.map((s, i) => `${i === 0 ? 'M' : 'L'} ${getX(i)} ${getY(s.mitigated_top_oil_c, minTempB, maxTempB)}`).join(' ');
  const pathMitHotSpot = steps.map((s, i) => `${i === 0 ? 'M' : 'L'} ${getX(i)} ${getY(s.mitigated_hot_spot_c, minTempB, maxTempB)}`).join(' ');

  const yCeiling140 = getY(140, minTempB, maxTempB);
  const yCeiling110 = getY(110, minTempB, maxTempB);

  // 3. Aging & Load Range: 0 to 20
  const minV = 0;
  const maxV = 18;
  const pathBaseAging = steps.map((s, i) => `${i === 0 ? 'M' : 'L'} ${getX(i)} ${getY(s.baseline_aging_factor_v, minV, maxV)}`).join(' ');
  const pathMitAging = steps.map((s, i) => `${i === 0 ? 'M' : 'L'} ${getX(i)} ${getY(s.mitigated_aging_factor_v, minV, maxV)}`).join(' ');

  const currentStep = steps[currentHourIndex] || steps[0];
  const currentX = getX(currentHourIndex);

  return (
    <div className="space-y-4">
      {/* Chart A: Boundary Condition Comparison */}
      <div className="glass-panel rounded-2xl p-4 border border-slate-800">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <Sun className="h-4 w-4 text-amber-400" />
            <h4 className="text-xs font-bold text-white uppercase tracking-wider font-heading">
              A. Thermal Boundary: FortyGuard 2-Meter Ambient (AOI Mean vs Coolest Tile)
            </h4>
          </div>
          <div className="flex items-center gap-3 text-[11px] font-mono">
            <span className="flex items-center gap-1 text-slate-400">
              <span className="h-2 w-2 rounded-full bg-slate-400 inline-block"></span> Coolest Tile In AOI
            </span>
            <span className="flex items-center gap-1 text-rose-400 font-bold">
              <span className="h-2 w-2 rounded-full bg-rose-500 inline-block"></span> FortyGuard 2m (+1.1°C measured)
            </span>
          </div>
        </div>

        <div className="relative w-full overflow-hidden">
          <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-auto">
            {/* Grid Lines */}
            <line x1={padding.left} y1={getY(35, minTempA, maxTempA)} x2={width - padding.right} y2={getY(35, minTempA, maxTempA)} stroke="#334155" strokeDasharray="3 3" opacity={0.4} />
            <line x1={padding.left} y1={getY(45, minTempA, maxTempA)} x2={width - padding.right} y2={getY(45, minTempA, maxTempA)} stroke="#334155" strokeDasharray="3 3" opacity={0.4} />
            
            {/* Y-axis labels */}
            <text x={padding.left - 8} y={getY(35, minTempA, maxTempA) + 3} fill="#94a3b8" fontSize="9" fontFamily="monospace" textAnchor="end">35°C</text>
            <text x={padding.left - 8} y={getY(45, minTempA, maxTempA) + 3} fill="#94a3b8" fontSize="9" fontFamily="monospace" textAnchor="end">45°C</text>

            {/* Curves */}
            <path d={pathCoolest} fill="none" stroke="#94a3b8" strokeWidth="2" strokeDasharray="4 4" />
            <path d={pathFortyGuard} fill="none" stroke="#f43f5e" strokeWidth="2.5" />

            {/* Current scrubber vertical line */}
            <line x1={currentX} y1={padding.top} x2={currentX} y2={height - padding.bottom} stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="2 2" />
            <circle cx={currentX} cy={getY(currentStep.fortyguard_2m_ambient_c, minTempA, maxTempA)} r="4" fill="#f43f5e" stroke="#fff" strokeWidth="1.5" />
          </svg>
        </div>
      </div>

      {/* Chart B: IEEE C57.91 / IEC 60076-7 Hot-Spot & Top-Oil Trajectory */}
      <div className="glass-panel rounded-2xl p-4 border border-slate-800">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <Flame className="h-4 w-4 text-rose-400" />
            <h4 className="text-xs font-bold text-white uppercase tracking-wider font-heading">
              B. Internal Physical State: Hot-Spot (T_hs) & Top-Oil (T_o) vs Limits
            </h4>
          </div>
          <div className="flex items-center gap-3 text-[11px] font-mono">
            <span className="flex items-center gap-1 text-rose-400 line-through">
              <span className="h-2 w-2 rounded-full bg-rose-600 inline-block"></span> Baseline Hot-Spot
            </span>
            <span className="flex items-center gap-1 text-emerald-400 font-bold">
              <span className="h-2 w-2 rounded-full bg-emerald-500 inline-block"></span> Mitigated Hot-Spot
            </span>
            <span className="flex items-center gap-1 text-amber-400">
              <span className="h-2 w-2 rounded-full bg-amber-500 inline-block"></span> Top-Oil
            </span>
          </div>
        </div>

        <div className="relative w-full overflow-hidden">
          <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-auto">
            {/* Ceiling Threshold Lines */}
            <line x1={padding.left} y1={yCeiling140} x2={width - padding.right} y2={yCeiling140} stroke="#ef4444" strokeWidth="1.5" strokeDasharray="4 4" />
            <text x={width - padding.right} y={yCeiling140 - 4} fill="#ef4444" fontSize="9" fontFamily="monospace" textAnchor="end" fontWeight="bold">
              140°C EMERGENCY HOT-SPOT CEILING
            </text>

            <line x1={padding.left} y1={yCeiling110} x2={width - padding.right} y2={yCeiling110} stroke="#f59e0b" strokeWidth="1" strokeDasharray="3 3" opacity={0.6} />
            <text x={width - padding.right} y={yCeiling110 - 4} fill="#f59e0b" fontSize="8" fontFamily="monospace" textAnchor="end">
              110°C Top-Oil Limit
            </text>

            {/* Y-axis labels */}
            <text x={padding.left - 8} y={getY(80, minTempB, maxTempB) + 3} fill="#94a3b8" fontSize="9" fontFamily="monospace" textAnchor="end">80°C</text>
            <text x={padding.left - 8} y={getY(110, minTempB, maxTempB) + 3} fill="#94a3b8" fontSize="9" fontFamily="monospace" textAnchor="end">110°C</text>
            <text x={padding.left - 8} y={getY(140, minTempB, maxTempB) + 3} fill="#ef4444" fontSize="9" fontFamily="monospace" textAnchor="end">140°C</text>

            {/* Curves */}
            {/* Baseline Curves */}
            <path d={pathBaseTopOil} fill="none" stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="3 3" opacity={0.4} />
            <path d={pathBaseHotSpot} fill="none" stroke="#ef4444" strokeWidth="2" strokeDasharray="4 4" opacity={isMitigated ? 0.4 : 1.0} />

            {/* Mitigated Curves (Active when mitigated) */}
            {isMitigated && (
              <>
                <path d={pathMitTopOil} fill="none" stroke="#f59e0b" strokeWidth="2" />
                <path d={pathMitHotSpot} fill="none" stroke="#10b981" strokeWidth="2.5" />
              </>
            )}

            {/* Scrubber indicator */}
            <line x1={currentX} y1={padding.top} x2={currentX} y2={height - padding.bottom} stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="2 2" />
            <circle
              cx={currentX}
              cy={getY(isMitigated ? currentStep.mitigated_hot_spot_c : currentStep.baseline_hot_spot_c, minTempB, maxTempB)}
              r="4"
              fill={isMitigated ? '#10b981' : '#ef4444'}
              stroke="#fff"
              strokeWidth="1.5"
            />
          </svg>
        </div>
      </div>

      {/* Chart C: Arrhenius Aging Factor V(t) & Feeder Load Ratio K(t) */}
      <div className="glass-panel rounded-2xl p-4 border border-slate-800">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <TrendingUp className="h-4 w-4 text-purple-400" />
            <h4 className="text-xs font-bold text-white uppercase tracking-wider font-heading">
              C. Degradation & Grid Constraints: Aging Factor V(t) [Arrhenius] & Feeder Load K(t)
            </h4>
          </div>
          <div className="flex items-center gap-3 text-[11px] font-mono">
            <span className="flex items-center gap-1 text-rose-400">
              <span className="h-2 w-2 rounded-full bg-rose-500 inline-block"></span> Baseline V (Peak: 88.4x)
            </span>
            <span className="flex items-center gap-1 text-purple-400 font-bold">
              <span className="h-2 w-2 rounded-full bg-purple-500 inline-block"></span> Mitigated V (2.1x)
            </span>
            <span className="flex items-center gap-1 text-cyan-400">
              <span className="h-2 w-2 rounded-full bg-cyan-400 inline-block"></span> BESS SOC ({currentStep.bess_soc_pct}%)
            </span>
          </div>
        </div>

        <div className="relative w-full overflow-hidden">
          <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-auto">
            {/* 1.0x Normal Life Reference Line */}
            <line x1={padding.left} y1={getY(1.0, minV, maxV)} x2={width - padding.right} y2={getY(1.0, minV, maxV)} stroke="#10b981" strokeWidth="1" strokeDasharray="3 3" opacity={0.6} />
            <text x={width - padding.right} y={getY(1.0, minV, maxV) - 3} fill="#10b981" fontSize="8" fontFamily="monospace" textAnchor="end">
              1.0x Normal Rated Aging Life (110°C)
            </text>

            {/* Y-axis labels */}
            <text x={padding.left - 8} y={getY(1.0, minV, maxV) + 3} fill="#94a3b8" fontSize="9" fontFamily="monospace" textAnchor="end">1.0x</text>
            <text x={padding.left - 8} y={getY(10.0, minV, maxV) + 3} fill="#94a3b8" fontSize="9" fontFamily="monospace" textAnchor="end">10.0x</text>
            <text x={padding.left - 8} y={getY(15.0, minV, maxV) + 3} fill="#ef4444" fontSize="9" fontFamily="monospace" textAnchor="end">15.0x</text>

            {/* Curves */}
            <path d={pathBaseAging} fill="none" stroke="#ef4444" strokeWidth="2" strokeDasharray="3 3" opacity={isMitigated ? 0.4 : 1.0} />
            {isMitigated && (
              <path d={pathMitAging} fill="none" stroke="#a855f7" strokeWidth="2.5" />
            )}

            {/* Scrubber indicator */}
            <line x1={currentX} y1={padding.top} x2={currentX} y2={height - padding.bottom} stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="2 2" />
            <circle
              cx={currentX}
              cy={getY(isMitigated ? currentStep.mitigated_aging_factor_v : currentStep.baseline_aging_factor_v, minV, maxV)}
              r="4"
              fill={isMitigated ? '#a855f7' : '#ef4444'}
              stroke="#fff"
              strokeWidth="1.5"
            />
          </svg>
        </div>
      </div>
    </div>
  );
};
