@echo off
echo.
echo   ____                   _    ____  _    _       _____
echo  / ___^| _ __   ___  __ _^| ^| _/ ___^|^| ^| _(_)_ __ ^|_   _^|   _ _ __   ___
echo  \___ \^| '_ \ / _ \/ _` ^| ^|/ \___ \^| ^|/ / ^| '_ \  ^| ^|^| ^| ^| ^| '_ \ / _ \
echo   ___) ^| ^|_) ^|  __/ (_^| ^|   ^< ___) ^|   ^<^| ^| ^|_) ^| ^| ^|^| ^|_^| ^| ^|_) ^|  __/
echo  ^|____/^| .__/ \___^|\__,_^|_^|\_\____/^|_^|\_\_^| .__/  ^|_^| \__, ^| .__/ \___^|
echo        ^|_^|                                ^|_^|         ^|___/^|_^|
echo.
echo Installing SpeakSkipType - Speech-to-Text for Terminal
echo ======================================================
echo.

echo [*] Installing Python dependencies...
pip install vosk sounddevice pynput -q

echo [+] Installation complete!
echo.
echo Run with: python speakskiptype.py
echo.
pause
