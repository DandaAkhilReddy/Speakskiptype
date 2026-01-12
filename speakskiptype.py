#!/usr/bin/env python3
"""
SpeakSkipType - Speech-to-Text directly in your terminal
No API. No cloud. 100% FREE. Works locally on any laptop.

Ctrl+R = Start Recording
Ctrl+S = Stop & Auto-Type
Ctrl+Q = Quit

Usage:
  python speakskiptype.py           # Run in terminal
  python speakskiptype.py --bg      # Run in background (global hotkeys work everywhere)
  pythonw speakskiptype.py --bg     # Run hidden in background (Windows)

Author: Your Name
License: MIT
"""

import os
import sys
import queue
import json
import threading
import time

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


# Global variables
audio_queue = queue.Queue()
is_recording = False
recorded_text = ""
ctrl_pressed = False
background_mode = False

# These will be initialized when running (not importing)
model = None
recognizer = None
keyboard_controller = None
Key = None


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
{Colors.GREEN}Speech-to-Text directly in your terminal - NO API, 100% FREE, Works Locally{Colors.END}
{Colors.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}
"""
    print(banner)


def print_controls():
    """Print the keyboard controls."""
    print(f"""
{Colors.BOLD}CONTROLS:{Colors.END}
  {Colors.GREEN}Ctrl + R{Colors.END}  =  Start Recording  {Colors.RED}(microphone ON){Colors.END}
  {Colors.GREEN}Ctrl + S{Colors.END}  =  Stop & Auto-Type {Colors.CYAN}(text appears at cursor){Colors.END}
  {Colors.GREEN}Ctrl + Q{Colors.END}  =  Quit Application

