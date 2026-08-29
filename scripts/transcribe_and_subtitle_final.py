import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import subprocess
import whisper

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RENDERS_DIR = os.path.join(PROJECT_ROOT, "videos/thermal-sentinel-pitch/renders")
INPUT_VIDEO = os.path.join(RENDERS_DIR, "final_submission_fortyguard.mov")
OUTPUT_SRT = os.path.join(RENDERS_DIR, "final_submission_fortyguard.srt")
OUTPUT_VTT = os.path.join(RENDERS_DIR, "final_submission_fortyguard.vtt")
OUTPUT_MP4 = os.path.join(RENDERS_DIR, "final_submission_fortyguard_subtitled.mp4")
PUBLIC_VTT = os.path.join(PROJECT_ROOT, "frontend/public/videos/final_submission_fortyguard.vtt")
PUBLIC_MP4 = os.path.join(PROJECT_ROOT, "frontend/public/videos/final_submission_fortyguard_subtitled.mp4")

os.makedirs(RENDERS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(PUBLIC_VTT), exist_ok=True)

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

def main():
    print("=================================================================")
    print("🎙️ TRANSCRIBING FINAL VIDEO & GENERATING SUBTITLES WITH WHISPER")
    print(f"🎬 Video: {INPUT_VIDEO}")
    print("=================================================================\n")

    if not os.path.exists(INPUT_VIDEO):
        print(f"❌ Error: {INPUT_VIDEO} not found!")
        return

    print("🧠 Loading Whisper Model (base.en)...")
    model = whisper.load_model("base.en")

    print("🎧 Transcribing exact audio stream from video...")
    result = model.transcribe(INPUT_VIDEO, language="en", fp16=False)

    segments = result.get("segments", [])
    print(f"✅ Transcription complete! Found {len(segments)} segments.\n")

    # Generate SRT and VTT
    srt_content = ""
    vtt_content = "WEBVTT - Thermal Sentinel Grid Final Submission\n\n"

    for idx, seg in enumerate(segments, 1):
        start = seg["start"]
        end = seg["end"]
        text = seg["text"].strip()

        # Write SRT
        srt_content += f"{idx}\n"
        srt_content += f"{format_time_srt(start)} --> {format_time_srt(end)}\n"
        srt_content += f"{text}\n\n"

        # Write VTT
        vtt_content += f"{idx}\n"
        vtt_content += f"{format_time_vtt(start)} --> {format_time_vtt(end)}\n"
        vtt_content += f"{text}\n\n"

    with open(OUTPUT_SRT, "w", encoding="utf-8") as f:
        f.write(srt_content)
    with open(OUTPUT_VTT, "w", encoding="utf-8") as f:
        f.write(vtt_content)
    with open(PUBLIC_VTT, "w", encoding="utf-8") as f:
        f.write(vtt_content)

    print(f"✅ Saved SRT Subtitles: {OUTPUT_SRT}")
    print(f"✅ Saved VTT Subtitles: {OUTPUT_VTT}")

    # Embed native subtitles into MP4
    print("\n🎬 Muxing Subtitled MP4 with native embedded subtitle track...")
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", INPUT_VIDEO,
        "-i", OUTPUT_SRT,
        "-c:v", "copy",
        "-c:a", "copy",
        "-c:s", "mov_text",
        "-metadata:s:s:0", "language=eng",
        "-metadata:s:s:0", "title=English Subtitles",
        OUTPUT_MP4
    ]
    subprocess.run(ffmpeg_cmd, check=True)
    subprocess.run(["cp", OUTPUT_MP4, PUBLIC_MP4], check=True)

    print(f"✅ Saved Subtitled MP4 Video: {OUTPUT_MP4}")
    print(f"✅ Public Asset Copied: {PUBLIC_MP4}")
    print("\n🎉 ALL DONE! Subtitles successfully synchronized and embedded.")

if __name__ == "__main__":
    main()
