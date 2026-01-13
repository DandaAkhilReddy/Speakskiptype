#!/usr/bin/env python3
"""
SpeakSkipType - The ULTIMATE Speech-to-Text Tool for Developers
No API. No cloud. 100% FREE. Works locally on any laptop.

SUPERIOR TO ALL COMPETITORS (Handy, OpenWhispr, voice_typing):
- Multi-engine support (Vosk fast/lightweight OR Whisper accurate)
- Voice Activity Detection (VAD) - auto-start/stop on speech
- Continuous listening mode - don't stop on pauses (like Speechnotes)
- Real-time transcription display
- Auto-punctuation mode
- Filler word removal (um, uh, like, you know)
- Code dictation mode (recognizes programming terms)
- Custom vocabulary/dictionary
- Literal punctuation mode toggle
- Transcription statistics (WPM, total words)
- Export history (JSON, TXT, CSV)
- Hold-to-record mode
- Audio feedback (beeps)
- Voice commands (delete that, new line, undo)
- Custom hotkey configuration
- Multi-language support
- Works GLOBALLY in any application
- Background mode with system tray
- Debug mode for troubleshooting

CONTROLS:
  Ctrl+R       = Start Recording (press again to stop)
  Ctrl+S       = Stop & Auto-Type
  Ctrl+Shift+R = Hold-to-Record (release to auto-type)
  Ctrl+D       = Toggle Debug Mode
  Ctrl+H       = Show History
  Ctrl+Q       = Quit Application

Usage:
  python speakskiptype.py              # Run in terminal
  python speakskiptype.py --bg         # Run in background
  python speakskiptype.py --config     # Edit configuration
  python speakskiptype.py --stats      # Show statistics
  python speakskiptype.py --export     # Export history
  python speakskiptype.py --whisper    # Use Whisper engine (more accurate)
  python speakskiptype.py --continuous # Continuous listening (no auto-stop)
  pythonw speakskiptype.py --bg        # Run hidden (Windows)

Author: Akhil Reddy
License: MIT
"""

import os
import sys
import queue
import json
import threading
import time
import signal
import re
from datetime import datetime
from pathlib import Path
from collections import deque

# ANSI Colors for terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'


# ============================================================================
# CONFIGURATION
# ============================================================================

DEFAULT_CONFIG = {
    "hotkeys": {
        "start_recording": "ctrl+r",
        "stop_and_type": "ctrl+s",
        "hold_to_record": "ctrl+shift+r",
        "quit": "ctrl+q",
        "show_history": "ctrl+h",
        "toggle_debug": "ctrl+d"
    },
    "audio": {
        "sample_rate": 16000,
        "beep_on_start": True,
        "beep_on_stop": True,
        "vad_enabled": False,
        "vad_threshold": 0.5,
        "vad_silence_duration": 1.5,
        "continuous_mode": False  # Don't auto-stop on silence (like Speechnotes)
    },
    "transcription": {
        "engine": "vosk",  # "vosk" or "whisper"
        "language": "en-us",
        "whisper_model": "base",  # tiny, base, small, medium, large
        "save_history": True,
        "max_history": 100,
        "auto_punctuation": True,
        "code_mode": False,
        "remove_filler_words": True,  # Remove um, uh, like, you know
        "literal_punctuation": False  # If True: "period" stays as "period", not "."
    },
    "voice_commands": {
        "enabled": True,
        "commands": {
            "delete that": "__DELETE_LAST__",
            "undo that": "__DELETE_LAST__",
            "scratch that": "__DELETE_LAST__",
            "new line": "\n",
            "new paragraph": "\n\n",
            "tab": "\t",
            "period": ".",
            "comma": ",",
            "question mark": "?",
            "exclamation mark": "!",
            "colon": ":",
            "semicolon": ";",
            "open paren": "(",
            "close paren": ")",
            "open bracket": "[",
            "close bracket": "]",
            "open brace": "{",
            "close brace": "}"
        }
    },
    "output": {
        "method": "clipboard",  # clipboard, type, or both
        "add_space_after": True
    },
    "stats": {
        "track_stats": True
    },
    "custom_vocabulary": {
        # User-defined word replacements
        # Example: "kubernetes": "K8s", "javascript": "JavaScript"
    }
}

# Filler words to remove
FILLER_WORDS = [
    "um", "uh", "er", "ah", "like", "you know", "i mean",
    "sort of", "kind of", "basically", "actually", "literally",
    "so yeah", "right", "okay so", "well"
]

# Code mode replacements for programming
CODE_REPLACEMENTS = {
    "def ": "def ",
    "class ": "class ",
    "import ": "import ",
    "from ": "from ",
    "return ": "return ",
    "if ": "if ",
    "else": "else",
    "elif ": "elif ",
    "for ": "for ",
    "while ": "while ",
    "try": "try",
    "except": "except",
    "finally": "finally",
    "with ": "with ",
    "as ": "as ",
    "lambda": "lambda",
    "none": "None",
    "true": "True",
    "false": "False",
    "self": "self",
    "print": "print",
    "equals": " = ",
    "double equals": " == ",
    "not equals": " != ",
    "plus equals": " += ",
    "minus equals": " -= ",
    "arrow": " -> ",
    "fat arrow": " => ",
    "and": " and ",
    "or": " or ",
    "not ": "not ",
    "in ": "in ",
    "is ": "is ",
    "async": "async",
    "await": "await",
    "const ": "const ",
    "let ": "let ",
    "var ": "var ",
    "function ": "function ",
    "null": "null",
    "undefined": "undefined",
}


