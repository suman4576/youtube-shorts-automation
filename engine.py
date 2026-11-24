#!/usr/bin/env python3
"""
TechSparks Hindi - All-in-One Autonomous Shorts Video Factory
Features:
- Hindi TTS Voiceover
- Upbeat/Ambient Background Music (BGM mixing)
- Dynamic Motion Cyber Background Video
- Animated Subtitles & Brand Badges
- Batch / Multi-Topic Generation
- Auto SEO Metadata (Title, Tags, Description)
"""

import os
import sys
import json
import argparse
import urllib.parse
import urllib.request
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
ASSETS_DIR = BASE_DIR / "assets"
MUSIC_DIR = ASSETS_DIR / "music"
BG_DIR = ASSETS_DIR / "backgrounds"
TOPICS_FILE = BASE_DIR / "topics.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MUSIC_DIR.mkdir(parents=True, exist_ok=True)
BG_DIR.mkdir(parents=True, exist_ok=True)

FONT_HINDI = "/system/fonts/NotoSansDevanagari-VF.ttf"
if not Path(FONT_HINDI).exists():
    FONT_HINDI = "/system/fonts/DroidSans-Bold.ttf"

BGM_TRACK = MUSIC_DIR / "tech_bgm.ogg"
CYBER_BG = BG_DIR / "cyber_bg.mp4"

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
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(result.stdout.strip())

