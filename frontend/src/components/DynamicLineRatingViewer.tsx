import React, { useState, useEffect } from 'react';
import { Wind, Sun, Activity, ShieldCheck, AlertTriangle, RefreshCw, Gauge, ArrowUpRight } from 'lucide-react';
import { API_BASE } from '../utils/api';

export const DynamicLineRatingViewer: React.FC = () => {
  const [currentAmps, setCurrentAmps] = useState<number>(820.0);
  const [ambientTempC, setAmbientTempC] = useState<number>(47.6);
  const [windSpeed, setWindSpeed] = useState<number>(1.2);
  const [windAngle, setWindAngle] = useState<number>(90.0);
  const [solarFlux, setSolarFlux] = useState<number>(950.0);
  const [dlrData, setDlrData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchDLR = async () => {
    setLoading(true);
    try {
      const resp = await fetch(`${API_BASE}/api/v1/physics/dlr-solve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          current_amps: currentAmps,
          t_ambient_c: ambientTempC,
          wind_speed_m_per_s: windSpeed,
          wind_angle_deg: windAngle,
          solar_irradiance_w_per_m2: solarFlux,
        }),
      });
      if (resp.ok) {
        const json = await resp.json();
        setDlrData(json);
      }
    } catch (err) {
      console.error('Failed to solve Dynamic Line Rating', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDLR();
  }, [currentAmps, ambientTempC, windSpeed, windAngle, solarFlux]);

  return (
    <div id="tour-dlr-panel" className="glass-panel rounded-3xl p-6 border border-cyan-500/30 bg-slate-950/80 shadow-2xl space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div className="flex items-center gap-3.5">
          <div className="h-11 w-11 rounded-2xl bg-gradient-to-br from-cyan-500 to-blue-600 p-[1px] shadow-lg shadow-cyan-500/20">
            <div className="h-full w-full bg-slate-950 rounded-[15px] flex items-center justify-center">
              <Wind className="h-5 w-5 text-cyan-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2.5">
              <h2 className="text-lg font-bold text-white tracking-wide">
                Dynamic Line Rating (DLR) & Conductor Catenary Sag
              </h2>
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono uppercase tracking-wider bg-cyan-500/15 text-cyan-300 border border-cyan-500/30">
                IEEE Std 738-2012
              </span>
            </div>
            <p className="text-xs text-slate-400 font-mono mt-0.5">
              Bare overhead conductor thermal equilibrium: qc(convection) + qr(radiation) = qs(solar) + I²R
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className={`px-3 py-1.5 rounded-xl text-xs font-mono font-bold flex items-center gap-2 border ${
            dlrData?.status === 'SAFE'
              ? 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30'
              : dlrData?.status === 'WARNING_SAG'
              ? 'bg-amber-500/10 text-amber-300 border-amber-500/30'
              : 'bg-rose-500/10 text-rose-300 border-rose-500/30'
          }`}>
            {dlrData?.status === 'SAFE' ? (
              <ShieldCheck className="h-4 w-4 text-emerald-400" />
            ) : (
              <AlertTriangle className="h-4 w-4 text-rose-400" />
            )}
            <span>STATUS: {dlrData?.status || 'CALCULATING'}</span>
          </div>
        </div>
      </div>

      {/* Sliders & Interactive Microclimate Controls */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 bg-slate-900/60 p-4 rounded-2xl border border-slate-800/80">
        <div>
          <div className="flex justify-between text-xs font-mono mb-1">
            <span className="text-slate-400">Load Current:</span>
            <span className="text-cyan-300 font-bold">{currentAmps} A</span>
          </div>
          <input
            type="range"
            min="200"
            max="1400"
            step="10"
            value={currentAmps}
            onChange={(e) => setCurrentAmps(parseFloat(e.target.value))}
            className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-400"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs font-mono mb-1">
            <span className="text-slate-400">2m Ambient:</span>
            <span className="text-amber-300 font-bold">{ambientTempC}°C</span>
          </div>
          <input
            type="range"
            min="20"
            max="55"
            step="0.5"
            value={ambientTempC}
            onChange={(e) => setAmbientTempC(parseFloat(e.target.value))}
            className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-amber-400"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs font-mono mb-1">
            <span className="text-slate-400">Wind Velocity:</span>
            <span className="text-emerald-300 font-bold">{windSpeed} m/s</span>
          </div>
          <input
            type="range"
            min="0.2"
            max="12.0"
            step="0.2"
            value={windSpeed}
            onChange={(e) => setWindSpeed(parseFloat(e.target.value))}
            className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-400"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs font-mono mb-1">
            <span className="text-slate-400">Wind Incidence:</span>
            <span className="text-blue-300 font-bold">{windAngle}°</span>
          </div>
          <input
            type="range"
            min="10"
            max="90"
            step="5"
            value={windAngle}
            onChange={(e) => setWindAngle(parseFloat(e.target.value))}
            className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-blue-400"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs font-mono mb-1">
            <span className="text-slate-400">Solar GHI:</span>
            <span className="text-orange-300 font-bold">{solarFlux} W/m²</span>
          </div>
          <input
            type="range"
            min="0"
            max="1200"
            step="50"
            value={solarFlux}
            onChange={(e) => setSolarFlux(parseFloat(e.target.value))}
            className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-orange-400"
          />
        </div>
      </div>

      {/* KPI Cards */}
      {dlrData && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
            <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
              Conductor Equilibrium Temp
            </span>
            <div className="flex items-baseline gap-2 mt-1.5">
              <span className={`text-2xl font-bold font-mono ${
                dlrData.conductor_temp_c > 75 ? 'text-rose-400' : 'text-cyan-300'
              }`}>
                {dlrData.conductor_temp_c}°C
              </span>
              <span className="text-xs text-slate-500 font-mono">/ 75°C max</span>
            </div>
            <div className="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
              <div
                className={`h-full ${dlrData.conductor_temp_c > 75 ? 'bg-rose-500' : 'bg-cyan-500'}`}
                style={{ width: `${Math.min((dlrData.conductor_temp_c / 75) * 100, 100)}%` }}
              />
            </div>
          </div>

          <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
            <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
              Max Dynamic Ampacity (DLR)
            </span>
            <div className="flex items-baseline gap-2 mt-1.5">
              <span className="text-2xl font-bold font-mono text-emerald-400">
                {dlrData.max_dynamic_ampacity_amps} A
              </span>
              <span className="text-xs text-slate-500 font-mono">(Static: {dlrData.static_ampacity_amps} A)</span>
            </div>
            <span className="text-[10px] font-mono text-emerald-300/80 mt-1 block flex items-center gap-1">
              <ArrowUpRight className="h-3 w-3" /> Headroom: {dlrData.capacity_margin_pct}%
            </span>
          </div>

          <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
            <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
              Catenary Sag / Elongation
            </span>
            <div className="flex items-baseline gap-2 mt-1.5">
              <span className="text-2xl font-bold font-mono text-amber-300">
                {dlrData.catenary_sag_m} m
              </span>
              <span className="text-xs text-slate-500 font-mono">(ΔL: +{dlrData.thermal_elongation_m}m)</span>
            </div>
            <span className="text-[10px] font-mono text-slate-400 mt-1 block">
              Span Length: 250m ruling span
            </span>
          </div>

          <div className="bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
            <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
              Ground Clearance Margin
            </span>
            <div className="flex items-baseline gap-2 mt-1.5">
              <span className={`text-2xl font-bold font-mono ${
                dlrData.ground_clearance_m < 6.5 ? 'text-rose-400' : 'text-cyan-300'
              }`}>
                {dlrData.ground_clearance_m} m
              </span>
              <span className="text-xs text-slate-500 font-mono">/ 6.5m NESC min</span>
            </div>
            <span className={`text-[10px] font-mono mt-1 block font-bold ${
              dlrData.flashover_clearance_violation ? 'text-rose-400' : 'text-emerald-400'
            }`}>
              {dlrData.flashover_clearance_violation ? '⚠️ FLASHOVER HAZARD DETECTED' : '✅ STATUTORY CLEARANCE OK'}
            </span>
          </div>
        </div>
      )}

      {/* Thermodynamic Balance Decomposition */}
      {dlrData && (
        <div className="bg-slate-900/50 p-4 rounded-2xl border border-slate-800/80">
          <h4 className="text-xs font-bold text-slate-300 font-mono uppercase tracking-wider mb-3">
            IEEE 738 Heat Transfer Rate Decomposition (W / meter of conductor)
          </h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono">
            <div className="p-2.5 rounded-xl bg-slate-950/60 border border-slate-800">
              <span className="text-slate-400 block text-[10px]">Convective Cooling (qc)</span>
              <span className="text-cyan-300 font-bold text-sm">+{dlrData.heat_loss_convection_w_per_m} W/m</span>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-950/60 border border-slate-800">
              <span className="text-slate-400 block text-[10px]">Radiative Cooling (qr)</span>
              <span className="text-blue-300 font-bold text-sm">+{dlrData.heat_loss_radiation_w_per_m} W/m</span>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-950/60 border border-slate-800">
              <span className="text-slate-400 block text-[10px]">Solar Irradiance Heat (qs)</span>
              <span className="text-orange-300 font-bold text-sm">-{dlrData.heat_gain_solar_w_per_m} W/m</span>
            </div>
            <div className="p-2.5 rounded-xl bg-slate-950/60 border border-slate-800">
              <span className="text-slate-400 block text-[10px]">Ohmic Joule Heat (I²R)</span>
              <span className="text-amber-300 font-bold text-sm">-{dlrData.heat_gain_joule_w_per_m} W/m</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