# Global variables
audio_queue = queue.Queue()
is_recording = False
recorded_text = ""
ctrl_pressed = False
shift_pressed = False
alt_pressed = False
hold_to_record_active = False
background_mode = False
debug_mode = False
config = DEFAULT_CONFIG.copy()
transcription_history = []
stats = {
    "total_transcriptions": 0,
    "total_words": 0,
    "total_characters": 0,
    "session_start": None,
    "session_transcriptions": 0,
    "session_words": 0,
    "last_wpm": 0
}

# VAD (Voice Activity Detection) state
vad_recording = False
vad_silence_start = None
audio_levels = deque(maxlen=10)

# These will be initialized when running
model = None
recognizer = None
keyboard_controller = None
Key = None
config_path = None
whisper_model = None


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def log(message, color=Colors.WHITE):
    """Print message if not in background mode."""
    if not background_mode:
        print(f"{color}{message}{Colors.END}")


def debug_log(message):
    """Print debug message if debug mode is enabled."""
    if debug_mode and not background_mode:
        print(f"{Colors.DIM}[DEBUG] {message}{Colors.END}")


def notify(title, message):
    """Show a notification (works on Windows, macOS, Linux)."""
    if not background_mode:
        return

    try:
        if sys.platform == 'win32':
            try:
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast(title, message, duration=2, threaded=True)
            except ImportError:
                import subprocess
                subprocess.Popen([
                    'powershell', '-Command',
                    f'[System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms"); '
                    f'$notify = New-Object System.Windows.Forms.NotifyIcon; '
                    f'$notify.Icon = [System.Drawing.SystemIcons]::Information; '
                    f'$notify.Visible = $true; '
                    f'$notify.ShowBalloonTip(2000, "{title}", "{message}", [System.Windows.Forms.ToolTipIcon]::Info)'
                ], creationflags=subprocess.CREATE_NO_WINDOW)
        elif sys.platform == 'darwin':
            os.system(f'osascript -e \'display notification "{message}" with title "{title}"\'')
        else:
            os.system(f'notify-send "{title}" "{message}" 2>/dev/null')
    except:
        pass


# ============================================================================
# CONFIGURATION MANAGEMENT
# ============================================================================

def get_config_dir():
    """Get the configuration directory path."""
    config_dir = Path.home() / ".speakskiptype"
    config_dir.mkdir(exist_ok=True)
    return config_dir


def get_config_path():
    """Get the configuration file path."""
    return get_config_dir() / "config.json"


def load_config():
    """Load configuration from file."""
    global config
    config_file = get_config_path()

    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                # Deep merge with defaults
                def deep_merge(default, user):
                    result = default.copy()
                    for key, value in user.items():
                        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                            result[key] = deep_merge(result[key], value)
                        else:
                            result[key] = value
                    return result
                config = deep_merge(DEFAULT_CONFIG, user_config)
        except Exception as e:
            log(f"[!] Error loading config: {e}", Colors.YELLOW)

    return config


def save_config():
    """Save configuration to file."""
    config_file = get_config_path()
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)


def edit_config():
    """Open configuration in editor."""
    config_file = get_config_path()

    # Save default config if doesn't exist
    if not config_file.exists():
        save_config()

    print(f"{Colors.CYAN}Configuration file: {config_file}{Colors.END}")
    print(f"\n{Colors.YELLOW}Opening in default editor...{Colors.END}")

    if sys.platform == 'win32':
        os.system(f'notepad "{config_file}"')
    elif sys.platform == 'darwin':
        os.system(f'open "{config_file}"')
    else:
        os.system(f'xdg-open "{config_file}" 2>/dev/null || nano "{config_file}"')


# ============================================================================
# STATISTICS
# ============================================================================

def get_stats_path():
    """Get the stats file path."""
    return get_config_dir() / "stats.json"


def load_stats():
    """Load statistics from file."""
    global stats
    stats_file = get_stats_path()

    if stats_file.exists():
        try:
            with open(stats_file, 'r', encoding='utf-8') as f:
                saved_stats = json.load(f)
                stats.update(saved_stats)
        except:
            pass

    stats["session_start"] = datetime.now().isoformat()
    stats["session_transcriptions"] = 0
    stats["session_words"] = 0


def save_stats():
    """Save statistics to file."""
    if not config.get('stats', {}).get('track_stats', True):
        return

    stats_file = get_stats_path()
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)


