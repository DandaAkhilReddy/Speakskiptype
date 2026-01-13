#!/usr/bin/env python3
"""
Claude Code Voice Input - Speak to Claude Code!
Press F8 to start recording, F8 again to stop and paste.

Usage:
  1. Run this in the background: python claude_voice.py
  2. Open Claude Code in another terminal
  3. Press F8 to start speaking
  4. Press F8 again to stop - your speech becomes Claude input!

Author: Akhil Reddy
"""

import os
import sys
import queue
import json
import threading
import time
from pathlib import Path

# ANSI Colors
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Global state
is_recording = False
recorded_text = ""
audio_queue = queue.Queue()
recognizer = None
model = None

# Filler words to remove
FILLER_WORDS = [
    "um", "uh", "er", "ah", "like", "you know", "i mean",
    "sort of", "kind of", "basically", "actually", "literally",
    "so yeah", "right", "okay so", "well"
]


def get_model_path():
    """Get path to Vosk model."""
    config_dir = Path.home() / ".speakskiptype"
    config_dir.mkdir(exist_ok=True)
    model_name = "vosk-model-small-en-us-0.15"
    return config_dir / model_name


def download_model():
    """Download Vosk model if not present."""
    import urllib.request
    import zipfile

    model_path = get_model_path()
    if model_path.exists():
        return str(model_path)

    print(f"{Colors.YELLOW}[*] Downloading speech model (first time only)...{Colors.END}")
    url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
    zip_path = model_path.parent / "model.zip"

    urllib.request.urlretrieve(url, zip_path)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(model_path.parent)

    zip_path.unlink()
    print(f"{Colors.GREEN}[+] Model downloaded!{Colors.END}")
    return str(model_path)


def init_recognizer():
    """Initialize Vosk recognizer."""
    global recognizer, model
    from vosk import Model, KaldiRecognizer

    model_path = download_model()
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)
    recognizer.SetWords(True)


def remove_filler_words(text):
    """Remove filler words like um, uh, like, you know."""
    import re
    result = text

    # Sort by length (longest first) for multi-word phrases
    sorted_fillers = sorted(FILLER_WORDS, key=len, reverse=True)

    for filler in sorted_fillers:
        if ' ' in filler:
            filler_pattern = r'\b' + r'\s+'.join(re.escape(word) for word in filler.split()) + r'\b'
        else:
            filler_pattern = r'\b' + re.escape(filler) + r'\b'
        pattern = filler_pattern + r'[,]?\s*'
        result = re.sub(pattern, ' ', result, flags=re.IGNORECASE)

    result = re.sub(r'\s+', ' ', result)
    return result.strip()


def audio_callback(indata, frames, time_info, status):
    """Callback for audio stream."""
    if is_recording:
        audio_queue.put(bytes(indata))


def process_audio():
    """Process audio from queue and transcribe."""
    global recorded_text

    while is_recording:
        try:
            data = audio_queue.get(timeout=0.1)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get('text', '')
                if text:
                    recorded_text += text + " "
                    # Show real-time transcription
                    print(f"\r{Colors.CYAN}[HEARING]{Colors.END} {recorded_text.strip()[:60]}...", end="", flush=True)
            else:
                partial = json.loads(recognizer.PartialResult())
                partial_text = partial.get('partial', '')
                if partial_text:
                    print(f"\r{Colors.CYAN}[...]{Colors.END} {partial_text[:60]}...", end="", flush=True)
        except queue.Empty:
            continue
        except Exception:
            continue


def start_recording():
    """Start recording audio."""
    global is_recording, recorded_text

    if is_recording:
        return

    is_recording = True
    recorded_text = ""

    # Clear audio queue
    while not audio_queue.empty():
        try:
            audio_queue.get_nowait()
        except queue.Empty:
            break

    print(f"\n{Colors.GREEN}[REC]{Colors.END} 🎤 Recording... Speak now! (Press F8 to stop)")

    # Start processing thread
    threading.Thread(target=process_audio, daemon=True).start()


