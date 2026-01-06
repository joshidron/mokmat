@echo off
REM Start Complete Interview System with Gesture Recognition
REM This script starts both the main interview app and gesture API

echo ============================================================
echo COMPLETE INTERVIEW SYSTEM WITH GESTURE RECOGNITION
echo ============================================================
echo.
echo This will start:
echo   1. Main Interview App (Port 5000)
echo   2. Gesture Recognition API (Port 5001)
echo.
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install gesture recognition dependencies if needed
echo Checking gesture recognition dependencies...
python -c "import cv2, mediapipe" >nul 2>&1
if errorlevel 1 (
    echo Installing gesture recognition dependencies...
    python install_gesture_recognition.py
)

echo.
echo Starting servers...
echo.

REM Start gesture API in new window
start "Gesture Recognition API" cmd /k "python gesture_api.py"

REM Wait a moment for gesture API to start
timeout /t 3 /nobreak >nul

REM Start main interview app
start "Interview System" cmd /k "python app.py"

echo.
echo ============================================================
echo SERVERS STARTED
echo ============================================================
echo.
echo Main Interview App:    http://localhost:5000
echo Gesture API:           http://localhost:5001
echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the servers.
echo.
echo ============================================================
echo.

pause
