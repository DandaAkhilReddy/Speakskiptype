<p align="center">
  <img src="https://img.shields.io/badge/🎤_SpeakSkipType-Speech_to_Text-blue?style=for-the-badge&logo=microphone" alt="SpeakSkipType"/>
</p>

<h1 align="center">🎤 SpeakSkipType</h1>

<p align="center">
  <strong>The ULTIMATE Speech-to-Text Tool for Developers</strong><br>
  <em>No API. No Cloud. 100% FREE. Works Locally.</em>
</p>

<p align="center">
  <a href="#-quick-start"><img src="https://img.shields.io/badge/Quick_Start-🚀-green?style=flat-square" alt="Quick Start"/></a>
  <a href="#-features"><img src="https://img.shields.io/badge/Features-✨-yellow?style=flat-square" alt="Features"/></a>
  <a href="#-installation"><img src="https://img.shields.io/badge/Install-📦-blue?style=flat-square" alt="Install"/></a>
  <a href="#-claude-code-integration"><img src="https://img.shields.io/badge/Claude_Code-🤖-purple?style=flat-square" alt="Claude Code"/></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue?style=flat-square&logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square" alt="Platform"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License"/>
  <img src="https://img.shields.io/badge/Tests-306%20Passing-brightgreen?style=flat-square" alt="Tests"/>
</p>

---

```
  ____                   _    ____  _    _       _____
 / ___| _ __   ___  __ _| | _/ ___|| | _(_)_ __ |_   _|   _ _ __   ___
 \___ \| '_ \ / _ \/ _` | |/ \___ \| |/ / | '_ \  | || | | | '_ \ / _ \
  ___) | |_) |  __/ (_| |   < ___) |   <| | |_) | | || |_| | |_) |  __/
 |____/| .__/ \___|\__,_|_|\_\____/|_|\_\_| .__/  |_| \__, | .__/ \___|
       |_|                                |_|         |___/|_|
```

<p align="center">
  <b>🗣️ Speak → 📝 Text appears at cursor → Done!</b>
</p>

---

## 🤔 The Problem

Every developer has been stuck in this painful loop:

```
┌─────────────────────────────────────────────────────────────┐
│  1. 🌐 Open browser/ChatGPT                                 │
│  2. 🎤 Click voice button                                   │
│  3. 🗣️ Speak                                                │
│  4. ⏳ Wait for transcription                               │
│  5. 📋 Copy text                                            │
│  6. 🔄 Switch back to terminal                              │
│  7. 📥 Paste                                                │
└─────────────────────────────────────────────────────────────┘
          ⬇️  That's 7 STEPS just to avoid typing!  ⬇️
```

## ✅ The Solution

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Press Ctrl+R  →  🗣️ Speak  →  Press Ctrl+S  →  ✅ Done!   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
              ⬆️  Just 2 STEPS with SpeakSkipType!  ⬆️
```

---

## 🚀 Quick Start

### One-Line Install & Run

```bash
git clone https://github.com/DandaAkhilReddy/Speakskiptype.git && cd Speakskiptype && pip install -r requirements.txt && python speakskiptype.py
```

### That's it! Now:
1. Press **`Ctrl+R`** to start recording
2. **Speak** your text
3. Press **`Ctrl+S`** to stop & paste

---

## ⌨️ Keyboard Controls

| Shortcut | Action | Description |
|:--------:|:------:|:------------|
| `Ctrl + R` | 🔴 **Toggle Record** | Start/Stop recording |
| `Ctrl + S` | ✅ **Stop & Paste** | Stop recording and paste text |
| `Ctrl + Shift + R` | 🎯 **Hold-to-Record** | Hold to record, release to paste |
| `Ctrl + D` | 🐛 **Debug Mode** | Toggle debug output |
| `Ctrl + H` | 📜 **History** | Show transcription history |
| `Ctrl + Q` | 🚪 **Quit** | Exit application |

---

## ✨ Features

### 🏆 Superior to ALL Competitors

| Feature | SpeakSkipType | Handy | OpenWhispr | voice_typing |
|:--------|:-------------:|:-----:|:----------:|:------------:|
| 100% Free | ✅ | ✅ | ✅ | ✅ |
| 100% Offline | ✅ | ❌ | ✅ | ✅ |
| Multi-Engine (Vosk + Whisper) | ✅ | ❌ | ❌ | ❌ |
| Filler Word Removal | ✅ | ❌ | ❌ | ❌ |
| Continuous Listening | ✅ | ❌ | ❌ | ❌ |
| Voice Commands | ✅ | ✅ | ❌ | ❌ |
| Custom Vocabulary | ✅ | ❌ | ❌ | ❌ |
| Code Dictation Mode | ✅ | ❌ | ❌ | ❌ |
| Hold-to-Record | ✅ | ❌ | ❌ | ❌ |
| Auto-Punctuation | ✅ | ❌ | ❌ | ❌ |
| Export History | ✅ | ❌ | ❌ | ❌ |

### 🎯 All Features at a Glance

```
┌────────────────────────────────────────────────────────────────────┐
│                        🎤 SPEAKSKIPTYPE                            │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  🔧 ENGINES              │  🎛️ MODES                               │
│  ├─ Vosk (fast/light)    │  ├─ Normal recording                   │
│  └─ Whisper (accurate)   │  ├─ Hold-to-record                     │
│                          │  ├─ Continuous listening               │
│  🧹 TEXT PROCESSING      │  └─ Background/tray mode               │
│  ├─ Filler word removal  │                                        │
│  ├─ Auto-punctuation     │  🗣️ VOICE COMMANDS                     │
│  ├─ Custom vocabulary    │  ├─ "new line" → ↵                     │
│  └─ Code dictation mode  │  ├─ "period" → .                       │
│                          │  ├─ "delete that" → undo               │
│  📊 EXTRAS               │  └─ "question mark" → ?                │
│  ├─ Statistics (WPM)     │                                        │
│  ├─ History export       │  🌍 MULTI-PLATFORM                     │
│  └─ Real-time display    │  ├─ Windows ✅                          │
│                          │  ├─ macOS ✅                             │
│                          │  └─ Linux ✅                             │
└────────────────────────────────────────────────────────────────────┘
```

