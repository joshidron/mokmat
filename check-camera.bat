@echo off
echo ========================================
echo Camera Usage Diagnostic Tool
echo ========================================
echo.
echo Checking which applications are using your camera...
echo.

REM Check for common video conferencing apps
echo [Checking Running Processes]
echo.

tasklist /FI "IMAGENAME eq Zoom.exe" 2>NUL | find /I /N "Zoom.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [FOUND] Zoom is running - This may be using your camera
) else (
    echo [OK] Zoom is not running
)

tasklist /FI "IMAGENAME eq Teams.exe" 2>NUL | find /I /N "Teams.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [FOUND] Microsoft Teams is running - This may be using your camera
) else (
    echo [OK] Microsoft Teams is not running
)

tasklist /FI "IMAGENAME eq Discord.exe" 2>NUL | find /I /N "Discord.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [FOUND] Discord is running - This may be using your camera
) else (
    echo [OK] Discord is not running
)

tasklist /FI "IMAGENAME eq Skype.exe" 2>NUL | find /I /N "Skype.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [FOUND] Skype is running - This may be using your camera
) else (
    echo [OK] Skype is not running
)

tasklist /FI "IMAGENAME eq obs64.exe" 2>NUL | find /I /N "obs64.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [FOUND] OBS Studio is running - This may be using your camera
) else (
    echo [OK] OBS Studio is not running
)

tasklist /FI "IMAGENAME eq chrome.exe" 2>NUL | find /I /N "chrome.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [INFO] Chrome is running - Check for tabs using camera
)

tasklist /FI "IMAGENAME eq msedge.exe" 2>NUL | find /I /N "msedge.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [INFO] Edge is running - Check for tabs using camera
)

echo.
echo ========================================
echo Camera Device Status
echo ========================================
echo.

REM Check if camera device is available
powershell -Command "Get-PnpDevice | Where-Object {$_.Class -eq 'Camera' -or $_.FriendlyName -like '*camera*'} | Format-Table -AutoSize Status, FriendlyName"

echo.
echo ========================================
echo Recommendations:
echo ========================================
echo.
echo 1. Close any applications marked as [FOUND] above
echo 2. Close browser tabs that might be using the camera
echo 3. Refresh your interview page after closing apps
echo 4. If issue persists, restart your browser
echo.
echo Press any key to exit...
pause >nul
