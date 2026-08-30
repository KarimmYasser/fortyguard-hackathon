import asyncio
import os
import subprocess
import edge_tts

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'videos/thermal-sentinel-pitch/renders')
VOICEOVER_MP3 = os.path.join(OUTPUT_DIR, 'voiceover_natural.mp3')
VOICEOVER_WITH_BGM = os.path.join(OUTPUT_DIR, 'voiceover_with_bgm.mp3')
BGM_AUDIO = os.path.join(PROJECT_ROOT, 'videos/thermal-sentinel-pitch/assets/audio/bgm_cyber_ambient.mp3')
SRT_FILE = os.path.join(OUTPUT_DIR, 'voiceover_subtitles.srt')
VTT_FILE = os.path.join(OUTPUT_DIR, 'voiceover_subtitles.vtt')
PUBLIC_VTT = os.path.join(PROJECT_ROOT, 'frontend/public/videos/business_value_demo.vtt')

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Select a natural, deep, confident neural voice:
# "en-US-ChristopherNeural" (Confident, authoritative, conversational tech founder)
# "en-US-AndrewNeural" (Warm, professional, crisp)
# "en-US-GuyNeural" (Clear, direct, engaging)
VOICE = "en-US-ChristopherNeural"
RATE = "-2%" # Slightly relaxed, natural human speaking pace

SCRIPT_SECTIONS = [
    {
        "id": "act1_intro",
        "text": "Hey everyone, this is Thermal Sentinel Grid for Track 03: Industrial & Enterprise. During extreme heatwaves, electric utilities manage billions of dollars in substation transformers using airport weather stations 10 miles away. But equipment actually sits in the 2-meter boundary layer above hot asphalt. Right here, we ingest FortyGuard's live 2-meter Temperature AI in real time across 60-meter microclimate parcel tiles.",
        "pause_after": 1.2
    },
    {
        "id": "act1_scan",
        "text": "Here we can see the real-time numbers of the scan we just generated. Now let's return to our canonical benchmark—our evidence contract explicitly distinguishes what uses real live API data from what is modeled.",
        "pause_after": 1.4
    },
    {
        "id": "act2_mission_control",
        "text": "Following FortyGuard's core doctrine: 42.7°C is just a fact. The finding is what truly matters. Watch what happens at 1:00 PM: under unmitigated baseline operation, the transformer winding hot-spot surges to a catastrophic 159.5°C—accelerating insulation aging by 88 times! We can see the graphs talk for themselves. When we turn on Thermal Sentinel mitigation, our engine coordinates proactive pre-cooling and battery support, safely clamping the hot-spot to 122.5°C.",
        "pause_after": 1.4
    },
    {
        "id": "act3_what_if",
        "text": "Here is our core engineering moat: our interactive What-If Studio re-solves non-linear IEEE differential equations in under 15 milliseconds as I move these sliders live. Why does this matter? Dumb threshold rules create false alarms on 20-minute heat spikes, or miss silent 12-hour thermal destruction on dry soil. We don't use arbitrary threshold rules—we use exact thermodynamic physics to gate our decisions, eliminating both false positives and false negatives.",
        "pause_after": 1.4
    },
    {
        "id": "act4_power_flow",
        "text": "We don't just model temperature—we model full AC power flow. Our engine enforces ANSI C84.1 voltage stability and dynamic line thermal ratings, actively tuning transformer tap changers and BESS reactive power to guarantee 100% continuous uptime for critical trauma hospital feeders.",
        "pause_after": 1.4
    },
    {
        "id": "act5_72h_heatwave",
        "text": "Single-day peak temperature is an amateur metric. In the desert, asphalt fails to cool below 36°C overnight. Our 72-hour compounding engine models nocturnal heat accumulation, showing how uncooled transformers start Day 2 and Day 3 already pre-heated.",
        "pause_after": 1.4
    },
    {
        "id": "act6_portfolio_ops",
        "text": "In Portfolio Operations, we rank critical assets across the entire city fleet and screen maintenance shift windows using OSHA and NIOSH Wet-Bulb temperature limits to protect utility field crews from heat stroke. We also generate COCO Customer Discovery Briefs across 4 key enterprise buyers: Utilities, AI Data Centers, Solar IPPs, and Hospitals.",
        "pause_after": 1.4
    },
    {
        "id": "act7_agent_roi",
        "text": "Our autonomous dispatch runs on a 5-node LangGraph StateGraph, protected by a deterministic non-LLM safety gate that prevents unauthorized breaker trips and generates auditable B2B work orders. Financially, Thermal Sentinel Grid is an acute painkiller: saving approximately $2.57 million in catastrophic outage and equipment replacement exposure per heatwave episode, delivering a 5,472x ROI.",
        "pause_after": 1.4
    },
    {
        "id": "act8_tour_outro",
        "text": "Finally, before I close the video, I want to invite you to a very quick tour. We have our presentation video integrated directly inside the site, along with an interactive Tour Guide button that walks you through every single window. You can also explore our live cloud database insights across 17 tables, and inspect all peer-reviewed research papers in our Academic Provenance tab. Thank you, and we invite you to test our live platform at thermal-sentinel-grid.live!",
        "pause_after": 1.0
    }
]

