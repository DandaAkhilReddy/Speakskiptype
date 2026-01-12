#!/bin/bash
# SpeakSkipType - One-Line Installer

echo ""
echo "  ____                   _    ____  _    _       _____"
echo " / ___| _ __   ___  __ _| | _/ ___|| | _(_)_ __ |_   _|   _ _ __   ___"
echo " \\___ \\| '_ \\ / _ \\/ _\` | |/ \\___ \\| |/ / | '_ \\  | || | | | '_ \\ / _ \\"
echo "  ___) | |_) |  __/ (_| |   < ___) |   <| | |_) | | || |_| | |_) |  __/"
echo " |____/| .__/ \\___|\\__,_|_|\\_\\____/|_|\\_\\_| .__/  |_| \\__, | .__/ \\___|"
echo "       |_|                                |_|         |___/|_|"
echo ""
echo "Installing SpeakSkipType - Speech-to-Text for Terminal"
echo "======================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[!] Python3 not found. Please install Python 3.7+"
    exit 1
fi

echo "[*] Installing Python dependencies..."
pip3 install vosk sounddevice pynput -q

echo "[+] Installation complete!"
echo ""
echo "Run with: python3 speakskiptype.py"
echo ""
