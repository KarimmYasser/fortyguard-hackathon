import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';
// katex.min.css is imported by MathView instead, so its ~25 KB of rules and
// font @font-face declarations stay out of the render-blocking entry CSS.


/**
 * Self-heal a tab that was open across a deployment.
 *
 * Asset filenames are content-hashed and each Vercel deployment only serves its
 * own hashes, so an already-loaded page holding the previous index.html will
 * 404 on every chunk it tries to fetch and render nothing. Reload once (guarded
 * by sessionStorage so a genuinely missing asset can't cause a reload loop).
 */
const RELOAD_FLAG = 'tsg:chunk-reload';
window.addEventListener('error', (event) => {
  const target = event.target as HTMLElement | null;
  const isAssetFailure =
    target instanceof HTMLScriptElement || target instanceof HTMLLinkElement;
  if (!isAssetFailure) return;
  if (sessionStorage.getItem(RELOAD_FLAG)) return;
  sessionStorage.setItem(RELOAD_FLAG, '1');
  window.location.reload();
}, true);
window.addEventListener('load', () => sessionStorage.removeItem(RELOAD_FLAG));

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
