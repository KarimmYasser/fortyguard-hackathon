import os
import re
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RENDERS_DIR = os.path.join(PROJECT_ROOT, "videos/thermal-sentinel-pitch/renders")
INPUT_VIDEO = os.path.join(RENDERS_DIR, "final_submission_fortyguard.mov")
SRT_FILE = os.path.join(RENDERS_DIR, "final_submission_fortyguard.srt")
VTT_FILE = os.path.join(RENDERS_DIR, "final_submission_fortyguard.vtt")
OUTPUT_MP4 = os.path.join(RENDERS_DIR, "final_submission_fortyguard_subtitled.mp4")
PUBLIC_VTT = os.path.join(PROJECT_ROOT, "frontend/public/videos/final_submission_fortyguard.vtt")
PUBLIC_MP4 = os.path.join(PROJECT_ROOT, "frontend/public/videos/final_submission_fortyguard_subtitled.mp4")

with open(SRT_FILE, 'r', encoding='utf-8') as f:
    srt_text = f.read()

# Polish proper nouns and formatting
replacements = [
    (r'\b40\s*guards\b', "FortyGuard's"),
    (r'\b40\s*guard\b', "FortyGuard"),
    (r'\b40\s*Guard\b', "FortyGuard"),
    (r'\bforty\s*guard\b', "FortyGuard"),
    (r'\bwhat\s*if\s*studio\b', "What-If Studio"),
    (r'\b1\s*p\.m\.\b', "1:00 PM"),
    (r'\bcoco\b', "COCO"),
    (r'\bCoco\b', "COCO"),
    (r'\bhotspot\b', "hot-spot"),
    (r'\bLang graph\b', "LangGraph"),
    (r'\blang graph\b', "LangGraph"),
    (r'\bLang Graph\b', "LangGraph"),
    (r'\b2\s*meter\b', "2-meter"),
    (r'\b60\s*meter\b', "60-meter"),
]

for pat, repl in replacements:
    srt_text = re.sub(pat, repl, srt_text, flags=re.IGNORECASE)

with open(SRT_FILE, 'w', encoding='utf-8') as f:
    f.write(srt_text)

# Generate VTT
vtt_lines = ["WEBVTT - Thermal Sentinel Grid Final Submission\n"]
for block in srt_text.strip().split('\n\n'):
    lines = block.split('\n')
    if len(lines) >= 3:
        idx = lines[0]
        timing = lines[1].replace(',', '.')
        content = "\n".join(lines[2:])
        vtt_lines.append(f"{idx}\n{timing}\n{content}\n")

with open(VTT_FILE, 'w', encoding='utf-8') as f:
    f.write("\n".join(vtt_lines))

with open(PUBLIC_VTT, 'w', encoding='utf-8') as f:
    f.write("\n".join(vtt_lines))

# Re-mux MP4
ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-i", INPUT_VIDEO,
    "-i", SRT_FILE,
    "-c:v", "copy",
    "-c:a", "copy",
    "-c:s", "mov_text",
    "-metadata:s:s:0", "language=eng",
    "-metadata:s:s:0", "title=English Subtitles",
    OUTPUT_MP4
]
subprocess.run(ffmpeg_cmd, check=True)
subprocess.run(["cp", OUTPUT_MP4, PUBLIC_MP4], check=True)

print("✨ Polished subtitles and re-muxed subtitled MP4 successfully!")
