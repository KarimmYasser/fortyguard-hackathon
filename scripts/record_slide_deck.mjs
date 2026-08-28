import puppeteer from 'puppeteer';
import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs';
import http from 'http';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');

const SLIDES_DIR = path.resolve(projectRoot, 'decks/thermal-sentinel-slides');
const OUTPUT_VIDEO = path.resolve(SLIDES_DIR, 'renders/slide_deck.mp4');
const PITCH_VIDEO_COPY = path.resolve(projectRoot, 'videos/thermal-sentinel-pitch/renders/slide_deck.mp4');
const PUBLIC_VIDEO = path.resolve(projectRoot, 'frontend/public/videos/slide_deck.mp4');
const RAW_VIDEO = path.resolve(SLIDES_DIR, 'renders/slide_deck_raw.mp4');
const BGM_AUDIO = path.resolve(projectRoot, 'videos/thermal-sentinel-pitch/assets/audio/bgm_cyber_ambient.mp3');

const FFMPEG = process.env.FFMPEG_PATH || (fs.existsSync('/opt/homebrew/bin/ffmpeg') ? '/opt/homebrew/bin/ffmpeg' : 'ffmpeg');

fs.mkdirSync(path.dirname(OUTPUT_VIDEO), { recursive: true });
fs.mkdirSync(path.dirname(PITCH_VIDEO_COPY), { recursive: true });
fs.mkdirSync(path.dirname(PUBLIC_VIDEO), { recursive: true });

function startStaticServer(port = 4180) {
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
    '.mp4': 'video/mp4',
    '.mp3': 'audio/mpeg',
  };

  const server = http.createServer((req, res) => {
    let reqPath = req.url.split('?')[0];
    if (reqPath === '/' || reqPath === '') {
      reqPath = '/index.html';
    }

    const filePath = path.join(SLIDES_DIR, reqPath);
    const ext = path.extname(filePath).toLowerCase();

    if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
      res.writeHead(200, { 'Content-Type': mimeTypes[ext] || 'application/octet-stream' });
      fs.createReadStream(filePath).pipe(res);
    } else {
      res.writeHead(404);
      res.end('Not found');
    }
  });

  return new Promise((resolve) => {
    server.listen(port, '127.0.0.1', () => {
      console.log(`📡 Slides Static Server running at http://127.0.0.1:${port}`);
      resolve(server);
    });
  });
}

