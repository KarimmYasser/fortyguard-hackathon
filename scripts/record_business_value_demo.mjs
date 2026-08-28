import puppeteer from 'puppeteer';
import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs';
import http from 'http';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');

const OUTPUT_VIDEO = path.resolve(projectRoot, 'videos/thermal-sentinel-pitch/renders/business_value_demo.mp4');
const RAW_VIDEO = path.resolve(projectRoot, 'videos/thermal-sentinel-pitch/renders/business_value_demo_raw.mp4');
const PUBLIC_VIDEO = path.resolve(projectRoot, 'frontend/public/videos/business_value_demo.mp4');
const BGM_AUDIO = path.resolve(projectRoot, 'videos/thermal-sentinel-pitch/assets/audio/bgm_cyber_ambient.mp3');
const DIST_DIR = path.resolve(projectRoot, 'frontend/dist');

// Resolve FFmpeg binary
const FFMPEG = process.env.FFMPEG_PATH || (fs.existsSync('/opt/homebrew/bin/ffmpeg') ? '/opt/homebrew/bin/ffmpeg' : 'ffmpeg');

// Ensure output dirs exist
fs.mkdirSync(path.dirname(OUTPUT_VIDEO), { recursive: true });
fs.mkdirSync(path.dirname(RAW_VIDEO), { recursive: true });
fs.mkdirSync(path.dirname(PUBLIC_VIDEO), { recursive: true });

// Optional local static server if TARGET_URL is not supplied or unreachable
function startLocalStaticServer(port = 4173) {
  const mimeTypes = {
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.svg': 'image/svg+xml',
    '.woff2': 'font/woff2',
    '.woff': 'font/woff',
    '.ttf': 'font/ttf',
    '.mp4': 'video/mp4',
    '.mp3': 'audio/mpeg',
  };

  const server = http.createServer((req, res) => {
    // Enable CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
      res.writeHead(200);
      res.end();
      return;
    }

    let reqPath = req.url.split('?')[0];
    if (reqPath === '/' || reqPath === '') {
      reqPath = '/index.html';
    }

    const filePath = path.join(DIST_DIR, reqPath);
    const ext = path.extname(filePath).toLowerCase();

    if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
      const contentType = mimeTypes[ext] || 'application/octet-stream';
      res.writeHead(200, { 'Content-Type': contentType });
      fs.createReadStream(filePath).pipe(res);
    } else {
      // SPA Fallback
      const indexPath = path.join(DIST_DIR, 'index.html');
      if (fs.existsSync(indexPath)) {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        fs.createReadStream(indexPath).pipe(res);
      } else {
        res.writeHead(404);
        res.end('Not found');
      }
    }
  });

  return new Promise((resolve) => {
    server.listen(port, '127.0.0.1', () => {
      console.log(`📡 Local static preview server running on http://127.0.0.1:${port}`);
      resolve(server);
    });
  });
}