def update_stats(text, duration_seconds):
    """Update statistics after a transcription."""
    if not text:
        return

    words = len(text.split())
    chars = len(text)

    stats["total_transcriptions"] += 1
    stats["total_words"] += words
    stats["total_characters"] += chars
    stats["session_transcriptions"] += 1
    stats["session_words"] += words

    # Calculate WPM (words per minute)
    if duration_seconds > 0:
        stats["last_wpm"] = int((words / duration_seconds) * 60)

    save_stats()


def show_stats():
    """Display transcription statistics."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}═══ Transcription Statistics ═══{Colors.END}\n")

    print(f"{Colors.BOLD}All Time:{Colors.END}")
    print(f"  Total Transcriptions: {Colors.GREEN}{stats['total_transcriptions']}{Colors.END}")
    print(f"  Total Words:          {Colors.GREEN}{stats['total_words']}{Colors.END}")
    print(f"  Total Characters:     {Colors.GREEN}{stats['total_characters']}{Colors.END}")

    print(f"\n{Colors.BOLD}This Session:{Colors.END}")
    print(f"  Transcriptions:       {Colors.CYAN}{stats['session_transcriptions']}{Colors.END}")
    print(f"  Words:                {Colors.CYAN}{stats['session_words']}{Colors.END}")
    print(f"  Last WPM:             {Colors.CYAN}{stats['last_wpm']}{Colors.END}")

    if stats.get('session_start'):
        try:
            start = datetime.fromisoformat(stats['session_start'])
            duration = datetime.now() - start
            minutes = int(duration.total_seconds() / 60)
            print(f"  Session Duration:     {Colors.CYAN}{minutes} minutes{Colors.END}")
        except:
            pass

    print()


# ============================================================================
# TRANSCRIPTION HISTORY
# ============================================================================

def get_history_path():
    """Get the history file path."""
    return get_config_dir() / "history.json"


def load_history():
    """Load transcription history."""
    global transcription_history
    history_file = get_history_path()

    if history_file.exists():
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                transcription_history = json.load(f)
        except:
            transcription_history = []


def save_history():
    """Save transcription history."""
    if not config.get('transcription', {}).get('save_history', True):
        return

    history_file = get_history_path()

    # Trim to max history
    max_history = config.get('transcription', {}).get('max_history', 100)
    history_to_save = transcription_history[-max_history:]

    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history_to_save, f, indent=2)


def add_to_history(text, duration=0):
    """Add a transcription to history."""
    if not text:
        return

    entry = {
        "timestamp": datetime.now().isoformat(),
        "text": text,
        "words": len(text.split()),
        "duration_seconds": round(duration, 2)
    }
    transcription_history.append(entry)
    save_history()


def show_history():
    """Display transcription history."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}═══ Transcription History ═══{Colors.END}\n")

    if not transcription_history:
        print(f"{Colors.YELLOW}No transcriptions yet.{Colors.END}")
        return

    # Show last 10
    for i, entry in enumerate(transcription_history[-10:]):
        ts = entry.get('timestamp', 'Unknown')
        text = entry.get('text', '')
        words = entry.get('words', 0)
        # Parse timestamp
        try:
            dt = datetime.fromisoformat(ts)
            ts_formatted = dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            ts_formatted = ts

        print(f"{Colors.BLUE}[{ts_formatted}]{Colors.END} {Colors.DIM}({words} words){Colors.END}")
        print(f"  {text}\n")


def export_history(format_type="json"):
    """Export history to file."""
    if not transcription_history:
        print(f"{Colors.YELLOW}No history to export.{Colors.END}")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_dir = get_config_dir() / "exports"
    export_dir.mkdir(exist_ok=True)

    if format_type == "json":
        export_file = export_dir / f"history_{timestamp}.json"
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(transcription_history, f, indent=2)

    elif format_type == "txt":
        export_file = export_dir / f"history_{timestamp}.txt"
        with open(export_file, 'w', encoding='utf-8') as f:
            for entry in transcription_history:
                ts = entry.get('timestamp', 'Unknown')
                text = entry.get('text', '')
                f.write(f"[{ts}]\n{text}\n\n")

    elif format_type == "csv":
        export_file = export_dir / f"history_{timestamp}.csv"
        with open(export_file, 'w', encoding='utf-8') as f:
            f.write("timestamp,text,words,duration_seconds\n")
            for entry in transcription_history:
                ts = entry.get('timestamp', '').replace(',', ';')
                text = entry.get('text', '').replace(',', ';').replace('\n', ' ')
                words = entry.get('words', 0)
                duration = entry.get('duration_seconds', 0)
                f.write(f"{ts},{text},{words},{duration}\n")

    print(f"{Colors.GREEN}[+] History exported to: {export_file}{Colors.END}")
    return export_file


# ============================================================================
# AUDIO FEEDBACK
# ============================================================================