async function renderSlideDeck() {
  console.log('=================================================================');
  console.log('🎬 THERMAL SENTINEL GRID — HYPERFRAMES SLIDE DECK RENDER ENGINE');
  console.log('⚡ 10-Slide Investor & Judge Presentation Deck (1920x1080 Full HD)');
  console.log('=================================================================\n');

  const server = await startStaticServer(4180);
  const targetUrl = 'http://127.0.0.1:4180';

  console.log(`🚀 Launching Chromium instance...`);
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

  console.log(`🌐 Opening Slide Deck at ${targetUrl}...`);
  await page.goto(targetUrl, { waitUntil: 'networkidle0', timeout: 30000 });
  await new Promise((r) => setTimeout(r, 1500));

  // Initialize FFmpeg CDP Screencast
  console.log('🎥 Initializing CDP Screencast to FFmpeg Encoder (Constant 30fps Clock)...');
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

  const client = await page.target().createCDPSession();
  await client.send('Page.startScreencast', {
    format: 'jpeg',
    quality: 98,
    maxWidth: 1920,
    maxHeight: 1080,
    everyNthFrame: 1,
  });

  let isStreaming = true;
  let latestBuffer = null;

  client.on('Page.screencastFrame', async ({ data, sessionId }) => {
    latestBuffer = Buffer.from(data, 'base64');
    try {
      await client.send('Page.screencastFrameAck', { sessionId });
    } catch (e) {}
  });

  // Write frames at constant 30fps to guarantee frame-perfect duration
  const frameWriterInterval = setInterval(() => {
    if (isStreaming && latestBuffer) {
      ffmpeg.stdin.write(latestBuffer);
    }
  }, 1000 / 30);

  // Wait for first frame to arrive
  while (!latestBuffer) {
    await new Promise((r) => setTimeout(r, 50));
  }

  const slideSequence = [
    { id: 'slide-1-hazard', title: 'Slide 1: The Invisible 2-Meter Hazard', duration: 7500 },
    { id: 'slide-2-architecture', title: 'Slide 2: 4-Layer Hybrid Physical-AI Architecture', duration: 7500 },
    { id: 'slide-3-moats', title: 'Slide 3: Ten Asymmetric Scientific Moats', duration: 7500 },
    { id: 'slide-4-sandbox', title: 'Slide 4: Unfair Moat #1 — What-If Simulation Studio (<15ms)', duration: 8000 },
    { id: 'slide-5-power-flow', title: 'Slide 5: Unfair Moat #2 — 14-Bus AC Power Flow & Stability', duration: 8000 },
    { id: 'slide-6-72h-heatwave', title: 'Slide 6: Unfair Moat #3 — 72H Compounding Nocturnal Heat', duration: 8000 },
    { id: 'slide-7-portfolio-ops', title: 'Slide 7: Portfolio Ops, Worker Safety (Twb) & COCO Briefs', duration: 8000 },
    { id: 'slide-8-agent-dispatch', title: 'Slide 8: Autonomous Multi-Agent Dispatch & Safety Gate', duration: 8000 },
    { id: 'slide-9-financial', title: 'Slide 9: Investment-Grade Avoided Loss ($2.57M VoLL)', duration: 8000 },
    { id: 'slide-10-leadership', title: 'Slide 10: Track 03 Industrial Category Winner & GTM', duration: 8500 },
  ];

  console.log('🎬 Sequentially presenting all 10 slides...\n');

  for (let i = 0; i < slideSequence.length; i++) {
    const s = slideSequence[i];
    console.log(`  📍 [${i + 1}/10] Presenting ${s.title}...`);
    await page.evaluate((targetId) => {
      window.goToSlide(targetId);
    }, s.id);
    await new Promise((r) => setTimeout(r, s.duration));
  }

  console.log('\n🏁 Slide presentation sequence completed. Finalizing video encoding...');
  isStreaming = false;
  clearInterval(frameWriterInterval);
  await client.send('Page.stopScreencast');
  await browser.close();
  server.close();

  ffmpeg.stdin.end();
  await new Promise((resolve) => ffmpeg.on('close', resolve));

  console.log(`✅ Raw Screencast captured: ${RAW_VIDEO}`);

  // Mux BGM Audio
  if (fs.existsSync(BGM_AUDIO)) {
    console.log(`🎵 Muxing clean ambient background score: ${BGM_AUDIO}...`);
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

    await new Promise((resolve) => muxProcess.on('close', resolve));

    fs.copyFileSync(OUTPUT_VIDEO, PITCH_VIDEO_COPY);
    fs.copyFileSync(OUTPUT_VIDEO, PUBLIC_VIDEO);

    console.log(`🎉 Final Slide Deck Video saved: ${OUTPUT_VIDEO}`);
    console.log(`🎉 Pitch folder copy: ${PITCH_VIDEO_COPY}`);
    console.log(`🎉 Public frontend asset: ${PUBLIC_VIDEO}`);
  } else {
    fs.copyFileSync(RAW_VIDEO, OUTPUT_VIDEO);
    fs.copyFileSync(RAW_VIDEO, PITCH_VIDEO_COPY);
    fs.copyFileSync(RAW_VIDEO, PUBLIC_VIDEO);
    console.log(`🎉 Video saved (silent): ${OUTPUT_VIDEO}`);
  }

  console.log('\n✨ Slide deck video render complete!');
}

renderSlideDeck().catch((err) => {
  console.error('Fatal render error:', err);
  process.exit(1);
});
