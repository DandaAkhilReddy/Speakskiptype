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
│   Press Alt+R  →  🗣️ Speak  →  Press Alt+S  →  ✅ Done!   │
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

> **Note:** On first run, wait **2-15 minutes** for the speech model to download (~40MB). Time depends on your internet speed. This only happens once!

### That's it! Now:
1. Press **`Alt+R`** to start recording
2. **Speak** your text
3. Press **`Alt+S`** to stop & paste

---

## ⌨️ Keyboard Controls

| Shortcut | Action | Description |
|:--------:|:------:|:------------|
| `Alt + R` | 🔴 **Start Record** | Start recording (no terminal conflict!) |
| `Alt + S` | ✅ **Stop & Paste** | Stop recording and paste text |
| `Alt + Q` | 🚪 **Quit** | Exit application |
| `Ctrl + D` | 🐛 **Debug Mode** | Toggle debug output |
| `Ctrl + H` | 📜 **History** | Show transcription history |

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

### First Run - IMPORTANT!

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ⚠️  FIRST RUN: Please wait for model download!                         │
│                                                                         │
│  The speech recognition model (~40MB) downloads automatically.          │
│  You'll see: "[*] Downloading speech model (first time only)..."       │
│                                                                         │
│  ⏱️  Download time: 2-15 minutes (depends on internet speed)            │
│      - Fast internet (50+ Mbps): ~2-3 minutes                           │
│      - Average internet (10-50 Mbps): ~5-8 minutes                      │
│      - Slow internet (<10 Mbps): ~10-15 minutes                         │
│                                                                         │
│  ✓ This only happens ONCE                                               │
│  ✓ After download, the app starts instantly                             │
│  ✓ Model is saved to ~/.speakskiptype/                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

**What to expect on first run:**
1. App starts and shows "Downloading speech model..."
2. **Wait 2-15 minutes** (depending on your internet speed)
3. You'll see "Model downloaded!" when complete
4. The main interface appears - you're ready to go!

**If it seems stuck:**
- The download IS happening in the background
- No progress bar is shown (this is normal)
- Just wait patiently - it WILL complete
- On slow connections, it can take up to 15 minutes
- Check `~/.speakskiptype/` folder to see if model is downloading

---

## 🧪 How to Test (Step-by-Step)

### 📋 Before You Start
Make sure you have:
- ✅ Python 3.7+ installed (`python --version` to check)
- ✅ A working microphone
- ✅ Speakers/headphones (to hear beep feedback)

---

### 🪟 Windows Testing

**Step 1: Open Command Prompt**
```cmd
Win + R → type "cmd" → Enter
```

**Step 2: Navigate to the folder**
```cmd
cd C:\Users\YourUsername\Speakskiptype
```

**Step 3: Install dependencies**
```cmd
pip install vosk sounddevice pynput pyperclip
```

**Step 4: Run the app**
```cmd
python speakskiptype.py
```

**Step 5: Test it!**
```
┌────────────────────────────────────────────────────────────┐
│  1. Open Notepad (or any text editor)                      │
│  2. Click inside Notepad so cursor is there                │
│  3. Press Alt+R (you'll hear a beep - recording started)  │
│  4. Say: "Hello world this is a test"                      │
│  5. Press Alt+S (you'll hear a beep - recording stopped)  │
│  6. Watch the text appear in Notepad! ✨                   │
└────────────────────────────────────────────────────────────┘
```

---

### 🍎 macOS Testing

**Step 1: Open Terminal**
```bash
Cmd + Space → type "Terminal" → Enter
```

**Step 2: Navigate and install**
```bash
cd ~/Speakskiptype
pip3 install vosk sounddevice pynput pyperclip
```

**Step 3: Grant permissions**
- Go to System Preferences → Security & Privacy → Privacy
- Enable **Microphone** access for Terminal
- Enable **Accessibility** access for Terminal (for hotkeys)

**Step 4: Run and test**
```bash
python3 speakskiptype.py
```

---

### 🐧 Linux Testing

**Step 1: Open Terminal**
```bash
Ctrl + Alt + T
```

**Step 2: Install system dependencies**
```bash
# Ubuntu/Debian
sudo apt install python3-pip portaudio19-dev

# Fedora
sudo dnf install python3-pip portaudio-devel
```

**Step 3: Install Python packages**
```bash
cd ~/Speakskiptype
pip3 install vosk sounddevice pynput pyperclip
```

**Step 4: Run and test**
```bash
python3 speakskiptype.py
```

---

### ✅ Test Checklist

Use this checklist to verify everything works:

