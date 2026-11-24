#!/usr/bin/env python3
"""
TechSparks Hindi - MoneyPrinterTurbo Cinematic Engine
Uses REAL 4K Stock Video Footage (Pexels / Mixkit) with:
- Zero Cartoon SVGs: 100% Real Cinematic Clips (Bitcoin, Hacker, Server, Encryption)
- Dynamic CapCut-style Glowing Neon Subtitle Cards
- Multi-Layered Sound Effects (Boom, Whoosh, Record Scratch, Buzzer, Ticking, Ding)
- Cinematic Ambient Suspense Music
- Output: 720x1280 (9:16 Vertical Shorts Format)
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
CLIPS_DIR = BASE_DIR / "assets" / "stock_clips"
SFX_DIR = BASE_DIR / "assets" / "sfx"
MUSIC_DIR = BASE_DIR / "assets" / "music"
TEMP_DIR = BASE_DIR / "stories" / "mpt_frames"

TEMP_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_HINDI = "/system/fonts/NotoSansDevanagari-VF.ttf"
if not Path(FONT_HINDI).exists():
    FONT_HINDI = "/system/fonts/DroidSans-Bold.ttf"

BGM_TRACK = MUSIC_DIR / "tech_bgm.ogg"

def download_tts(text: str, output_path: str, lang: str = "hi"):
    """Downloads speech audio via Google TTS."""
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

def build_scene_clip(scene_idx: int, scene: dict, output_clip: str):
    """
    Renders a vertical 720x1280 scene combining real stock footage + CapCut subtitles.
    """
    video_source = str(CLIPS_DIR / scene["video_file"])
    dur = scene["duration"]
    voice_audio = scene["audio_path"]
    
    badge_text = scene["badge"]
    card_title = scene["card_title"].replace("'", "\\'").replace(":", "\\:")
    card_hindi = scene["card_hindi"].replace("'", "\\'").replace(":", "\\:")
    accent_color = scene.get("accent", "0x00E5FF")

    # Filtergraph:
    # 1. Scale 16:9 stock video to vertical 9:16 (scale height to 1280, center crop 720 width)
    # 2. Add cinematic dark grading (darken 45% for high text readability)
    # 3. Add Top Brand Bar + Badge
    # 4. Add CapCut Glowing Center Card
    # 5. Add Bottom Subtitles & Subscribe Bar
    filters = [
        # Scale to 2276x1280, center crop to 720x1280
        "scale=2276:1280,crop=720:1280:(2276-720)/2:0",
        # Dark vignette overlay
        "drawbox=y=0:color=black@0.45:width=iw:height=ih:t=fill",
        
        # Top Brand Bar
        "drawbox=y=30:color=black@0.85:width=iw-60:x=30:height=130:t=fill",
        f"drawbox=y=30:color={accent_color}@0.8:width=iw-60:x=30:height=130:t=3",
        f"drawtext=fontfile='{FONT_HINDI}':text='⚡ TECHSPARKS HINDI':fontcolor=0xFFD600:fontsize=36:x=(w-text_w)/2:y=55",
        f"drawtext=fontfile='{FONT_HINDI}':text='{badge_text}':fontcolor={accent_color}:fontsize=26:x=(w-text_w)/2:y=105",
        
        # Big Center CapCut Hook Card
        "drawbox=y=540:color=black@0.88:width=iw-60:x=30:height=260:t=fill",
        f"drawbox=y=540:color={accent_color}@0.9:width=iw-60:x=30:height=260:t=4",
        f"drawtext=fontfile='{FONT_HINDI}':text='{card_title}':fontcolor=0xFFD600:fontsize=38:line_spacing=12:x=(w-text_w)/2:y=580",
        f"drawtext=fontfile='{FONT_HINDI}':text='{card_hindi}':fontcolor=white:fontsize=30:line_spacing=14:x=(w-text_w)/2:y=680",
        
        # Bottom Subscribe CTA
        "drawbox=y=1120:color=black@0.85:width=iw-60:x=30:height=100:t=fill",
        f"drawbox=y=1120:color=0xFF3366@0.8:width=iw-60:x=30:height=100:t=3",
        f"drawtext=fontfile='{FONT_HINDI}':text='🔔 SUBSCRIBE @TechSparksHindi':fontcolor=white:fontsize=30:x=(w-text_w)/2:y=1155"
    ]

    vf = ",".join(filters)

    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", video_source,
        "-i", voice_audio,
        "-vf", vf,
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{dur:.2f}",
        output_clip
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"❌ Error rendering clip {scene_idx}:")
        print(res.stderr[-500:])

def build_money_printer_video():
    scenes = [
        # Scene 1: Real Bitcoin Footage Hook
        {
            "video_file": "bitcoin_coins.mp4",
            "badge": "🚨 TRUE CYBER CRIME & MYSTERY",
            "accent": "0xFF3366",
            "card_title": "₹2400 CRORE KA LOST PASSWORD!",
            "card_hindi": "सोचिए अगर आपके पास ₹2400 करोड़ हों\nऔर आप पासवर्ड भूल जाएं? 😱",
            "speech": "सोचिए अगर आपके पास चौबीस सौ करोड़ रुपये हों, लेकिन आप उसका पासवर्ड भूल जाएं?",
            "sfx": ["boom.mp3", "whoosh.mp3"]
        },
        # Scene 2: Real Encrypted Security Vault Footage
        {
            "video_file": "cyber_padlock.mp4",
            "badge": "🔒 7,002 BITCOINS LOCKED",
            "accent": "0x00E5FF",
            "card_title": "7,002 BITCOINS IN A PENDRIVE",
            "card_hindi": "यह असली कहानी है स्टेफ़न थॉमस की\nजिसके पेनड्राइव में ₹2400 करोड़ बंद हैं!",
            "speech": "यह असली कहानी है स्टेफ़न थॉमस की, जिसके एक पेनड्राइव में सात हज़ार बिटकॉइन्स बंद हैं।",
            "sfx": ["whoosh.mp3", "glitch.mp3"]
        },
        # Scene 3: Real Hacker Searching / Frustration Footage
        {
            "video_file": "hacker_typing.mp4",
            "badge": "🤦‍♂️ THE FATAL BLUNDER",
            "accent": "0xA855F7",
            "card_title": "PASSWORD NOTE WAS LOST!",
            "card_hindi": "पासवर्ड एक कागज़ पर लिखा था...\nऔर वो कागज़ हमेशा के लिए खो गया! ❌",
            "speech": "उसने पासवर्ड एक कागज़ पर लिखकर रखा था, लेकिन वो कागज़ खो गया!",
            "sfx": ["scratch.mp3"]
        },
        # Scene 4: Real Security Alert Footage (8/10 Failed)
        {
            "video_file": "cyber_padlock.mp4",
            "badge": "⚠️ SELF-DESTRUCT IN 10 TRIES",
            "accent": "0xEF4444",
            "card_title": "8/10 FAILED ATTEMPTS!",
            "card_hindi": "सिर्फ 10 मौके मिलते हैं...\nऔर वो 8 बार गलत पासवर्ड डाल चुका है! 💀",
            "speech": "इस पेनड्राइव में सिर्फ दस बार पासवर्ड डालने का मौका मिलता है, और वो आठ बार गलत पासवर्ड डाल चुका है!",
            "sfx": ["buzzer.mp3", "tick.mp3"]
        },
        # Scene 5: Real Server Matrix Footage (Only 2 Tries Left)
        {
            "video_file": "server_matrix.mp4",
            "badge": "💀 FINAL COUNTDOWN",
            "accent": "0xFFD600",
            "card_title": "ONLY 2 TRIES LEFT!",
            "card_hindi": "सिर्फ 2 मौके बचे हैं!\nवरना सारा पैसा हमेशा के लिए मिट जाएगा! 💥",
            "speech": "अब उसके पास सिर्फ दो मौके बचे हैं! अगर दोनों गलत हुए, तो सारा पैसा हमेशा के लिए खत्म!",
            "sfx": ["boom.mp3", "buzzer.mp3"]
        },
        # Scene 6: Real Golden Bitcoin Question Footage
        {
            "video_file": "bitcoin_coins.mp4",
            "badge": "🤔 WHAT WOULD YOU DO?",
            "accent": "0x00E5FF",
            "card_title": "AAP HOTE TOH KYA KARTE?",
            "card_hindi": "A) 9वां पासवर्ड डालते? 🎲\nB) तिजोरी में बंद रखते? 🔒",
            "speech": "अगर आप उसकी जगह होते, तो क्या नौवां पासवर्ड डालते? कमेंट्स में बताइए और सब्सक्राइब करें!",
            "sfx": ["whoosh.mp3", "ding.mp3"]
        }
    ]

    print("🚀 Running MoneyPrinterTurbo Native Engine with Real 4K Stock Footage...")
    scene_clips = []
    durations = []
    cumulative_time = 0.0
    sfx_schedule = []

    for idx, scene in enumerate(scenes):
        print(f"\n--- Scene {idx+1}/{len(scenes)}: {scene['badge']} ---")
        
        # 1. Download TTS audio
        audio_path = str(TEMP_DIR / f"mpt_voice_{idx}.mp3")
        download_tts(scene["speech"], audio_path, lang="hi")
        dur = get_duration(audio_path)
        scene["duration"] = dur
        scene["audio_path"] = audio_path
        durations.append(dur)
        print(f"  🎙️ Voiceover: {dur:.1f}s")

        # 2. Schedule SFX
        for sfx_name in scene.get("sfx", []):
            sfx_file = SFX_DIR / sfx_name
            if sfx_file.exists():
                sfx_schedule.append((cumulative_time, str(sfx_file)))
                print(f"  🔊 Scheduled SFX: {sfx_name} at {cumulative_time:.1f}s")

        # 3. Build Video Scene Clip from Real Stock Footage
        clip_path = str(TEMP_DIR / f"mpt_clip_{idx}.mp4")
        print(f"  🎥 Rendering Real Stock Video Clip: {scene['video_file']}...")
        build_scene_clip(idx, scene, clip_path)
        scene_clips.append(clip_path)
        cumulative_time += dur

    # Concat all scene video clips
    concat_txt = TEMP_DIR / "mpt_concat.txt"
    with open(concat_txt, "w") as f:
        for c in scene_clips:
            f.write(f"file '{c}'\n")

    raw_video = str(TEMP_DIR / "mpt_raw.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-c", "copy", raw_video
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    total_duration = cumulative_time
    print(f"\n⏱️ Total Video Duration: {total_duration:.1f}s")

    # Master Audio Mix: Voice (100%) + BGM (12%) + 11 SFX cues (90%)
    print(f"🎛️ Mixing Master Soundtrack with {len(sfx_schedule)} SFX cues & BGM...")
    extracted_voice = str(TEMP_DIR / "mpt_full_voice.mp3")
    subprocess.run([
        "ffmpeg", "-y", "-i", raw_video, "-vn", "-c:a", "libmp3lame", "-b:a", "192k", extracted_voice
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    ffmpeg_inputs = ["-i", extracted_voice]
    if BGM_TRACK.exists():
        ffmpeg_inputs.extend(["-stream_loop", "-1", "-i", str(BGM_TRACK)])

    filter_complex_parts = ["[0:a]volume=1.0[voice]"]
    next_stream_idx = 1
    if BGM_TRACK.exists():
        filter_complex_parts.append(f"[{next_stream_idx}:a]volume=0.12[bgm]")
        next_stream_idx += 1

    mix_inputs = ["[voice]"]
    if BGM_TRACK.exists():
        mix_inputs.append("[bgm]")

    for sfx_time, sfx_path in sfx_schedule:
        ffmpeg_inputs.extend(["-i", sfx_path])
        delay_ms = int(sfx_time * 1000)
        filter_complex_parts.append(
            f"[{next_stream_idx}:a]volume=0.9,adelay={delay_ms}|{delay_ms}[sfx_{next_stream_idx}]"
        )
        mix_inputs.append(f"[sfx_{next_stream_idx}]")
        next_stream_idx += 1

    num_mix_inputs = len(mix_inputs)
    filter_complex_parts.append(
        f"{''.join(mix_inputs)}amix=inputs={num_mix_inputs}:duration=first:dropout_transition=2[master_audio]"
    )

    final_filtergraph = ";".join(filter_complex_parts)
    master_audio_file = str(TEMP_DIR / "mpt_master_audio.mp3")

    mix_cmd = ["ffmpeg", "-y"] + ffmpeg_inputs + [
        "-filter_complex", final_filtergraph,
        "-map", "[master_audio]",
        "-c:a", "libmp3lame", "-b:a", "192k",
        master_audio_file
    ]
    subprocess.run(mix_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Multiplex Final Video + Master Soundtrack
    final_output = str(OUTPUT_DIR / "money_printer_bitcoin_mystery.mp4")
    print(f"🎬 Multiplexing Final MoneyPrinterTurbo Video...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", raw_video,
        "-i", master_audio_file,
        "-map", "0:v", "-map", "1:a",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        final_output
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"\n🎉 REAL 4K STOCK FOOTAGE SHORT READY: {final_output}")
    return final_output

if __name__ == "__main__":
    build_money_printer_video()