def generate_video(topic_data: dict) -> str:
    """Generates complete Short video with BGM, motion background, and synced text."""
    topic_id = topic_data["id"]
    title = topic_data["title"]
    category = topic_data.get("category", "TECH TRICK")
    beats = topic_data["beats"]

    print(f"\n==================================================")
    print(f"🎬 Generating Short: {title}")
    print(f"==================================================")

    # 1. Download TTS audio for each beat
    audio_files = []
    durations = []
    for idx, beat in enumerate(beats):
        beat_audio = str(OUTPUT_DIR / f"{topic_id}_beat_{idx}.mp3")
        download_tts(beat["text"], beat_audio, lang="hi")
        dur = get_duration(beat_audio)
        audio_files.append(beat_audio)
        durations.append(dur)
        print(f"  [Beat {idx+1}] ({dur:.1f}s) {beat['display']}")

    total_duration = sum(durations) + 0.8
    print(f"⏱️ Total Video Length: {total_duration:.1f}s")

    # 2. Concat voice audio
    concat_list_file = OUTPUT_DIR / f"{topic_id}_concat.txt"
    with open(concat_list_file, "w") as f:
        for a in audio_files:
            f.write(f"file '{a}'\n")

    combined_voice = str(OUTPUT_DIR / f"{topic_id}_voice.mp3")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list_file),
        "-c", "copy", combined_voice
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 3. Build mixed audio (Voice 100% + BGM 12%)
    final_audio = str(OUTPUT_DIR / f"{topic_id}_final_audio.mp3")
    if BGM_TRACK.exists():
        mix_cmd = [
            "ffmpeg", "-y",
            "-i", combined_voice,
            "-stream_loop", "-1", "-i", str(BGM_TRACK),
            "-filter_complex", "[0:a]volume=1.0[v];[1:a]volume=0.12[b];[v][b]amix=inputs=2:duration=first:dropout_transition=2[aout]",
            "-map", "[aout]",
            "-c:a", "libmp3lame", "-b:a", "128k",
            final_audio
        ]
        subprocess.run(mix_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        final_audio = combined_voice

    # 4. Build text overlay filtergraph
    drawtext_filters = [
        # Dark vignette / contrast box for background
        "drawbox=y=0:color=black@0.4:width=iw:height=ih:t=fill",
        # Top Brand Bar
        "drawbox=y=0:color=black@0.75:width=iw:height=140:t=fill",
        f"drawtext=fontfile='{FONT_HINDI}':text='⚡ TECHSPARKS HINDI':fontcolor=0xFFD600:fontsize=42:x=(w-text_w)/2:y=45",
        f"drawtext=fontfile='{FONT_HINDI}':text='{category}':fontcolor=0x00E5FF:fontsize=28:x=(w-text_w)/2:y=100",
    ]

    current_time = 0.0
    for idx, beat in enumerate(beats):
        start = current_time
        end = current_time + durations[idx]
        display_text = beat["display"].replace("'", "\\'").replace(":", "\\:")
        
        # Highlight card
        box_filter = f"drawbox=y=550:color=black@0.8:width=iw-80:x=40:height=260:t=fill:enable='between(t,{start:.2f},{end:.2f})'"
        # Border accent
        border_filter = f"drawbox=y=550:color=0x00E5FF@0.6:width=iw-80:x=40:height=260:t=4:enable='between(t,{start:.2f},{end:.2f})'"
        # Text
        text_filter = f"drawtext=fontfile='{FONT_HINDI}':text='{display_text}':fontcolor=white:fontsize=38:line_spacing=14:x=(w-text_w)/2:y=610:enable='between(t,{start:.2f},{end:.2f})'"
        
        drawtext_filters.extend([box_filter, border_filter, text_filter])
        current_time = end

    # Bottom Subscribe Bar
    drawtext_filters.append("drawbox=y=1120:color=black@0.75:width=iw:height=100:t=fill")
    drawtext_filters.append(f"drawtext=fontfile='{FONT_HINDI}':text='SUBSCRIBE @TechSparksHindi':fontcolor=0x00E5FF:fontsize=30:x=(w-text_w)/2:y=1155")

    filter_complex = ",".join(drawtext_filters)
    output_video = str(OUTPUT_DIR / f"{topic_id}.mp4")

    # Render final MP4
    bg_input = str(CYBER_BG) if CYBER_BG.exists() else f"color=c=0x0a1128:s=720x1280:d={total_duration}"
    is_lavfi = not CYBER_BG.exists()

    cmd = ["ffmpeg", "-y"]
    if is_lavfi:
        cmd.extend(["-f", "lavfi", "-i", bg_input])
    else:
        cmd.extend(["-stream_loop", "-1", "-i", bg_input])

    cmd.extend([
        "-i", final_audio,
        "-vf", filter_complex,
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "24",
        "-c:a", "aac", "-b:a", "128k",
        "-t", f"{total_duration:.2f}",
        output_video
    ])

    print("🚀 Rendering with FFmpeg (Voice + BGM + Motion)...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        print(f"✅ Video Generated: {output_video}")
        # Save metadata file
        meta_file = OUTPUT_DIR / f"{topic_id}_meta.json"
        with open(meta_file, "w") as f:
            json.dump({
                "title": title,
                "description": f"{topic_data.get('description', '')}\n\nSubscribe to @TechSparksHindi for daily smart tech & computer tricks! ⚡",
                "tags": topic_data.get("tags", []),
                "video_path": output_video
            }, f, indent=2)
        print(f"📄 Metadata saved: {meta_file}")
        return output_video
    else:
        print("❌ Error:", res.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description="TechSparks Hindi Video Automation Factory")
    parser.add_argument("--all", action="store_true", help="Generate all topics")
    parser.add_argument("--topic", type=str, help="Topic ID or index (1, 2, 3...)")
    parser.add_argument("--list", action="store_true", help="List all topics")
    args = parser.parse_args()

    if not TOPICS_FILE.exists():
        print(f"Error: {TOPICS_FILE} not found.")
        return

    with open(TOPICS_FILE) as f:
        topics = json.load(f)

    if args.list:
        print("\n📋 Available Topics in Factory:")
        for idx, t in enumerate(topics, 1):
            print(f"  {idx}. [{t['id']}] {t['title']} ({t['category']})")
        return

    if args.all:
        print(f"🚀 Batch generating all {len(topics)} videos...")
        for t in topics:
            generate_video(t)
        print("\n🎉 All videos generated successfully!")
        return

    if args.topic:
        chosen = None
        if args.topic.isdigit():
            idx = int(args.topic) - 1
            if 0 <= idx < len(topics):
                chosen = topics[idx]
        else:
            for t in topics:
                if t["id"] == args.topic:
                    chosen = t
                    break
        if chosen:
            generate_video(chosen)
        else:
            print(f"Topic '{args.topic}' not found. Run --list to see available topics.")
        return

    # Default: Generate the first topic
    print("Generating default topic 1...")
    generate_video(topics[0])

if __name__ == "__main__":
    main()
