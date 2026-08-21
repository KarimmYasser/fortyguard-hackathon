import puppeteer from 'puppeteer';
import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');

const OUTPUT_VIDEO = path.resolve(projectRoot, 'videos/thermal-sentinel-pitch/renders/live_product_demo.mp4');
const PUBLIC_VIDEO = path.resolve(projectRoot, 'frontend/public/videos/live_product_demo.mp4');
const BGM_AUDIO = path.resolve(projectRoot, 'videos/thermal-sentinel-pitch/assets/audio/bgm_cyber_ambient.mp3');
const RAW_VIDEO = path.resolve(projectRoot, 'scratch/raw_screencast.mp4');

// Ensure output dirs exist
fs.mkdirSync(path.dirname(OUTPUT_VIDEO), { recursive: true });
fs.mkdirSync(path.dirname(PUBLIC_VIDEO), { recursive: true });
fs.mkdirSync(path.dirname(RAW_VIDEO), { recursive: true });

async function recordLiveWalkthrough() {
  console.log('🚀 Launching Puppeteer for Snappy High-Energy UI Walkthrough (1920x1080)...');
  const browser = await puppeteer.launch({
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--window-size=1920,1080',
      '--disable-gpu-sandbox',
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

  const TARGET_URL = process.env.TARGET_URL || 'https://fortyguard-hackathon.vercel.app';
  console.log(`🌐 Opening ${TARGET_URL} ...`);
  await page.goto(TARGET_URL, { waitUntil: 'networkidle0', timeout: 30000 });
  await new Promise((r) => setTimeout(r, 1500));

  // Inject Cursor Overlay and Action Effects
  await page.evaluate(() => {
    const style = document.createElement('style');
    style.innerHTML = `
      #ai-virtual-cursor {
        position: fixed;
        width: 32px;
        height: 32px;
        pointer-events: none;
        z-index: 999999;
        transition: transform 0.04s ease-out, opacity 0.15s ease;
        transform: translate(-4px, -4px);
      }
      .cursor-dot {
        width: 16px;
        height: 16px;
        background: #38bdf8;
        border: 2.5px solid #ffffff;
        border-radius: 50%;
        box-shadow: 0 0 16px #38bdf8, 0 0 24px rgba(56, 189, 248, 0.9);
      }
      .cursor-ring {
        position: absolute;
        top: -6px;
        left: -6px;
        width: 28px;
        height: 28px;
        border: 2px solid rgba(56, 189, 248, 0.7);
        border-radius: 50%;
        animation: pulseRing 1.2s infinite;
      }
      .click-burst {
        position: fixed;
        width: 44px;
        height: 44px;
        border-radius: 50%;
        border: 3px solid #f59e0b;
        pointer-events: none;
        z-index: 999998;
        animation: burstAnim 0.4s cubic-bezier(0, 0, 0.2, 1) forwards;
        transform: translate(-50%, -50%);
      }
      @keyframes pulseRing {
        0% { transform: scale(0.9); opacity: 0.9; }
        50% { transform: scale(1.3); opacity: 0.3; }
        100% { transform: scale(0.9); opacity: 0.9; }
      }
      @keyframes burstAnim {
        0% { transform: translate(-50%, -50%) scale(0.3); opacity: 1; }
        100% { transform: translate(-50%, -50%) scale(2.0); opacity: 0; }
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
      setTimeout(() => burst.remove(), 400);
    };
  });

  // Start FFmpeg process for CDP Screencast
  console.log('🎥 Initializing CDP Screencast & FFmpeg...');
  const ffmpeg = spawn('/opt/homebrew/bin/ffmpeg', [
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

  const client = await page.target().createCDPSession();
  await client.send('Page.startScreencast', {
    format: 'jpeg',
    quality: 95,
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

  // Snappy Motion helpers
  let curX = 960, curY = 540;
  async function smoothMouseMove(targetX, targetY, durationMs = 350) {
    const steps = Math.max(8, Math.round(durationMs / 16));
    const startX = curX, startY = curY;
    for (let i = 1; i <= steps; i++) {
      const t = i / steps;
      const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
      const x = Math.round(startX + (targetX - startX) * ease);
      const y = Math.round(startY + (targetY - startY) * ease);
      await page.evaluate((px, py) => window.updateVirtualCursor(px, py), x, y);
      await new Promise((r) => setTimeout(r, 16));
    }
    curX = targetX;
    curY = targetY;
  }

  async function clickElement(selector, waitAfter = 500) {
    try {
      const rect = await page.evaluate((sel) => {
        const el = document.querySelector(sel);
        if (!el) return null;
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        const r = el.getBoundingClientRect();
        return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
      }, selector);

      if (rect) {
        await smoothMouseMove(rect.x, rect.y, 300);
        await page.evaluate((x, y) => window.triggerClickEffect(x, y), rect.x, rect.y);
        await page.click(selector);
      }
    } catch (err) {}
    await new Promise((r) => setTimeout(r, waitAfter));
  }

  async function clickTabByText(tabLabel, waitAfter = 600) {
    try {
      const rect = await page.evaluate((text) => {
        const btns = Array.from(document.querySelectorAll('nav button'));
        const target = btns.find((b) => b.textContent?.includes(text));
        if (!target) return null;
        const r = target.getBoundingClientRect();
        return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
      }, tabLabel);

      if (rect) {
        await smoothMouseMove(rect.x, rect.y, 350);
        await page.evaluate((x, y) => window.triggerClickEffect(x, y), rect.x, rect.y);
        await page.evaluate((text) => {
          const btns = Array.from(document.querySelectorAll('nav button'));
          const target = btns.find((b) => b.textContent?.includes(text));
          if (target) target.click();
        }, tabLabel);
      }
    } catch (err) {}
    await new Promise((r) => setTimeout(r, waitAfter));
  }

  async function smoothScroll(deltaY, durationMs = 500) {
    const steps = Math.max(6, Math.round(durationMs / 20));
    for (let i = 0; i < steps; i++) {
      await page.evaluate((dy) => window.scrollBy(0, dy), deltaY / steps);
      await new Promise((r) => setTimeout(r, 20));
    }
  }

  console.log('🎬 Starting Snappy, High-Energy Choreographed Walkthrough...\n');

  // ==========================================
  // SECTION 1: HOME PITCH & LIVE SCAN (0 - 10s)
  // ==========================================
  console.log('📍 [01/10] Home View & Live API Scan Modal...');
  await smoothMouseMove(500, 280, 400);
  await new Promise((r) => setTimeout(r, 600));

  // Open Live API Scan Modal
  await clickTabByText('Live API Scan', 600);
  await smoothMouseMove(960, 480, 350);
  await new Promise((r) => setTimeout(r, 600));

  // Click Execute Live Cloud Ingestion
  try {
    await clickElement('button:has-text("Execute Live Cloud Ingestion")', 1200);
  } catch (e) {}
  await new Promise((r) => setTimeout(r, 800));

  // Close Modal
  try {
    await page.evaluate(() => {
      const closeBtn = Array.from(document.querySelectorAll('button')).find((b) => b.textContent?.includes('Close'));
      if (closeBtn) closeBtn.click();
    });
  } catch (e) {}
  await new Promise((r) => setTimeout(r, 600));

  // ==========================================
  // SECTION 2: MISSION CONTROL (10 - 22s)
  // ==========================================
  console.log('📍 [02/10] Mission Control Telemetry & 12h Scrubbing...');
  await clickTabByText('Overview', 800);

  // Scrub through 12h replay bar
  await smoothMouseMove(500, 140, 300);
  const hourButtons = await page.$$('div.flex.gap-1 button, div.space-x-1 button');
  if (hourButtons.length >= 8) {
    await hourButtons[2].click(); // Hour 2
    await new Promise((r) => setTimeout(r, 400));
    await hourButtons[5].click(); // Hour 5 (ramp)
    await new Promise((r) => setTimeout(r, 400));
    await hourButtons[7].click(); // Hour 7 (peak 47.6°C)
    await new Promise((r) => setTimeout(r, 600));
  }

  // Toggle Baseline vs Mitigated
  await clickTabByText('MITIGATED', 600);
  await new Promise((r) => setTimeout(r, 600));
  await clickTabByText('BASELINE', 600);
  await new Promise((r) => setTimeout(r, 600));
  await clickTabByText('MITIGATED', 600);

  await smoothScroll(300, 400);
  await smoothMouseMove(600, 600, 350);
  await new Promise((r) => setTimeout(r, 800));
  await smoothScroll(-300, 400);

  // ==========================================
  // SECTION 3: WHAT-IF STUDIO (22 - 32s)
  // ==========================================
  console.log('📍 [03/10] What-If Stress Studio...');
  await clickTabByText('What-If', 800);

  // Click Stress Presets
  const presetButtons = await page.$$('button');
  for (const btn of presetButtons) {
    const text = await page.evaluate((el) => el.textContent, btn);
    if (text?.includes('Airport SCADA Blindspot')) {
      await btn.click();
      await new Promise((r) => setTimeout(r, 500));
    } else if (text?.includes('Zero-BESS Stress')) {
      await btn.click();
      await new Promise((r) => setTimeout(r, 500));
    } else if (text?.includes('Phoenix')) {
      await btn.click();
      await new Promise((r) => setTimeout(r, 600));
      break;
    }
  }

  await smoothScroll(200, 300);
  await new Promise((r) => setTimeout(r, 600));
  await smoothScroll(-200, 300);

  // ==========================================
  // SECTION 4: 72H COMPOUNDING HEATWAVE (32 - 40s)
  // ==========================================
  console.log('📍 [04/10] 72-Hour Compounding Heatwave Simulation...');
  await clickTabByText('72h Heatwave', 800);

  // Click Day 1 -> Day 2 -> Day 3
  const dayButtons = await page.$$('button');
  for (const btn of dayButtons) {
    const text = await page.evaluate((el) => el.textContent, btn);
    if (text?.includes('Day 2')) {
      await btn.click();
      await new Promise((r) => setTimeout(r, 500));
    } else if (text?.includes('Day 3')) {
      await btn.click();
      await new Promise((r) => setTimeout(r, 600));
    }
  }

  await smoothScroll(250, 400);
  await new Promise((r) => setTimeout(r, 600));
  await smoothScroll(-250, 400);

  // ==========================================
  // SECTION 5: 14-BUS AC POWER FLOW (40 - 48s)
  // ==========================================
  console.log('📍 [05/10] 14-Bus AC Distribution Feeder Power Flow...');
  await clickTabByText('Power Flow', 800);

  await smoothMouseMove(960, 450, 400);
  await smoothScroll(200, 350);
  await new Promise((r) => setTimeout(r, 800));
  await smoothScroll(-200, 350);

  // ==========================================
  // SECTION 6: IEEE ANNEX G BENCHMARK (48 - 54s)
  // ==========================================
  console.log('📍 [06/10] IEEE Std C57.91 Annex G Validation Table...');
  await clickTabByText('IEEE Annex G', 800);

  await smoothMouseMove(700, 400, 350);
  await smoothScroll(250, 400);
  await new Promise((r) => setTimeout(r, 800));
  await smoothScroll(-250, 400);

  // ==========================================
  // SECTION 7: 2M GIS HEATMAP (54 - 62s)
  // ==========================================
  console.log('📍 [07/10] Hyperlocal 2m Microclimate GIS Heatmap...');
  await clickTabByText('2m GIS Heatmap', 800);

  await smoothMouseMove(600, 500, 400);
  await new Promise((r) => setTimeout(r, 1000));

  // ==========================================
  // SECTION 8: 4 SCIENTIFIC MOATS (62 - 68s)
  // ==========================================
  console.log('📍 [08/10] 4 Asymmetric Scientific Moats...');
  await clickTabByText('Scientific Moats', 800);

  await smoothMouseMove(800, 400, 350);
  await smoothScroll(200, 300);
  await new Promise((r) => setTimeout(r, 800));
  await smoothScroll(-200, 300);

  // ==========================================
  // SECTION 9: LANGGRAPH AGENT ENGINE WITH LIVE GPT-5.4 (68 - 82s)
  // ==========================================
  console.log('📍 [09/10] LangGraph Multi-Agent Stack & Live GPT-5.4...');
  await clickTabByText('LangGraph', 800);

  // Click nodes in DAG
  const dagButtons = await page.$$('div#tour-agent-dag button');
  if (dagButtons.length >= 5) {
    await dagButtons[0].click(); // forecast_node
    await new Promise((r) => setTimeout(r, 350));
    await dagButtons[1].click(); // physics_node
    await new Promise((r) => setTimeout(r, 350));
    await dagButtons[2].click(); // planner_node
    await new Promise((r) => setTimeout(r, 350));
    await dagButtons[3].click(); // safety_gate_node
    await new Promise((r) => setTimeout(r, 350));
    await dagButtons[4].click(); // audit_dispatch_node
    await new Promise((r) => setTimeout(r, 400));
  }

  // Trigger Live LangGraph Execution with GPT-5.4
  console.log('⚡ Triggering Live Agentic Scan & Mitigation with GPT-5.4...');
  try {
    await clickElement('#tour-agent-trigger-btn', 2800);
  } catch (e) {}

  await smoothScroll(300, 400);
  await smoothMouseMove(960, 650, 400);
  await new Promise((r) => setTimeout(r, 1200));
  await smoothScroll(-300, 400);

  // ==========================================
  // SECTION 10: FINANCIAL ROI MODEL & CONCLUSION (82 - 90s)
  // ==========================================
  console.log('📍 [10/10] Financial ROI & Final Pitch Screen...');
  await clickTabByText('Financial ROI', 800);

  await smoothMouseMove(600, 400, 350);
  await smoothScroll(300, 400);
  await new Promise((r) => setTimeout(r, 1000));
  await smoothScroll(-300, 400);

  // Return to Home view for a clean finish
  await clickTabByText('Home', 800);
  await smoothMouseMove(960, 450, 400);
  await new Promise((r) => setTimeout(r, 1500));

  console.log('🏁 Walkthrough finished. Finalizing screencast...');
  isStreaming = false;
  await client.send('Page.stopScreencast');
  await browser.close();

  ffmpeg.stdin.end();

  await new Promise((resolve) => {
    ffmpeg.on('close', resolve);
  });

  console.log(`✅ Raw Screencast captured: ${RAW_VIDEO}`);

  // Mux BGM Audio (No Voiceover)
  console.log(`🎵 Muxing clean background sound (No Voiceover): ${BGM_AUDIO}...`);
  const muxProcess = spawn('/opt/homebrew/bin/ffmpeg', [
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
  console.log(`🎉 Final Live Walkthrough Video saved: ${OUTPUT_VIDEO}`);
  console.log(`🎉 Public frontend asset updated: ${PUBLIC_VIDEO}`);
}

recordLiveWalkthrough().catch((err) => {
  console.error('Fatal recording error:', err);
  process.exit(1);
});