{Colors.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}
""")


def notify(title, message):
    """Show a notification (works on Windows, macOS, Linux)."""
    if not background_mode:
        return

    try:
        if sys.platform == 'win32':
            # Windows toast notification
            try:
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast(title, message, duration=2, threaded=True)
            except ImportError:
                # Fallback: use PowerShell
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
            # macOS
            os.system(f'osascript -e \'display notification "{message}" with title "{title}"\'')
        else:
            # Linux
            os.system(f'notify-send "{title}" "{message}" 2>/dev/null')
    except:
        pass  # Silently fail if notifications don't work


def log(message, color=Colors.WHITE):
    """Print message if not in background mode."""
    if not background_mode:
        print(f"{color}{message}{Colors.END}")


def download_model():
    """Download the Vosk model if not present."""
    model_path = os.path.expanduser("~/.speakskiptype/vosk-model-small-en-us-0.15")
    model_dir = os.path.dirname(model_path)

    if os.path.exists(model_path):
        return model_path

    print(f"{Colors.YELLOW}[*] First-time setup: Downloading speech recognition model...{Colors.END}")
    print(f"{Colors.CYAN}    (This is a one-time download, ~40MB){Colors.END}\n")

    os.makedirs(model_dir, exist_ok=True)

    import urllib.request
    import zipfile

    url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
    zip_path = os.path.join(model_dir, "model.zip")

    # Download with progress
    def download_progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        percent = min(100, (downloaded / total_size) * 100)
        bar_length = 40
        filled = int(bar_length * percent / 100)
        bar = '=' * filled + '-' * (bar_length - filled)
        sys.stdout.write(f'\r    [{bar}] {percent:.1f}%')
        sys.stdout.flush()

    try:
        urllib.request.urlretrieve(url, zip_path, download_progress)
        print(f"\n{Colors.GREEN}[+] Download complete! Extracting...{Colors.END}")

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(model_dir)

        os.remove(zip_path)
        print(f"{Colors.GREEN}[+] Model ready!{Colors.END}\n")

    except Exception as e:
        print(f"\n{Colors.RED}[!] Error downloading model: {e}{Colors.END}")
        print(f"{Colors.YELLOW}[*] Please download manually from: {url}{Colors.END}")
        print(f"{Colors.YELLOW}    Extract to: {model_dir}{Colors.END}")
        sys.exit(1)

    return model_path


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
        return

    is_recording = True
    recorded_text = ""

    log(f"\n[REC] Recording... Speak now! (Ctrl+S to stop)", Colors.RED + Colors.BOLD)
    notify("🎤 Recording", "Speak now! Press Ctrl+S to stop.")


def stop_recording_and_type():
    """Stop recording and type the recognized text."""
    global is_recording, recorded_text

    if not is_recording:
        return

    is_recording = False

    # Process any remaining audio
    time.sleep(0.3)

    # Get final result
    final = json.loads(recognizer.FinalResult())
    final_text = final.get('text', '')
    if final_text:
        recorded_text += final_text

    recorded_text = recorded_text.strip()

    log(f"\n[STOP] Recording stopped.", Colors.GREEN)

    if recorded_text:
        log(f"[TEXT] \"{recorded_text}\"", Colors.GREEN)
        log(f"[TYPE] Auto-typing to cursor position...", Colors.YELLOW)
        notify("✅ Typing", f'"{recorded_text}"')

        # Small delay to ensure key release
        time.sleep(0.2)

        # Type the text at cursor position
        keyboard_controller.type(recorded_text)

        log(f"[DONE] Text inserted!\n", Colors.GREEN)
    else:
        log(f"[!] No speech detected. Try again.\n", Colors.YELLOW)
        notify("⚠️ No Speech", "No speech detected. Try again.")


def on_hotkey(key_combination):
    """Handle hotkey press."""
    try:
        if hasattr(key_combination, 'char'):
            return
    except:
        pass


def on_press(key):
    """Handle key press events."""
    global ctrl_pressed

    try:
        if key == Key.ctrl_l or key == Key.ctrl_r:
            ctrl_pressed = True
        elif ctrl_pressed:
            if hasattr(key, 'char'):
                if key.char == 'r' or key.char == '\x12':  # Ctrl+R
                    start_recording()
                elif key.char == 's' or key.char == '\x13':  # Ctrl+S
                    stop_recording_and_type()
                elif key.char == 'q' or key.char == '\x11':  # Ctrl+Q
                    log(f"\n[*] Exiting SpeakSkipType...", Colors.YELLOW)
                    notify("👋 Goodbye", "SpeakSkipType stopped.")
                    os._exit(0)
    except AttributeError:
        pass


def on_release(key):
    """Handle key release events."""
    global ctrl_pressed

    if key == Key.ctrl_l or key == Key.ctrl_r:
        ctrl_pressed = False


def run_background():
    """Run in background mode with system tray (Windows) or daemon (Unix)."""
    global background_mode
    background_mode = True

    # On Windows, try to create a system tray icon
    if sys.platform == 'win32':
        try:
            import pystray
            from PIL import Image, ImageDraw

            # Create a simple icon
            def create_icon():
                image = Image.new('RGB', (64, 64), color=(0, 128, 255))
                draw = ImageDraw.Draw(image)
                draw.ellipse([8, 8, 56, 56], fill=(255, 255, 255))
                draw.ellipse([20, 20, 44, 44], fill=(0, 128, 255))
                return image

            def on_quit(icon, item):
                icon.stop()
                os._exit(0)

            def on_status(icon, item):
                status = "Recording..." if is_recording else "Ready"
                notify("SpeakSkipType Status", f"Status: {status}\n\nCtrl+R: Record\nCtrl+S: Stop & Type\nCtrl+Q: Quit")

            menu = pystray.Menu(
                pystray.MenuItem("Status", on_status),
                pystray.MenuItem("Quit", on_quit)
            )

            icon = pystray.Icon("SpeakSkipType", create_icon(), "SpeakSkipType - Ctrl+R to record", menu)

            # Run main loop in background
            def run_main():
                main_loop()

            threading.Thread(target=run_main, daemon=True).start()

            notify("🎤 SpeakSkipType", "Running in background!\nCtrl+R: Record | Ctrl+S: Type | Ctrl+Q: Quit")
            icon.run()
            return

        except ImportError:
            # pystray not installed, run without system tray
            pass

    # Fallback: run without system tray
    notify("🎤 SpeakSkipType", "Running in background!\nCtrl+R: Record | Ctrl+S: Type | Ctrl+Q: Quit")
    main_loop()


def main_loop():
    """Main application loop."""
    global model, recognizer

    # Import after dependency check
    import sounddevice as sd
    from vosk import Model, KaldiRecognizer
    from pynput import keyboard

    # Initialize keyboard
    init_keyboard()

    # Download model if needed
    model_path = download_model()

    if not background_mode:
        print(f"{Colors.CYAN}[*] Loading speech recognition model...{Colors.END}")

    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)

    if not background_mode:
        print(f"{Colors.GREEN}[+] Model loaded successfully!{Colors.END}")
        print_controls()
        print(f"{Colors.GREEN}[*] SpeakSkipType is ready! Waiting for commands...{Colors.END}\n")

    # Start audio processing thread
    process_thread = threading.Thread(target=process_audio, daemon=True)
    process_thread.start()

    # Start audio stream
    try:
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=audio_callback):

            # Start keyboard listener (suppress=False to not block other apps)
            with keyboard.Listener(on_press=on_press, on_release=on_release, suppress=False) as listener:
                listener.join()

    except KeyboardInterrupt:
        log(f"\n[*] Exiting SpeakSkipType...", Colors.YELLOW)
    except Exception as e:
        if not background_mode:
            print(f"{Colors.RED}[!] Error: {e}{Colors.END}")
            print(f"{Colors.YELLOW}[*] Make sure your microphone is connected and accessible.{Colors.END}")
        sys.exit(1)


def main():
    """Main function."""
    global background_mode

    # Check and install dependencies
    check_dependencies()

    # Check for background mode
    if '--bg' in sys.argv or '--background' in sys.argv:
        run_background()
    else:
        print_banner()
        main_loop()


if __name__ == "__main__":
    main()
