@echo off
REM Start Gesture Recognition API Server
REM This script starts the Flask API server for gesture recognition

echo ============================================================
echo GESTURE RECOGNITION API SERVER
echo ============================================================
echo.
echo Starting Flask server on http://localhost:5001
echo.
echo Available Endpoints:
echo   POST   /api/gesture/start       - Start gesture recognition
echo   POST   /api/gesture/stop        - Stop gesture recognition
echo   GET    /api/gesture/status      - Get current status
echo   GET    /api/gesture/stats       - Get session statistics
echo   GET    /api/gesture/video_feed  - Video stream
echo   GET    /api/gesture/frame       - Get current frame
echo   POST   /api/gesture/save_session - Save session data
echo   GET    /api/gesture/health      - Health check
echo.
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
python -c "import cv2, mediapipe, flask" >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: Required packages not found
    echo Installing dependencies...
    python install_gesture_recognition.py
    echo.
)

REM Start the API server
echo Starting API server...
echo.
python gesture_api.py

pause
