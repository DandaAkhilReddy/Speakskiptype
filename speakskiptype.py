#!/usr/bin/env python3
"""
SpeakSkipType - The BEST Speech-to-Text Tool for Developers
No API. No cloud. 100% FREE. Works locally on any laptop.

UNIQUE FEATURES (that competitors don't have):
- Hold-to-record mode (hold key, release to auto-type)
- Audio feedback (beep sounds)
- Transcription history with timestamps
- Voice commands (delete that, new line, undo)
- Custom hotkey configuration
- Multi-language support
- Works GLOBALLY in any application

CONTROLS:
  Ctrl+R      = Start Recording (press again or Ctrl+S to stop)
  Ctrl+S      = Stop & Auto-Type
  Ctrl+Shift+R = Hold-to-Record (release to auto-type)
  Ctrl+Q      = Quit Application
  Ctrl+H      = Show History

Usage:
  python speakskiptype.py              # Run in terminal
  python speakskiptype.py --bg         # Run in background
  python speakskiptype.py --config     # Edit configuration
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
from datetime import datetime
from pathlib import Path

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
        "show_history": "ctrl+h"
    },
    "audio": {
        "sample_rate": 16000,
        "beep_on_start": True,
        "beep_on_stop": True
    },
    "transcription": {
        "language": "en-us",
        "save_history": True,
        "max_history": 100
    },
    "voice_commands": {
        "enabled": True,
        "commands": {
            "delete that": "__DELETE_LAST__",
            "new line": "\n",
            "new paragraph": "\n\n",
            "tab": "\t",
            "period": ".",
            "comma": ",",
            "question mark": "?",
            "exclamation mark": "!"
        }
    },
    "output": {
        "method": "clipboard",  # clipboard, type, or both
        "add_space_after": True
    }
}


# Global variables
audio_queue = queue.Queue()
is_recording = False
recorded_text = ""
ctrl_pressed = False
shift_pressed = False
hold_to_record_active = False
background_mode = False
config = DEFAULT_CONFIG.copy()
transcription_history = []

# These will be initialized when running
model = None
recognizer = None
keyboard_controller = None
Key = None
config_path = None


# ============================================================================
# CONFIGURATION MANAGEMENT
# ============================================================================

def get_config_path():
    """Get the configuration file path."""
    config_dir = Path.home() / ".speakskiptype"
    config_dir.mkdir(exist_ok=True)
    return config_dir / "config.json"


def load_config():
    """Load configuration from file."""
    global config
    config_file = get_config_path()

    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                # Merge with defaults
                for key in DEFAULT_CONFIG:
                    if key in user_config:
                        if isinstance(DEFAULT_CONFIG[key], dict):
                            config[key] = {**DEFAULT_CONFIG[key], **user_config[key]}
                        else:
                            config[key] = user_config[key]
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
# TRANSCRIPTION HISTORY
# ============================================================================

def get_history_path():
    """Get the history file path."""
    config_dir = Path.home() / ".speakskiptype"
    config_dir.mkdir(exist_ok=True)
    return config_dir / "history.json"


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


def add_to_history(text):
    """Add a transcription to history."""
    if not text:
        return

    entry = {
        "timestamp": datetime.now().isoformat(),
        "text": text
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
    for entry in transcription_history[-10:]:
        ts = entry.get('timestamp', 'Unknown')
        text = entry.get('text', '')
        # Parse timestamp
        try:
            dt = datetime.fromisoformat(ts)
            ts_formatted = dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            ts_formatted = ts

        print(f"{Colors.BLUE}[{ts_formatted}]{Colors.END}")
        print(f"  {text}\n")


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
# VOICE COMMANDS
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
                import re
                result = re.sub(re.escape(trigger), action, result, flags=re.IGNORECASE)

    return result.strip()


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
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
  ____                   _    ____  _    _       _____
 / ___| _ __   ___  __ _| | _/ ___|| | _(_)_ __ |_   _|   _ _ __   ___
 \\___ \\| '_ \\ / _ \\/ _` | |/ \\___ \\| |/ / | '_ \\  | || | | | '_ \\ / _ \\
  ___) | |_) |  __/ (_| |   < ___) |   <| | |_) | | || |_| | |_) |  __/
 |____/| .__/ \\___|\\__,_|_|\\_\\____/|_|\\_\\_| .__/  |_| \\__, | .__/ \\___|
       |_|                                |_|         |___/|_|
{Colors.END}
{Colors.GREEN}The BEST Speech-to-Text for Developers - NO API, 100% FREE, Works Locally{Colors.END}
{Colors.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}
"""
    print(banner)


