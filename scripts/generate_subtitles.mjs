import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');

const SRT_FILE = path.resolve(projectRoot, 'videos/thermal-sentinel-pitch/renders/business_value_demo.srt');
const VTT_FILE = path.resolve(projectRoot, 'videos/thermal-sentinel-pitch/renders/business_value_demo.vtt');
const ASS_FILE = path.resolve(projectRoot, 'videos/thermal-sentinel-pitch/renders/business_value_demo.ass');
const PUBLIC_VTT = path.resolve(projectRoot, 'frontend/public/videos/business_value_demo.vtt');
const INPUT_VIDEO = path.resolve(projectRoot, 'videos/thermal-sentinel-pitch/renders/business_value_demo.mp4');
const SUBTITLED_VIDEO = path.resolve(projectRoot, 'videos/thermal-sentinel-pitch/renders/business_value_demo_subtitled.mp4');
const PUBLIC_SUBTITLED_VIDEO = path.resolve(projectRoot, 'frontend/public/videos/business_value_demo_subtitled.mp4');

const FFMPEG = process.env.FFMPEG_PATH || (fs.existsSync('/opt/homebrew/bin/ffmpeg') ? '/opt/homebrew/bin/ffmpeg' : 'ffmpeg');

// Subtitle cues aligned with the 157.9s 9-Act recording
const cues = [
  {
    start: '00:00:01.00',
    end: '00:00:08.00',
    text: '⚡ THERMAL SENTINEL GRID\\nPhysical-AI Industrial Thermal Resilience Engine (Track 03)',
  },
  {
    start: '00:00:08.50',
    end: '00:00:16.00',
    text: 'During extreme heatwaves, critical electrical infrastructure sits inside the 2-meter boundary layer above asphalt.',
  },
  {
    start: '00:00:16.50',
    end: '00:00:24.00',
    text: '📍 ACT 1: FortyGuard Live Cloud Ingestion\\nConnecting to the 2m Boundary Engine with 2,000,000 credit quota.',
  },
  {
    start: '00:00:24.50',
    end: '00:00:32.00',
    text: 'Executing live ingestion across 60m parcel tiles in downtown Phoenix.',
  },
  {
    start: '00:00:32.50',
    end: '00:00:40.00',
    text: '📍 ACT 2: Mission Control — "Fact vs. Finding"\\nFortyGuard captures 42.7°C ambient air with 12 unbroken hours above 40°C.',
  },
  {
    start: '00:00:40.50',
    end: '00:00:48.00',
    text: 'Scrubbing 12-hour heatwave progression from morning baseline (35°C) to peak afternoon heat (13:00).',
  },
  {
    start: '00:00:48.50',
    end: '00:00:56.50',
    text: 'Baseline Mode: Hot-spot surges to 159.5°C (88.4x aging) vs. Mitigated Mode safely clamped to 122.5°C.',
  },
  {
    start: '00:00:57.00',
    end: '00:01:05.00',
    text: '📍 ACT 3: UNFAIR MOAT #1 — What-If Simulation Studio\\nSub-15ms live ODE recalculations as sliders and scenario presets modulate.',
  },
  {
    start: '00:01:05.50',
    end: '00:01:13.50',
    text: 'Testing 31-Day Desertification & AI Data Center presets to pass the judge "Kill-Switch" test.',
  },
  {
    start: '00:01:14.00',
    end: '00:01:22.50',
    text: '📍 ACT 4: UNFAIR MOAT #2 — 14-Bus AC Power Flow & Grid Stability\\nNewton-Raphson power flow, ANSI C84.1 voltage regulation (0.95-1.05 pu) & 100% hospital uptime.',
  },
  {
    start: '00:01:23.00',
    end: '00:01:31.50',
    text: 'Dynamic line rating (IEEE 738) and BESS Volt/VAR support protecting critical feeders.',
  },
  {
    start: '00:01:32.00',
    end: '00:01:40.50',
    text: '📍 ACT 5: UNFAIR MOAT #3 — 72-Hour Compounding Nocturnal Heat\\nJuly 24–26 multi-day replay modeling asphalt heat retention (>36°C night) and equipment pre-heating.',
  },
  {
    start: '00:01:41.00',
    end: '00:01:49.00',
    text: '📍 ACT 6: Portfolio Operations & Worker Safety\\nRisk-ranked fleet triage and OSHA/NIOSH Wet-Bulb (Twb) maintenance shift window screening.',
  },
  {
    start: '00:01:49.50',
    end: '00:01:58.00',
    text: 'COCO Customer Discovery Briefs across 4 sectors: Utility ($2.57M saved), Data Center, Solar IPP & Hospital.',
  },
  {
    start: '00:01:58.50',
    end: '00:02:07.00',
    text: '📍 ACT 7: Hyperlocal 2m GIS & Spatial Causality\\n60m parcel heatmap revealing UHI root cause: 78% impervious asphalt vs. 2% tree canopy.',
  },
  {
    start: '00:02:07.50',
    end: '00:02:16.50',
    text: '📍 ACT 8: LangGraph Multi-Agent Stack & Deterministic Safety Gate\\n5-node StateGraph DAG (Forecast → Physics → Planner → Safety Gate → Dispatch).',
  },
  {
    start: '00:02:17.00',
    end: '00:02:26.00',
    text: 'Non-LLM Safety Gate verifies all dispatch actions before issuing automated B2B utility work orders.',
  },
  {
    start: '00:02:26.50',
    end: '00:02:35.00',
    text: '📍 ACT 9: Avoided Loss Financial Model & Executive ROI\\n$2,566,193 net avoided loss (180 MWh VoLL), $540k replacement deferral, and 5,472x ROI multiple.',
  },
  {
    start: '00:02:35.50',
    end: '00:02:44.00',
    text: '365.4 equivalent transformer aging hours saved per heatwave episode.',
  },
  {
    start: '00:02:44.50',
    end: '00:02:57.00',
    text: '⚡ Thermal Sentinel Grid: Industrial Physical-AI Resilience for the World\'s Energy Grids.\\nTest live at www.thermal-sentinel-grid.live',
  },
];

