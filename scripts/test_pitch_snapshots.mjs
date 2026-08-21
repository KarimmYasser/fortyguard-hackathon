import puppeteer from 'puppeteer';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');

const HTML_PATH = path.resolve(projectRoot, 'videos/thermal-sentinel-pitch/index.html');
const SNAPSHOTS_DIR = path.resolve(projectRoot, 'scratch/pitch_snapshots');

fs.mkdirSync(SNAPSHOTS_DIR, { recursive: true });

async function checkSnapshots() {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
    defaultViewport: { width: 1920, height: 1080 },
  });

  const page = await browser.newPage();
  await page.goto(`file://${HTML_PATH}`, { waitUntil: 'networkidle0' });

  const testTimes = [
    { t: 5, name: 'scene1_5s.png' },
    { t: 35, name: 'scene2_35s.png' },
    { t: 65, name: 'scene3_65s.png' },
    { t: 95, name: 'scene4_95s.png' },
    { t: 140, name: 'scene5_140s.png' },
    { t: 170, name: 'scene6_170s.png' },
  ];

  for (const item of testTimes) {
    await page.evaluate((seekT) => {
      if (window.__timelines && window.__timelines.main) {
        window.__timelines.main.seek(seekT);
      }
    }, item.t);

    await new Promise((r) => setTimeout(r, 200));
    const snapPath = path.join(SNAPSHOTS_DIR, item.name);
    await page.screenshot({ path: snapPath });
    console.log(`📸 Saved snapshot at ${item.t}s: ${snapPath}`);
  }

  await browser.close();
  console.log('✅ All test snapshots captured!');
}

checkSnapshots().catch(console.error);
