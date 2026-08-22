import React, { useState } from 'react';
import { MapPin, Navigation, Info, ShieldCheck, Flame, Building2, Hospital } from 'lucide-react';
import { HeatmapCollection } from '../types';

interface MicroclimateMapProps {
  heatmapData: HeatmapCollection;
  currentAmbient2m: number;
  coolestTile2m: number;
  deltaAmbient: number;
}

export const MicroclimateMap: React.FC<MicroclimateMapProps> = ({
  heatmapData,
  currentAmbient2m,
  coolestTile2m,
  deltaAmbient,
}) => {
  const [selectedTile, setSelectedTile] = useState<string>('tile_phx_sub_04');

  const tiles = heatmapData?.features || [];

  return (
    <div className="glass-panel rounded-2xl p-4 border border-slate-800 flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-2.5 mb-3">
        <div className="flex items-center gap-2">
          <Navigation className="h-4 w-4 text-amber-400" />
          <h3 className="text-xs font-bold text-white uppercase tracking-wider font-heading">
            Hyperlocal 2m Microclimate GIS Layer
          </h3>
        </div>
        {/* Coolest-tile delta badge */}
        <div className="flex items-center gap-1.5 text-[11px] font-mono">
          <span className="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-400">
            Coolest tile: {coolestTile2m.toFixed(1)}°C
          </span>
          <span className="px-2 py-0.5 rounded bg-rose-950/80 border border-rose-800/80 text-rose-300 font-bold flex items-center gap-1">
            <Flame className="h-3 w-3" /> Parcel 2m: {currentAmbient2m.toFixed(1)}°C (+{deltaAmbient.toFixed(1)}°C)
          </span>
        </div>
      </div>

      {/* Geospatial Canvas Mock Grid Viewer */}
      <div className="relative flex-1 min-h-[260px] bg-slate-950 rounded-xl border border-slate-800/90 overflow-hidden flex items-center justify-center p-3">
        {/* Background Grid Lines & Street Geometry */}
        <div className="absolute inset-0 opacity-20 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>

        {/* Interactive Street Corridor & Substation Parcels */}
        <div className="relative z-10 w-full h-full grid grid-cols-3 gap-3">
          {tiles.map((tile) => {
            const isSubstation = tile.properties.tile_id === 'tile_phx_sub_04';
            const isCanyon = tile.properties.tile_id === 'tile_phx_canyon_01';
            const isHospital = tile.properties.tile_id === 'tile_phx_med_center';
            const isSelected = selectedTile === tile.properties.tile_id;

            return (
              <button
                key={tile.properties.tile_id}
                onClick={() => setSelectedTile(tile.properties.tile_id)}
                className={`relative rounded-xl p-3 text-left transition-all flex flex-col justify-between border ${
                  isSelected
                    ? 'ring-2 ring-amber-400 border-amber-400/80 shadow-lg shadow-amber-500/20'
                    : 'border-slate-800/80 hover:border-slate-700'
                } ${
                  isSubstation
                    ? 'bg-gradient-to-br from-rose-950/80 via-rose-900/40 to-slate-950'
                    : isCanyon
                    ? 'bg-gradient-to-br from-orange-950/80 via-orange-900/30 to-slate-950'
                    : 'bg-gradient-to-br from-blue-950/80 via-blue-900/30 to-slate-950'
                }`}
              >
                {/* Top Badge */}
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono font-bold px-1.5 py-0.5 rounded bg-slate-950/80 text-slate-300 border border-slate-800">
                    {tile.properties.land_cover.replace('_', ' ')}
                  </span>
                  {isSubstation && (
                    <span className="flex h-2 w-2 relative">
                      <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                      <span className="relative inline-flex rounded-full h-2 w-2 bg-rose-500"></span>
                    </span>
                  )}
                </div>

                {/* Center Icon & Label */}
                <div className="my-2">
                  <div className="flex items-center gap-1.5 text-xs font-bold text-white">
                    {isSubstation && <ShieldCheck className="h-4 w-4 text-amber-400" />}
                    {isCanyon && <Building2 className="h-4 w-4 text-orange-400" />}
                    {isHospital && <Hospital className="h-4 w-4 text-cyan-400" />}
                    <span>{tile.properties.asset_present}</span>
                  </div>
                  <div className="text-[10px] text-slate-400 font-mono mt-0.5">
                    Albedo: {tile.properties.albedo} · P40: {tile.properties.persistence_hours_p40}h
                  </div>
                </div>

                {/* Bottom Temperature Reading */}
                <div className="flex items-baseline justify-between border-t border-slate-800/60 pt-1.5">
                  <span className="text-[10px] text-slate-400">2m Ambient:</span>
                  <span className="text-sm font-black font-mono text-rose-300">
                    {tile.properties.ambient_temp_c.toFixed(1)}°C
                  </span>
                </div>
              </button>
            );
          })}
        </div>

        {/* Reference-tile marker annotation */}
        <div className="absolute bottom-2 left-2 z-20 px-2 py-1 rounded bg-slate-900/90 border border-slate-800 text-[10px] font-mono text-slate-400 flex items-center gap-1.5 backdrop-blur-md">
          <MapPin className="h-3 w-3 text-slate-500" />
          Phoenix Sky Harbor Station: 7.2 mi East (Shaded Airfield)
        </div>
      </div>

      {/* Footer Info */}
      <div className="text-[11px] text-slate-400 mt-2.5 flex items-center gap-1.5">
        <Info className="h-3.5 w-3.5 text-amber-400 flex-shrink-0" />
        <span>
          FortyGuard’s 2m layer incorporates surface albedo, canyon wind-stagnation, and asphalt radiation.
        </span>
      </div>
    </div>
  );
};