async function recordBusinessValueDemo() {
  console.log('=================================================================');
  console.log('⚡ THERMAL SENTINEL GRID — BUSINESS VALUE VIDEO RECORDING ENGINE');
  console.log('🎯 Curated for Hackathon Judges: Problem, Pain & Commercial Impact');
  console.log('=================================================================\n');

  let localServer = null;
  let targetUrl = process.env.TARGET_URL;

  if (!targetUrl) {
    // If no target URL specified, check if dist exists and start local server
    if (fs.existsSync(DIST_DIR)) {
      localServer = await startLocalStaticServer(4173);
      targetUrl = 'http://127.0.0.1:4173';
    } else {
      targetUrl = 'https://www.thermal-sentinel-grid.live';
    }
  }

  console.log(`🚀 Launching Chromium (1920x1080 Full HD, 60fps capable)...`);
  const browser = await puppeteer.launch({
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--window-size=1920,1080',
      '--disable-gpu-sandbox',
      '--disable-web-security',
      '--enable-features=NetworkService,NetworkServiceInProcess',
    ],
    defaultViewport: {
      width: 1920,
      height: 1080,
      deviceScaleFactor: 1,
    },
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });

  console.log(`🌐 Opening Application at ${targetUrl} ...`);
  try {
    await page.goto(targetUrl, { waitUntil: 'networkidle0', timeout: 35000 });
  } catch (err) {
    console.warn(`Initial networkidle0 timed out, falling back to domcontentloaded: ${err.message}`);
    await page.goto(targetUrl, { waitUntil: 'domcontentloaded', timeout: 35000 });
  }

  await new Promise((r) => setTimeout(r, 2000));

  // Inject High-Visibility Virtual Cursor & Action Effects
  await page.evaluate(() => {
    const style = document.createElement('style');
    style.innerHTML = `
      #ai-virtual-cursor {
        position: fixed;
        width: 36px;
        height: 36px;
        pointer-events: none;
        z-index: 999999;
        transition: transform 0.04s ease-out, opacity 0.15s ease;
        transform: translate(-6px, -6px);
      }
      .cursor-dot {
        width: 18px;
        height: 18px;
        background: #38bdf8;
        border: 3px solid #ffffff;
        border-radius: 50%;
        box-shadow: 0 0 16px #38bdf8, 0 0 28px rgba(56, 189, 248, 0.95);
      }
      .cursor-ring {
        position: absolute;
        top: -7px;
        left: -7px;
        width: 32px;
        height: 32px;
        border: 2.5px solid rgba(56, 189, 248, 0.8);
        border-radius: 50%;
        animation: pulseRing 1.3s infinite ease-in-out;
      }
      .click-burst {
        position: fixed;
        width: 52px;
        height: 52px;
        border-radius: 50%;
        border: 3.5px solid #f59e0b;
        pointer-events: none;
        z-index: 999998;
        animation: burstAnim 0.45s cubic-bezier(0, 0, 0.2, 1) forwards;
        transform: translate(-50%, -50%);
      }
      @keyframes pulseRing {
        0% { transform: scale(0.9); opacity: 0.9; }
        50% { transform: scale(1.35); opacity: 0.25; }
        100% { transform: scale(0.9); opacity: 0.9; }
      }
      @keyframes burstAnim {
        0% { transform: translate(-50%, -50%) scale(0.2); opacity: 1; }
        100% { transform: translate(-50%, -50%) scale(2.2); opacity: 0; }
      }
    `;
    document.head.appendChild(style);

    const cursor = document.createElement('div');
    cursor.id = 'ai-virtual-cursor';
    cursor.innerHTML = '<div class="cursor-ring"></div><div class="cursor-dot"></div>';
    document.body.appendChild(cursor);

    window.updateVirtualCursor = (x, y) => {
      cursor.style.left = `${x}px`;
      cursor.style.top = `${y}px`;
    };

    window.triggerClickEffect = (x, y) => {
      const burst = document.createElement('div');
      burst.className = 'click-burst';
      burst.style.left = `${x}px`;
      burst.style.top = `${y}px`;
      document.body.appendChild(burst);
      setTimeout(() => burst.remove(), 450);
    };
  });

  // Start FFmpeg process for CDP Screencast
  console.log('🎥 Initializing CDP Screencast & FFmpeg H.264 Encoder...');
  const ffmpeg = spawn(FFMPEG, [
    '-y',
    '-f', 'image2pipe',
    '-vcodec', 'mjpeg',
    '-r', '30',
    '-i', '-',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'veryfast',
    '-crf', '17',
    RAW_VIDEO,
  ]);

  ffmpeg.stderr.on('data', (data) => {
    // suppress verbose output
  });

  const client = await page.target().createCDPSession();
  await client.send('Page.startScreencast', {
    format: 'jpeg',
    quality: 96,
    maxWidth: 1920,
    maxHeight: 1080,
    everyNthFrame: 1,
  });

  let isStreaming = true;
  client.on('Page.screencastFrame', async ({ data, sessionId }) => {
    if (!isStreaming) return;
    try {
      const buffer = Buffer.from(data, 'base64');
      ffmpeg.stdin.write(buffer);
      await client.send('Page.screencastFrameAck', { sessionId });
    } catch (e) {}
  });

  // Motion helpers for natural, human-like, unhurried choreography
  let curX = 960, curY = 540;
  async function smoothMouseMove(targetX, targetY, durationMs = 600) {
    const steps = Math.max(12, Math.round(durationMs / 16));
    const startX = curX, startY = curY;
    for (let i = 1; i <= steps; i++) {
      const t = i / steps;
      // Smooth cubic ease in-out
      const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
      const x = Math.round(startX + (targetX - startX) * ease);
      const y = Math.round(startY + (targetY - startY) * ease);
      await page.evaluate((px, py) => window.updateVirtualCursor(px, py), x, y);
      await new Promise((r) => setTimeout(r, 16));
    }
    curX = targetX;
    curY = targetY;
  }

  async function clickElement(selector, waitAfter = 800) {
    try {
      const rect = await page.evaluate((sel) => {
        const el = document.querySelector(sel);
        if (!el) return null;
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        const r = el.getBoundingClientRect();
        return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
      }, selector);

      if (rect) {
        await smoothMouseMove(rect.x, rect.y, 450);
        await page.evaluate((x, y) => window.triggerClickEffect(x, y), rect.x, rect.y);
        await page.click(selector);
      }
    } catch (err) {}
    await new Promise((r) => setTimeout(r, waitAfter));
  }

  async function clickTabByText(tabLabel, waitAfter = 1000) {
    const rect = await page.evaluate((text) => {
      const btns = Array.from(document.querySelectorAll('button'));
      const target = btns.find((b) => b.textContent?.trim() === text);
      if (!target) return null;
      target.scrollIntoView({ block: 'center' });
      const r = target.getBoundingClientRect();
      return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
    }, tabLabel);

    if (!rect) {
      console.warn(`Tab not found by exact text: "${tabLabel}". Searching substring...`);
      const fallbackRect = await page.evaluate((text) => {
        const btns = Array.from(document.querySelectorAll('button'));
        const target = btns.find((b) => b.textContent?.includes(text));
        if (!target) return null;
        const r = target.getBoundingClientRect();
        return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
      }, tabLabel);

      if (fallbackRect) {
        await smoothMouseMove(fallbackRect.x, fallbackRect.y, 450);
        await page.evaluate((x, y) => window.triggerClickEffect(x, y), fallbackRect.x, fallbackRect.y);
        await page.evaluate((text) => {
          const target = Array.from(document.querySelectorAll('button')).find((b) => b.textContent?.includes(text));
          if (target) target.click();
        }, tabLabel);
        await new Promise((r) => setTimeout(r, waitAfter));
        return;
      }
      throw new Error(`Control not found: "${tabLabel}"`);
    }

    await smoothMouseMove(rect.x, rect.y, 450);
    await page.evaluate((x, y) => window.triggerClickEffect(x, y), rect.x, rect.y);
    await page.evaluate((text) => {
      const target = Array.from(document.querySelectorAll('button'))
        .find((b) => b.textContent?.trim() === text);
      if (target) target.click();
    }, tabLabel);
    await new Promise((r) => setTimeout(r, waitAfter));
  }

  async function smoothScroll(deltaY, durationMs = 800) {
    const steps = Math.max(10, Math.round(durationMs / 20));
    for (let i = 0; i < steps; i++) {
      await page.evaluate((dy) => window.scrollBy(0, dy), deltaY / steps);
      await new Promise((r) => setTimeout(r, 20));
    }
  }

  console.log('🎬 Commencing Unhurried, Story-Driven Business Value Walkthrough...\n');

  // =========================================================================
  // ACT 1: THE HIGH-STAKES PROBLEM & FORTYGUARD LIVE CLOUD INGESTION (~0s - 35s)
  // Guidance: Ahmed (Session 5), Tarek (Session 6), Constantine (Session 14)
  // =========================================================================
  console.log('📍 [ACT 1/7] Executive Problem Hook & FortyGuard Live Cloud Ingestion...');
  await smoothMouseMove(500, 320, 600);
  await new Promise((r) => setTimeout(r, 2200)); // Dwell on title & hero statement

  // Hover over the brand & active safety badges
  await smoothMouseMove(380, 75, 500);
  await new Promise((r) => setTimeout(r, 1400));

  // Open Live FortyGuard API Scan Modal
  console.log('  ↳ Opening FortyGuard Live Cloud Ingestion Modal...');
  await clickTabByText('Live Cloud Scan', 1800);

  // Hover over FortyGuard API Parameters in modal
  await smoothMouseMove(800, 420, 500);
  await new Promise((r) => setTimeout(r, 2200));

  // Trigger Live Ingestion
  console.log('  ↳ Executing Live Cloud Ingestion across 60m Parcel Tiles...');
  try {
    const liveScanBtn = await page.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const btn = btns.find((b) => b.textContent?.includes('Execute Live Cloud Ingestion') || b.textContent?.includes('Scan'));
      if (btn) {
        btn.click();
        return true;
      }
      return false;
    });
    if (liveScanBtn) {
      await page.evaluate(() => window.triggerClickEffect(curX, curY));
    }
  } catch (e) {}

  await new Promise((r) => setTimeout(r, 3500)); // Dwell on the live status & credit quota

  // Close Live Scan Modal
  try {
    await page.evaluate(() => {
      const closeBtn = Array.from(document.querySelectorAll('button')).find((b) => b.textContent?.includes('Close') || b.textContent?.includes('Dismiss'));
      if (closeBtn) closeBtn.click();
    });
  } catch (e) {}
  await new Promise((r) => setTimeout(r, 1500));

  // =========================================================================
  // ACT 2: MISSION CONTROL — "FACT VS. FINDING" & MITIGATION CLAMP (~35s - 95s)
  // Guidance: Mudethir & Aamir (Session 7), Snehil (Session 9), Reichental (Session 10)
  // =========================================================================
  console.log('📍 [ACT 2/7] Mission Control Telemetry & Fact vs. Finding Discovery...');
  await clickTabByText('Mission Control', 1800);

  // Dwell on Hero KPI Grid (highlighting 2m Ambient 42.7°C, Land-Cover Delta +1.1°C, 12.0h Persistence above 40°C)
  await smoothMouseMove(400, 220, 600);
  await new Promise((r) => setTimeout(r, 2200));
  await smoothMouseMove(800, 220, 600);
  await new Promise((r) => setTimeout(r, 2200));
  await smoothMouseMove(1200, 220, 600);
  await new Promise((r) => setTimeout(r, 2200));

  // Scrub through the 12-Hour Heatwave Timeline
  console.log('  ↳ Scrubbing 12-Hour Heatwave Progression (Morning -> Afternoon Peak)...');
  const hourButtons = await page.$$('div.flex.gap-1 button, div.space-x-1 button');
  if (hourButtons.length >= 8) {
    // Hour 2: Morning cool baseline
    await hourButtons[2].click();
    await page.evaluate(() => window.triggerClickEffect(450, 140));
    await new Promise((r) => setTimeout(r, 1800));

    // Hour 5: Rapid thermal ramp
    await hourButtons[5].click();
    await page.evaluate(() => window.triggerClickEffect(550, 140));
    await new Promise((r) => setTimeout(r, 1800));

    // Hour 7: Dangerous Afternoon Peak (13:00 Phoenix heatwave)
    await hourButtons[7].click();
    await page.evaluate(() => window.triggerClickEffect(650, 140));
    await new Promise((r) => setTimeout(r, 3000));
  }

  // Demonstrate Baseline vs. Mitigated Operational Toggle
  console.log('  ↳ Demonstrating Baseline vs. Mitigated Operational Toggle...');
  // Toggle to Baseline (danger state)
  await clickTabByText('Baseline', 2000);
  await smoothMouseMove(550, 320, 500);
  await new Promise((r) => setTimeout(r, 3000)); // Let the viewer see 159.5°C hot-spot & 88x aging

  // Toggle back to Mitigated (safe state)
  await clickTabByText('Mitigated', 2000);
  await smoothMouseMove(550, 320, 500);
  await new Promise((r) => setTimeout(r, 3000)); // Let the viewer see 122.5°C clamp

  // Smooth scroll down to review the ECharts Physics Telemetry & Safety Gate Card
  console.log('  ↳ Inspecting Physical ECharts Telemetry & Deterministic Safety Gate...');
  await smoothScroll(400, 800);
  await smoothMouseMove(650, 550, 600);
  await new Promise((r) => setTimeout(r, 3500));
  await smoothScroll(-400, 800);
  await new Promise((r) => setTimeout(r, 1200));

  // =========================================================================
  // ACT 3: PORTFOLIO OPERATIONS, WORKER SAFETY & COCO DISCOVERY (~95s - 170s)
  // Guidance: Thamir (Session 8 PMF), Karel (Session 11), Stelfox (Session 13)
  // =========================================================================
  console.log('📍 [ACT 3/7] Portfolio Operations, Worker Safety & COCO Discovery Generator...');
  await clickTabByText('Portfolio Ops', 1800);

  // Review the Portfolio Risk Ranking Table
  console.log('  ↳ Inspecting Portfolio Risk-Ranked Triage Table...');
  await smoothMouseMove(600, 380, 600);
  await new Promise((r) => setTimeout(r, 3000));

  // Review Worker Intervention Screen (Wet-Bulb Temperature limits)
  console.log('  ↳ Reviewing Worker Intervention Screen (Wet-Bulb Thermal Stress)...');
  await smoothScroll(300, 800);
  await smoothMouseMove(450, 520, 600);
  await new Promise((r) => setTimeout(r, 3500));

  // COCO Customer Discovery Brief Generator (Session 8 PMF - Thamir)
  console.log('  ↳ Demonstrating COCO Customer Discovery Engine across 4 ICP Sectors...');
  await smoothScroll(350, 800);
  await smoothMouseMove(960, 480, 500);
  await new Promise((r) => setTimeout(r, 2200));

  // Click Sector 1: Utility Substation
  console.log('    1. ⚡ Utility Substation Sector Brief...');
  try {
    await page.evaluate(() => {
      const cards = Array.from(document.querySelectorAll('div'));
      const sec = cards.find((c) => c.textContent?.includes('Utility Substation'));
      if (sec) sec.click();
    });
  } catch (e) {}
  await new Promise((r) => setTimeout(r, 3000));

  // Click Sector 2: AI Data Center
  console.log('    2. 🏢 AI Data Center Sector Brief...');
  try {
    await page.evaluate(() => {
      const cards = Array.from(document.querySelectorAll('div'));
      const sec = cards.find((c) => c.textContent?.includes('AI Data Center'));
      if (sec) sec.click();
    });
  } catch (e) {}
  await new Promise((r) => setTimeout(r, 3000));

  // Click Sector 3: Solar & BESS IPP
  console.log('    3. ☀️ Solar & BESS IPP Sector Brief...');
  try {
    await page.evaluate(() => {
      const cards = Array.from(document.querySelectorAll('div'));
      const sec = cards.find((c) => c.textContent?.includes('Solar & BESS'));
      if (sec) sec.click();
    });
  } catch (e) {}
  await new Promise((r) => setTimeout(r, 3000));

  // Click Sector 4: Hospital Trauma Center
  console.log('    4. 🏥 Hospital Trauma Center Sector Brief...');
  try {
    await page.evaluate(() => {
      const cards = Array.from(document.querySelectorAll('div'));
      const sec = cards.find((c) => c.textContent?.includes('Hospital Trauma'));
      if (sec) sec.click();
    });
  } catch (e) {}
  await new Promise((r) => setTimeout(r, 3500)); // Dwell on COCO 4 pillars

  // Copy MCP Call (showing enterprise tool compatibility)
  console.log('  ↳ Demonstrating MCP Tool-Calling Integration...');
  try {
    await page.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const copyBtn = btns.find((b) => b.textContent?.includes('Copy MCP'));
      if (copyBtn) copyBtn.click();
    });
  } catch (e) {}
  await new Promise((r) => setTimeout(r, 1500));

  await smoothScroll(-650, 800);
  await new Promise((r) => setTimeout(r, 1200));

  // =========================================================================
  // ACT 4: HYPERLOCAL 2M GIS & SPATIAL LAND COVER CAUSALITY (~170s - 225s)
  // Guidance: Mudethir (Session 7), Snehil (Session 9), Stelfox (Session 13)
  // =========================================================================
  console.log('📍 [ACT 4/7] Hyperlocal 2m Microclimate GIS Map & Spatial Causality...');
  await clickTabByText('Hyperlocal 2m GIS', 1800);

  // Explore 60m microclimate heat map
  await smoothMouseMove(550, 450, 600);
  await new Promise((r) => setTimeout(r, 3000));

  // Inspect Substation Asset Parcel
  console.log('  ↳ Inspecting Downtown Substation Parcel & Land Cover Breakdown...');
  await smoothMouseMove(850, 480, 500);
  await new Promise((r) => setTimeout(r, 3500)); // Dwell on 78% asphalt vs. 2% canopy

  await smoothScroll(250, 600);
  await new Promise((r) => setTimeout(r, 2200));
  await smoothScroll(-250, 600);
  await new Promise((r) => setTimeout(r, 1200));

  // =========================================================================
  // ACT 5: AUTONOMOUS LANGGRAPH MULTI-AGENT ENGINE (~225s - 290s)
  // Guidance: Fawad (Session 2), Reichental (Session 10), Constantine (Session 14)
  // =========================================================================
  console.log('📍 [ACT 5/7] LangGraph Multi-Agent Stack & Deterministic Safety Gate...');
  await clickTabByText('LangGraph Engine', 1800);

  // Step through the 5-node StateGraph DAG
  console.log('  ↳ Inspecting 5-Node StateGraph Architecture...');
  const dagButtons = await page.$$('div#tour-agent-dag button');
  if (dagButtons.length >= 5) {
    // 1. Forecast Node
    await dagButtons[0].click();
    await page.evaluate(() => window.triggerClickEffect(curX, curY));
    await new Promise((r) => setTimeout(r, 1800));

    // 2. Physics Node
    await dagButtons[1].click();
    await page.evaluate(() => window.triggerClickEffect(curX, curY));
    await new Promise((r) => setTimeout(r, 1800));

    // 3. Planner Node
    await dagButtons[2].click();
    await page.evaluate(() => window.triggerClickEffect(curX, curY));
    await new Promise((r) => setTimeout(r, 1800));

    // 4. Deterministic Safety Gate Node
    await dagButtons[3].click();
    await page.evaluate(() => window.triggerClickEffect(curX, curY));
    await new Promise((r) => setTimeout(r, 3000)); // Dwell on Non-LLM Safety Verification

    // 5. Audit & Dispatch Node
    await dagButtons[4].click();
    await page.evaluate(() => window.triggerClickEffect(curX, curY));
    await new Promise((r) => setTimeout(r, 1800));
  }

  // Trigger Live LangGraph StateGraph Execution
  console.log('  ↳ Executing Live Multi-Agent Pipeline & Generating Work Orders...');
  try {
    const executed = await page.evaluate(() => {
      const btn = document.querySelector('#tour-agent-trigger-btn') || Array.from(document.querySelectorAll('button')).find((b) => b.textContent?.includes('Execute Multi-Agent') || b.textContent?.includes('Trigger'));
      if (btn) {
        btn.click();
        return true;
      }
      return false;
    });
    if (executed) {
      await page.evaluate(() => window.triggerClickEffect(curX, curY));
    }
  } catch (e) {}

  await new Promise((r) => setTimeout(r, 4000)); // Dwell on execution logs & generated work order

  // Smooth scroll to view generated B2B work order & citizen advisory
  await smoothScroll(350, 800);
  await smoothMouseMove(960, 600, 500);
  await new Promise((r) => setTimeout(r, 3500));
  await smoothScroll(-350, 800);
  await new Promise((r) => setTimeout(r, 1200));

  // =========================================================================
  // ACT 6: AVOIDED LOSS ROI FINANCIAL MODEL (~290s - 345s)
  // Guidance: Ahmed (Session 5), Karel (Session 11), Vikram (Session 12)
  // =========================================================================
  console.log('📍 [ACT 6/7] Avoided Loss ROI & Hard Financial Impact...');
  await clickTabByText('Avoided Loss ROI', 1800);

  // Dwell on the Net Avoided Loss Banner ($2,566,193)
  await smoothMouseMove(400, 220, 600);
  await new Promise((r) => setTimeout(r, 3000));

  // Dwell on Customer Interruption Cost & Replacement Deferral
  await smoothMouseMove(800, 220, 600);
  await new Promise((r) => setTimeout(r, 3000));
  await smoothMouseMove(1200, 220, 600);
  await new Promise((r) => setTimeout(r, 3000));

  // Scroll to review the complete financial formula and assumption-based matrix
  await smoothScroll(350, 800);
  await smoothMouseMove(650, 550, 600);
  await new Promise((r) => setTimeout(r, 4000));
  await smoothScroll(-350, 800);
  await new Promise((r) => setTimeout(r, 1200));

  // =========================================================================
  // ACT 7: CINEMATIC CONCLUSION & EXECUTIVE SUMMARY (~345s - 365s)
  // Guidance: Tarek (Session 6), Constantine (Session 14)
  // =========================================================================
  console.log('📍 [ACT 7/7] Final Executive Summary & Pitch Conclusion...');
  await clickTabByText('Pitch & Video', 1800);

  await smoothMouseMove(960, 480, 600);
  await new Promise((r) => setTimeout(r, 3500));

  console.log('🏁 Walkthrough interaction complete. Stopping screencast...');
  isStreaming = false;
  await client.send('Page.stopScreencast');
  await browser.close();

  if (localServer) {
    localServer.close();
  }

  ffmpeg.stdin.end();

  await new Promise((resolve) => {
    ffmpeg.on('close', resolve);
  });

  console.log(`✅ Raw Screencast captured: ${RAW_VIDEO}`);

  // Mux BGM Audio Track
  if (fs.existsSync(BGM_AUDIO)) {
    console.log(`🎵 Muxing clean background ambient audio track: ${BGM_AUDIO}...`);
    const muxProcess = spawn(FFMPEG, [
      '-y',
      '-i', RAW_VIDEO,
      '-i', BGM_AUDIO,
      '-c:v', 'copy',
      '-c:a', 'aac',
      '-b:a', '192k',
      '-map', '0:v:0',
      '-map', '1:a:0',
      '-shortest',
      OUTPUT_VIDEO,
    ]);

    await new Promise((resolve) => {
      muxProcess.on('close', resolve);
    });

    fs.copyFileSync(OUTPUT_VIDEO, PUBLIC_VIDEO);
    console.log(`🎉 Final Business-Value Demo Video saved: ${OUTPUT_VIDEO}`);
    console.log(`🎉 Public frontend asset updated: ${PUBLIC_VIDEO}`);
  } else {
    fs.copyFileSync(RAW_VIDEO, OUTPUT_VIDEO);
    fs.copyFileSync(RAW_VIDEO, PUBLIC_VIDEO);
    console.log(`🎉 Video saved (silent): ${OUTPUT_VIDEO}`);
  }

  console.log('\n✨ ALL DONE! You can now use the video directly or edit/voiceover it as needed.');
}

recordBusinessValueDemo().catch((err) => {
  console.error('Fatal recording error:', err);
  process.exit(1);
});
