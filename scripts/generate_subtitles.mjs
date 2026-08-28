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

// Subtitle cues aligned with the 248.5s recording
const cues = [
  {
    start: '00:00:01.00',
    end: '00:00:07.50',
    text: '⚡ THERMAL SENTINEL GRID\\nPhysics-Constrained Industrial Thermal Resilience Engine (Track 03)',
  },
  {
    start: '00:00:08.00',
    end: '00:00:14.50',
    text: 'During extreme heatwaves, critical electrical infrastructure sits inside the 2-meter boundary layer above hot asphalt.',
  },
  {
    start: '00:00:15.00',
    end: '00:00:22.00',
    text: 'Standard 25km weather stations miss the localized asphalt heat traps that destroy distribution transformers.',
  },
  {
    start: '00:00:22.50',
    end: '00:00:30.00',
    text: '📍 ACT 1: FortyGuard Live Cloud Ingestion\\nOpening the 2m Boundary Engine with 2,000,000 credit quota.',
  },
  {
    start: '00:00:30.50',
    end: '00:00:38.00',
    text: 'Executing live ingestion across 60-meter microclimate parcel tiles in downtown Phoenix.',
  },
  {
    start: '00:00:38.50',
    end: '00:00:46.00',
    text: '📍 ACT 2: Mission Control — "Fact vs. Finding"\\nFortyGuard captures 42.7°C ambient air with 12 consecutive hours above 40°C.',
  },
  {
    start: '00:00:46.50',
    end: '00:00:54.50',
    text: 'Land-cover delta reaches +1.1°C over natural desert — sustained persistence is what drives equipment aging.',
  },
  {
    start: '00:00:55.00',
    end: '00:01:03.00',
    text: 'Scrubbing the 12-hour heatwave progression from morning cool baseline (35°C) to peak afternoon heat (13:00).',
  },
  {
    start: '00:01:03.50',
    end: '00:01:13.00',
    text: 'Baseline Mode (No Mitigation): Winding hot-spot surges to 159.5°C, causing an 88.4x accelerated insulation aging factor.',
  },
  {
    start: '00:01:13.50',
    end: '00:01:23.50',
    text: 'Thermal Sentinel Mitigated Mode: Proactive BESS peak shaving & radiator staging clamps hot-spot safely to 122.5°C.',
  },
  {
    start: '00:01:24.00',
    end: '00:01:33.50',
    text: 'Physical ECharts Telemetry: Transparent IEEE C57.91 non-linear ODE differential equations and deterministic safety gates.',
  },
  {
    start: '00:01:34.00',
    end: '00:01:43.00',
    text: '📍 ACT 3: Portfolio Operations & Worker Safety\\nRisk-ranked triage sorting substations, solar farms, data centers, and hospitals.',
  },
  {
    start: '00:01:43.50',
    end: '00:01:53.50',
    text: 'Worker Intervention Screen: Monitoring OSHA & NIOSH Wet-Bulb Temperature (Twb) limits to protect utility maintenance crews.',
  },
  {
    start: '00:01:54.00',
    end: '00:02:03.50',
    text: 'COCO Customer Discovery Brief Generator (Thamir / Session 8):\\nSynthesizing Context, Outcomes, Constraints, and Options across 4 sectors.',
  },
  {
    start: '00:02:04.00',
    end: '00:02:13.00',
    text: '1. ⚡ Utility Substation Sector:\\nProtects $2.57M in avoided outage exposure and prevents multi-million dollar transformer blowouts.',
  },
  {
    start: '00:02:13.50',
    end: '00:02:22.00',
    text: '2. 🏢 AI Data Center Sector:\\nOptimizes facility PUE and prevents GPU cluster thermal throttling during regional grid peaks.',
  },
  {
    start: '00:02:22.50',
    end: '00:02:30.50',
    text: '3. ☀️ Solar & BESS IPP Sector:\\nMitigates inverter thermal derating and prevents lithium battery degradation runaway.',
  },
  {
    start: '00:02:31.00',
    end: '00:02:39.50',
    text: '4. 🏥 Hospital Trauma Center Sector:\\nGuarantees continuous backup power reliability and life-safety compliance.',
  },
  {
    start: '00:02:40.00',
    end: '00:02:48.00',
    text: 'Auditable Mitigation Evidence:\\nExporting Model Context Protocol (MCP) tool calls with cryptographic SHA-256 tamper-proof ledger hashes.',
  },
  {
    start: '00:02:48.50',
    end: '00:02:57.50',
    text: '📍 ACT 4: Hyperlocal 2m GIS & Spatial Causality\\n60m parcel heatmap showing UHI root cause: 78% impervious asphalt vs. 2% canopy cover.',
  },
  {
    start: '00:02:58.00',
    end: '00:03:07.50',
    text: '📍 ACT 5: LangGraph Multi-Agent Stack & Deterministic Safety Gate\\n5-node StateGraph DAG (Forecast → Physics → Planner → Safety Gate → Audit Dispatch).',
  },
  {
    start: '00:03:08.00',
    end: '00:03:17.50',
    text: 'Deterministic Non-LLM Safety Gate:\\nVerifies candidate actions against ANSI C84.1 voltage and IEEE thermal limits before dispatch.',
  },
  {
    start: '00:03:18.00',
    end: '00:03:28.00',
    text: 'Live Agent Execution: Generating automated B2B utility work orders and public citizen heat advisories in real-time.',
  },
  {
    start: '00:03:28.50',
    end: '00:03:39.00',
    text: '📍 ACT 6: Avoided Loss Financial Model & Executive ROI\\n$2,566,193 net avoided loss per heat event, $540k replacement deferral, and 5,472x ROI multiple.',
  },
  {
    start: '00:03:39.50',
    end: '00:03:50.00',
    text: '365.4 equivalent transformer aging hours saved per heatwave episode — turning microclimate data into hard enterprise value.',
  },
  {
    start: '00:03:50.50',
    end: '00:04:08.00',
    text: '📍 ACT 7: Conclusion\\nThermal Sentinel Grid: Physical AI & Industrial Resilience for the World\'s Energy Grid.',
  },
];

