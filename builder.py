#!/usr/bin/env python3
"""
TechSparks Hindi - Autonomous YouTube Shorts Generator
Generates full 9:16 vertical videos with Hindi voiceover and animated subtitles.
Zero external pip dependencies required.
"""

import os
import sys
import json
import urllib.parse
import urllib.request
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_HINDI = "/system/fonts/NotoSansDevanagari-VF.ttf"
if not Path(FONT_HINDI).exists():
    FONT_HINDI = "/system/fonts/DroidSans-Bold.ttf"

def download_tts(text: str, output_path: str, lang: str = "hi"):
    """Downloads zero-dependency TTS audio."""
    encoded_text = urllib.parse.quote(text)
    url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded_text}&tl={lang}&client=tw-ob"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response, open(output_path, "wb") as f:
        f.write(response.read())

def get_duration(audio_path: str) -> float:
    """Gets audio duration in seconds using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(result.stdout.strip())

def build_short_video(title: str, script_beats: list, output_filename: str = "short_1.mp4"):
    """
    Builds a complete 9:16 vertical video from script beats.
    script_beats: list of dicts: [{"text": "Hindi speech", "display": "Screen text"}]
    """
    print(f"🎬 Creating video: {title}")
    audio_files = []
    durations = []

    # 1. Generate audio for each beat
    for idx, beat in enumerate(script_beats):
        audio_file = str(OUTPUT_DIR / f"beat_{idx}.mp3")
        download_tts(beat["text"], audio_file, lang="hi")
        dur = get_duration(audio_file)
        audio_files.append(audio_file)
        durations.append(dur)
        print(f"  Beat {idx+1}: {dur:.1f}s | {beat['display']}")

    total_duration = sum(durations) + 1.0
    print(f"⏱️ Total duration: {total_duration:.1f}s")

    # 2. Concat audio files using ffmpeg
    concat_list_file = OUTPUT_DIR / "audio_list.txt"
    with open(concat_list_file, "w") as f:
        for a in audio_files:
            f.write(f"file '{a}'\n")

    combined_audio = str(OUTPUT_DIR / "combined_audio.mp3")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list_file),
        "-c", "copy", combined_audio
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 3. Build FFmpeg video with animated text overlays
    # Vertical resolution: 720x1280 (Fast rendering on mobile)
    output_video_path = str(OUTPUT_DIR / output_filename)

    # Build drawtext filters for each beat
    drawtext_filters = [
        # Permanent Top Brand Bar
        f"drawbox=y=0:color=black@0.6:width=iw:height=140:t=fill",
        f"drawtext=fontfile='{FONT_HINDI}':text='⚡ TECHSPARKS HINDI':fontcolor=yellow:fontsize=42:x=(w-text_w)/2:y=45",
        # Category pill
        f"drawtext=fontfile='{FONT_HINDI}':text='SUPER SHORTCUT':fontcolor=white:fontsize=28:x=(w-text_w)/2:y=100",
    ]

    current_time = 0.0
    for idx, beat in enumerate(script_beats):
        start = current_time
        end = current_time + durations[idx]
        display_text = beat["display"].replace("'", "\\'").replace(":", "\\:")
        
        # Highlight card
        box_filter = f"drawbox=y=550:color=black@0.75:width=iw-80:x=40:height=260:t=fill:enable='between(t,{start:.2f},{end:.2f})'"
        # Text display
        text_filter = f"drawtext=fontfile='{FONT_HINDI}':text='{display_text}':fontcolor=white:fontsize=38:line_spacing=14:x=(w-text_w)/2:y=610:enable='between(t,{start:.2f},{end:.2f})'"
        
        drawtext_filters.append(box_filter)
        drawtext_filters.append(text_filter)
        current_time = end

    # Permanent bottom Call To Action
    drawtext_filters.append(f"drawbox=y=1120:color=black@0.6:width=iw:height=100:t=fill")
    drawtext_filters.append(f"drawtext=fontfile='{FONT_HINDI}':text='SUBSCRIBE FOR DAILY TECH HACKS':fontcolor=cyan:fontsize=30:x=(w-text_w)/2:y=1155")

    filter_complex = ",".join(drawtext_filters)

    # Render video with color background + audio
    render_cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"color=c=0x111625:s=720x1280:d={total_duration}",
        "-i", combined_audio,
        "-vf", filter_complex,
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "26",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        output_video_path
    ]

    print("🚀 Rendering video with FFmpeg...")
    res = subprocess.run(render_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        print(f"✅ Video successfully created: {output_video_path}")
        return output_video_path
    else:
        print("❌ Error rendering video:")
        print(res.stderr)
        return None

if __name__ == "__main__":
    beats = [
        {
            "text": "क्या आप जानते हैं कंप्यूटर का सबसे सीक्रेट शॉर्टकट?",
            "display": "COMPUTER KA SECRET SHORTCUT"
        },
        {
            "text": "अगर आप बार बार कॉपी पेस्ट करते हैं, तो अब रुक जाइए।",
            "display": "Stop Copy-Pasting Again & Again!"
        },
        {
            "text": "कीबोर्ड पर दबाइए Windows प्लस V. इससे आपका पूरा क्लिपबोर्ड हिस्ट्री खुल जाएगा।",
            "display": "PRESS: Windows + V\n(Clipboard History Open!)"
        },
        {
            "text": "अब आप पुरानी कॉपी की हुई कोई भी चीज़ एक सेकंड में पेस्ट कर सकते हैं।",
            "display": "Paste anything copied earlier in 1-Click!"
        },
        {
            "text": "ऐसे ही कमाल के कंप्यूटर ट्रिक्स के लिए अभी सब्सक्राइब करें।",
            "display": "LIKE & SUBSCRIBE TechSparks Hindi"
        }
    ]
    build_short_video("Windows Secret Clipboard Shortcut", beats, "windows_v_shortcut.mp4")
