import asyncio
import os
import subprocess
import edge_tts

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'videos/thermal-sentinel-pitch/renders')
BGM_AUDIO = os.path.join(PROJECT_ROOT, 'videos/thermal-sentinel-pitch/assets/audio/bgm_cyber_ambient.mp3')

os.makedirs(OUTPUT_DIR, exist_ok=True)

# High-energy, passionate, engaging text with punctuation designed for expressive pitch delivery
PASSIONATE_SCRIPT = [
    {
        "id": "act1_intro",
        "text": "Hey everyone! This is Thermal Sentinel Grid for Track 03: Industrial and Enterprise! During extreme heatwaves, electric utilities manage billions of dollars in substation transformers using airport weather stations 10 miles away! But equipment actually sits in the 2-meter boundary layer right above scorching asphalt! Right here, we ingest FortyGuard's live 2-meter Temperature AI in real time across 60-meter microclimate parcel tiles!",
        "pause_after": 1.0
    },
    {
        "id": "act1_scan",
        "text": "Look right here—we can see the real-time numbers of the live scan we just triggered! Now let's jump back to our canonical benchmark: our evidence contract explicitly proves what uses real live API telemetry versus what is simulated!",
        "pause_after": 1.1
    },
    {
        "id": "act2_mission_control",
        "text": "Following FortyGuard's core doctrine: 42.7 degrees is just a fact! The finding is what truly matters! Watch what happens at 1:00 PM: under unmitigated baseline operation, the transformer winding hot-spot surges to a catastrophic 159.5 degrees—accelerating insulation destruction by 88 times! The graphs speak for themselves! But when we engage Thermal Sentinel mitigation, our engine coordinates proactive pre-cooling and battery support, safely clamping the hot-spot down to 122.5 degrees!",
        "pause_after": 1.1
    },
    {
        "id": "act3_what_if",
        "text": "Here is our unfair engineering moat: our interactive What-If Studio re-solves non-linear IEEE differential equations in under 15 milliseconds as I move these sliders live! Why does this matter? Dumb threshold rules create false alarms on 20-minute heat spikes, or miss silent 12-hour thermal destruction on dry soil! We don't use arbitrary threshold rules—we use exact thermodynamic physics to gate our decisions, completely eliminating both false positives and false negatives!",
        "pause_after": 1.1
    },
    {
        "id": "act4_power_flow",
        "text": "We don't just model temperature—we model full AC power flow! Our engine enforces ANSI C84.1 voltage stability and dynamic line thermal ratings, actively tuning transformer tap changers and BESS reactive power to guarantee 100% continuous uptime for critical trauma hospital feeders!",
        "pause_after": 1.1
    },
    {
        "id": "act5_72h_heatwave",
        "text": "Single-day peak temperature is an amateur metric! In the desert, asphalt fails to cool below 36 degrees overnight! Our 72-hour compounding engine models nocturnal heat accumulation, showing how uncooled transformers start Day 2 and Day 3 already dangerously pre-heated!",
        "pause_after": 1.1
    },
    {
        "id": "act6_portfolio_ops",
        "text": "In Portfolio Operations, we rank critical assets across the entire city fleet and screen maintenance shift windows using OSHA and NIOSH Wet-Bulb temperature limits to protect utility field crews from severe heat stroke! We also generate instant COCO Customer Discovery Briefs across 4 key enterprise buyers: Utilities, AI Data Centers, Solar IPPs, and Hospitals!",
        "pause_after": 1.1
    },
    {
        "id": "act7_agent_roi",
        "text": "Our autonomous dispatch runs on a 5-node LangGraph StateGraph, protected by a deterministic non-LLM safety gate that prevents unauthorized breaker trips and generates auditable B2B work orders! Financially, Thermal Sentinel Grid is an acute painkiller: saving approximately 2.57 million dollars in catastrophic outage and equipment replacement exposure per heatwave episode—delivering an incredible 5,472x ROI!",
        "pause_after": 1.1
    },
    {
        "id": "act8_tour_outro",
        "text": "Finally, before I close, I want to invite you to explore the platform yourself! We have our video integrated directly inside the site, along with an interactive Tour Guide button that walks you through every single window! You can inspect our live cloud database across 17 tables, and review all peer-reviewed research papers in our Academic Provenance tab! Thank you, and we invite you to test our live platform at thermal-sentinel-grid.live!",
        "pause_after": 0.8
    }
]