function generateSRT() {
  let srt = '';
  cues.forEach((c, idx) => {
    const s = c.start.replace('.', ',');
    const e = c.end.replace('.', ',');
    const t = c.text.replace(/\\n/g, '\n');
    srt += `${idx + 1}\n0${s}0 --> 0${e}0\n${t}\n\n`;
  });
  return srt;
}

function generateVTT() {
  let vtt = 'WEBVTT\n\n';
  cues.forEach((c, idx) => {
    const t = c.text.replace(/\\n/g, '\n');
    vtt += `${idx + 1}\n0${c.start}0 --> 0${c.end}0\n${t}\n\n`;
  });
  return vtt;
}

function generateASS() {
  let ass = `[Script Info]
Title: Thermal Sentinel Grid Demo Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Helvetica,26,&H00FFFFFF,&H000000FF,&H00000000,&HA0050810,-1,0,0,0,100,100,0,0,3,3,0,2,40,40,48,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
`;

  cues.forEach((c) => {
    // Format: 0:00:01.00
    const start = `0:${c.start.substring(3)}`;
    const end = `0:${c.end.substring(3)}`;
    ass += `Dialogue: 0,${start},${end},Default,,0,0,0,,${c.text}\n`;
  });

  return ass;
}

async function run() {
  console.log('📝 Generating Subtitle Files (.srt, .vtt & .ass)...');
  const srtContent = generateSRT();
  const vttContent = generateVTT();
  const assContent = generateASS();

  fs.writeFileSync(SRT_FILE, srtContent, 'utf-8');
  fs.writeFileSync(VTT_FILE, vttContent, 'utf-8');
  fs.writeFileSync(ASS_FILE, assContent, 'utf-8');
  fs.writeFileSync(PUBLIC_VTT, vttContent, 'utf-8');

  console.log(`✅ SRT generated: ${SRT_FILE}`);
  console.log(`✅ VTT generated: ${VTT_FILE}`);
  console.log(`✅ ASS generated: ${ASS_FILE}`);
  console.log(`✅ Public VTT updated: ${PUBLIC_VTT}`);

  if (fs.existsSync(INPUT_VIDEO)) {
    console.log(`🎥 Burning styled subtitles into dedicated video: ${SUBTITLED_VIDEO}...`);
    const srtDir = path.dirname(SRT_FILE);
    const burnProcess = spawn(FFMPEG, [
      '-y',
      '-i', 'business_value_demo.mp4',
      '-vf', 'ass=business_value_demo.ass',
      '-c:v', 'libx264',
      '-preset', 'veryfast',
      '-crf', '17',
      '-c:a', 'copy',
      'business_value_demo_subtitled.mp4',
    ], {
      cwd: srtDir,
    });

    burnProcess.stderr.on('data', (d) => {
      const msg = d.toString();
      if (msg.includes('Error') || msg.includes('failed')) {
        console.error('FFmpeg stderr:', msg);
      }
    });

    const exitCode = await new Promise((resolve) => {
      burnProcess.on('close', resolve);
    });

    if (exitCode !== 0) {
      throw new Error(`FFmpeg exited with code ${exitCode}`);
    }

    fs.copyFileSync(SUBTITLED_VIDEO, PUBLIC_SUBTITLED_VIDEO);
    console.log(`🎉 Subtitled Video successfully created: ${SUBTITLED_VIDEO}`);
    console.log(`🎉 Public Subtitled Video updated: ${PUBLIC_SUBTITLED_VIDEO}`);
  }
}

run().catch((e) => {
  console.error('Error generating subtitles:', e);
  process.exit(1);
});