def format_time_srt(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def format_time_vtt(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

def get_audio_duration(file_path: str) -> float:
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        file_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        return float(res.stdout.strip())
    except:
        return 0.0

async def generate_voiceover():
    print("=================================================================")
    print("🎙️ THERMAL SENTINEL GRID — NATURAL HUMAN NEURAL TTS GENERATOR")
    print(f"🗣️ Voice: {VOICE} | Speed Rate: {RATE} (Unhurried, Confident, Natural)")
    print("=================================================================\n")

    temp_files = []
    cues = []
    current_time = 0.5 # start with 0.5s breathing space

    for idx, sec in enumerate(SCRIPT_SECTIONS):
        temp_mp3 = os.path.join(OUTPUT_DIR, f"temp_chunk_{idx}.mp3")
        temp_files.append(temp_mp3)

        print(f"  🔊 Synthesizing chunk {idx+1}/{len(SCRIPT_SECTIONS)} ({sec['id']})...")
        communicate = edge_tts.Communicate(sec['text'], VOICE, rate=RATE)
        await communicate.save(temp_mp3)

        duration = get_audio_duration(temp_mp3)
        end_time = current_time + duration

        cues.append({
            "index": idx + 1,
            "start": current_time,
            "end": end_time,
            "text": sec['text']
        })

        current_time = end_time + sec['pause_after']

    print("\n🔗 Stitching audio chunks with natural conversational pauses...")
    
    # Build ffmpeg filter_complex for seamless concatenation with exact silence gaps
    inputs = []
    filter_parts = []
    for idx, f in enumerate(temp_files):
        inputs.extend(['-i', f])
        pause = SCRIPT_SECTIONS[idx]['pause_after']
        filter_parts.append(f"[{idx}:a]apad=pad_dur={pause}[a{idx}]")

    concat_inputs = "".join([f"[a{i}]" for i in range(len(temp_files))])
    filter_complex = ";".join(filter_parts) + f";{concat_inputs}concat=n={len(temp_files)}:v=0:a=1[outa]"

    cmd = ['ffmpeg', '-y'] + inputs + ['-filter_complex', filter_complex, '-map', '[outa]', '-c:a', 'libmp3lame', '-b:a', '192k', VOICEOVER_MP3]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Clean up temp chunks
    for f in temp_files:
        if os.path.exists(f):
            os.remove(f)

    total_duration = get_audio_duration(VOICEOVER_MP3)
    print(f"✅ Generated Clean Voiceover MP3: {VOICEOVER_MP3}")
    print(f"⏱️ Total Natural Voiceover Duration: {total_duration:.2f} seconds ({int(total_duration//60)}m {int(total_duration%60)}s)\n")

    # Mux Voiceover with subtle background music bed
    if os.path.exists(BGM_AUDIO):
        print(f"🎵 Mixing Voiceover with Ambient BGM (-22 dB ducking)...")
        # Duck BGM to -22dB and mix with 0dB voiceover
        mix_cmd = [
            'ffmpeg', '-y',
            '-i', VOICEOVER_MP3,
            '-i', BGM_AUDIO,
            '-filter_complex', '[1:a]volume=0.08[bgm];[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[outa]',
            '-map', '[outa]',
            '-c:a', 'libmp3lame',
            '-b:a', '192k',
            VOICEOVER_WITH_BGM
        ]
        subprocess.run(mix_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"✅ Generated Voiceover with Music Bed: {VOICEOVER_WITH_BGM}\n")

    # Write aligned SRT and VTT subtitles matching exact audio timestamps
    print("📝 Generating synchronized SRT and VTT subtitle files...")
    srt_content = ""
    vtt_content = "WEBVTT - Thermal Sentinel Grid Narration\n\n"

    for c in cues:
        srt_content += f"{c['index']}\n"
        srt_content += f"{format_time_srt(c['start'])} --> {format_time_srt(c['end'])}\n"
        srt_content += f"{c['text']}\n\n"

        vtt_content += f"{c['index']}\n"
        vtt_content += f"{format_time_vtt(c['start'])} --> {format_time_vtt(c['end'])}\n"
        vtt_content += f"{c['text']}\n\n"

    with open(SRT_FILE, 'w', encoding='utf-8') as f:
        f.write(srt_content)
    with open(VTT_FILE, 'w', encoding='utf-8') as f:
        f.write(vtt_content)
    with open(PUBLIC_VTT, 'w', encoding='utf-8') as f:
        f.write(vtt_content)

    print(f"✅ Aligned Subtitles Saved: {SRT_FILE}")
    print(f"✅ Aligned WebVTT Saved: {VTT_FILE}")
    print("\n🎉 Natural voiceover generation complete!")

if __name__ == "__main__":
    asyncio.run(generate_voiceover())
