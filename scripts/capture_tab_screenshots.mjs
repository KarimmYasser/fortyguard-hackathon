import puppeteer from 'puppeteer';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');
const DASHBOARD_DIR = path.resolve(projectRoot, 'videos/thermal-sentinel-pitch/assets/dashboard');

fs.mkdirSync(DASHBOARD_DIR, { recursive: true });

const tabsToCapture = [
  { tabText: 'Pitch & Video', filename: 'dashboard_home.png' },
  { tabText: 'Mission Control', filename: 'dashboard_overview.png' },
  { tabText: 'What-If Studio', filename: 'dashboard_sandbox.png' },
  { tabText: '72h Compounding', filename: 'dashboard_72h_heatwave.png' },
  { tabText: 'AC Power Flow', filename: 'dashboard_power_flow.png' },
  { tabText: 'IEEE Annex G', filename: 'dashboard_ieee_annex_g.png' },
  { tabText: 'Academic Provenance', filename: 'dashboard_academic_provenance.png' },
  { tabText: 'Hyperlocal 2m GIS', filename: 'dashboard_gis_map.png' },
  { tabText: '4 Scientific Moats', filename: 'dashboard_physics_moats.png' },
  { tabText: 'LangGraph Engine', filename: 'dashboard_agent_graph.png' },
  { tabText: 'Avoided Loss ROI', filename: 'dashboard_financial_roi.png' },
  { tabText: 'Data Science Studio', filename: 'dashboard_data_science.png' },
];

async function captureAllTabs() {
  console.log('🚀 Launching Puppeteer to capture all tab screenshots in 1920x1080...');
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1920,1080'],
    defaultViewport: { width: 1920, height: 1080, deviceScaleFactor: 2 },
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 2 });

  const TARGET_URL = process.env.TARGET_URL || 'https://fortyguard-hackathon.vercel.app';
  console.log(`🌐 Opening ${TARGET_URL} ...`);
  await page.goto(TARGET_URL, { waitUntil: 'networkidle0', timeout: 30000 });
  await page.waitForSelector('nav button', { timeout: 30000 });
  await new Promise((r) => setTimeout(r, 2500));

  const available = await page.evaluate(() =>
    Array.from(document.querySelectorAll('nav button')).map((b) => b.textContent.trim()));
  const missing = tabsToCapture.map((t) => t.tabText).filter((l) => !available.includes(l));
  if (missing.length) {
    console.error('❌ Tab labels not present in the UI:', missing);
    console.error('   Available:', available);
    await browser.close();
    process.exit(1);
  }

  const failures = [];
  for (const { tabText, filename } of tabsToCapture) {
    console.log(`📸 Capturing tab: "${tabText}" -> ${filename}...`);
    try {
      const clicked = await page.evaluate((text) => {
        const btn = Array.from(document.querySelectorAll('nav button'))
          .find((b) => b.textContent.trim() === text);
        if (!btn) return false;
        btn.click();
        return true;
      }, tabText);
      if (!clicked) throw new Error(`tab button "${tabText}" disappeared`);

      // Charts, maps and KaTeX need a beat to lay out after the tab swaps.
      await new Promise((r) => setTimeout(r, 2200));

      const outPath = path.resolve(DASHBOARD_DIR, filename);
      await page.screenshot({ path: outPath, type: 'png' });
      console.log(`✅ Saved ${outPath}`);
    } catch (err) {
      console.error(`❌ Failed capturing tab "${tabText}":`, err.message);
      failures.push(tabText);
    }
  }

  await browser.close();

  if (failures.length) {
    console.error(`\n❌ ${failures.length} tab(s) failed: ${failures.join(', ')}`);
    process.exit(1);
  }
  console.log(`\n🎉 Captured ${tabsToCapture.length} tabs to ${DASHBOARD_DIR}`);
}

captureAllTabs().catch((err) => {
  console.error('Fatal error:', err);
  process.exit(1);
});
