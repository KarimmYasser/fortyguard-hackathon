import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';
import { isStaleChunkError, recoverFromStaleDeploy } from '../utils/staleDeploy';

/**
 * Contains a render failure to the tab that caused it.
 *
 * There are ~49 `.toFixed()` call sites across the dashboard, each of which
 * assumes its field is present. A payload missing one number - a response
 * cached under an older schema, a partial live scan, a field rename that
 * outran a deployment - therefore threw during render and unmounted the whole
 * React tree, leaving a blank page with only a console trace.
 *
 * A boundary is the right level of defence here: the alternative is guarding
 * every individual call site, which is easy to regress and hides the fault.
 * This keeps the rest of the dashboard usable and states plainly which panel
 * failed and why.
 */
interface Props {
  children: React.ReactNode;
  /** Human-readable panel name, shown in the fallback. */
  name: string;
}

interface State {
  error: Error | null;
}

export class TabErrorBoundary extends React.Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error(`[TabErrorBoundary] "${this.props.name}" failed to render`, error, info);
    // A vanished chunk is a deployment fact, not a fault in this panel. Clearing
    // the error would only re-request the same dead URL, so recover instead.
    if (isStaleChunkError(error)) recoverFromStaleDeploy();
  }

  /** Reset when the user switches to a different panel. */
  componentDidUpdate(prev: Props) {
    if (prev.name !== this.props.name && this.state.error) {
      this.setState({ error: null });
    }
  }

  render() {
    const { error } = this.state;
    if (!error) return this.props.children;

    const stale = isStaleChunkError(error);

    return (
      <div className="rounded-2xl border border-amber-800/60 bg-amber-950/20 p-6">
        <div className="flex items-center gap-2 text-amber-300 font-bold font-heading uppercase text-sm tracking-wide">
          <AlertTriangle className="h-4 w-4" />
          {stale
            ? `${this.props.name} is from an older version of this page`
            : `${this.props.name} could not render`}
        </div>
        <p className="mt-2 text-xs text-slate-400 font-mono">
          {stale
            ? 'This page was loaded before the latest deploy, so the file for this panel no longer exists at that address. Reloading fetches the current version.'
            : 'This panel hit a data shape it did not expect. The rest of the dashboard is unaffected.'}
        </p>
        <pre className="mt-3 text-[11px] text-amber-200/80 font-mono whitespace-pre-wrap break-words">
          {error.message}
        </pre>
        <button
          onClick={() => (stale ? recoverFromStaleDeploy(true) : this.setState({ error: null }))}
          className="mt-4 px-3 py-1.5 rounded-lg text-xs font-bold font-mono bg-amber-600/90 text-white hover:bg-amber-500 transition-colors inline-flex items-center gap-1.5"
        >
          {stale ? <><RefreshCw className="h-3 w-3" /> Reload page</> : 'Retry'}
        </button>
      </div>
    );
  }
}
