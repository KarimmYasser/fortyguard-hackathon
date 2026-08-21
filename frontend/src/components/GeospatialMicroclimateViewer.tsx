import React, { useState } from 'react';
import {
  MapPin,
  Layers,
  Flame,
  ShieldCheck,
  Building2,
  Hospital,
  Sun,
  Wind,
  Info,
  ExternalLink,
  Sliders,
  Eye,
  Radio,
} from 'lucide-react';
import { HeatmapCollection, HeatmapFeature } from '../types';

interface GeospatialMicroclimateViewerProps {
  heatmapData: HeatmapCollection;
  currentAmbient2m: number;
  airportAmbient: number;
  deltaAmbient: number;
  onOpenLiveScan?: () => void;
}

export const GeospatialMicroclimateViewer: React.FC<GeospatialMicroclimateViewerProps> = ({
  heatmapData,
  currentAmbient2m,
  airportAmbient,
  deltaAmbient,
  onOpenLiveScan,
}) => {
  const [selectedTileId, setSelectedTileId] = useState<string>('tile_phx_sub_04');
  const [activeLayer, setActiveLayer] = useState<'2m_ambient' | 'persistence' | 'albedo'>('2m_ambient');

  const tiles = heatmapData?.features || [];
  const selectedTile = tiles.find((t) => t.properties.tile_id === selectedTileId) || tiles[0];

  return (
    <div className="space-y-6">
      {/* Top GIS Header & Layer Controls */}
      <div id="tour-gis-header" className="glass-panel rounded-3xl p-6 border border-slate-800/90 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20">
              <Layers className="h-5 w-5" />
            </div>
            <div>
              <h2 className="text-base font-extrabold text-white uppercase tracking-wide font-heading">
                Hyperlocal 2-Meter Microclimate GIS Engine
              </h2>
              <p className="text-xs text-slate-400 font-mono">
                FortyGuard tOS 2m Convective & Radiative Layer · 60m Spatial Granularity · Phoenix Metro Bounding Box
              </p>
            </div>
          </div>
        </div>

        {/* GIS Controls & Live Scan Trigger */}
        <div className="flex flex-wrap items-center gap-3">
          {onOpenLiveScan && (
            <button
              id="tour-gis-scan-btn"
              onClick={onOpenLiveScan}
              className="px-3.5 py-1.5 rounded-2xl bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-400 hover:to-orange-400 text-slate-950 font-bold text-xs shadow-lg shadow-amber-500/20 flex items-center gap-1.5 transition-all font-mono"
              title="Trigger Live Cloud API Scan"
            >
              <Radio className="h-3.5 w-3.5 animate-pulse" />
              <span>Live Cloud Scan</span>
            </button>
          )}

          {/* GIS Layer Switcher Pills */}
          <div className="flex items-center gap-2 bg-slate-900 border border-slate-800 p-1 rounded-2xl text-xs font-mono">
          <button
            onClick={() => setActiveLayer('2m_ambient')}
            className={`px-3 py-1.5 rounded-xl font-bold transition-all flex items-center gap-1.5 ${
              activeLayer === '2m_ambient'
                ? 'bg-rose-500 text-white shadow-md shadow-rose-500/30'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Flame className="h-3.5 w-3.5" /> 2m Ambient Heat
          </button>
          <button
            onClick={() => setActiveLayer('persistence')}
            className={`px-3 py-1.5 rounded-xl font-bold transition-all flex items-center gap-1.5 ${
              activeLayer === 'persistence'
                ? 'bg-amber-500 text-slate-950 shadow-md shadow-amber-500/30'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Sun className="h-3.5 w-3.5" /> Persistence (P40)
          </button>
          <button
            onClick={() => setActiveLayer('albedo')}
            className={`px-3 py-1.5 rounded-xl font-bold transition-all flex items-center gap-1.5 ${
              activeLayer === 'albedo'
                ? 'bg-cyan-500 text-slate-950 shadow-md shadow-cyan-500/30'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Eye className="h-3.5 w-3.5" /> Land Cover & Albedo
          </button>
        </div>
      </div>
    </div>

      {/* Main Map & Parcel Inspector Grid */}
      <div id="tour-gis-map" className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: High-Tech Interactive GIS Canvas */}
        <div className="lg:col-span-8 glass-panel rounded-3xl p-6 border border-slate-800/90 shadow-2xl relative min-h-[480px] flex flex-col justify-between overflow-hidden">
          {/* Top Map Status Overlay */}
          <div className="flex items-center justify-between z-10">
            <div className="flex items-center gap-2 bg-slate-950/80 backdrop-blur-md px-3 py-1.5 rounded-xl border border-slate-800 text-xs font-mono">
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-ping"></span>
              <span className="text-slate-300 font-bold">Phoenix Central Substation TX-04</span>
              <span className="text-slate-500">(33.4484° N, 112.0740° W)</span>
            </div>

            {/* Natural-terrain reference delta badge */}
            <div className="bg-rose-950/90 backdrop-blur-md px-3 py-1.5 rounded-xl border border-rose-800/80 text-xs font-mono text-rose-300 font-bold flex items-center gap-2 shadow-lg">
              <Flame className="h-4 w-4 text-rose-400" />
              <span>Parcel: {currentAmbient2m.toFixed(1)}°C</span>
              <span className="text-slate-400 text-[10px]">(Coolest tile: {airportAmbient.toFixed(1)}°C · +{deltaAmbient.toFixed(1)}°C)</span>
            </div>
          </div>

          {/* Interactive Map Grid Center */}
          <div className="relative my-6 flex-1 min-h-[300px] bg-[#050812] rounded-2xl border border-slate-800/90 p-6 flex flex-col justify-center overflow-hidden">
            {/* Grid Coordinates & Radial Atmosphere */}
            <div className="absolute inset-0 bg-[radial-gradient(#f59e0b10_1px,transparent_1px)] [background-size:20px_20px] opacity-40"></div>
            <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent to-transparent"></div>

            {/* Parcel Polygons */}
            <div className="relative z-10 grid grid-cols-1 sm:grid-cols-3 gap-4">
              {tiles.map((tile) => {
                const isSelected = tile.properties.tile_id === selectedTileId;
                const isSubstation = tile.properties.tile_id === 'tile_phx_sub_04';
                const isCanyon = tile.properties.tile_id === 'tile_phx_canyon_01';

                return (
                  <div
                    key={tile.properties.tile_id}
                    onClick={() => setSelectedTileId(tile.properties.tile_id)}
                    className={`cursor-pointer rounded-2xl p-4 border transition-all duration-300 relative ${
                      isSelected
                        ? 'ring-2 ring-amber-400 border-amber-400 bg-gradient-to-b from-amber-950/40 via-slate-900 to-slate-950 shadow-2xl shadow-amber-500/25'
                        : 'border-slate-800 bg-slate-900/60 hover:border-slate-700 hover:bg-slate-900/90'
                    }`}
                  >
                    {/* Header */}
                    <div className="flex items-center justify-between text-[11px] font-mono">
                      <span className="px-2 py-0.5 rounded bg-slate-950 text-slate-300 font-bold border border-slate-800">
                        {tile.properties.tile_id}
                      </span>
                      {isSubstation && (
                        <span className="flex h-2.5 w-2.5 relative">
                          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                          <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-rose-500"></span>
                        </span>
                      )}
                    </div>

                    {/* Content */}
                    <div className="my-3">
                      <div className="text-sm font-bold text-white flex items-center gap-1.5">
                        {isSubstation && <ShieldCheck className="h-4 w-4 text-amber-400" />}
                        {isCanyon && <Building2 className="h-4 w-4 text-orange-400" />}
                        {!isSubstation && !isCanyon && <Hospital className="h-4 w-4 text-cyan-400" />}
                        {tile.properties.asset_present}
                      </div>
                      <div className="text-xs text-slate-400 font-mono mt-1">
                        Land: {tile.properties.land_cover.replace('_', ' ')}
                      </div>
                    </div>

                    {/* Dynamic Metric Display based on Active Layer */}
                    <div className="pt-2 border-t border-slate-800/80 flex items-baseline justify-between font-mono">
                      <span className="text-[10px] text-slate-500 uppercase">
                        {activeLayer === '2m_ambient' ? '2m Ambient' : activeLayer === 'persistence' ? 'P40 Duration' : 'Albedo'}
                      </span>
                      <span className="text-base font-black text-rose-300">
                        {activeLayer === '2m_ambient'
                          ? `${tile.properties.ambient_temp_c.toFixed(1)}°C`
                          : activeLayer === 'persistence'
                          ? `${tile.properties.persistence_hours_p40}h`
                          : tile.properties.albedo}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Natural-terrain reference annotation box */}
            <div className="mt-6 z-10 p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-xs font-mono flex items-center justify-between text-slate-400">
              <span className="flex items-center gap-1.5">
                <MapPin className="h-4 w-4 text-slate-500" />
                South Mountain natural desert (9.5 mi S): <strong>41.6°C</strong>
              </span>
              <span className="text-rose-400 font-bold">
                Measured land-cover delta: +1.1°C
              </span>
            </div>
          </div>

          {/* Bottom GIS Context Bar */}
          <div className="flex items-center justify-between text-xs text-slate-400 font-mono z-10 pt-2 border-t border-slate-800/80">
            <span>Projection: WGS84 (EPSG:4326)</span>
            <span className="text-amber-400 font-bold">Overpass QL Bounding Box: 33.20,-112.40,33.90,-111.80</span>
          </div>
        </div>

        {/* Right: Selected Parcel Deep-Dive Inspector */}
        <div className="lg:col-span-4 glass-panel rounded-3xl p-6 border border-slate-800/90 shadow-2xl flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
              <div>
                <h3 className="text-xs font-extrabold text-white uppercase tracking-wider font-heading">
                  Parcel Physics Inspector
                </h3>
                <p className="text-[11px] text-slate-400 font-mono">
                  Asset: {selectedTile.properties.asset_present}
                </p>
              </div>
              <span className="px-2.5 py-1 rounded-full text-xs font-bold font-mono bg-amber-500/15 text-amber-300 border border-amber-500/30">
                ACTIVE
              </span>
            </div>

            {/* Metrics Breakdown */}
            <div className="space-y-3 font-mono text-xs">
              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800/80 flex items-center justify-between">
                <span className="text-slate-400">2-Meter Ambient Air:</span>
                <span className="text-base font-black text-rose-400">
                  {selectedTile.properties.ambient_temp_c.toFixed(1)}°C ({selectedTile.properties.ambient_temp_f.toFixed(1)}°F)
                </span>
              </div>

              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800/80 flex items-center justify-between">
                <span className="text-slate-400">Continuous Persistence (P40):</span>
                <span className="text-amber-400 font-bold">{selectedTile.properties.persistence_hours_p40} Hours</span>
              </div>

              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800/80 flex items-center justify-between">
                <span className="text-slate-400">Degree-Hours Exceedance:</span>
                <span className="text-slate-200 font-bold">{selectedTile.properties.exceedance_degree_hours}°C·h</span>
              </div>

              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800/80 flex items-center justify-between">
                <span className="text-slate-400">Surface Albedo & Imperviousness:</span>
                <span className="text-cyan-400 font-bold">{selectedTile.properties.albedo} (High Heat Retention)</span>
              </div>

              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800/80 flex items-center justify-between">
                <span className="text-slate-400">Morphology Classification:</span>
                <span className="text-slate-200 font-bold">{selectedTile.properties.land_cover}</span>
              </div>
            </div>
          </div>

          <div className="mt-4 p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 text-xs text-slate-300 flex items-start gap-2">
            <Info className="h-4 w-4 text-amber-400 flex-shrink-0 mt-0.5" />
            <p className="leading-relaxed">
              Against natural desert terrain the measured land-cover delta is <strong>+1.1°C</strong> — modest on its own. What damages the asset is that FortyGuard’s 2-meter model holds it above 40°C for <strong>12 unbroken hours</strong>. Aging integrates over time, so it is the soak, not the peak, that drives insulation loss. (We also probed Sky Harbor: it reads <em>warmer</em> than downtown — an airport ringed by runways is itself a heat island, not a cool reference.)
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
