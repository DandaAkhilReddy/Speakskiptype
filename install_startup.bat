@echo off
echo ============================================
echo   SpeakSkipType - Global Startup Installer
echo ============================================
echo.

:: Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
set "PYTHON_SCRIPT=%SCRIPT_DIR%speakskiptype.py"

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

:: Install dependencies
echo [*] Installing dependencies...
pip install vosk sounddevice pynput -q

:: Create VBS launcher (runs Python hidden, no console window)
echo [*] Creating hidden launcher...
set "VBS_FILE=%SCRIPT_DIR%SpeakSkipType_Hidden.vbs"
echo Set WshShell = CreateObject("WScript.Shell") > "%VBS_FILE%"
echo WshShell.Run "pythonw ""%PYTHON_SCRIPT%"" --bg", 0, False >> "%VBS_FILE%"

:: Create startup shortcut
echo [*] Adding to Windows Startup...
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT=%STARTUP_FOLDER%\SpeakSkipType.lnk"

:: Use PowerShell to create shortcut
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT%'); $s.TargetPath = '%VBS_FILE%'; $s.WorkingDirectory = '%SCRIPT_DIR%'; $s.Description = 'SpeakSkipType - Speech to Text'; $s.Save()"

echo.
echo ============================================
echo [SUCCESS] SpeakSkipType installed!
echo ============================================
echo.
echo SpeakSkipType will now start automatically when Windows boots.
echo.
echo CONTROLS (work ANYWHERE):
echo   Ctrl + R  =  Start Recording
echo   Ctrl + S  =  Stop and Auto-Type
echo   Ctrl + Q  =  Quit SpeakSkipType
echo.
echo Starting SpeakSkipType now...
echo.

:: Start it now
start "" "%VBS_FILE%"

echo [READY] SpeakSkipType is running in the background!
echo.
echo You can now open Command Prompt, PowerShell, Claude CLI,
echo or ANY application and use Ctrl+R to start voice typing!
echo.
pause
