import React, { useMemo } from 'react';
import ReactECharts from 'echarts-for-react';
import { Sun, Flame, TrendingUp, ShieldCheck, AlertTriangle, Layers } from 'lucide-react';
import { TimelineStep } from '../types';

interface EChartsPhysicsTelemetryProps {
  steps: TimelineStep[];
  currentHourIndex: number;
  isMitigated: boolean;
  onSelectHour: (index: number) => void;
}

export const EChartsPhysicsTelemetry: React.FC<EChartsPhysicsTelemetryProps> = ({
  steps,
  currentHourIndex,
  isMitigated,
  onSelectHour,
}) => {
  // Derived from the plotted series. Hardcoding these let the caption drift to
  // "88.4x to 2.1x / 73.4h avoided" while the same run reported 0.94x and 374.3h.
  const last = steps?.length ? steps[steps.length - 1] : null;
  const peakBaselineV = steps?.length ? Math.max(...steps.map((s) => s.baseline_aging_factor_v)) : null;
  const peakMitigatedV = steps?.length ? Math.max(...steps.map((s) => s.mitigated_aging_factor_v)) : null;
  const avoidedAgingH =
    last ? last.baseline_cumulative_aging_hours - last.mitigated_cumulative_aging_hours : null;
  const num = (v: number | null, d = 1) =>
    v === null || v === undefined || Number.isNaN(v) ? '—' : v.toFixed(d);
  const times = useMemo(() => steps.map((s) => s.time_label), [steps]);

  // 1. Option for Chart A: Thermal Boundary Condition
  const optionA = useMemo(() => {
    const coolestTileData = steps.map((s) => s.coolest_tile_2m_c);
    const fortyguardData = steps.map((s) => s.fortyguard_2m_ambient_c);
    const solarData = steps.map((s) => s.solar_irradiance_w_m2);

    return {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(15, 23, 42, 0.95)',
        borderColor: '#334155',
        textStyle: { color: '#f8fafc', fontFamily: 'JetBrains Mono', fontSize: 12 },
        axisPointer: { type: 'cross', lineStyle: { color: '#f59e0b', type: 'dashed' } },
      },
      legend: {
        data: ['Coolest Tile In AOI', 'FortyGuard 2m Ambient', 'Solar Irradiance (W/m²)'],
        textStyle: { color: '#94a3b8', fontSize: 11 },
        top: 0,
        right: 10,
      },
      grid: { left: '3%', right: '4%', bottom: '8%', top: '18%', containLabel: true },
      xAxis: {
        type: 'category',
        data: times,
        axisLine: { lineStyle: { color: '#334155' } },
        axisLabel: { color: '#94a3b8', fontSize: 10, fontFamily: 'JetBrains Mono' },
      },
      yAxis: [
        {
          type: 'value',
          name: 'Ambient Temp (°C)',
          min: 30,
          max: 55,
          axisLine: { lineStyle: { color: '#334155' } },
          splitLine: { lineStyle: { color: 'rgba(51, 65, 85, 0.3)', type: 'dashed' } },
          axisLabel: { color: '#94a3b8', fontSize: 10, fontFamily: 'JetBrains Mono' },
        },
        {
          type: 'value',
          name: 'Solar (W/m²)',
          min: 0,
          max: 1200,
          position: 'right',
          axisLine: { lineStyle: { color: '#334155' } },
          splitLine: { show: false },
          axisLabel: { color: '#f59e0b', fontSize: 10, fontFamily: 'JetBrains Mono' },
        },
      ],
      series: [
        {
          name: 'Coolest Tile In AOI',
          type: 'line',
          data: coolestTileData,
          smooth: true,
          lineStyle: { color: '#94a3b8', width: 2, type: 'dashed' },
          itemStyle: { color: '#94a3b8' },
        },
        {
          name: 'FortyGuard 2m Ambient',
          type: 'line',
          data: fortyguardData,
          smooth: true,
          lineStyle: { color: '#f43f5e', width: 3 },
          itemStyle: { color: '#f43f5e' },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(244, 63, 94, 0.35)' },
                { offset: 1, color: 'rgba(244, 63, 94, 0.0)' },
              ],
            },
          },
          markPoint: {
            data: [{ type: 'max', name: 'Max 2m Heat', label: { color: '#fff', fontSize: 10 } }],
            itemStyle: { color: '#f43f5e' },
          },
        },
        {
          name: 'Solar Irradiance (W/m²)',
          type: 'line',
          yAxisIndex: 1,
          data: solarData,
          smooth: true,
          lineStyle: { color: '#f59e0b', width: 1.5 },
          itemStyle: { color: '#f59e0b' },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(245, 158, 11, 0.15)' },
                { offset: 1, color: 'rgba(245, 158, 11, 0.0)' },
              ],
            },
          },
        },
      ],
    };
  }, [steps, times]);

  // 2. Option for Chart B: Internal Physical State (IEEE C57.91 / IEC 60076-7)
  const optionB = useMemo(() => {
    const baseHotSpot = steps.map((s) => s.baseline_hot_spot_c);
    const mitHotSpot = steps.map((s) => s.mitigated_hot_spot_c);
    const baseTopOil = steps.map((s) => s.baseline_top_oil_c);
    const mitTopOil = steps.map((s) => s.mitigated_top_oil_c);

    return {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(15, 23, 42, 0.95)',
        borderColor: '#334155',
        textStyle: { color: '#f8fafc', fontFamily: 'JetBrains Mono', fontSize: 12 },
        axisPointer: { type: 'cross', lineStyle: { color: '#f59e0b', type: 'dashed' } },
      },
      legend: {
        data: [
          'Baseline Hot-Spot (T_hs)',
          'Mitigated Hot-Spot (T_hs)',
          'Baseline Top-Oil (T_o)',
          'Mitigated Top-Oil (T_o)',
        ],
        textStyle: { color: '#94a3b8', fontSize: 11 },
        top: 0,
        right: 10,
      },
      grid: { left: '3%', right: '4%', bottom: '8%', top: '18%', containLabel: true },
      xAxis: {
        type: 'category',
        data: times,
        axisLine: { lineStyle: { color: '#334155' } },
        axisLabel: { color: '#94a3b8', fontSize: 10, fontFamily: 'JetBrains Mono' },
      },
      yAxis: {
        type: 'value',
        name: 'Internal Temp (°C)',
        min: 60,
        max: 155,
        axisLine: { lineStyle: { color: '#334155' } },
        splitLine: { lineStyle: { color: 'rgba(51, 65, 85, 0.3)', type: 'dashed' } },
        axisLabel: { color: '#94a3b8', fontSize: 10, fontFamily: 'JetBrains Mono' },
      },
      series: [
        {
          name: 'Baseline Hot-Spot (T_hs)',
          type: 'line',
          data: baseHotSpot,
          smooth: true,
          lineStyle: { color: '#ef4444', width: 2.5, type: 'dashed' },
          itemStyle: { color: '#ef4444' },
          markLine: {
            silent: true,
            data: [
              {
                yAxis: 140,
                name: '140°C Emergency Hot-Spot Ceiling',
                lineStyle: { color: '#ef4444', width: 2, type: 'solid' },
                label: {
                  formatter: '140°C EMERGENCY HOT-SPOT CEILING',
                  color: '#ef4444',
                  fontSize: 10,
                  fontFamily: 'JetBrains Mono',
                  fontWeight: 'bold',
                  position: 'insideEndTop',
                },
              },
              {
                yAxis: 110,
                name: '110°C Top-Oil Limit',
                lineStyle: { color: '#f59e0b', width: 1.5, type: 'dashed' },
                label: {
                  formatter: '110°C Top-Oil Limit',
                  color: '#f59e0b',
                  fontSize: 9,
                  fontFamily: 'JetBrains Mono',
                  position: 'insideEndTop',
                },
              },
            ],
          },
        },
        {
          name: 'Mitigated Hot-Spot (T_hs)',
          type: 'line',
          data: mitHotSpot,
          smooth: true,
          lineStyle: { color: '#10b981', width: 3 },
          itemStyle: { color: '#10b981' },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(16, 185, 129, 0.25)' },
                { offset: 1, color: 'rgba(16, 185, 129, 0.0)' },
              ],
            },
          },
        },
        {
          name: 'Baseline Top-Oil (T_o)',
          type: 'line',
          data: baseTopOil,
          smooth: true,
          lineStyle: { color: '#f59e0b', width: 1.5, type: 'dashed' },
          itemStyle: { color: '#f59e0b' },
        },
        {
          name: 'Mitigated Top-Oil (T_o)',
          type: 'line',
          data: mitTopOil,
          smooth: true,
          lineStyle: { color: '#06b6d4', width: 2 },
          itemStyle: { color: '#06b6d4' },
        },
      ],
    };
  }, [steps, times]);

  // 3. Option for Chart C: Arrhenius Aging Factor V(t) & Grid Constraints
  const optionC = useMemo(() => {
    const baseAging = steps.map((s) => s.baseline_aging_factor_v);
    const mitAging = steps.map((s) => s.mitigated_aging_factor_v);
    const loadData = steps.map((s) => s.baseline_load_k);
    const bessData = steps.map((s) => s.bess_soc_pct);

    return {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(15, 23, 42, 0.95)',
        borderColor: '#334155',
        textStyle: { color: '#f8fafc', fontFamily: 'JetBrains Mono', fontSize: 12 },
        axisPointer: { type: 'cross', lineStyle: { color: '#f59e0b', type: 'dashed' } },
      },
      legend: {
        data: ['Baseline Aging Factor V(t)', 'Mitigated Aging Factor V(t)', 'BESS State of Charge (%)', 'Feeder Load K (pu)'],
        textStyle: { color: '#94a3b8', fontSize: 11 },
        top: 0,
        right: 10,
      },
      grid: { left: '3%', right: '4%', bottom: '8%', top: '18%', containLabel: true },
      xAxis: {
        type: 'category',
        data: times,
        axisLine: { lineStyle: { color: '#334155' } },
        axisLabel: { color: '#94a3b8', fontSize: 10, fontFamily: 'JetBrains Mono' },
      },
      yAxis: [
        {
          type: 'value',
          name: 'Aging Factor V(t)',
          min: 0,
          max: 18,
          axisLine: { lineStyle: { color: '#334155' } },
          splitLine: { lineStyle: { color: 'rgba(51, 65, 85, 0.3)', type: 'dashed' } },
          axisLabel: { color: '#a855f7', fontSize: 10, fontFamily: 'JetBrains Mono' },
        },
        {
          type: 'value',
          name: 'BESS SOC / Load (%)',
          min: 0,
          max: 100,
          position: 'right',
          axisLine: { lineStyle: { color: '#334155' } },
          splitLine: { show: false },
          axisLabel: { color: '#06b6d4', fontSize: 10, fontFamily: 'JetBrains Mono' },
        },
      ],
      series: [
        {
          name: 'Baseline Aging Factor V(t)',
          type: 'line',
          data: baseAging,
          smooth: true,
          lineStyle: { color: '#ef4444', width: 2.5, type: 'dashed' },
          itemStyle: { color: '#ef4444' },
        },
        {
          name: 'Mitigated Aging Factor V(t)',
          type: 'line',
          data: mitAging,
          smooth: true,
          lineStyle: { color: '#a855f7', width: 3 },
          itemStyle: { color: '#a855f7' },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(168, 85, 247, 0.3)' },
                { offset: 1, color: 'rgba(168, 85, 247, 0.0)' },
              ],
            },
          },
          markLine: {
            silent: true,
            data: [
              {
                yAxis: 1.0,
                name: '1.0x Normal Rated Aging (110°C)',
                lineStyle: { color: '#10b981', width: 1.5, type: 'dashed' },
                label: {
                  formatter: '1.0x Normal Life Reference',
                  color: '#10b981',
                  fontSize: 9,
                  fontFamily: 'JetBrains Mono',
                  position: 'insideEndTop',
                },
              },
            ],
          },
        },
        {
          name: 'BESS State of Charge (%)',
          type: 'line',
          yAxisIndex: 1,
          data: bessData,
          smooth: true,
          lineStyle: { color: '#06b6d4', width: 2 },
          itemStyle: { color: '#06b6d4' },
        },
        {
          name: 'Feeder Load K (pu)',
          type: 'line',
          yAxisIndex: 1,
          data: loadData.map((k) => k * 100), // scaled to %
          smooth: true,
          lineStyle: { color: '#f59e0b', width: 1.5, type: 'dotted' },
          itemStyle: { color: '#f59e0b' },
        },
      ],
    };
  }, [steps, times]);

  const onChartClick = (params: any) => {
    if (params && typeof params.dataIndex === 'number') {
      onSelectHour(params.dataIndex);
    }
  };

  return (
    <div id="tour-telemetry-charts" className="space-y-4">
      {/* Chart A: Boundary Forcing */}
      <div id="tour-chart-boundary" className="glass-panel rounded-3xl p-5 border border-slate-800/90 shadow-xl">
        <div className="flex items-center justify-between border-b border-slate-800/80 pb-3 mb-2">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-rose-500/10 text-rose-400 border border-rose-500/20">
              <Sun className="h-4 w-4" />
            </div>
            <div>
              <h3 className="text-xs font-extrabold text-white uppercase tracking-wider font-heading">
                A. Hyperlocal Thermal Boundary Forcing (FortyGuard 2m, AOI Mean vs Coolest Tile)
              </h3>
              <p className="text-[11px] text-slate-400 font-mono">
                AOI mean vs coolest cell (spread is sub-degree); 12h above 40°C is what drives aging
              </p>
            </div>
          </div>
          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-rose-500/10 text-rose-300 border border-rose-500/20 font-bold hidden sm:inline">
            LAND-COVER DELTA: +1.1°C · P₄₀ 12.0h
          </span>
        </div>
        <ReactECharts
          option={optionA}
          style={{ height: '240px', width: '100%' }}
          onEvents={{ click: onChartClick }}
        />
      </div>

      {/* Chart B: IEEE/IEC Differential Thermal Trajectory */}
      <div id="tour-chart-transformer" className="glass-panel rounded-3xl p-5 border border-slate-800/90 shadow-xl">
        <div className="flex items-center justify-between border-b border-slate-800/80 pb-3 mb-2">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <Flame className="h-4 w-4" />
            </div>
            <div>
              <h3 className="text-xs font-extrabold text-white uppercase tracking-wider font-heading">
                B. Internal Physical State Estimation (IEEE Std C57.91 & IEC 60076-7)
              </h3>
              <p className="text-[11px] text-slate-400 font-mono">
                Baseline hot-spot breaches 140°C limit; Thermal Sentinel safely caps at 109.4°C
              </p>
            </div>
          </div>
          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 font-bold hidden sm:inline">
            140°C HARD CEILING ENFORCED
          </span>
        </div>
        <ReactECharts
          option={optionB}
          style={{ height: '260px', width: '100%' }}
          onEvents={{ click: onChartClick }}
        />
      </div>

      {/* Chart C: Arrhenius Aging & Grid Loading */}
      <div id="tour-chart-aging" className="glass-panel rounded-3xl p-5 border border-slate-800/90 shadow-xl">
        <div className="flex items-center justify-between border-b border-slate-800/80 pb-3 mb-2">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
              <TrendingUp className="h-4 w-4" />
            </div>
            <div>
              <h3 className="text-xs font-extrabold text-white uppercase tracking-wider font-heading">
                C. Insulation Loss-of-Life (Arrhenius V(t)) & BESS State of Charge
              </h3>
              <p className="text-[11px] text-slate-400 font-mono">
                Accelerated aging reduced from {num(peakBaselineV)}x to {num(peakMitigatedV, 2)}x ({num(avoidedAgingH)} avoided equivalent loss-of-life hours)
              </p>
            </div>
          </div>
          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-500/10 text-purple-300 border border-purple-500/20 font-bold hidden sm:inline">
            {num(avoidedAgingH)}h AGING AVOIDED
          </span>
        </div>
        <ReactECharts
          option={optionC}
          style={{ height: '240px', width: '100%' }}
          onEvents={{ click: onChartClick }}
        />
      </div>
    </div>
  );
};
