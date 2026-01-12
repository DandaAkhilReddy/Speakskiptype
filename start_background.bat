@echo off
echo Starting SpeakSkipType in background...
echo.
echo CONTROLS (work in ANY application):
echo   Ctrl + R  =  Start Recording
echo   Ctrl + S  =  Stop and Auto-Type
echo   Ctrl + Q  =  Quit
echo.
start "" pythonw "%~dp0speakskiptype.py" --bg
echo [READY] SpeakSkipType is running!
echo You can close this window. Use Ctrl+Q to quit SpeakSkipType.
timeout /t 3
