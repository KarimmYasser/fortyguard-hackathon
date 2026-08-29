import os
import re
import sys
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RENDERS_DIR = os.path.join(PROJECT_ROOT, "videos/thermal-sentinel-pitch/renders")
INPUT_VIDEO = os.path.join(RENDERS_DIR, "final_submission_fortyguard.mov")
SRT_FILE = os.path.join(RENDERS_DIR, "final_submission_fortyguard.srt")
OUTPUT_VIDEO = os.path.join(RENDERS_DIR, "final_submission_fortyguard_burned_subtitles.mp4")
PUBLIC_VIDEO = os.path.join(PROJECT_ROOT, "frontend/public/videos/final_submission_fortyguard_burned_subtitles.mp4")

FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"

FONT_SIZE = 34

def parse_srt_time(time_str: str) -> float:
    time_str = time_str.strip().replace(',', '.')
    parts = time_str.split(':')
    h = float(parts[0])
    m = float(parts[1])
    s = float(parts[2])
    return h * 3600 + m * 60 + s

def load_subtitles(srt_path: str):
    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    blocks = content.split('\n\n')
    subtitles = []
    
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            time_match = re.match(r'(\d+:\d+:\d+[,\.]\d+)\s*-->\s*(\d+:\d+:\d+[,\.]\d+)', lines[1])
            if time_match:
                start_sec = parse_srt_time(time_match.group(1))
                end_sec = parse_srt_time(time_match.group(2))
                text = " ".join(lines[2:]).strip()
                subtitles.append({
                    "start": start_sec,
                    "end": end_sec,
                    "text": text
                })
    return subtitles

def wrap_text(text: str, max_chars_per_line: int = 56) -> list[str]:
    words = text.split()
    lines = []
    current_line = []
    current_len = 0
    
    for w in words:
        if current_len + len(w) + 1 > max_chars_per_line and current_line:
            lines.append(" ".join(current_line))
            current_line = [w]
            current_len = len(w)
        else:
            current_line.append(w)
            current_len += len(w) + 1
            
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def pre_render_overlays(subtitles: list[dict], width: int, height: int, font):
    """Pre-render RGBA overlay images for each subtitle so per-frame blending is instant."""
    overlays = []
    
    for sub in subtitles:
        lines = wrap_text(sub["text"], max_chars_per_line=54)
        
        # Calculate bounding box for multiline text
        dummy_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        dummy_draw = ImageDraw.Draw(dummy_img)
        
        line_height = FONT_SIZE + 10
        total_text_height = len(lines) * line_height
        
        max_line_width = 0
        line_sizes = []
        for line in lines:
            bbox = dummy_draw.textbbox((0, 0), line, font=font)
            lw = bbox[2] - bbox[0]
            line_sizes.append(lw)
            if lw > max_line_width:
                max_line_width = lw
                
        pad_x = 24
        pad_y = 14
        box_width = max_line_width + pad_x * 2
        box_height = total_text_height + pad_y * 2
        
        box_x0 = (width - box_width) // 2
        box_y0 = height - box_height - 50 # 50px from bottom edge
        box_x1 = box_x0 + box_width
        box_y1 = box_y0 + box_height
        
        # Draw background pill box + text onto transparent RGBA image
        overlay_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay_img)
        
        # Draw rounded rectangle background (semi-transparent dark glass)
        draw.rounded_rectangle(
            [box_x0, box_y0, box_x1, box_y1],
            radius=16,
            fill=(6, 10, 18, 220), # Deep slate dark with 86% opacity
            outline=(56, 189, 248, 120), # Subtle cyan accent border
            width=2
        )
        
        # Draw text lines (crisp white with subtle shadow)
        cur_y = box_y0 + pad_y
        for idx, line in enumerate(lines):
            lw = line_sizes[idx]
            text_x = (width - lw) // 2
            
            # Text shadow / stroke for maximum readability
            draw.text((text_x, cur_y), line, font=font, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 240))
            cur_y += line_height
            
        # Convert to numpy array RGBA
        overlay_np = np.array(overlay_img, dtype=np.uint8)
        alpha = overlay_np[:, :, 3:4] / 255.0
        rgb = overlay_np[:, :, 0:3]
        
        overlays.append({
            "start": sub["start"],
            "end": sub["end"],
            "rgb": rgb,
            "alpha": alpha,
            "has_content": True
        })
        
    return overlays

