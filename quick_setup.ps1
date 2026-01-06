# Quick Setup Script for Enhanced Interview System
# Run this to install dependencies and start the server

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "ENHANCED INTERVIEW SYSTEM - QUICK SETUP" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

# Step 1: Set execution policy
Write-Host "[1/4] Setting PowerShell execution policy..." -ForegroundColor Yellow
try {
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    Write-Host "      [OK] Execution policy set`n" -ForegroundColor Green
} catch {
    Write-Host "      [WARNING] Could not set execution policy. You may need admin rights.`n" -ForegroundColor Yellow
}

# Step 2: Activate virtual environment
Write-Host "[2/4] Activating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    & .\.venv\Scripts\Activate.ps1
    Write-Host "      [OK] Virtual environment activated`n" -ForegroundColor Green
} else {
    Write-Host "      [INFO] Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    & .\.venv\Scripts\Activate.ps1
    Write-Host "      [OK] Virtual environment created and activated`n" -ForegroundColor Green
}

# Step 3: Install dependencies
Write-Host "[3/4] Installing dependencies..." -ForegroundColor Yellow
Write-Host "      This may take a few minutes...`n" -ForegroundColor Gray

# Install essential packages first
$essentialPackages = @(
    "flask==3.0.0",
    "flask-cors==4.0.0",
    "authlib==1.3.0"
)

foreach ($package in $essentialPackages) {
    Write-Host "      Installing $package..." -ForegroundColor Gray
    pip install $package --quiet
}

# Install ML packages (these take longer)
Write-Host "      Installing ML packages (this may take a while)..." -ForegroundColor Gray
pip install pandas numpy scikit-learn --quiet

Write-Host "`n      [OK] All dependencies installed`n" -ForegroundColor Green

# Step 4: Start the server
Write-Host "[4/4] Starting Enhanced Interview System Server..." -ForegroundColor Yellow
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "Server will start in 3 seconds..." -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "============================================================`n" -ForegroundColor Cyan

Start-Sleep -Seconds 3

# Run the enhanced server
python auth_app.py
