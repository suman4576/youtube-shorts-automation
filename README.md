# 🎬 YouTube Shorts Automation & Cartoon Mystery Engine

An end-to-end, high-retention YouTube Shorts automation pipeline built for creators and faceless channels. Designed to run natively on Linux / Termux with zero heavy pip dependencies.

---

## ⚡ Features

- **🎨 Multi-Style Cartoon & Comic Rendering:** Generates SVG & HTML5 cartoon visual frames with glowing neon borders, comic speech bubbles, and expressive character reaction art.
- **🔊 Multi-Layered Sound Design (SFX):**
  - Dramatic Sub Bass Drop (`boom.mp3`)
  - Cinematic Transition Swoosh (`whoosh.mp3`)
  - Comic Blunder Stop (`scratch.mp3`)
  - Alarm Warning Buzzer (`buzzer.mp3`)
  - Urgent Clock Ticking (`tick.mp3`)
  - Success Bell Chime (`ding.mp3`)
- **🎙️ Zero-Dependency Voiceover:** Studio-quality speech synthesis without external API keys.
- **🎵 Automated BGM Mixing & Ducking:** Lowers background music volume during speech and swells during dramatic pauses.
- **🚀 Ken Burns Dynamic Motion:** Smooth pan and zoom camera movements on every cartoon scene.
- **📈 Integrated with `youtube-agent-skill`:**
  - 21 viral hook formulas scored with `hookscore.py`
  - Title and thumbnail pairing linter with `title.py`
  - Automated YouTube SEO descriptions and tags

---

## 📁 Project Structure

```text
├── generate_cinematic_cartoon.py  # Cinema-grade cartoon & mystery short generator
├── generate_cartoon_story.py      # Multi-scene cartoon story generator
├── engine.py                      # Multi-topic batch video factory
├── builder.py                     # Rapid short generator
├── topics.json                    # Viral topics & script beats catalog
├── assets/
│   ├── music/                     # Background music loops
│   └── sfx/                       # Synthesized sound effects (boom, whoosh, tick...)
└── output/                        # Rendered MP4 videos & SEO metadata
```

---

## 🚀 Quick Start

### 1. Generate a Cinema-Grade Mystery Cartoon Short:
```bash
python3 generate_cinematic_cartoon.py
```

### 2. Batch Generate Multi-Topic Shorts:
```bash
python3 engine.py --all
```

---

## 📄 License
MIT License. Created for **@TechSparksHindi**.
