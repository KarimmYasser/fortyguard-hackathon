import puppeteer from 'puppeteer';
import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');

const HTML_PATH = path.resolve(projectRoot, 'videos/thermal-sentinel-pitch/index.html');
const OUTPUT_VIDEO = path.resolve(projectRoot, 'videos/thermal-sentinel-pitch/renders/video_with_audio.mp4');
const RAW_VIDEO_SILENT = path.resolve(projectRoot, 'videos/thermal-sentinel-pitch/renders/video.mp4');
const PUBLIC_VIDEO = path.resolve(projectRoot, 'frontend/public/videos/video_with_audio.mp4');
const PUBLIC_SILENT = path.resolve(projectRoot, 'frontend/public/videos/video.mp4');
const BGM_AUDIO = path.resolve(projectRoot, 'videos/thermal-sentinel-pitch/assets/audio/bgm_cyber_ambient.mp3');
const RAW_MP4 = path.resolve(projectRoot, 'scratch/raw_motion_pitch.mp4');

fs.mkdirSync(path.dirname(OUTPUT_VIDEO), { recursive: true });
fs.mkdirSync(path.dirname(PUBLIC_VIDEO), { recursive: true });
fs.mkdirSync(path.dirname(RAW_MP4), { recursive: true });

async function recordMotionPitch() {
  console.log('🚀 Launching Puppeteer for Real-Time 1080p Pitch Video Capture...');
  const browser = await puppeteer.launch({
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--window-size=1920,1080',
      '--disable-gpu-sandbox',
      '--enable-features=NetworkService,NetworkServiceInProcess',
    ],
    defaultViewport: { width: 1920, height: 1080, deviceScaleFactor: 1 },
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });

  const fileUrl = `file://${HTML_PATH}`;
  console.log(`🌐 Loading ${fileUrl}...`);
  await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 30000 });
  await new Promise((r) => setTimeout(r, 1000));

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
    '-crf', '17',
    RAW_MP4,
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

  console.log('🎬 Playing GSAP Timeline (180 seconds)...');
  await page.evaluate(() => {
    if (window.__timelines && window.__timelines.main) {
      window.__timelines.main.play(0);
    }
  });

  const totalSeconds = 180;
  for (let s = 0; s < totalSeconds; s += 10) {
    await new Promise((r) => setTimeout(r, 10000));
    console.log(`⏳ Progress: ${s + 10}s / ${totalSeconds}s (${Math.round(((s + 10) / totalSeconds) * 100)}%)...`);
  }

  // Small buffer at end
  await new Promise((r) => setTimeout(r, 1000));

  console.log('🏁 Animation completed. Stopping screencast...');
  isStreaming = false;
  await client.send('Page.stopScreencast');
  await browser.close();

  ffmpeg.stdin.end();

  await new Promise((resolve) => {
    ffmpeg.on('close', resolve);
  });

  console.log(`✅ Raw silent video created: ${RAW_MP4}`);

  // Copy to silent outputs
  fs.copyFileSync(RAW_MP4, RAW_VIDEO_SILENT);
  fs.copyFileSync(RAW_MP4, PUBLIC_SILENT);

  // Mux BGM Audio (No Voiceover)
  console.log(`🎵 Muxing clean background sound (No Voiceover): ${BGM_AUDIO}...`);
  const muxProcess = spawn('/opt/homebrew/bin/ffmpeg', [
    '-y',
    '-i', RAW_MP4,
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
  console.log(`🎉 Final Video with BGM saved: ${OUTPUT_VIDEO}`);
  console.log(`🎉 Public frontend asset updated: ${PUBLIC_VIDEO}`);
}

recordMotionPitch().catch((err) => {
  console.error('Fatal recording error:', err);
  process.exit(1);
});