def main():
    print("=================================================================")
    print("🎬 BURNING SUBTITLES DIRECTLY INTO VIDEO FRAMES (OPEN CAPTIONS)")
    print(f"📹 Input Video: {INPUT_VIDEO}")
    print(f"📝 Subtitle File: {SRT_FILE}")
    print(f"🚀 Output Video: {OUTPUT_VIDEO}")
    print("=================================================================\n")

    if not os.path.exists(INPUT_VIDEO) or not os.path.exists(SRT_FILE):
        print("❌ Error: Input video or SRT file missing!")
        return

    # Probe video dimensions & FPS
    probe_cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,duration",
        "-of", "default=noprint_wrappers=1",
        INPUT_VIDEO
    ]
    probe_res = subprocess.run(probe_cmd, stdout=subprocess.PIPE, text=True, check=True).stdout
    
    width = 1728
    height = 1080
    fps = 30.0
    
    for line in probe_res.strip().split('\n'):
        if line.startswith('width='):
            width = int(line.split('=')[1])
        elif line.startswith('height='):
            height = int(line.split('=')[1])
        elif line.startswith('r_frame_rate='):
            num, den = line.split('=')[1].split('/')
            fps = float(num) / float(den)

    print(f"📐 Video Geometry: {width}x{height} @ {fps:.2f} FPS")

    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    subtitles = load_subtitles(SRT_FILE)
    print(f"📑 Loaded {len(subtitles)} subtitle cues.")

    print("🎨 Pre-rendering stylized subtitle overlay badges...")
    overlays = pre_render_overlays(subtitles, width, height, font)

    # Launch FFmpeg decoder pipe (rawvideo rgb24)
    decode_cmd = [
        "ffmpeg", "-v", "error",
        "-i", INPUT_VIDEO,
        "-f", "image2pipe",
        "-vcodec", "rawvideo",
        "-pix_fmt", "rgb24",
        "-"
    ]
    decoder = subprocess.Popen(decode_cmd, stdout=subprocess.PIPE, bufsize=10**8)

    # Launch FFmpeg encoder pipe
    encode_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{width}x{height}",
        "-r", str(fps),
        "-i", "-",
        "-i", INPUT_VIDEO, # Grab audio from original video
        "-map", "0:v:0",
        "-map", "1:a:0?",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "veryfast",
        "-crf", "17",
        "-c:a", "copy",
        OUTPUT_VIDEO
    ]
    encoder = subprocess.Popen(encode_cmd, stdin=subprocess.PIPE, bufsize=10**8)

    frame_bytes = width * height * 3
    frame_idx = 0
    
    print("⚡ Burning subtitles into video stream frame-by-frame...")
    
    while True:
        raw_frame = decoder.stdout.read(frame_bytes)
        if len(raw_frame) < frame_bytes:
            break
            
        cur_time = frame_idx / fps
        frame_idx += 1
        
        # Check active subtitle
        active_overlay = None
        for ov in overlays:
            if ov["start"] <= cur_time <= ov["end"]:
                active_overlay = ov
                break
                
        if active_overlay is not None:
            # Fast alpha composite in numpy
            frame_np = np.frombuffer(raw_frame, dtype=np.uint8).reshape((height, width, 3))
            alpha = active_overlay["alpha"]
            rgb_ov = active_overlay["rgb"]
            
            # Blend: result = frame * (1 - alpha) + overlay * alpha
            blended = (frame_np * (1.0 - alpha) + rgb_ov * alpha).astype(np.uint8)
            encoder.stdin.write(blended.tobytes())
        else:
            encoder.stdin.write(raw_frame)
            
        if frame_idx % 300 == 0:
            print(f"  ⏳ Processed frame {frame_idx} ({cur_time:.1f}s)...", end="\r", flush=True)

    print(f"\n✅ Finished processing all {frame_idx} frames.")
    
    decoder.stdout.close()
    decoder.wait()
    encoder.stdin.close()
    encoder.wait()

    subprocess.run(["cp", OUTPUT_VIDEO, PUBLIC_VIDEO], check=True)

    print(f"\n🎉 Burned-In Subtitled Video Ready: {OUTPUT_VIDEO}")
    print(f"🎉 Public Frontend Asset Updated: {PUBLIC_VIDEO}")

if __name__ == "__main__":
    main()