---

## 📦 Installation

### Prerequisites
- Python 3.7+
- Microphone
- ~40MB disk space

### Step-by-Step

```bash
# 1. Clone the repo
git clone https://github.com/DandaAkhilReddy/Speakskiptype.git
cd Speakskiptype

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run!
python speakskiptype.py
```

### First Run
The tool automatically downloads the speech model (~40MB, one-time only).

---

## 🎮 Usage Examples

### Basic Usage
```bash
python speakskiptype.py
```

### With Whisper (More Accurate)
```bash
python speakskiptype.py --whisper
```

### Continuous Listening (Like Speechnotes)
```bash
python speakskiptype.py --continuous
```

### Code Dictation Mode
```bash
python speakskiptype.py --code
```

### Background Mode (System Tray)
```bash
python speakskiptype.py --bg
```

### All Options Combined
```bash
python speakskiptype.py --whisper --continuous --no-filler --code
```

---

## 🤖 Claude Code Integration

**NEW!** Use voice input directly with Claude Code!

### Setup
```bash
# Terminal 1: Start voice input helper
python claude_voice.py

# Terminal 2: Open Claude Code
claude
```

### Usage
| Key | Action |
|:---:|:-------|
| `F8` | Toggle recording (start/stop + auto-paste) |
| `ESC` | Exit voice helper |

### Workflow
```
┌─────────────────────────────────────────────────────────────┐
│  1. Run claude_voice.py (keep open)                         │
│  2. Run claude in another terminal                          │
│  3. Press F8 → Speak → Press F8                             │
│  4. Your speech appears in Claude Code! 🎉                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗣️ Voice Commands

Speak these commands while recording:

| Say This | Get This |
|:---------|:---------|
| "new line" | ↵ (line break) |
| "new paragraph" | ↵↵ (double line break) |
| "period" | . |
| "comma" | , |
| "question mark" | ? |
| "exclamation mark" | ! |
| "open paren" | ( |
| "close paren" | ) |
| "delete that" | (removes last phrase) |

---

## 🧹 Filler Word Removal

SpeakSkipType automatically removes filler words:

| You Say | You Get |
|:--------|:--------|
| "I um want to uh test this" | "I want to test this" |
| "So like you know it works" | "So it works" |
| "I mean basically it's done" | "it's done" |

**Filler words removed:** um, uh, er, ah, like, you know, i mean, sort of, kind of, basically, actually, literally, so yeah, right, okay so, well

---

## ⚙️ Configuration

### Command Line Flags

| Flag | Description |
|:-----|:------------|
| `--whisper` | Use Whisper engine (more accurate) |
| `--continuous` | Continuous listening mode |
| `--code` | Code dictation mode |
| `--vad` | Voice Activity Detection |
| `--no-filler` | Remove filler words |
| `--literal` | Literal punctuation mode |
| `--bg` | Run in background |
| `--stats` | Show statistics |
| `--export` | Export history |

### Custom Vocabulary

Edit the config to add custom word replacements:
```python
"custom_vocabulary": {
    "kubernetes": "K8s",
    "javascript": "JavaScript",
    "python": "Python"
}
```

---

## 📊 Performance

| Metric | Vosk | Whisper |
|:-------|:----:|:-------:|
| Model Size | ~40MB | ~150MB |
| RAM Usage | ~200MB | ~500MB |
| Speed | ⚡ Fast | 🐢 Slower |
| Accuracy | 90% | 98% |
| Offline | ✅ Yes | ✅ Yes |

---

## 🔧 Troubleshooting

<details>
<summary><b>🔇 "No speech detected"</b></summary>

- Check microphone is connected and not muted
- Speak clearly at normal pace
- Check system microphone permissions
</details>

<details>
<summary><b>🎤 "Audio Error"</b></summary>

- Close other apps using microphone
- Try different audio input device
- Restart the application
</details>

<details>
<summary><b>🐧 Linux: Permission issues</b></summary>

```bash
sudo usermod -a -G audio $USER
# Log out and log back in
```
</details>

<details>
<summary><b>🪟 Windows: Hotkeys not working</b></summary>

- Run terminal as Administrator
- Try different terminal (PowerShell, CMD)
</details>

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=speakskiptype

# 306 tests passing ✅
```

---

## 🤝 Contributing

Pull requests welcome! For major changes, open an issue first.

```bash
# Fork & clone
git clone https://github.com/YOUR_USERNAME/Speakskiptype.git

# Create feature branch
git checkout -b feature/amazing-feature

# Make changes & test
pytest tests/ -v

# Commit & push
git commit -m "Add amazing feature"
git push origin feature/amazing-feature

# Open Pull Request
```

---

## 📄 License

MIT License - Use it, modify it, share it freely.

---

## ⭐ Star This Repo!

If SpeakSkipType saves you time, please give it a ⭐!

It helps others discover this tool.

---

<p align="center">
  <b>Built with ❤️ by developers, for developers.</b>
</p>

<p align="center">
  <em>Stop copy-pasting. Start speaking.</em>
</p>

<p align="center">
  <a href="https://github.com/DandaAkhilReddy/Speakskiptype">
    <img src="https://img.shields.io/badge/GitHub-⭐_Star_This_Repo-yellow?style=for-the-badge&logo=github" alt="Star"/>
  </a>
</p>
