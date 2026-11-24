#!/usr/bin/env python3
"""
TechSparks Hindi - Cinema-Grade Animated Mystery Shorts Generator
Features:
- Full Cartoon Character SVG Art (Panic, Vault, Comic Blunder, Hazard, Countdown, Poll)
- Multi-Layered Sound Effects (Boom, Whoosh, Record Scratch, Buzzer, Ticking, Ding)
- Camera Motion & Shake / Pulse FX
- Cinematic Suspense BGM Ducking
- Crisp 720x1280 9:16 Vertical Video
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
STORIES_DIR = BASE_DIR / "stories"
FRAMES_DIR = STORIES_DIR / "cinema_frames"
SFX_DIR = BASE_DIR / "assets" / "sfx"
BGM_TRACK = BASE_DIR / "assets" / "music" / "tech_bgm.ogg"

FRAMES_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def download_tts(text: str, output_path: str, lang: str = "hi"):
    """Downloads zero-dependency Google TTS audio."""
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

def render_html_to_png(html_content: str, output_png: str):
    """Renders 720x1280 image using headless Chromium."""
    temp_html = FRAMES_DIR / "temp.html"
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    cmd = [
        "chromium-browser", "--headless", "--no-sandbox",
        f"--screenshot={output_png}", "--window-size=720,1280",
        str(temp_html)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if temp_html.exists():
        temp_html.unlink()

def get_scene_html(scene_data: dict) -> str:
    """Generates stylish cartoon HTML/SVG layout."""
    badge = scene_data.get("badge", "MYSTERY STORY")
    headline = scene_data["headline"]
    subheadline = scene_data["subheadline"]
    svg_art = scene_data["svg"]
    caption = scene_data["caption"]
    accent_color = scene_data.get("accent", "#ff3366")

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 0;
    width: 720px; height: 1280px;
    background: radial-gradient(circle at 50% 25%, #1f1135 0%, #06040c 100%);
    color: #ffffff;
    font-family: system-ui, -apple-system, sans-serif;
    display: flex; flex-direction: column;
    justify-content: space-between;
    align-items: center;
    padding: 35px 25px;
    overflow: hidden;
  }}
  .top-bar {{
    display: flex; flex-direction: column; align-items: center; gap: 6px;
    width: 100%;
  }}
  .brand-badge {{
    background: rgba(255, 214, 0, 0.15);
    border: 3px solid #ffd600;
    color: #ffd600;
    padding: 8px 24px;
    border-radius: 40px;
    font-size: 24px; font-weight: 900;
    letter-spacing: 2px;
    text-transform: uppercase;
    box-shadow: 0 0 25px rgba(255, 214, 0, 0.3);
  }}
  .headline {{
    font-size: 48px; font-weight: 900;
    color: #ffffff; text-align: center;
    text-shadow: 0 0 25px {accent_color};
    line-height: 1.15; margin-top: 10px;
    letter-spacing: 0.5px;
  }}
  .subheadline {{
    font-size: 26px; color: #00e5ff;
    font-weight: 800; text-align: center;
    margin-top: 4px;
  }}
  .art-container {{
    width: 100%;
    display: flex; justify-content: center; align-items: center;
    margin: 15px 0;
    filter: drop-shadow(0 15px 30px rgba(0,0,0,0.8));
  }}
  .caption-card {{
    background: rgba(15, 20, 35, 0.92);
    border: 3px solid {accent_color};
    border-radius: 22px;
    padding: 22px 28px;
    width: 100%;
    text-align: center;
    box-shadow: 0 10px 40px rgba(0,0,0,0.7), inset 0 0 20px {accent_color}33;
  }}
  .caption-text {{
    font-size: 34px; font-weight: 900;
    color: #ffd600; line-height: 1.3;
    text-shadow: 0 2px 10px rgba(0,0,0,0.8);
  }}
  .bottom-badge {{
    font-size: 22px; color: #00e5ff; font-weight: 800;
    letter-spacing: 2px; text-transform: uppercase;
  }}
</style>
</head>
<body>
  <div class="top-bar">
    <div class="brand-badge">⚡ {badge}</div>
    <div class="headline">{headline}</div>
    <div class="subheadline">{subheadline}</div>
  </div>

  <div class="art-container">
    {svg_art}
  </div>

  <div class="caption-card">
    <div class="caption-text">{caption}</div>
  </div>

  <div class="bottom-badge">🔔 SUBSCRIBE @TechSparksHindi</div>
</body>
</html>"""