def print_controls():
    """Print the keyboard controls."""
    print(f"""
{Colors.BOLD}CONTROLS:{Colors.END}
  {Colors.GREEN}Ctrl + R{Colors.END}        = Start Recording {Colors.RED}(press again to stop){Colors.END}
  {Colors.GREEN}Ctrl + S{Colors.END}        = Stop & Auto-Paste {Colors.CYAN}(text at cursor){Colors.END}
  {Colors.GREEN}Ctrl + Shift + R{Colors.END} = Hold-to-Record {Colors.MAGENTA}(release to paste){Colors.END}
  {Colors.GREEN}Ctrl + H{Colors.END}        = Show History
  {Colors.GREEN}Ctrl + Q{Colors.END}        = Quit Application

{Colors.BOLD}VOICE COMMANDS:{Colors.END}
  {Colors.CYAN}"new line"{Colors.END}      → inserts line break
  {Colors.CYAN}"new paragraph"{Colors.END} → inserts double line break
  {Colors.CYAN}"delete that"{Colors.END}   → removes last phrase
  {Colors.CYAN}"period/comma"{Colors.END}  → inserts punctuation

{Colors.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}
""")


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


def log(message, color=Colors.WHITE):
    """Print message if not in background mode."""
    if not background_mode:
        print(f"{color}{message}{Colors.END}")


def download_model():
    """Download the Vosk model if not present."""
    lang = config.get('transcription', {}).get('language', 'en-us')
    model_name = f"vosk-model-small-{lang}-0.15"
    model_path = Path.home() / ".speakskiptype" / model_name
    model_dir = model_path.parent

    if model_path.exists():
        return str(model_path)

    print(f"{Colors.YELLOW}[*] First-time setup: Downloading speech recognition model...{Colors.END}")
    print(f"{Colors.CYAN}    (This is a one-time download, ~40MB){Colors.END}\n")

    model_dir.mkdir(parents=True, exist_ok=True)

    import urllib.request
    import zipfile

    url = f"https://alphacephei.com/vosk/models/{model_name}.zip"
    zip_path = model_dir / "model.zip"

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
            zip_ref.extractall(str(model_dir))

        zip_path.unlink()
        print(f"{Colors.GREEN}[+] Model ready!{Colors.END}\n")

    except Exception as e:
        print(f"\n{Colors.RED}[!] Error downloading model: {e}{Colors.END}")
        print(f"{Colors.YELLOW}[*] Please download manually from: {url}{Colors.END}")
        sys.exit(1)

    return str(model_path)


def audio_callback(indata, frames, time_info, status):
    """Callback for audio stream."""
    if status and not background_mode:
        print(f"{Colors.RED}Audio Error: {status}{Colors.END}", file=sys.stderr)
    if is_recording:
        audio_queue.put(bytes(indata))


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


def start_recording():
    """Start recording audio."""
    global is_recording, recorded_text

    if is_recording:
        # Already recording - stop instead (toggle behavior)
        stop_recording_and_type()
        return

    is_recording = True
    recorded_text = ""

    # Audio feedback
    play_beep(beep_type="start")

    log(f"\n{Colors.RED}{Colors.BOLD}[REC]{Colors.END} Recording... Speak now! (Ctrl+S to stop)", Colors.RED)
    notify("🎤 Recording", "Speak now! Press Ctrl+S to stop.")


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
    global is_recording, recorded_text

    if not is_recording:
        return

    is_recording = False

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

    # Process voice commands
    recorded_text = process_voice_commands(recorded_text)

    log(f"\n{Colors.GREEN}[STOP]{Colors.END} Recording stopped.", Colors.GREEN)

    if recorded_text:
        # Add to history
        add_to_history(recorded_text)

        log(f"{Colors.GREEN}[TEXT]{Colors.END} \"{recorded_text}\"", Colors.GREEN)
        log(f"{Colors.YELLOW}[PASTE]{Colors.END} Pasting to cursor position...", Colors.YELLOW)
        notify("✅ Pasting", f'"{recorded_text[:50]}..."' if len(recorded_text) > 50 else f'"{recorded_text}"')

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

        log(f"{Colors.GREEN}[DONE]{Colors.END} Text inserted!\n", Colors.GREEN)
    else:
        log(f"{Colors.YELLOW}[!]{Colors.END} No speech detected. Try again.\n", Colors.YELLOW)
        notify("⚠️ No Speech", "No speech detected. Try again.")