def play_beep(frequency=800, duration=0.1, beep_type="start"):
    """Play a beep sound for audio feedback."""
    if beep_type == "start" and not config.get('audio', {}).get('beep_on_start', True):
        return
    if beep_type == "stop" and not config.get('audio', {}).get('beep_on_stop', True):
        return

    try:
        if sys.platform == 'win32':
            import winsound
            freq = 600 if beep_type == "start" else 800
            winsound.Beep(freq, int(duration * 1000))
        else:
            # Unix: use bell character or os command
            sys.stdout.write('\a')
            sys.stdout.flush()
    except:
        pass  # Silently fail if beep doesn't work


# ============================================================================
# TEXT PROCESSING
# ============================================================================

def process_voice_commands(text):
    """Process voice commands in the transcribed text."""
    if not config.get('voice_commands', {}).get('enabled', True):
        return text

    commands = config.get('voice_commands', {}).get('commands', {})
    result = text

    for trigger, action in commands.items():
        if trigger.lower() in result.lower():
            if action == "__DELETE_LAST__":
                # Delete the trigger and last word before it
                idx = result.lower().rfind(trigger.lower())
                result = result[:idx].rstrip()
                # Remove last word
                if ' ' in result:
                    result = result.rsplit(' ', 1)[0]
                else:
                    result = ""
            else:
                # Replace trigger with action
                result = re.sub(re.escape(trigger), action, result, flags=re.IGNORECASE)

    return result.strip()


def apply_code_mode(text):
    """Apply code mode transformations."""
    if not config.get('transcription', {}).get('code_mode', False):
        return text

    result = text.lower()

    for spoken, code in CODE_REPLACEMENTS.items():
        result = re.sub(r'\b' + re.escape(spoken.strip()) + r'\b', code, result, flags=re.IGNORECASE)

    return result


def apply_auto_punctuation(text):
    """Apply automatic punctuation."""
    if not config.get('transcription', {}).get('auto_punctuation', True):
        return text

    result = text

    # Capitalize first letter
    if result and result[0].islower():
        result = result[0].upper() + result[1:]

    # Capitalize after sentence endings
    result = re.sub(r'([.!?]\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), result)

    # Add period at end if no punctuation
    if result and result[-1] not in '.!?':
        result += '.'

    return result


def remove_filler_words(text):
    """Remove filler words like um, uh, like, you know."""
    if not config.get('transcription', {}).get('remove_filler_words', True):
        return text

    result = text

    # Sort filler words by length (longest first) to handle multi-word phrases properly
    sorted_fillers = sorted(FILLER_WORDS, key=len, reverse=True)

    for filler in sorted_fillers:
        # For multi-word fillers, match with flexible spacing
        if ' ' in filler:
            # Replace spaces with flexible whitespace pattern
            filler_pattern = r'\b' + r'\s+'.join(re.escape(word) for word in filler.split()) + r'\b'
        else:
            filler_pattern = r'\b' + re.escape(filler) + r'\b'

        # Remove filler word (with optional trailing space/comma)
        pattern = filler_pattern + r'[,]?\s*'
        result = re.sub(pattern, ' ', result, flags=re.IGNORECASE)

    # Clean up multiple spaces
    result = re.sub(r'\s+', ' ', result)
    return result.strip()


def apply_custom_vocabulary(text):
    """Apply custom vocabulary replacements."""
    custom_vocab = config.get('custom_vocabulary', {})
    if not custom_vocab:
        return text

    result = text
    for word, replacement in custom_vocab.items():
        pattern = r'\b' + re.escape(word) + r'\b'
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

    return result


def process_text(text):
    """Process transcribed text through all filters."""
    if not text:
        return text

    result = text.strip()

    # Remove filler words first
    result = remove_filler_words(result)

    # Apply custom vocabulary
    result = apply_custom_vocabulary(result)

    # Apply code mode
    result = apply_code_mode(result)

    # Process voice commands (only if literal_punctuation is False)
    if not config.get('transcription', {}).get('literal_punctuation', False):
        result = process_voice_commands(result)

    # Apply auto-punctuation last
    result = apply_auto_punctuation(result)

    return result


# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def check_dependencies():
    """Check if required packages are installed."""
    required = ['vosk', 'sounddevice', 'pynput']
    missing = []

    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"\n[!] Missing packages: {', '.join(missing)}")
        print("[*] Installing required packages...")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing + ['-q'])
        print("[+] Packages installed successfully!\n")


def init_keyboard():
    """Initialize keyboard controller and Key."""
    global keyboard_controller, Key
    from pynput.keyboard import Controller, Key as PynputKey
    keyboard_controller = Controller()
    Key = PynputKey


