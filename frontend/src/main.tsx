import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';
import {
  clearStaleDeployMarker,
  isStaleChunkError,
  recoverFromStaleDeploy,
} from './utils/staleDeploy';
// katex.min.css is imported by MathView instead, so its ~25 KB of rules and
// font @font-face declarations stay out of the render-blocking entry CSS.


/**
 * Self-heal a tab that was open across a deployment.
 *
 * Two failure shapes have to be covered. A stylesheet or eagerly-loaded script
 * that 404s raises an `error` event on its element - but a `React.lazy()` chunk
 * is fetched with `import()` and fails as a *rejected promise*, raising no
 * element event at all. Only the first was handled, which is why lazily-loaded
 * panels reached the error boundary and were reported as bad data.
 */
window.addEventListener('error', (event) => {
  const target = event.target as HTMLElement | null;
  if (!(target instanceof HTMLScriptElement || target instanceof HTMLLinkElement)) return;
  recoverFromStaleDeploy();
}, true);

window.addEventListener('unhandledrejection', (event) => {
  if (isStaleChunkError(event.reason)) recoverFromStaleDeploy();
});

// The fresh document has already loaded its current entry bundle, so leave the
// visible URL clean without issuing a second request.
clearStaleDeployMarker();

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
