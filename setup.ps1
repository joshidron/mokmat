# AI Interview System - Setup Script
# Run this script to set up the system

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AI Interview System - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Install Dependencies
Write-Host "[1/3] Installing Python dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray
Write-Host ""

try {
    pip install flask==3.0.0
    pip install flask-cors==4.0.0
    pip install pandas
    pip install scikit-learn
    pip install numpy
    
    Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Error installing dependencies" -ForegroundColor Red
    Write-Host "Please run: pip install flask flask-cors pandas scikit-learn numpy" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Step 2: Train the Model
Write-Host "[2/3] Training the AI model..." -ForegroundColor Yellow
Write-Host "This will take 30-60 seconds..." -ForegroundColor Gray
Write-Host ""

try {
    python train_model.py
    Write-Host "✅ Model trained successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Error training model" -ForegroundColor Red
    Write-Host "Please run manually: python train_model.py" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Step 3: Instructions
Write-Host "[3/3] Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Next Steps" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the ENHANCED server (with login, limits, tab detection):" -ForegroundColor Yellow
Write-Host "  python auth_app.py" -ForegroundColor White
Write-Host ""
Write-Host "To start the BASIC server (no authentication):" -ForegroundColor Yellow
Write-Host "  python app.py" -ForegroundColor White
Write-Host ""
Write-Host "Then open your browser to:" -ForegroundColor Yellow
Write-Host "  http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Features" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ User Authentication" -ForegroundColor Green
Write-Host "✅ Interview Limits (2 per 24h, 5 total)" -ForegroundColor Green
Write-Host "✅ Tab Switching Detection" -ForegroundColor Green
Write-Host "✅ Dynamic Performance Reports" -ForegroundColor Green
Write-Host "✅ 600+ Interview Questions" -ForegroundColor Green
Write-Host "✅ AI-Powered Question Selection" -ForegroundColor Green
Write-Host ""
Write-Host "Happy Interviewing! 🎯" -ForegroundColor Cyan
Write-Host ""