def on_press(key):
    """Handle key press events."""
    global ctrl_pressed, shift_pressed, hold_to_record_active

    try:
        # Track modifier keys
        if key == Key.ctrl_l or key == Key.ctrl_r:
            ctrl_pressed = True
        elif key == Key.shift_l or key == Key.shift_r:
            shift_pressed = True
        elif ctrl_pressed:
            if hasattr(key, 'char'):
                char = key.char

                # Ctrl+Shift+R: Hold-to-record
                if shift_pressed and (char == 'r' or char == '\x12' or char == 'R'):
                    if not hold_to_record_active:
                        hold_to_record_active = True
                        start_recording()

                # Ctrl+R: Toggle recording
                elif char == 'r' or char == '\x12':
                    start_recording()

                # Ctrl+S: Stop and type
                elif char == 's' or char == '\x13':
                    stop_recording_and_type()

                # Ctrl+H: Show history
                elif char == 'h' or char == '\x08':
                    if not background_mode:
                        show_history()

                # Ctrl+Q: Quit
                elif char == 'q' or char == '\x11':
                    log(f"\n{Colors.YELLOW}[*] Exiting SpeakSkipType...{Colors.END}", Colors.YELLOW)
                    notify("👋 Goodbye", "SpeakSkipType stopped.")
                    os._exit(0)
    except AttributeError:
        pass


def on_release(key):
    """Handle key release events."""
    global ctrl_pressed, shift_pressed, hold_to_record_active

    if key == Key.ctrl_l or key == Key.ctrl_r:
        ctrl_pressed = False

        # If hold-to-record was active, stop and type
        if hold_to_record_active:
            hold_to_record_active = False
            stop_recording_and_type()

    elif key == Key.shift_l or key == Key.shift_r:
        shift_pressed = False


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
                status = "🔴 Recording..." if is_recording else "✅ Ready"
                notify("SpeakSkipType", f"Status: {status}\n\nCtrl+R: Record\nCtrl+S: Stop\nCtrl+Q: Quit")

            def on_history(icon, item):
                # Show last transcription
                if transcription_history:
                    last = transcription_history[-1].get('text', 'None')
                    notify("Last Transcription", last[:100])
                else:
                    notify("History", "No transcriptions yet")

            menu = pystray.Menu(
                pystray.MenuItem("Status", on_status),
                pystray.MenuItem("Last Transcription", on_history),
                pystray.MenuItem("Quit", on_quit)
            )

            icon = pystray.Icon("SpeakSkipType", create_icon(), "SpeakSkipType - Ctrl+R", menu)

            def run_main():
                main_loop()

            threading.Thread(target=run_main, daemon=True).start()

            notify("🎤 SpeakSkipType", "Running!\nCtrl+R: Record | Ctrl+S: Type | Ctrl+Q: Quit")
            icon.run()
            return

        except ImportError:
            pass

    notify("🎤 SpeakSkipType", "Running!\nCtrl+R: Record | Ctrl+S: Type | Ctrl+Q: Quit")
    main_loop()


def main_loop():
    """Main application loop."""
    global model, recognizer

    import sounddevice as sd
    from vosk import Model, KaldiRecognizer
    from pynput import keyboard

    init_keyboard()
    load_history()

    model_path = download_model()

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

    if '--bg' in sys.argv or '--background' in sys.argv:
        run_background()
    else:
        print_banner()
        main_loop()


if __name__ == "__main__":
    main()
