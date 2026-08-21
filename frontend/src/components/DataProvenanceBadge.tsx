import { Satellite, Database, AlertTriangle } from 'lucide-react';
import type { DataSourceTag } from '../types';

/**
 * States plainly where the numbers on screen came from.
 *
 * This exists because the system previously reported `mock_mode: false` while
 * serving bundled fixture data — the health flag described configuration, not
 * what the last response actually contained. A viewer could not tell the
 * difference. Now every analytics payload carries `data_source` and the UI
 * shows it.
 */
export function DataProvenanceBadge({
  source,
  analysisDate,
  className = '',
}: {
  source?: DataSourceTag;
  analysisDate?: string;
  className?: string;
}) {
  const config = {
    fortyguard_live: {
      Icon: Satellite,
      label: 'Live FortyGuard API',
      detail: '2m temperature, persistence and exceedance measured',
      cls: 'border-emerald-500/40 bg-emerald-500/10 text-emerald-300',
      dot: 'bg-emerald-400',
    },
    fortyguard_live_partial: {
      Icon: AlertTriangle,
      label: 'Live (partial)',
      detail: 'Temperature live; humidity/solar from benchmark',
      cls: 'border-amber-500/40 bg-amber-500/10 text-amber-300',
      dot: 'bg-amber-400',
    },
    phoenix_fixture: {
      Icon: Database,
      label: 'Cached benchmark replay',
      detail: 'Captured FortyGuard response, replayed offline',
      cls: 'border-sky-500/40 bg-sky-500/10 text-sky-300',
      dot: 'bg-sky-400',
    },
  }[source ?? 'phoenix_fixture'];

  const { Icon, label, detail, cls, dot } = config;

  return (
    <div
      title={detail}
      className={`inline-flex items-center gap-2 rounded-full border px-3 py-1 text-[11px] font-medium ${cls} ${className}`}
    >
      <span className={`h-1.5 w-1.5 rounded-full ${dot} ${source === 'fortyguard_live' ? 'animate-pulse' : ''}`} />
      <Icon className="h-3 w-3" />
      <span>{label}</span>
      {analysisDate && <span className="opacity-60">· {analysisDate}</span>}
    </div>
  );
}

export default DataProvenanceBadge;
