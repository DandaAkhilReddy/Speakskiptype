@echo off
echo ============================================
echo   SpeakSkipType - Uninstaller
echo ============================================
echo.

set "SCRIPT_DIR=%~dp0"
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

:: Kill any running instance
echo [*] Stopping SpeakSkipType...
taskkill /f /im pythonw.exe 2>nul

:: Remove startup shortcut
echo [*] Removing from Windows Startup...
del "%STARTUP_FOLDER%\SpeakSkipType.lnk" 2>nul

:: Remove VBS launcher
echo [*] Removing launcher...
del "%SCRIPT_DIR%SpeakSkipType_Hidden.vbs" 2>nul

echo.
echo ============================================
echo [DONE] SpeakSkipType has been uninstalled!
echo ============================================
echo.
echo SpeakSkipType will no longer start with Windows.
echo You can still run it manually with: python speakskiptype.py
echo.
pause