def stop_recording():
    """Stop recording and return transcribed text."""
    global is_recording, recorded_text

    if not is_recording:
        return ""

    is_recording = False
    time.sleep(0.3)

    # Get final result
    final = json.loads(recognizer.FinalResult())
    final_text = final.get('text', '')
    if final_text:
        recorded_text += final_text

    recorded_text = recorded_text.strip()

    # Remove filler words
    recorded_text = remove_filler_words(recorded_text)

    print(f"\n{Colors.GREEN}[STOP]{Colors.END} Recording stopped.")

    return recorded_text


def copy_and_paste(text):
    """Copy text to clipboard and paste it."""
    try:
        import pyperclip
        pyperclip.copy(text)
    except ImportError:
        # Fallback for systems without pyperclip
        if sys.platform == 'win32':
            import subprocess
            subprocess.run(['clip'], input=text.encode('utf-8'), check=True)
        elif sys.platform == 'darwin':
            import subprocess
            subprocess.run(['pbcopy'], input=text.encode('utf-8'), check=True)
        else:
            import subprocess
            try:
                subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode('utf-8'), check=True)
            except FileNotFoundError:
                subprocess.run(['xsel', '--clipboard', '--input'], input=text.encode('utf-8'), check=True)

    # Simulate Ctrl+V to paste
    from pynput.keyboard import Controller, Key
    keyboard = Controller()
    time.sleep(0.1)

    if sys.platform == 'darwin':
        keyboard.press(Key.cmd)
        keyboard.press('v')
        keyboard.release('v')
        keyboard.release(Key.cmd)
    else:
        keyboard.press(Key.ctrl)
        keyboard.press('v')
        keyboard.release('v')
        keyboard.release(Key.ctrl)


def toggle_recording():
    """Toggle recording on/off."""
    global is_recording

    if is_recording:
        text = stop_recording()
        if text:
            print(f"{Colors.GREEN}[TEXT]{Colors.END} \"{text}\"")
            print(f"{Colors.YELLOW}[PASTE]{Colors.END} Pasting to Claude Code...")
            time.sleep(0.2)
            copy_and_paste(text)
            print(f"{Colors.GREEN}[DONE]{Colors.END} Text pasted! ✓\n")
        else:
            print(f"{Colors.YELLOW}[!]{Colors.END} No speech detected. Try again.\n")
    else:
        start_recording()


def on_press(key):
    """Handle key press."""
    from pynput.keyboard import Key as PynputKey

    try:
        # F8 to toggle recording
        if key == PynputKey.f8:
            toggle_recording()
        # Escape to quit
        elif key == PynputKey.esc:
            print(f"\n{Colors.YELLOW}[*]{Colors.END} Exiting Claude Voice Input...")
            os._exit(0)
    except Exception:
        pass


def print_banner():
    """Print welcome banner."""
    print(f"""
{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗
║        🎤 CLAUDE CODE VOICE INPUT 🎤                        ║
║          Speak to Claude Code!                               ║
╠══════════════════════════════════════════════════════════════╣
║  F8     = Toggle Recording (start/stop)                      ║
║  ESC    = Exit                                               ║
╠══════════════════════════════════════════════════════════════╣
║  1. Keep this window open                                    ║
║  2. Open Claude Code in another terminal                     ║
║  3. Press F8 to speak, F8 again to paste to Claude!          ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}
""")


def main():
    """Main function."""
    import sounddevice as sd
    from pynput import keyboard

    print_banner()

    # Initialize recognizer
    print(f"{Colors.YELLOW}[*]{Colors.END} Initializing speech recognition...")
    init_recognizer()
    print(f"{Colors.GREEN}[+]{Colors.END} Ready! Press F8 to start speaking.\n")

    # Start audio stream
    stream = sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype='int16',
        channels=1,
        callback=audio_callback
    )
    stream.start()

    # Start keyboard listener
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[*]{Colors.END} Exiting...")
        sys.exit(0)
