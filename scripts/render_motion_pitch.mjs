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

async function renderMotionPitch() {
  console.log('🚀 Launching Puppeteer for Exact Frame-Stepped 1080p Pitch Video Render...');
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1920,1080'],
    defaultViewport: { width: 1920, height: 1080, deviceScaleFactor: 1 },
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });

  const fileUrl = `file://${HTML_PATH}`;
  console.log(`🌐 Loading ${fileUrl}...`);
  await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 30000 });
  await new Promise((r) => setTimeout(r, 1000));

  const totalDuration = 180; // 3 minutes = 180 seconds
  const fps = 30;
  const totalFrames = totalDuration * fps; // 5400 frames

  console.log(`🎬 Rendering ${totalFrames} frames at 30 FPS (1920x1080)...`);

  const ffmpeg = spawn('/opt/homebrew/bin/ffmpeg', [
    '-y',
    '-f', 'image2pipe',
    '-vcodec', 'png',
    '-r', '30',
    '-i', '-',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'fast',
    '-crf', '18',
    RAW_MP4,
  ]);

  ffmpeg.stderr.on('data', () => {});

  const startTime = Date.now();
  for (let f = 0; f < totalFrames; f++) {
    const timeSec = f / fps;
    await page.evaluate((t) => {
      if (window.__timelines && window.__timelines.main) {
        window.__timelines.main.seek(t);
      }
    }, timeSec);

    const buffer = await page.screenshot({ type: 'png' });
    ffmpeg.stdin.write(buffer);

    if (f % 300 === 0 || f === totalFrames - 1) {
      const pct = ((f / totalFrames) * 100).toFixed(1);
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
      console.log(`⏳ Progress: ${pct}% (Frame ${f}/${totalFrames} · Time: ${timeSec.toFixed(1)}s · Elapsed: ${elapsed}s)`);
    }
  }

  ffmpeg.stdin.end();

  await new Promise((resolve) => {
    ffmpeg.on('close', resolve);
  });

  await browser.close();
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

renderMotionPitch().catch((err) => {
  console.error('Fatal render error:', err);
  process.exit(1);
});
