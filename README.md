# SpeakSkipType

**Speech-to-Text directly in your terminal. No API. No cloud. 100% FREE. Works locally on any laptop.**

```
  ____                   _    ____  _    _       _____
 / ___| _ __   ___  __ _| | _/ ___|| | _(_)_ __ |_   _|   _ _ __   ___
 \___ \| '_ \ / _ \/ _` | |/ \___ \| |/ / | '_ \  | || | | | '_ \ / _ \
  ___) | |_) |  __/ (_| |   < ___) |   <| | |_) | | || |_| | |_) |  __/
 |____/| .__/ \___|\__,_|_|\_\____/|_|\_\_| .__/  |_| \__, | .__/ \___|
       |_|                                |_|         |___/|_|
```

## The Problem

Every developer has been stuck in this loop:

1. Open ChatGPT or Google Voice
2. Click voice button
3. Speak
4. Wait for transcription
5. Copy text
6. Switch back to terminal
7. Paste

**That's 7 steps just to avoid typing!**

## The Solution

**SpeakSkipType** eliminates all that friction:

| Press | Action |
|-------|--------|
| `Ctrl+R` | Start recording |
| `Ctrl+S` | Stop & auto-type at cursor |
| `Ctrl+Q` | Quit |

**That's it. Speak directly into your terminal.**

## Features

- **100% FREE** - No API keys, no subscriptions
- **100% LOCAL** - All processing on your machine
- **100% OFFLINE** - Works without internet (after first setup)
- **Works Everywhere** - Windows, Linux, macOS
- **Any Terminal** - CMD, PowerShell, WSL, bash, zsh, fish
- **Auto-Type** - Text appears exactly where your cursor is
- **Lightweight** - ~40MB model, minimal CPU usage

## Quick Start

### One-Line Install

**Linux/macOS:**
```bash
git clone https://github.com/DandaAkhilReddy/Speakskiptype.git && cd Speakskiptype && pip install -r requirements.txt && python speakskiptype.py
```

**Windows:**
```cmd
git clone https://github.com/DandaAkhilReddy/Speakskiptype.git && cd Speakskiptype && pip install -r requirements.txt && python speakskiptype.py
```

### Step-by-Step

1. **Clone the repository**
   ```bash
   git clone https://github.com/DandaAkhilReddy/Speakskiptype.git
   cd Speakskiptype
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run**
   ```bash
   python speakskiptype.py
   ```

4. **First run** - The tool will automatically download the speech model (~40MB, one-time only)

## Usage

```
CONTROLS:
  Ctrl + R  =  Start Recording  (microphone ON)
  Ctrl + S  =  Stop & Auto-Type (text appears at cursor)
  Ctrl + Q  =  Quit Application
```

### Example Workflow

1. Open your terminal
2. Run `python speakskiptype.py` (keep it running in background)
3. Open another terminal or any text field
4. Press `Ctrl+R` and say "git commit -m fix authentication bug"
5. Press `Ctrl+S`
6. Watch the text auto-type at your cursor!

## Requirements

- Python 3.7+
- Microphone
- ~40MB disk space (for speech model)

## Dependencies

| Package | Purpose |
|---------|---------|
| `vosk` | Offline speech recognition (no API!) |
| `sounddevice` | Audio capture |
| `pynput` | Global hotkeys & auto-typing |

## How It Works

```
Your Voice --> Microphone --> Vosk (Local AI) --> Auto-Type at Cursor
                              (No Internet!)
```

1. **Vosk** runs a lightweight neural network locally on your CPU
2. **No data leaves your machine** - complete privacy
3. **No API calls** - no rate limits, no costs, no latency

## Troubleshooting

### "No speech detected"
- Check your microphone is connected and not muted
- Speak clearly and at a normal pace
- Check microphone permissions in system settings

### "Audio Error"
- Close other apps using the microphone
- Try a different audio input device

### Linux: Permission issues
```bash
# Add user to audio group
sudo usermod -a -G audio $USER
# Then log out and log back in
```

### Windows: Hotkeys not working
- Run the terminal as Administrator
- Or try running in a different terminal (PowerShell, CMD)

## Performance

| Metric | Value |
|--------|-------|
| Model Size | ~40MB |
| RAM Usage | ~200MB |
| CPU Usage | Low (runs on any laptop) |
| Latency | <500ms |
| Accuracy | 95%+ (clear speech) |

## Contributing

Pull requests are welcome! For major changes, please open an issue first.

## License

MIT License - Use it, modify it, share it freely.

## Star This Repo!

If this tool saves you time, please give it a star! It helps others discover it.

---

**Built with frustration by developers, for developers.**

*Stop copy-pasting. Start speaking.*