def format_time_srt(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def get_audio_duration(file_path: str) -> float:
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        return float(res.stdout.strip())
    except:
        return 0.0

async def synthesize_passionate_voice(voice_name: str, voice_label: str, pitch: str = "+2Hz", rate: str = "+1%"):
    print(f"\n🔥 Synthesizing Passionate Voice: {voice_label} ({voice_name} | Pitch: {pitch} | Rate: {rate})...")
    
    out_mp3 = os.path.join(OUTPUT_DIR, f"voiceover_passionate_{voice_label}.mp3")
    out_bgm = os.path.join(OUTPUT_DIR, f"voiceover_passionate_{voice_label}_bgm.mp3")
    out_srt = os.path.join(OUTPUT_DIR, f"voiceover_passionate_{voice_label}.srt")
    
    temp_files = []
    cues = []
    current_time = 0.4

    for idx, sec in enumerate(PASSIONATE_SCRIPT):
        temp_mp3 = os.path.join(OUTPUT_DIR, f"temp_{voice_label}_{idx}.mp3")
        temp_files.append(temp_mp3)

        communicate = edge_tts.Communicate(sec['text'], voice_name, pitch=pitch, rate=rate)
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

    # Stitch with ffmpeg
    inputs = []
    filter_parts = []
    for idx, f in enumerate(temp_files):
        inputs.extend(['-i', f])
        pause = PASSIONATE_SCRIPT[idx]['pause_after']
        filter_parts.append(f"[{idx}:a]apad=pad_dur={pause}[a{idx}]")

    concat_inputs = "".join([f"[a{i}]" for i in range(len(temp_files))])
    filter_complex = ";".join(filter_parts) + f";{concat_inputs}concat=n={len(temp_files)}:v=0:a=1[outa]"

    cmd = ['ffmpeg', '-y'] + inputs + ['-filter_complex', filter_complex, '-map', '[outa]', '-c:a', 'libmp3lame', '-b:a', '192k', out_mp3]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for f in temp_files:
        if os.path.exists(f):
            os.remove(f)

    # Mix with BGM
    if os.path.exists(BGM_AUDIO):
        mix_cmd = [
            'ffmpeg', '-y',
            '-i', out_mp3,
            '-i', BGM_AUDIO,
            '-filter_complex', '[1:a]volume=0.07[bgm];[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[outa]',
            '-map', '[outa]',
            '-c:a', 'libmp3lame',
            '-b:a', '192k',
            out_bgm
        ]
        subprocess.run(mix_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Save SRT
    srt_content = ""
    for c in cues:
        srt_content += f"{c['index']}\n"
        srt_content += f"{format_time_srt(c['start'])} --> {format_time_srt(c['end'])}\n"
        srt_content += f"{c['text']}\n\n"

    with open(out_srt, 'w', encoding='utf-8') as f:
        f.write(srt_content)

    duration = get_audio_duration(out_mp3)
    print(f"  ✅ Saved: {out_mp3} ({duration:.1f}s)")
    print(f"  ✅ Saved with BGM: {out_bgm}")
    return out_mp3

async def main():
    print("=================================================================")
    print("🚀 GENERATING PASSIONATE, HIGH-ENERGY TECH FOUNDER VOICEOVERS")
    print("=================================================================")

    # 1. Guy - Enthusiastic, high-energy Silicon Valley pitch style
    await synthesize_passionate_voice("en-US-GuyNeural", "guy_energetic", pitch="+3Hz", rate="+2%")

    # 2. Brian - Rich, lively, highly expressive storytelling voice
    await synthesize_passionate_voice("en-US-BrianNeural", "brian_passionate", pitch="+2Hz", rate="+1%")

    # 3. Aria - Dynamic, confident, passionate female founder voice
    await synthesize_passionate_voice("en-US-AriaNeural", "aria_passionate", pitch="+1Hz", rate="+1%")

    # 4. Andrew - Warm, punchy, authoritative presenter
    await synthesize_passionate_voice("en-US-AndrewNeural", "andrew_punchy", pitch="+2Hz", rate="+2%")

    print("\n🎉 ALL PASSIONATE VOICES GENERATED!")

if __name__ == "__main__":
    asyncio.run(main())