function formatTimeSRT(timeStr) {
  const [hms, cs] = timeStr.split('.');
  const ms = (parseInt(cs, 10) * 10).toString().padStart(3, '0');
  return `${hms},${ms}`;
}

function formatTimeVTT(timeStr) {
  return timeStr;
}

function formatTimeASS(timeStr) {
  const [hms, cs] = timeStr.split('.');
  const [h, m, s] = hms.split(':');
  const hNum = parseInt(h, 10);
  return `${hNum}:${m}:${s}.${cs}`;
}

function generateSRT() {
  let srt = '';
  cues.forEach((cue, index) => {
    srt += `${index + 1}\n`;
    srt += `${formatTimeSRT(cue.start)} --> ${formatTimeSRT(cue.end)}\n`;
    srt += `${cue.text.replace(/\\n/g, '\n')}\n\n`;
  });
  return srt;
}

function generateVTT() {
  let vtt = 'WEBVTT - Thermal Sentinel Grid Business Value Walkthrough\n\n';
  cues.forEach((cue, index) => {
    vtt += `${index + 1}\n`;
    vtt += `${formatTimeVTT(cue.start)} --> ${formatTimeVTT(cue.end)}\n`;
    vtt += `${cue.text.replace(/\\n/g, '\n')}\n\n`;
  });
  return vtt;
}

function generateASS() {
  let ass = `[Script Info]
Title: Thermal Sentinel Grid Walkthrough Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,36,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,2,2,40,40,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
`;
  cues.forEach((cue) => {
    const textFormatted = cue.text.replace(/\\n/g, '\\N');
    ass += `Dialogue: 0,${formatTimeASS(cue.start)},${formatTimeASS(cue.end)},Default,,0,0,0,,${textFormatted}\n`;
  });
  return ass;
}

async function run() {
  console.log('📝 Generating Subtitle Files (.srt, .vtt, .ass)...');
  
  const srtContent = generateSRT();
  fs.writeFileSync(SRT_FILE, srtContent, 'utf-8');
  console.log(`✅ Saved: ${SRT_FILE}`);

  const vttContent = generateVTT();
  fs.writeFileSync(VTT_FILE, vttContent, 'utf-8');
  fs.writeFileSync(PUBLIC_VTT, vttContent, 'utf-8');
  console.log(`✅ Saved: ${VTT_FILE}`);
  console.log(`✅ Saved: ${PUBLIC_VTT}`);

  const assContent = generateASS();
  fs.writeFileSync(ASS_FILE, assContent, 'utf-8');
  console.log(`✅ Saved: ${ASS_FILE}`);

  // Embed subtitles into MP4
  if (fs.existsSync(INPUT_VIDEO)) {
    console.log('\n🎬 Embedding Subtitle Track into MP4 using mov_text...');
    const ffmpegProcess = spawn(FFMPEG, [
      '-y',
      '-i', INPUT_VIDEO,
      '-i', SRT_FILE,
      '-c:v', 'copy',
      '-c:a', 'copy',
      '-c:s', 'mov_text',
      '-metadata:s:s:0', 'language=eng',
      '-metadata:s:s:0', 'title=English Subtitles',
      SUBTITLED_VIDEO,
    ]);

    await new Promise((resolve, reject) => {
      ffmpegProcess.on('close', (code) => {
        if (code === 0) {
          console.log(`✅ Subtitled Video Created: ${SUBTITLED_VIDEO}`);
          fs.copyFileSync(SUBTITLED_VIDEO, PUBLIC_SUBTITLED_VIDEO);
          console.log(`✅ Public Asset Updated: ${PUBLIC_SUBTITLED_VIDEO}`);
          resolve();
        } else {
          console.warn(`⚠️ FFmpeg subtitling exited with code ${code}`);
          resolve();
        }
      });
    });
  }

  console.log('\n🎉 Subtitle generation and embedding completed!');
}

run().catch((err) => {
  console.error('Fatal subtitle error:', err);
  process.exit(1);
});
