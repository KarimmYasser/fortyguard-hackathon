import puppeteer from 'puppeteer';
import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');

const OUTPUT_VIDEO = path.resolve(projectRoot, 'videos/thermal-sentinel-pitch/renders/live_product_demo.mp4');
const MASTER_AUDIO = path.resolve(projectRoot, 'videos/thermal-sentinel-pitch/assets/audio/master_audio.mp3');
const RAW_VIDEO = path.resolve(projectRoot, 'scratch/raw_screencast.mp4');

// Ensure output dirs exist
fs.mkdirSync(path.dirname(OUTPUT_VIDEO), { recursive: true });
fs.mkdirSync(path.dirname(RAW_VIDEO), { recursive: true });

async function recordLiveWalkthrough() {
  console.log('🚀 Launching Puppeteer browser in 1920x1080...');
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

  // Navigate to local FastAPI / React dashboard
  console.log('🌐 Navigating to http://127.0.0.1:8000 ...');
  await page.goto('http://127.0.0.1:8000', { waitUntil: 'networkidle0', timeout: 30000 });
  await new Promise((r) => setTimeout(r, 2000));

  // Inject Cursor Overlay and Animation Styles
  await page.evaluate(() => {
    const style = document.createElement('style');
    style.innerHTML = `
      #ai-virtual-cursor {
        position: fixed;
        width: 28px;
        height: 28px;
        pointer-events: none;
        z-index: 999999;
        transition: transform 0.08s ease-out, opacity 0.2s ease;
        transform: translate(-4px, -4px);
      }
      .cursor-dot {
        width: 14px;
        height: 14px;
        background: #06b6d4;
        border: 2.5px solid #ffffff;
        border-radius: 50%;
        box-shadow: 0 0 16px #06b6d4, 0 0 24px rgba(6, 182, 212, 0.8);
      }
      .cursor-ring {
        position: absolute;
        top: -6px;
        left: -6px;
        width: 26px;
        height: 26px;
        border: 2px solid rgba(6, 182, 212, 0.6);
        border-radius: 50%;
        animation: pulseRing 1.5s infinite;
      }
      .click-burst {
        position: fixed;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        border: 3px solid #f59e0b;
        pointer-events: none;
        z-index: 999998;
        animation: burstAnim 0.5s ease-out forwards;
        transform: translate(-50%, -50%);
      }
      @keyframes pulseRing {
        0% { transform: scale(0.9); opacity: 0.8; }
        50% { transform: scale(1.4); opacity: 0.2; }
        100% { transform: scale(0.9); opacity: 0.8; }
      }
      @keyframes burstAnim {
        0% { transform: translate(-50%, -50%) scale(0.4); opacity: 1; }
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
      setTimeout(() => burst.remove(), 500);
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
    '-preset', 'fast',
    '-crf', '18',
    RAW_VIDEO,
  ]);

  ffmpeg.stderr.on('data', (d) => {
    // optional debug
  });

  const client = await page.target().createCDPSession();
  await client.send('Page.startScreencast', {
    format: 'jpeg',
    quality: 92,
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
    } catch (e) {
      // ignore frame ack error on teardown
    }
  });

  // Helper motion functions
  let curX = 960, curY = 540;
  async function smoothMouseMove(targetX, targetY, durationMs = 600) {
    const steps = Math.max(10, Math.round(durationMs / 20));
    const startX = curX, startY = curY;
    for (let i = 1; i <= steps; i++) {
      const t = i / steps;
      // easeInOutCubic
      const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
      const x = Math.round(startX + (targetX - startX) * ease);
      const y = Math.round(startY + (targetY - startY) * ease);
      await page.evaluate((px, py) => window.updateVirtualCursor(px, py), x, y);
      await new Promise((r) => setTimeout(r, 20));
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
        await smoothMouseMove(rect.x, rect.y, 500);
        await page.evaluate((x, y) => window.triggerClickEffect(x, y), rect.x, rect.y);
        await page.click(selector);
      }
    } catch (err) {
      console.warn(`Click failed on ${selector}:`, err.message);
    }
    await new Promise((r) => setTimeout(r, waitAfter));
  }

  async function clickTabByText(tabLabel, waitAfter = 1000) {
    try {
      const rect = await page.evaluate((text) => {
        const btns = Array.from(document.querySelectorAll('nav button'));
        const target = btns.find((b) => b.textContent?.includes(text));
        if (!target) return null;
        const r = target.getBoundingClientRect();
        return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
      }, tabLabel);

      if (rect) {
        await smoothMouseMove(rect.x, rect.y, 600);
        await page.evaluate((x, y) => window.triggerClickEffect(x, y), rect.x, rect.y);
        await page.evaluate((text) => {
          const btns = Array.from(document.querySelectorAll('nav button'));
          const target = btns.find((b) => b.textContent?.includes(text));
          if (target) (target).click();
        }, tabLabel);
      }
    } catch (err) {
      console.warn(`Tab click failed on ${tabLabel}:`, err.message);
    }
    await new Promise((r) => setTimeout(r, waitAfter));
  }

  async function hoverElement(selector, durationMs = 1500) {
    try {
      const rect = await page.evaluate((sel) => {
        const el = document.querySelector(sel);
        if (!el) return null;
        const r = el.getBoundingClientRect();
        return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
      }, selector);
      if (rect) {
        await smoothMouseMove(rect.x, rect.y, 500);
        await new Promise((r) => setTimeout(r, durationMs));
      }
    } catch (err) {}
  }

  async function smoothScroll(deltaY, durationMs = 1200) {
    const steps = Math.max(10, Math.round(durationMs / 30));
    for (let i = 0; i < steps; i++) {
      await page.evaluate((dy) => window.scrollBy(0, dy), deltaY / steps);
      await new Promise((r) => setTimeout(r, 30));
    }
  }

  const startTime = Date.now();
  const getElapsed = () => ((Date.now() - startTime) / 1000).toFixed(1);

  console.log('🎬 Starting Choreographed 180-second Walkthrough...\n');

  // ==========================================
  // SCENE 1: The Hook & Market Blindspot (0:00 - 0:30, 30s)
  // ==========================================
  console.log(`[${getElapsed()}s] Scene 1: Showing Hyperlocal 2m GIS Map...`);
  await clickTabByText('Hyperlocal 2m GIS', 2000);

  // Hover on 2m Ambient Heat vs Phoenix Substation
  await smoothMouseMove(400, 350, 1000);
  await new Promise((r) => setTimeout(r, 3000));

  // Switch GIS layers: Persistence (P40)
  console.log(`[${getElapsed()}s] Switching to Persistence (P40) layer...`);
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button'));
    const p40 = btns.find((b) => b.textContent?.includes('Persistence'));
    if (p40) {
      const r = p40.getBoundingClientRect();
      window.updateVirtualCursor(r.left + r.width/2, r.top + r.height/2);
      window.triggerClickEffect(r.left + r.width/2, r.top + r.height/2);
      p40.click();
    }
  });
  await new Promise((r) => setTimeout(r, 4000));

  // Switch GIS layers: Land Cover & Albedo
  console.log(`[${getElapsed()}s] Switching to Land Cover & Albedo layer...`);
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button'));
    const albedo = btns.find((b) => b.textContent?.includes('Land Cover'));
    if (albedo) {
      const r = albedo.getBoundingClientRect();
      window.updateVirtualCursor(r.left + r.width/2, r.top + r.height/2);
      window.triggerClickEffect(r.left + r.width/2, r.top + r.height/2);
      albedo.click();
    }
  });
  await new Promise((r) => setTimeout(r, 4000));

  // Inspect Map Tile Card
  await smoothMouseMove(1250, 450, 1000);
  await new Promise((r) => setTimeout(r, 5000));

  // Wait until 30s mark
  while (Date.now() - startTime < 30000) {
    await new Promise((r) => setTimeout(r, 200));
  }

  // ==========================================
  // SCENE 2: The Solution & 4 Scientific Moats (0:30 - 1:00, 30s)
  // ==========================================
  console.log(`[${getElapsed()}s] Scene 2: Four Asymmetric Scientific Moats...`);
  await clickTabByText('4 Scientific Moats', 1500);

  // Moat 1: Soil Dryout
  await smoothMouseMove(900, 400, 800);
  await new Promise((r) => setTimeout(r, 5000));

  // Moat 2: CBF-QP Safety Gate
  console.log(`[${getElapsed()}s] Clicking Moat 2: CBF-QP Safety Gate...`);
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button'));
    const m2 = btns.find((b) => b.textContent?.includes('2. CBF-QP'));
    if (m2) {
      const r = m2.getBoundingClientRect();
      window.updateVirtualCursor(r.left + r.width/2, r.top + r.height/2);
      window.triggerClickEffect(r.left + r.width/2, r.top + r.height/2);
      m2.click();
    }
  });
  await new Promise((r) => setTimeout(r, 6000));

  // Moat 3: Canyon Aerodynamics
  console.log(`[${getElapsed()}s] Clicking Moat 3: Canyon Aerodynamics...`);
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button'));
    const m3 = btns.find((b) => b.textContent?.includes('3. Canyon'));
    if (m3) {
      const r = m3.getBoundingClientRect();
      window.updateVirtualCursor(r.left + r.width/2, r.top + r.height/2);
      window.triggerClickEffect(r.left + r.width/2, r.top + r.height/2);
      m3.click();
    }
  });
  await new Promise((r) => setTimeout(r, 6000));

  // Moat 4: Virtual Moisture
  console.log(`[${getElapsed()}s] Clicking Moat 4: Virtual Moisture...`);
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button'));
    const m4 = btns.find((b) => b.textContent?.includes('4. Virtual Moisture'));
    if (m4) {
      const r = m4.getBoundingClientRect();
      window.updateVirtualCursor(r.left + r.width/2, r.top + r.height/2);
      window.triggerClickEffect(r.left + r.width/2, r.top + r.height/2);
      m4.click();
    }
  });
  await new Promise((r) => setTimeout(r, 6000));

  // Wait until 60s mark
  while (Date.now() - startTime < 60000) {
    await new Promise((r) => setTimeout(r, 200));
  }

  // ==========================================
  // SCENE 3: Why Agentic Physical AI & LangGraph (1:00 - 1:30, 30s)
  // ==========================================
  console.log(`[${getElapsed()}s] Scene 3: LangGraph Engine & Safety Barrier...`);
  await clickTabByText('LangGraph Engine', 1500);

  // Click Node 1: Forecast Ingest
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button'));
    const n1 = btns.find((b) => b.textContent?.includes('1. Forecast'));
    if (n1) {
      const r = n1.getBoundingClientRect();
      window.updateVirtualCursor(r.left + r.width/2, r.top + r.height/2);
      window.triggerClickEffect(r.left + r.width/2, r.top + r.height/2);
      n1.click();
    }
  });
  await new Promise((r) => setTimeout(r, 5000));

  // Click Node 2: Physics State Estimation
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button'));
    const n2 = btns.find((b) => b.textContent?.includes('2. Physics'));
    if (n2) {
      const r = n2.getBoundingClientRect();
      window.updateVirtualCursor(r.left + r.width/2, r.top + r.height/2);
      window.triggerClickEffect(r.left + r.width/2, r.top + r.height/2);
      n2.click();
    }
  });
  await new Promise((r) => setTimeout(r, 5000));

  // Click Node 3: Mitigation Planner
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button'));
    const n3 = btns.find((b) => b.textContent?.includes('3. Mitigation'));
    if (n3) {
      const r = n3.getBoundingClientRect();
      window.updateVirtualCursor(r.left + r.width/2, r.top + r.height/2);
      window.triggerClickEffect(r.left + r.width/2, r.top + r.height/2);
      n3.click();
    }
  });
  await new Promise((r) => setTimeout(r, 5000));

  // Click Node 4: Safety Gate (CBF-QP)
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button'));
    const n4 = btns.find((b) => b.textContent?.includes('4. Safety Gate'));
    if (n4) {
      const r = n4.getBoundingClientRect();
      window.updateVirtualCursor(r.left + r.width/2, r.top + r.height/2);
      window.triggerClickEffect(r.left + r.width/2, r.top + r.height/2);
      n4.click();
    }
  });
  await new Promise((r) => setTimeout(r, 6000));

  // Wait until 90s mark
  while (Date.now() - startTime < 90000) {
    await new Promise((r) => setTimeout(r, 200));
  }

  // ==========================================
  // SCENE 4: Live Mission Control & What-If Studio (1:30 - 2:15, 45s)
  // ==========================================
  console.log(`[${getElapsed()}s] Scene 4: Mission Control & Scrubber...`);
  await clickTabByText('Mission Control', 1500);

  // Toggle Baseline vs Mitigated
  console.log(`[${getElapsed()}s] Toggling to Baseline Unmitigated Mode...`);
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button'));
    const baseBtn = btns.find((b) => b.textContent?.includes('Baseline'));
    if (baseBtn) {
      const r = baseBtn.getBoundingClientRect();
      window.updateVirtualCursor(r.left + r.width/2, r.top + r.height/2);
      window.triggerClickEffect(r.left + r.width/2, r.top + r.height/2);
      baseBtn.click();
    }
  });
  await new Promise((r) => setTimeout(r, 5000));

  console.log(`[${getElapsed()}s] Toggling back to Mitigated Mode...`);
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button'));
    const mitBtn = btns.find((b) => b.textContent?.includes('Mitigated'));
    if (mitBtn) {
      const r = mitBtn.getBoundingClientRect();
      window.updateVirtualCursor(r.left + r.width/2, r.top + r.height/2);
      window.triggerClickEffect(r.left + r.width/2, r.top + r.height/2);
      mitBtn.click();
    }
  });
  await new Promise((r) => setTimeout(r, 3000));

  // Drag Scrubber / Trigger Playback
  console.log(`[${getElapsed()}s] Triggering 12-hour Replay Scrubber Playback...`);
  await page.evaluate(() => {
    const playBtn = document.querySelector('button[title*="Play"], button[aria-label*="Play"]') ||
                    Array.from(document.querySelectorAll('button')).find(b => b.innerHTML.includes('Play') || b.querySelector('svg'));
    if (playBtn) {
      const r = playBtn.getBoundingClientRect();
      window.updateVirtualCursor(r.left + r.width/2, r.top + r.height/2);
      window.triggerClickEffect(r.left + r.width/2, r.top + r.height/2);
      playBtn.click();
    }
  });
  await new Promise((r) => setTimeout(r, 8000));

  // Switch to What-If Studio
  console.log(`[${getElapsed()}s] Opening What-If Studio...`);
  await clickTabByText('What-If Studio', 1500);

  // Click Preset: Severe Grid Heat Stress
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button'));
    const severe = btns.find((b) => b.textContent?.includes('Severe') || b.textContent?.includes('Heat Stress'));
    if (severe) {
      const r = severe.getBoundingClientRect();
      window.updateVirtualCursor(r.left + r.width/2, r.top + r.height/2);
      window.triggerClickEffect(r.left + r.width/2, r.top + r.height/2);
      severe.click();
    }
  });
  await new Promise((r) => setTimeout(r, 6000));

  // Switch to AC Power Flow
  console.log(`[${getElapsed()}s] Opening AC Power Flow Single-Line...`);
  await clickTabByText('AC Power Flow', 1500);
  await smoothMouseMove(960, 500, 1000);
  await new Promise((r) => setTimeout(r, 8000));

  // Wait until 135s mark
  while (Date.now() - startTime < 135000) {
    await new Promise((r) => setTimeout(r, 200));
  }

  // ==========================================
  // SCENE 5: Auditable ROI & Impact (2:15 - 2:45, 30s)
  // ==========================================
  console.log(`[${getElapsed()}s] Scene 5: Avoided Loss & ROI Audit...`);
  await clickTabByText('Avoided Loss ROI', 1500);

  // Hover over Net Avoided Loss Hero Card
  await smoothMouseMove(400, 300, 1000);
  await new Promise((r) => setTimeout(r, 6000));

  // Smooth scroll down to LBNL ICE table
  console.log(`[${getElapsed()}s] Scrolling to LBNL ICE Table...`);
  await smoothScroll(350, 1000);
  await smoothMouseMove(900, 600, 1000);
  await new Promise((r) => setTimeout(r, 10000));

  // Wait until 165s mark
  while (Date.now() - startTime < 165000) {
    await new Promise((r) => setTimeout(r, 200));
  }

  // ==========================================
  // SCENE 6: Outro & Submission Lockup (2:45 - 3:00, 15s)
  // ==========================================
  console.log(`[${getElapsed()}s] Scene 6: Outro & Summary Lockup...`);
  await clickTabByText('Mission Control', 1200);
  await smoothScroll(600, 1200);
  await smoothMouseMove(960, 800, 1000);

  // Wait until full 180s mark
  while (Date.now() - startTime < 180000) {
    await new Promise((r) => setTimeout(r, 200));
  }

  console.log(`[${getElapsed()}s] 🛑 180s Completed! Stopping Screencast & Browser...`);
  isStreaming = false;
  await client.send('Page.stopScreencast');
  await browser.close();

  ffmpeg.stdin.end();
  await new Promise((resolve) => ffmpeg.on('close', resolve));
  console.log('✅ Raw screencast recorded to', RAW_VIDEO);

  // Mux audio and video using FFmpeg
  console.log('🎵 Muxing video with Master Voiceover Audio...');
  const muxProcess = spawn('/opt/homebrew/bin/ffmpeg', [
    '-y',
    '-i', RAW_VIDEO,
    '-i', MASTER_AUDIO,
    '-c:v', 'copy',
    '-c:a', 'aac',
    '-b:a', '192k',
    '-shortest',
    OUTPUT_VIDEO,
  ]);

  muxProcess.on('close', (code) => {
    if (code === 0) {
      console.log('🎉 Final Live Walkthrough Video Created Successfully!');
      console.log('📁 Output:', OUTPUT_VIDEO);
    } else {
      console.error('❌ FFmpeg muxing failed with code', code);
    }
  });
}

recordLiveWalkthrough().catch((err) => {
  console.error('Fatal Walkthrough Error:', err);
  process.exit(1);
});