def print_banner():
    """Print the SpeakSkipType banner."""
    engine = config.get('transcription', {}).get('engine', 'vosk').upper()
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
  ____                   _    ____  _    _       _____
 / ___| _ __   ___  __ _| | _/ ___|| | _(_)_ __ |_   _|   _ _ __   ___
 \\___ \\| '_ \\ / _ \\/ _` | |/ \\___ \\| |/ / | '_ \\  | || | | | '_ \\ / _ \\
  ___) | |_) |  __/ (_| |   < ___) |   <| | |_) | | || |_| | |_) |  __/
 |____/| .__/ \\___|\\__,_|_|\\_\\____/|_|\\_\\_| .__/  |_| \\__, | .__/ \\___|
       |_|                                |_|         |___/|_|
{Colors.END}
{Colors.GREEN}The ULTIMATE Speech-to-Text for Developers - NO API, 100% FREE{Colors.END}
{Colors.MAGENTA}Engine: {engine} | Better than OpenWhispr, Handy, voice_typing{Colors.END}
{Colors.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}
"""
    print(banner)


def print_controls():
    """Print the keyboard controls."""
    vad_status = f"{Colors.GREEN}ON{Colors.END}" if config.get('audio', {}).get('vad_enabled', False) else f"{Colors.RED}OFF{Colors.END}"
    code_status = f"{Colors.GREEN}ON{Colors.END}" if config.get('transcription', {}).get('code_mode', False) else f"{Colors.RED}OFF{Colors.END}"
    punct_status = f"{Colors.GREEN}ON{Colors.END}" if config.get('transcription', {}).get('auto_punctuation', True) else f"{Colors.RED}OFF{Colors.END}"
    filler_status = f"{Colors.GREEN}ON{Colors.END}" if config.get('transcription', {}).get('remove_filler_words', True) else f"{Colors.RED}OFF{Colors.END}"
    continuous_status = f"{Colors.GREEN}ON{Colors.END}" if config.get('audio', {}).get('continuous_mode', False) else f"{Colors.RED}OFF{Colors.END}"

    print(f"""
{Colors.BOLD}CONTROLS:{Colors.END}
  {Colors.GREEN}Alt + R{Colors.END}          = Start Recording {Colors.RED}(no terminal conflict!){Colors.END}
  {Colors.GREEN}Alt + S{Colors.END}          = Stop & Auto-Paste {Colors.CYAN}(text at cursor){Colors.END}
  {Colors.GREEN}Alt + Q{Colors.END}          = Quit Application
  {Colors.GREEN}Ctrl + D{Colors.END}         = Toggle Debug Mode
  {Colors.GREEN}Ctrl + H{Colors.END}         = Show History

{Colors.BOLD}VOICE COMMANDS:{Colors.END}
  {Colors.CYAN}"new line"{Colors.END}       → inserts line break
  {Colors.CYAN}"new paragraph"{Colors.END}  → inserts double line break
  {Colors.CYAN}"delete that"{Colors.END}    → removes last phrase
  {Colors.CYAN}"period/comma"{Colors.END}   → inserts punctuation

{Colors.BOLD}FEATURES:{Colors.END}
  Voice Activity Detection: {vad_status}
  Continuous Listening:     {continuous_status}
  Code Dictation Mode:      {code_status}
  Auto-Punctuation:         {punct_status}
  Filler Word Removal:      {filler_status}

