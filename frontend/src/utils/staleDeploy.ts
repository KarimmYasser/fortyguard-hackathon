/**
 * Recovery from a tab left open across a deployment.
 *
 * Asset filenames are content-hashed and each Vercel deployment serves only its
 * own hashes, so a page still holding the previous index.html will 404 on any
 * chunk it lazily imports. That is not a fault in the panel being imported -
 * the code it is asking for no longer exists at that URL - and it cannot be
 * recovered by retrying the same URL. Only re-fetching index.html fixes it.
 */

/** Matches the dynamic-import failures browsers emit for a vanished chunk. */
export function isStaleChunkError(error: unknown): boolean {
  const msg = error instanceof Error ? `${error.name}: ${error.message}` : String(error ?? '');
  return (
    /Failed to fetch dynamically imported module/i.test(msg) ||
    /error loading dynamically imported module/i.test(msg) ||
    /Importing a module script failed/i.test(msg) ||
    /ChunkLoadError/i.test(msg) ||
    /Loading chunk \S+ failed/i.test(msg)
  );
}

// Rate-limit rather than latch. The previous guard cleared its sessionStorage
// flag on the `load` event - which also fires on the reloaded page - so a chunk
// that was genuinely gone rather than merely stale would reload forever.
const STAMP_KEY = 'tsg:stale-deploy-reload-at';
const RECOVERY_PARAM = '__tsg_refresh';
const COOLDOWN_MS = 30_000;

/**
 * Re-fetch index.html once to pick up the current asset manifest.
 * Returns false when a reload was suppressed by the cooldown, so callers can
 * surface the error instead of appearing to hang.
 */
export function recoverFromStaleDeploy(force = false): boolean {
  const now = Date.now();
  try {
    const last = Number(sessionStorage.getItem(STAMP_KEY) || 0);
    if (!force && now - last < COOLDOWN_MS) return false;
    sessionStorage.setItem(STAMP_KEY, String(now));
  } catch {
    // Private-mode sessionStorage can throw on write. One navigation is still
    // better than a permanently broken panel; the cooldown is the only loss.
  }

  // `location.reload()` can revalidate `/` to 304 and retain the stale document.
  // A unique document URL forces a 200 with the current index and chunk map.
  const url = new URL(window.location.href);
  url.searchParams.set(RECOVERY_PARAM, String(now));
  window.location.replace(url.toString());
  return true;
}

/** Remove the cache-busting marker without causing another navigation. */
export function clearStaleDeployMarker(): void {
  const url = new URL(window.location.href);
  if (!url.searchParams.has(RECOVERY_PARAM)) return;
  url.searchParams.delete(RECOVERY_PARAM);
  window.history.replaceState(window.history.state, '', `${url.pathname}${url.search}${url.hash}`);
}
