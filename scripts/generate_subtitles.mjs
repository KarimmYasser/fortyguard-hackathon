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

// Subtitle cues aligned with the complete interactive speech
const cues = [
  {
    start: '00:00:01.00',
    end: '00:00:07.50',
    text: '⚡ THERMAL SENTINEL GRID\\nTrack 03: Industrial & Enterprise (FortyGuard Hackathon \'26)',
  },
  {
    start: '00:00:07.80',
    end: '00:00:15.00',
    text: 'In extreme heatwaves, electric utilities manage billions of dollars in substation transformers using airport weather stations 10 miles away.',
  },
  {
    start: '00:00:15.30',
    end: '00:00:22.00',
    text: 'But equipment actually sits in the 2-meter boundary layer above radiating asphalt.',
  },
  {
    start: '00:00:22.30',
    end: '00:00:29.50',
    text: 'Right here, we ingest FortyGuard\'s live 2-meter Temperature AI in real time across 60-meter microclimate parcel tiles.',
  },
  {
    start: '00:00:29.80',
    end: '00:00:36.50',
    text: 'Here we can see the real-time numbers of the scan we just generated.',
  },
  {
    start: '00:00:36.80',
    end: '00:00:44.50',
    text: 'Now let\'s return to our canonical benchmark—our evidence contract explicitly distinguishes what uses real live API data from what is modeled.',
  },
  {
    start: '00:00:44.80',
    end: '00:00:51.50',
    text: 'Following FortyGuard\'s core doctrine: 42.7°C is just a fact. The finding is what truly matters.',
  },
  {
    start: '00:00:51.80',
    end: '00:01:00.00',
    text: 'Watch what happens at 1:00 PM: under unmitigated baseline operation, winding hot-spot surges to 159.5°C—accelerating aging by 88 times!',
  },
  {
    start: '00:01:00.30',
    end: '00:01:05.50',
    text: 'The graphs speak for themselves.',
  },
  {
    start: '00:01:05.80',
    end: '00:01:14.00',
    text: 'When we engage Thermal Sentinel mitigation, our engine coordinates proactive pre-cooling and battery support, safely clamping the hot-spot to 122.5°C.',
  },
  {
    start: '00:01:14.30',
    end: '00:01:23.00',
    text: 'Here is our core engineering moat: our interactive What-If Studio re-solves non-linear IEEE differential equations in under 15 milliseconds live.',
  },
  {
    start: '00:01:23.30',
    end: '00:01:31.50',
    text: 'Dumb threshold rules create false alarms on 20-minute heat spikes, or miss silent 12-hour thermal destruction on dry soil.',
  },
  {
    start: '00:01:31.80',
    end: '00:01:40.00',
    text: 'We don\'t use arbitrary rules—we use exact thermodynamic physics to gate our decisions, eliminating both false positives and false negatives.',
  },
  {
    start: '00:01:40.30',
    end: '00:01:46.50',
    text: 'We don\'t just model temperature—we model full AC power flow.',
  },
  {
    start: '00:01:46.80',
    end: '00:01:55.50',
    text: 'Our engine enforces ANSI C84.1 voltage stability and dynamic line thermal ratings, guaranteeing 100% continuous uptime for trauma hospital feeders.',
  },
  {
    start: '00:01:55.80',
    end: '00:02:03.00',
    text: 'Single-day peak temperature is an amateur metric. In the desert, asphalt fails to cool below 36°C overnight.',
  },
  {
    start: '00:02:03.30',
    end: '00:02:11.50',
    text: 'Our 72-hour compounding engine models nocturnal heat accumulation, showing how uncooled transformers start Day 2 and Day 3 already pre-heated.',
  },
  {
    start: '00:02:11.80',
    end: '00:02:20.50',
    text: 'In Portfolio Operations, we rank critical assets across the entire city fleet and screen maintenance shift windows using OSHA/NIOSH Wet-Bulb limits.',
  },
  {
    start: '00:02:20.80',
    end: '00:02:29.00',
    text: 'We also generate COCO Customer Discovery Briefs across 4 key enterprise buyers: Utilities, AI Data Centers, Solar IPPs, and Hospitals.',
  },
  {
    start: '00:02:29.30',
    end: '00:02:37.50',
    text: 'Our autonomous dispatch runs on a 5-node LangGraph StateGraph, protected by a deterministic non-LLM safety gate.',
  },
  {
    start: '00:02:37.80',
    end: '00:02:46.50',
    text: 'Financially, Thermal Sentinel Grid is an acute painkiller: saving ~$2.57M in catastrophic outage and equipment replacement exposure per heatwave (5,472x ROI).',
  },
  {
    start: '00:02:46.80',
    end: '00:02:54.00',
    text: 'Finally, before I close, we have our video integrated directly inside the site, along with an interactive Tour Guide button across every window.',
  },
  {
    start: '00:02:54.30',
    end: '00:03:01.50',
    text: 'You can explore our Live Cloud Database (17 Tables) and review all peer-reviewed research in our Academic Provenance tab.',
  },
  {
    start: '00:03:01.80',
    end: '00:03:10.00',
    text: '⚡ Thank you, and we invite you to test our live platform at thermal-sentinel-grid.live!',
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