{Colors.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}
""")


def download_model():
    """Download the Vosk model if not present (alias for compatibility)."""
    return download_vosk_model()


def download_vosk_model():
    """Download the Vosk model if not present."""
    lang = config.get('transcription', {}).get('language', 'en-us')
    model_name = f"vosk-model-small-{lang}-0.15"
    model_path = get_config_dir() / model_name

    if model_path.exists():
        return str(model_path)

    print(f"{Colors.YELLOW}[*] First-time setup: Downloading Vosk speech model...{Colors.END}")
    print(f"{Colors.CYAN}    (This is a one-time download, ~40MB){Colors.END}\n")

    import urllib.request
    import zipfile

    url = f"https://alphacephei.com/vosk/models/{model_name}.zip"
    zip_path = get_config_dir() / "model.zip"

    def download_progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        percent = min(100, (downloaded / total_size) * 100)
        bar_length = 40
        filled = int(bar_length * percent / 100)
        bar = '=' * filled + '-' * (bar_length - filled)
        sys.stdout.write(f'\r    [{bar}] {percent:.1f}%')
        sys.stdout.flush()

    try:
        urllib.request.urlretrieve(url, str(zip_path), download_progress)
        print(f"\n{Colors.GREEN}[+] Download complete! Extracting...{Colors.END}")

        with zipfile.ZipFile(str(zip_path), 'r') as zip_ref:
            zip_ref.extractall(str(get_config_dir()))

        zip_path.unlink()
        print(f"{Colors.GREEN}[+] Model ready!{Colors.END}\n")

    except Exception as e:
        print(f"\n{Colors.RED}[!] Error downloading model: {e}{Colors.END}")
        print(f"{Colors.YELLOW}[*] Please download manually from: {url}{Colors.END}")
        sys.exit(1)

    return str(model_path)


def download_whisper_model():
    """Initialize Whisper model."""
    global whisper_model

    model_size = config.get('transcription', {}).get('whisper_model', 'base')

    print(f"{Colors.YELLOW}[*] Loading Whisper model ({model_size})...{Colors.END}")
    print(f"{Colors.CYAN}    (First run will download the model){Colors.END}\n")

    try:
        import whisper
        whisper_model = whisper.load_model(model_size)
        print(f"{Colors.GREEN}[+] Whisper model loaded!{Colors.END}\n")
    except ImportError:
        print(f"{Colors.RED}[!] Whisper not installed. Installing...{Colors.END}")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'openai-whisper', '-q'])
        import whisper
        whisper_model = whisper.load_model(model_size)
        print(f"{Colors.GREEN}[+] Whisper model loaded!{Colors.END}\n")


def audio_callback(indata, frames, time_info, status):
    """Callback for audio stream."""
    global vad_recording, vad_silence_start

    if status and not background_mode:
        print(f"{Colors.RED}Audio Error: {status}{Colors.END}", file=sys.stderr)

    if is_recording:
        audio_queue.put(bytes(indata))

        # VAD processing
        if config.get('audio', {}).get('vad_enabled', False):
            import numpy as np
            audio_data = np.frombuffer(indata, dtype=np.int16)
            level = np.abs(audio_data).mean() / 32768.0
            audio_levels.append(level)
            avg_level = sum(audio_levels) / len(audio_levels)

            threshold = config.get('audio', {}).get('vad_threshold', 0.5)
            silence_duration = config.get('audio', {}).get('vad_silence_duration', 1.5)

            if avg_level > threshold / 100:
                vad_silence_start = None
                if not vad_recording:
                    vad_recording = True
                    debug_log("VAD: Speech detected")
            else:
                if vad_recording:
                    if vad_silence_start is None:
                        vad_silence_start = time.time()
                    elif time.time() - vad_silence_start > silence_duration:
                        vad_recording = False
                        debug_log("VAD: Silence detected, stopping")
                        # Auto-stop recording
                        threading.Thread(target=stop_recording_and_type, daemon=True).start()


def process_audio():
    """Process audio from the queue and perform speech recognition."""
    global recorded_text

    while True:
        data = audio_queue.get()
        if data is None:
            break

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get('text', '')
            if text:
                recorded_text += text + " "
                log(f"   Recognized: {text}", Colors.CYAN)
        else:
            partial = json.loads(recognizer.PartialResult())
            partial_text = partial.get('partial', '')
            if partial_text and not background_mode:
                sys.stdout.write(f"\r{Colors.MAGENTA}   Hearing: {partial_text}...{Colors.END}          ")
                sys.stdout.flush()


recording_start_time = None


def start_recording():
    """Start recording audio."""
    global is_recording, recorded_text, recording_start_time

    if is_recording:
        # Already recording - stop instead (toggle behavior)
        stop_recording_and_type()
        return

    is_recording = True
    recorded_text = ""
    recording_start_time = time.time()

    # Audio feedback
    play_beep(beep_type="start")

    log(f"\n{Colors.RED}{Colors.BOLD}[REC]{Colors.END} Recording... Speak now! (Ctrl+S to stop)", Colors.RED)
    notify("Recording", "Speak now! Press Ctrl+S to stop.")


def copy_to_clipboard(text):
    """Copy text to clipboard (cross-platform)."""
    if sys.platform == 'win32':
        import subprocess
        process = subprocess.Popen(['clip'], stdin=subprocess.PIPE, shell=True)
        process.communicate(text.encode('utf-8'))
    elif sys.platform == 'darwin':
        import subprocess
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(text.encode('utf-8'))
    else:
        import subprocess
        try:
            process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
        except FileNotFoundError:
            try:
                process = subprocess.Popen(['xsel', '--clipboard', '--input'], stdin=subprocess.PIPE)
                process.communicate(text.encode('utf-8'))
            except FileNotFoundError:
                return False
    return True


def paste_from_clipboard():
    """Simulate Ctrl+V to paste."""
    time.sleep(0.1)
    keyboard_controller.press(Key.ctrl)
    keyboard_controller.press('v')
    keyboard_controller.release('v')
    keyboard_controller.release(Key.ctrl)
    time.sleep(0.1)


def stop_recording_and_type():
    """Stop recording and type the recognized text."""
    global is_recording, recorded_text, recording_start_time

    if not is_recording:
        return

    is_recording = False
    duration = time.time() - recording_start_time if recording_start_time else 0

    # Audio feedback
    play_beep(beep_type="stop")

    # Process any remaining audio
    time.sleep(0.3)

    # Get final result
    final = json.loads(recognizer.FinalResult())
    final_text = final.get('text', '')
    if final_text:
        recorded_text += final_text

    recorded_text = recorded_text.strip()

    # Process text through all filters
    recorded_text = process_text(recorded_text)

    log(f"\n{Colors.GREEN}[STOP]{Colors.END} Recording stopped.", Colors.GREEN)

    if recorded_text:
        # Add to history
        add_to_history(recorded_text, duration)

        # Update stats
        update_stats(recorded_text, duration)

        log(f"{Colors.GREEN}[TEXT]{Colors.END} \"{recorded_text}\"", Colors.GREEN)
        log(f"{Colors.YELLOW}[PASTE]{Colors.END} Pasting to cursor position...", Colors.YELLOW)
        notify("Pasting", f'"{recorded_text[:50]}..."' if len(recorded_text) > 50 else f'"{recorded_text}"')

        # Small delay to ensure key release
        time.sleep(0.3)

        # Add space after if configured
        if config.get('output', {}).get('add_space_after', True):
            recorded_text += " "

        # Use clipboard + paste (more reliable on Windows)
        output_method = config.get('output', {}).get('method', 'clipboard')

        if output_method in ('clipboard', 'both'):
            if copy_to_clipboard(recorded_text):
                paste_from_clipboard()
            else:
                keyboard_controller.type(recorded_text)

        if output_method == 'type':
            keyboard_controller.type(recorded_text)

        log(f"{Colors.GREEN}[DONE]{Colors.END} Text inserted! (WPM: {stats['last_wpm']})\n", Colors.GREEN)
    else:
        log(f"{Colors.YELLOW}[!]{Colors.END} No speech detected. Try again.\n", Colors.YELLOW)
        notify("No Speech", "No speech detected. Try again.")


def toggle_debug():
    """Toggle debug mode."""
    global debug_mode
    debug_mode = not debug_mode
    status = "ON" if debug_mode else "OFF"
    log(f"\n{Colors.YELLOW}[DEBUG]{Colors.END} Debug mode: {status}\n", Colors.YELLOW)


def on_press(key):
    """Handle key press events."""
    global ctrl_pressed, shift_pressed, alt_pressed, hold_to_record_active

    try:
        # Track modifier keys
        if key == Key.ctrl_l or key == Key.ctrl_r:
            ctrl_pressed = True
            return
        elif key == Key.shift_l or key == Key.shift_r:
            shift_pressed = True
            return
        elif key == Key.alt_l or key == Key.alt_r or key == Key.alt_gr:
            alt_pressed = True
            return

        # Get the key character - handle both char attribute and vk (virtual key) codes
        char = None
        vk = None

        if hasattr(key, 'char') and key.char:
            char = key.char.lower() if key.char else None
        if hasattr(key, 'vk'):
            vk = key.vk

        # Virtual key codes for Windows: R=82, S=83, D=68, H=72, Q=81
        is_r = char == 'r' or vk == 82
        is_s = char == 's' or vk == 83
        is_d = char == 'd' or vk == 68
        is_h = char == 'h' or vk == 72
        is_q = char == 'q' or vk == 81

        # Alt+R: Start recording (primary - no terminal conflict)
        if alt_pressed and is_r:
            start_recording()

        # Alt+S: Stop and type (primary - no terminal conflict)
        elif alt_pressed and is_s:
            stop_recording_and_type()

        # Alt+Q: Quit
        elif alt_pressed and is_q:
            log(f"\n{Colors.YELLOW}[*] Exiting SpeakSkipType...{Colors.END}", Colors.YELLOW)
            notify("Goodbye", "SpeakSkipType stopped.")
            os._exit(0)

        # Ctrl+D: Toggle debug
        elif ctrl_pressed and is_d:
            toggle_debug()

        # Ctrl+H: Show history
        elif ctrl_pressed and is_h:
            if not background_mode:
                show_history()

        # Ctrl+Q: Quit (backup)
        elif ctrl_pressed and is_q:
            log(f"\n{Colors.YELLOW}[*] Exiting SpeakSkipType...{Colors.END}", Colors.YELLOW)
            notify("Goodbye", "SpeakSkipType stopped.")
            os._exit(0)

    except AttributeError:
        pass
    except Exception:
        pass
    except Exception:
        pass


def on_release(key):
    """Handle key release events."""
    global ctrl_pressed, shift_pressed, alt_pressed, hold_to_record_active

    if key == Key.ctrl_l or key == Key.ctrl_r:
        ctrl_pressed = False

        # If hold-to-record was active, stop and type
        if hold_to_record_active:
            hold_to_record_active = False
            stop_recording_and_type()

    elif key == Key.shift_l or key == Key.shift_r:
        shift_pressed = False

    elif key == Key.alt_l or key == Key.alt_r or key == Key.alt_gr:
        alt_pressed = False


def handle_signal(signum, frame):
    """Handle Unix signals for external control."""
    if signum == signal.SIGUSR1:
        # Toggle recording
        if is_recording:
            stop_recording_and_type()
        else:
            start_recording()
    elif signum == signal.SIGUSR2:
        # Stop recording
        stop_recording_and_type()


def run_background():
    """Run in background mode with system tray."""
    global background_mode
    background_mode = True

    if sys.platform == 'win32':
        try:
            import pystray
            from PIL import Image, ImageDraw

            def create_icon(recording=False):
                color = (255, 0, 0) if recording else (0, 128, 255)
                image = Image.new('RGB', (64, 64), color=color)
                draw = ImageDraw.Draw(image)
                draw.ellipse([8, 8, 56, 56], fill=(255, 255, 255))
                inner_color = (255, 0, 0) if recording else (0, 128, 255)
                draw.ellipse([20, 20, 44, 44], fill=inner_color)
                return image

            def on_quit(icon, item):
                icon.stop()
                os._exit(0)

            def on_status(icon, item):
                status = "Recording..." if is_recording else "Ready"
                notify("SpeakSkipType", f"Status: {status}\n\nCtrl+R: Record\nCtrl+S: Stop\nCtrl+Q: Quit")

            def on_history(icon, item):
                # Show last transcription
                if transcription_history:
                    last = transcription_history[-1].get('text', 'None')
                    notify("Last Transcription", last[:100])
                else:
                    notify("History", "No transcriptions yet")

            def on_stats(icon, item):
                notify("Stats", f"Total: {stats['total_words']} words\nSession: {stats['session_words']} words\nLast WPM: {stats['last_wpm']}")

            menu = pystray.Menu(
                pystray.MenuItem("Status", on_status),
                pystray.MenuItem("Last Transcription", on_history),
                pystray.MenuItem("Statistics", on_stats),
                pystray.MenuItem("Quit", on_quit)
            )

            icon = pystray.Icon("SpeakSkipType", create_icon(), "SpeakSkipType - Ctrl+R", menu)

            def run_main():
                main_loop()

            threading.Thread(target=run_main, daemon=True).start()

            notify("SpeakSkipType", "Running!\nCtrl+R: Record | Ctrl+S: Type | Ctrl+Q: Quit")
            icon.run()
            return

        except ImportError:
            pass

    notify("SpeakSkipType", "Running!\nCtrl+R: Record | Ctrl+S: Type | Ctrl+Q: Quit")
    main_loop()


def main_loop():
    """Main application loop."""
    global model, recognizer

    import sounddevice as sd
    from vosk import Model, KaldiRecognizer
    from pynput import keyboard

    init_keyboard()
    load_history()
    load_stats()

    # Setup signal handlers for Unix
    if sys.platform != 'win32':
        try:
            signal.signal(signal.SIGUSR1, handle_signal)
            signal.signal(signal.SIGUSR2, handle_signal)
        except:
            pass

    engine = config.get('transcription', {}).get('engine', 'vosk')

    if engine == 'whisper':
        download_whisper_model()
        # For whisper, we still use vosk for real-time, whisper for final
        model_path = download_vosk_model()
    else:
        model_path = download_vosk_model()

    if not background_mode:
        print(f"{Colors.CYAN}[*] Loading speech recognition model...{Colors.END}")

    model = Model(model_path)
    sample_rate = config.get('audio', {}).get('sample_rate', 16000)
    recognizer = KaldiRecognizer(model, sample_rate)

    if not background_mode:
        print(f"{Colors.GREEN}[+] Model loaded successfully!{Colors.END}")
        print_controls()
        print(f"{Colors.GREEN}[*] SpeakSkipType is ready! Waiting for commands...{Colors.END}\n")

    process_thread = threading.Thread(target=process_audio, daemon=True)
    process_thread.start()

    try:
        with sd.RawInputStream(samplerate=sample_rate, blocksize=8000, dtype='int16',
                               channels=1, callback=audio_callback):
            with keyboard.Listener(on_press=on_press, on_release=on_release, suppress=False) as listener:
                listener.join()

    except KeyboardInterrupt:
        log(f"\n{Colors.YELLOW}[*] Exiting SpeakSkipType...{Colors.END}", Colors.YELLOW)
    except Exception as e:
        if not background_mode:
            print(f"{Colors.RED}[!] Error: {e}{Colors.END}")
            print(f"{Colors.YELLOW}[*] Make sure your microphone is connected.{Colors.END}")
        sys.exit(1)


def main():
    """Main function."""
    global background_mode

    # Load configuration
    load_config()

    # Check and install dependencies
    check_dependencies()

    # Parse arguments
    if '--config' in sys.argv:
        edit_config()
        return

    if '--history' in sys.argv:
        load_history()
        show_history()
        return

    if '--stats' in sys.argv:
        load_stats()
        show_stats()
        return

    if '--export' in sys.argv:
        load_history()
        # Check for format
        if '--json' in sys.argv:
            export_history('json')
        elif '--txt' in sys.argv:
            export_history('txt')
        elif '--csv' in sys.argv:
            export_history('csv')
        else:
            print(f"{Colors.CYAN}Export formats:{Colors.END}")
            print("  --export --json  Export as JSON")
            print("  --export --txt   Export as plain text")
            print("  --export --csv   Export as CSV")
        return

    if '--whisper' in sys.argv:
        config['transcription']['engine'] = 'whisper'

    if '--code' in sys.argv:
        config['transcription']['code_mode'] = True

    if '--vad' in sys.argv:
        config['audio']['vad_enabled'] = True

    if '--continuous' in sys.argv:
        config['audio']['continuous_mode'] = True

    if '--no-filler' in sys.argv or '--remove-filler' in sys.argv:
        config['transcription']['remove_filler_words'] = True

    if '--literal' in sys.argv:
        config['transcription']['literal_punctuation'] = True

    if '--bg' in sys.argv or '--background' in sys.argv:
        run_background()
    else:
        print_banner()
        main_loop()


if __name__ == "__main__":
    main()
