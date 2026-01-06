@echo off
echo.
echo ============================================================
echo ENHANCED INTERVIEW SYSTEM - QUICK SETUP
echo ============================================================
echo.

echo [1/3] Activating virtual environment...
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    echo       [OK] Virtual environment activated
) else (
    echo       [INFO] Creating virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo       [OK] Virtual environment created and activated
)
echo.

echo [2/3] Installing dependencies...
echo       This may take a few minutes...
echo.
pip install flask flask-cors authlib pandas numpy scikit-learn --quiet
echo.
echo       [OK] All dependencies installed
echo.

echo [3/3] Starting Enhanced Interview System Server...
echo.
echo ============================================================
echo Server starting...
echo Open your browser to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python auth_app.py