| # | Test | Expected Result | Status |
|:-:|:-----|:----------------|:------:|
| 1 | Run `python speakskiptype.py` | Banner appears with controls | ⬜ |
| 2 | Press `Alt+R` | See `[REC] Recording...` + beep | ⬜ |
| 3 | Speak "hello world" | See `Hearing: hello world...` | ⬜ |
| 4 | Press `Alt+S` | See `[STOP]` + `[DONE]` + beep | ⬜ |
| 5 | Check Notepad/editor | Text "hello world" appeared | ⬜ |
| 6 | Press `Alt+Q` | App exits cleanly | ⬜ |

---

### 🎤 Test Filler Word Removal

**Say this:**
> "Um I would like to you know test this application"

**Expected output:**
> "I would like to test this application"

The filler words (um, you know) are automatically removed! ✨

---

### 🔊 Test Voice Commands

| Say This | Expected Output |
|:---------|:----------------|
| "hello period" | hello. |
| "new line test" | hello<br>test |
| "open paren test close paren" | (test) |

---

### 🐛 Common Issues & Fixes

<details>
<summary><b>❌ "No module named 'vosk'"</b></summary>

```bash
pip install vosk
```
</details>

<details>
<summary><b>❌ "No speech detected" every time</b></summary>

1. Check microphone is not muted
2. Check microphone permissions in system settings
3. Try speaking louder/closer to mic
4. Run: `python -c "import sounddevice; print(sounddevice.query_devices())"` to see devices
</details>

<details>
<summary><b>❌ Text not appearing in editor</b></summary>

1. Make sure the editor window is focused/active
2. Try clicking in the editor right before pressing Alt+S
3. Check if clipboard is working: `python -c "import pyperclip; pyperclip.copy('test'); print(pyperclip.paste())"`
</details>

<details>
<summary><b>❌ Hotkeys not working (Windows)</b></summary>

Run Command Prompt as Administrator:
1. Search "cmd" in Start Menu
2. Right-click → "Run as administrator"
3. Try again
</details>

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

## 🧠 Anthropic API with Extended Thinking

**NEW!** Direct integration with Claude's API including proper support for Extended Thinking.

### The Problem

When using Claude's **extended thinking** feature via the Anthropic API, you might encounter this error:

```
Error: thinking blocks must be preserved exactly as received
```

This happens when:
- Thinking blocks are modified or removed from conversation history
- The order of content blocks is changed
- Follow-up messages don't include the original thinking blocks

### The Solution

We provide `anthropic_client.py` - a client that **automatically handles extended thinking** correctly.

### Installation

```bash
pip install anthropic
```

### Quick Start

```python
from anthropic_client import ClaudeClient

# Create client (uses ANTHROPIC_API_KEY env var)
client = ClaudeClient()

# First message - thinking blocks are generated internally
response = client.send_message("Explain quantum entanglement")
print(response)

# Follow-up - thinking blocks are automatically preserved!
response = client.send_message("Can you give a simpler analogy?")
print(response)

# Start fresh conversation (clears all history including thinking)
client.clear_conversation()
```

### Configuration Options

```python
from anthropic_client import ClaudeClient

client = ClaudeClient(
    api_key="your-api-key",           # Or set ANTHROPIC_API_KEY env var
    model="claude-sonnet-4-20250514",    # Model to use
    max_tokens=16000,                  # Max response tokens
    thinking_enabled=True,             # Enable extended thinking
    thinking_budget=10000              # Token budget for thinking
)

# Disable thinking for simpler queries
client.disable_thinking()

# Re-enable with custom budget
client.enable_thinking(budget_tokens=5000)
```

### How It Works

The key fix is preserving `response.content` exactly as returned:

```python
# CORRECT - Store complete response including thinking blocks
self._messages.append({
    "role": "assistant",
    "content": response.content  # Includes ALL blocks unchanged
})

# WRONG - Don't filter or modify!
# content = [b for b in response.content if b.type == "text"]  # BAD!
```

### Extended Thinking Rules

| Rule | Description |
|:-----|:------------|
| Never modify | Keep thinking/redacted_thinking blocks exactly as received |
| Never remove | Include all blocks in conversation history |
| Keep order | Don't reorder content blocks |
| First position | Thinking block must be first in assistant's content array |

### API Reference

| Method | Description |
|:-------|:------------|
| `send_message(text)` | Send message, returns text response |
| `clear_conversation()` | Start fresh conversation |
| `get_conversation_history()` | Get full history with thinking blocks |
| `disable_thinking()` | Turn off extended thinking |
| `enable_thinking(budget)` | Turn on with token budget |

### Example: Multi-turn Conversation

```python
from anthropic_client import ClaudeClient

client = ClaudeClient(thinking_budget=8000)

# Turn 1 - Claude thinks through the problem
r1 = client.send_message("What's 15 * 23?")
print(f"Answer: {r1}")

# Turn 2 - Previous thinking is preserved automatically
r2 = client.send_message("Now multiply that by 2")
print(f"Answer: {r2}")

# Turn 3 - Full context maintained
r3 = client.send_message("What was my first question?")
print(f"Answer: {r3}")
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