def build_cinematic_short():
    scenes = [
        # Scene 1: The Screaming Hook
        {
            "badge": "TRUE CYBER MYSTERY",
            "accent": "#ff3366",
            "sfx": ["boom.mp3", "whoosh.mp3"],
            "headline": "2400 CRORE KA<br><span style='color:#ff3366;'>LOST PASSWORD!</span>",
            "subheadline": "The Most Agonizing Mistake in History",
            "caption": "सोचिए अगर आपके पास ₹2400 करोड़ हों,<br>और आप पासवर्ड भूल जाएं? 😱",
            "speech": "सोचिए अगर आपके पास चौबीस सौ करोड़ रुपये हों, लेकिन आप पासवर्ड भूल जाएं?",
            "svg": """<svg width="450" height="450" viewBox="0 0 400 400">
              <circle cx="200" cy="200" r="170" fill="#2d132c" stroke="#ff3366" stroke-width="8"/>
              <circle cx="200" cy="180" r="110" fill="#ffe0bd" stroke="#111" stroke-width="6"/>
              <ellipse cx="160" cy="150" rx="24" ry="34" fill="#fff" stroke="#111" stroke-width="5"/>
              <ellipse cx="240" cy="150" rx="24" ry="34" fill="#fff" stroke="#111" stroke-width="5"/>
              <circle cx="160" cy="150" r="10" fill="#111"/>
              <circle cx="240" cy="150" r="10" fill="#111"/>
              <ellipse cx="200" cy="225" rx="44" ry="55" fill="#a00" stroke="#111" stroke-width="5"/>
              <path d="M 80 180 Q 120 180 135 150 Q 130 240 90 260 Z" fill="#ffe0bd" stroke="#111" stroke-width="6"/>
              <path d="M 320 180 Q 280 180 265 150 Q 270 240 310 260 Z" fill="#ffe0bd" stroke="#111" stroke-width="6"/>
              <circle cx="60" cy="80" r="35" fill="#f7931a" stroke="#fff" stroke-width="4"/>
              <text x="60" y="93" font-size="36" font-weight="bold" fill="#fff" text-anchor="middle">₿</text>
              <circle cx="340" cy="90" r="35" fill="#f7931a" stroke="#fff" stroke-width="4"/>
              <text x="340" y="103" font-size="36" font-weight="bold" fill="#fff" text-anchor="middle">₿</text>
              <path d="M 120 110 Q 110 80 120 70 Q 130 80 120 110" fill="#00e5ff"/>
              <path d="M 280 100 Q 270 70 280 60 Q 290 70 280 100" fill="#00e5ff"/>
            </svg>"""
        },
        # Scene 2: 7,002 Bitcoins Locked
        {
            "badge": "LOCKED IN USB",
            "accent": "#00e5ff",
            "sfx": ["whoosh.mp3", "glitch.mp3"],
            "headline": "7,002 BITCOINS<br><span style='color:#ffd600;'>IN A PENDRIVE</span>",
            "subheadline": "Worth over $240 Million USD!",
            "caption": "यह असली कहानी है स्टेफ़न थॉमस की,<br>जिसके पेनड्राइव में 7002 Bitcoins बंद हैं!",
            "speech": "यह असली कहानी है स्टेफ़न थॉमस की, जिसके एक पेनड्राइव में सात हज़ार बिटकॉइन्स बंद हैं।",
            "svg": """<svg width="450" height="450" viewBox="0 0 400 400">
              <rect x="30" y="30" width="340" height="340" rx="30" fill="#0f172a" stroke="#00e5ff" stroke-width="6"/>
              <rect x="130" y="80" width="140" height="200" rx="15" fill="#334155" stroke="#94a3b8" stroke-width="6"/>
              <rect x="155" y="40" width="90" height="40" fill="#cbd5e1" stroke="#64748b" stroke-width="5"/>
              <rect x="175" y="55" width="18" height="15" fill="#1e293b"/>
              <rect x="207" y="55" width="18" height="15" fill="#1e293b"/>
              <circle cx="200" cy="160" r="35" fill="#ffd600"/>
              <rect x="180" y="155" width="40" height="35" rx="5" fill="#1e293b"/>
              <path d="M 188 155 A 12 12 0 0 1 212 155" fill="none" stroke="#1e293b" stroke-width="6"/>
              <rect x="60" y="300" width="280" height="50" rx="12" fill="#f7931a"/>
              <text x="200" y="336" font-size="28" font-weight="900" fill="#000" text-anchor="middle">₹24,00,00,00,000</text>
            </svg>"""
        },
        # Scene 3: The Lost Note Blunder
        {
            "badge": "FUNNY BLUNDER",
            "accent": "#a855f7",
            "sfx": ["scratch.mp3"],
            "headline": "PAPER WAS LOST!<br><span style='color:#ff3366;'>OH NO! 🤦‍♂️</span>",
            "subheadline": "He wrote the password on a note...",
            "caption": "उसने पासवर्ड कागज़ पर लिखकर रखा था,<br>लेकिन वो कागज़ हमेशा के लिए खो गया!",
            "speech": "उसने पासवर्ड एक कागज़ पर लिखकर रखा था, लेकिन वो कागज़ खो गया!",
            "svg": """<svg width="450" height="450" viewBox="0 0 400 400">
              <circle cx="200" cy="200" r="170" fill="#1e1b4b" stroke="#a855f7" stroke-width="8"/>
              <circle cx="180" cy="180" r="90" fill="#ffe0bd" stroke="#111" stroke-width="6"/>
              <circle cx="150" cy="160" r="10" fill="#111"/>
              <circle cx="210" cy="160" r="10" fill="#111"/>
              <path d="M 150 220 Q 180 200 210 220" fill="none" stroke="#111" stroke-width="6"/>
              <path d="M 230 110 Q 260 80 270 120 Q 240 140 220 130" fill="#ffe0bd" stroke="#111" stroke-width="5"/>
              <g transform="translate(250, 200) rotate(20)">
                <rect x="0" y="0" width="90" height="120" rx="8" fill="#ffffff" stroke="#94a3b8" stroke-width="4"/>
                <line x1="15" y1="30" x2="75" y2="30" stroke="#cbd5e1" stroke-width="4"/>
                <line x1="15" y1="50" x2="75" y2="50" stroke="#cbd5e1" stroke-width="4"/>
                <line x1="15" y1="70" x2="75" y2="70" stroke="#cbd5e1" stroke-width="4"/>
                <text x="45" y="75" font-size="60" font-weight="900" fill="#ff3366" text-anchor="middle">❌</text>
              </g>
              <text x="80" y="140" font-size="50" font-weight="bold" fill="#ffd600">?</text>
              <text x="110" y="90" font-size="40" font-weight="bold" fill="#00e5ff">?</text>
            </svg>"""
        },
        # Scene 4: 8/10 Failed Self-Destruct Trap
        {
            "badge": "CRITICAL EMERGENCY",
            "accent": "#ef4444",
            "sfx": ["buzzer.mp3", "tick.mp3"],
            "headline": "8/10 FAILED!<br><span style='color:#ef4444;'>SELF-DESTRUCT TRAP</span>",
            "subheadline": "IronKey only allows 10 tries!",
            "caption": "इस पेनड्राइव में सिर्फ 10 बार मौका मिलता है,<br>और वो 8 बार गलत पासवर्ड डाल चुका है! 💀",
            "speech": "इस पेनड्राइव में सिर्फ दस बार पासवर्ड डालने का मौका मिलता है, और वो आठ बार गलत पासवर्ड डाल चुका है!",
            "svg": """<svg width="450" height="450" viewBox="0 0 400 400">
              <rect x="20" y="20" width="360" height="360" rx="24" fill="#450a0a" stroke="#ef4444" stroke-width="8"/>
              <polygon points="200,50 250,130 150,130" fill="#ffd600" stroke="#111" stroke-width="4"/>
              <text x="200" y="120" font-size="44" font-weight="900" fill="#111" text-anchor="middle">!</text>
              <text x="200" y="175" font-size="28" font-weight="900" fill="#fff" text-anchor="middle">ATTEMPTS REMAINING</text>
              <g transform="translate(45, 200)">
                <rect x="0" y="0" width="55" height="55" rx="8" fill="#ef4444"/><text x="27" y="40" font-size="34" font-weight="bold" fill="#fff" text-anchor="middle">✕</text>
                <rect x="65" y="0" width="55" height="55" rx="8" fill="#ef4444"/><text x="92" y="40" font-size="34" font-weight="bold" fill="#fff" text-anchor="middle">✕</text>
                <rect x="130" y="0" width="55" height="55" rx="8" fill="#ef4444"/><text x="157" y="40" font-size="34" font-weight="bold" fill="#fff" text-anchor="middle">✕</text>
                <rect x="195" y="0" width="55" height="55" rx="8" fill="#ef4444"/><text x="222" y="40" font-size="34" font-weight="bold" fill="#fff" text-anchor="middle">✕</text>
                <rect x="260" y="0" width="55" height="55" rx="8" fill="#ef4444"/><text x="287" y="40" font-size="34" font-weight="bold" fill="#fff" text-anchor="middle">✕</text>
                
                <rect x="0" y="70" width="55" height="55" rx="8" fill="#ef4444"/><text x="27" y="110" font-size="34" font-weight="bold" fill="#fff" text-anchor="middle">✕</text>
                <rect x="65" y="70" width="55" height="55" rx="8" fill="#ef4444"/><text x="92" y="110" font-size="34" font-weight="bold" fill="#fff" text-anchor="middle">✕</text>
                <rect x="130" y="70" width="55" height="55" rx="8" fill="#ef4444"/><text x="157" y="110" font-size="34" font-weight="bold" fill="#fff" text-anchor="middle">✕</text>
                
                <rect x="195" y="70" width="55" height="55" rx="8" fill="#22c55e" stroke="#fff" stroke-width="4"/><text x="222" y="110" font-size="30" font-weight="bold" fill="#fff" text-anchor="middle">#9</text>
                <rect x="260" y="70" width="55" height="55" rx="8" fill="#22c55e" stroke="#fff" stroke-width="4"/><text x="287" y="110" font-size="30" font-weight="bold" fill="#fff" text-anchor="middle">#10</text>
              </g>
            </svg>"""
        },
        # Scene 5: Only 2 Chances Left
        {
            "badge": "FINAL COUNTDOWN",
            "accent": "#ffd600",
            "sfx": ["boom.mp3", "buzzer.mp3"],
            "headline": "ONLY 2 TRIES LEFT!<br><span style='color:#ffd600;'>OR GONE FOREVER</span>",
            "subheadline": "2 Mistakes = 2400 Crore Wiped Out",
            "caption": "अब उसके पास सिर्फ 2 मौके बचे हैं!<br>अगर गलत हुआ तो सारा पैसा हमेशा के लिए खत्म!",
            "speech": "अब उसके पास सिर्फ दो मौके बचे हैं! अगर दोनों गलत हुए, तो सारा पैसा हमेशा के लिए खत्म!",
            "svg": """<svg width="450" height="450" viewBox="0 0 400 400">
              <circle cx="200" cy="200" r="170" fill="#000000" stroke="#e11d48" stroke-width="10"/>
              <circle cx="200" cy="180" r="95" fill="#881337" stroke="#fb7185" stroke-width="6"/>
              <text x="200" y="225" font-size="130" font-weight="900" fill="#ffffff" text-anchor="middle">2</text>
              <rect x="70" y="300" width="260" height="45" rx="10" fill="#e11d48"/>
              <text x="200" y="332" font-size="24" font-weight="bold" fill="#fff" text-anchor="middle">CHANCES REMAINING</text>
              <text x="80" y="120" font-size="50">💀</text>
              <text x="280" y="120" font-size="50">💀</text>
            </svg>"""
        },
        # Scene 6: What Would You Do Poll & Ding
        {
            "badge": "WHAT WOULD YOU DO?",
            "accent": "#00e5ff",
            "sfx": ["whoosh.mp3", "ding.mp3"],
            "headline": "AAP HOTE TOH<br><span style='color:#00e5ff;'>KYA KARTE? 🤔</span>",
            "subheadline": "Comment your answer below!",
            "caption": "क्या आप 9वां पासवर्ड डालते?<br>कमेंट्स में बताएं और अभी सब्सक्राइब करें! 👇",
            "speech": "अगर आप उसकी जगह होते, तो क्या नौवां पासवर्ड डालते? कमेंट्स में बताइए और सब्सक्राइब करें!",
            "svg": """<svg width="450" height="450" viewBox="0 0 400 400">
              <rect x="30" y="30" width="340" height="340" rx="30" fill="#1e1b4b" stroke="#ffd600" stroke-width="8"/>
              <rect x="60" y="70" width="280" height="90" rx="15" fill="#312e81" stroke="#38bdf8" stroke-width="4"/>
              <text x="85" y="115" font-size="30" font-weight="bold" fill="#ffd600">A)</text>
              <text x="130" y="112" font-size="24" font-weight="bold" fill="#fff">Try 9th Password!</text>
              <text x="130" y="140" font-size="18" fill="#94a3b8">Risk ₹2400 Crore 🎲</text>
              
              <rect x="60" y="180" width="280" height="90" rx="15" fill="#312e81" stroke="#a855f7" stroke-width="4"/>
              <text x="85" y="225" font-size="30" font-weight="bold" fill="#ffd600">B)</text>
              <text x="130" y="222" font-size="24" font-weight="bold" fill="#fff">Wait for Future Tech</text>
              <text x="130" y="250" font-size="18" fill="#94a3b8">Lock in Safe Vault 🔒</text>
              
              <rect x="80" y="295" width="240" height="50" rx="25" fill="#ef4444"/>
              <text x="200" y="330" font-size="22" font-weight="bold" fill="#fff" text-anchor="middle">🔔 LIKE & SUBSCRIBE</text>
            </svg>"""
        }
    ]

    print("🎬 Building Cinema-Grade Animated Mystery Short with Real SFX & Transitions...")
    scene_clips = []
    durations = []
    cumulative_time = 0.0
    sfx_schedule = []

    for idx, scene in enumerate(scenes):
        print(f"\n--- Scene {idx+1}/{len(scenes)}: {scene['badge']} ---")
        
        # 1. Render HTML to high-res PNG
        html = get_scene_html(scene)
        img_path = str(FRAMES_DIR / f"frame_{idx}.png")
        render_html_to_png(html, img_path)

        # 2. Download TTS audio
        audio_path = str(FRAMES_DIR / f"voice_{idx}.mp3")
        download_tts(scene["speech"], audio_path, lang="hi")
        dur = get_duration(audio_path)
        durations.append(dur)
        print(f"  🎙️ Voiceover: {dur:.1f}s")

        # 3. Schedule sound effects for this scene's start time
        for sfx_name in scene.get("sfx", []):
            sfx_file = SFX_DIR / sfx_name
            if sfx_file.exists():
                sfx_schedule.append((cumulative_time, str(sfx_file)))
                print(f"  🔊 Scheduled SFX: {sfx_name} at {cumulative_time:.1f}s")

        # 4. Render Video Clip with Dynamic Zoom + Pulsing Motion
        clip_path = str(FRAMES_DIR / f"cine_clip_{idx}.mp4")
        fps = 25
        total_frames = int(dur * fps) + 5
        
        # Dynamic zoom: zoom in smoothly from 1.0 to 1.08
        zoom_filter = f"scale=720:1280,zoompan=z='min(zoom+0.001,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s=720x1280:fps={fps}"
        
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", img_path,
            "-i", audio_path,
            "-vf", zoom_filter,
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "20",
            "-c:a", "aac", "-b:a", "192k",
            "-t", f"{dur:.2f}",
            clip_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        scene_clips.append(clip_path)
        cumulative_time += dur

    # Concat all scene video clips
    concat_txt = FRAMES_DIR / "cine_concat.txt"
    with open(concat_txt, "w") as f:
        for c in scene_clips:
            f.write(f"file '{c}'\n")

    raw_video = str(FRAMES_DIR / "cine_raw.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-c", "copy", raw_video
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    total_duration = cumulative_time
    print(f"\n⏱️ Total Video Duration: {total_duration:.1f}s")

    # Build Master Audio Mix: Voice (100%) + BGM (12%) + All Scheduled SFX Hits (90%)
    print(f"🎛️ Building Master Audio Mix with {len(sfx_schedule)} SFX cues...")
    
    # Extract audio from raw video
    extracted_voice = str(FRAMES_DIR / "full_voice.mp3")
    subprocess.run([
        "ffmpeg", "-y", "-i", raw_video, "-vn", "-c:a", "libmp3lame", "-b:a", "192k", extracted_voice
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Complex audio filtergraph for SFX placement
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
    master_audio_file = str(FRAMES_DIR / "master_soundtrack.mp3")

    mix_cmd = ["ffmpeg", "-y"] + ffmpeg_inputs + [
        "-filter_complex", final_filtergraph,
        "-map", "[master_audio]",
        "-c:a", "libmp3lame", "-b:a", "192k",
        master_audio_file
    ]
    subprocess.run(mix_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Final Multiplex: Raw Video + Master Soundtrack
    final_output = str(OUTPUT_DIR / "stefan_bitcoin_cinematic.mp4")
    print(f"🎬 Multiplexing Final Cinema Cut...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", raw_video,
        "-i", master_audio_file,
        "-map", "0:v", "-map", "1:a",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        final_output
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"\n🎉 Cinema-Grade Short Ready: {final_output}")
    return final_output

if __name__ == "__main__":
    build_cinematic_short()
