# CryptoMatch Quick Start Script for Windows PowerShell
# Run this script to quickly set up and start the application

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  CRYPTOMATCH QUICK START  " -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if conda is available
$condaExists = Get-Command conda -ErrorAction SilentlyContinue
$inCondaEnv = $env:CONDA_DEFAULT_ENV

if (-not $condaExists) {
    Write-Host "❌ Anaconda not found!" -ForegroundColor Red
    Write-Host "Please install Anaconda from: https://www.anaconda.com/download" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Anaconda found" -ForegroundColor Green

# Check if environment exists
$envExists = conda env list | Select-String "cryptomatch"

if (-not $envExists) {
    Write-Host ""
    Write-Host "📦 Creating conda environment..." -ForegroundColor Yellow
    conda create -n cryptomatch python=3.9 -y
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create environment" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Environment created" -ForegroundColor Green
}
else {
    Write-Host "✅ Environment 'cryptomatch' already exists" -ForegroundColor Green
}

# Activate environment
Write-Host ""
Write-Host "🔄 Activating environment..." -ForegroundColor Yellow
conda activate cryptomatch

# Install dependencies
Write-Host ""
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Dependencies installed" -ForegroundColor Green

# Check for .env file
if (-not (Test-Path ".env")) {
    Write-Host ""
    Write-Host "⚠️  No .env file found!" -ForegroundColor Yellow
    Write-Host "Creating .env from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    
    Write-Host ""
    Write-Host "🔑 IMPORTANT: Please edit .env and add your OpenAI API key!" -ForegroundColor Red
    Write-Host "   Run: notepad .env" -ForegroundColor Yellow
    Write-Host ""
    
    $response = Read-Host "Do you want to open .env now? (y/n)"
    if ($response -eq "y" -or $response -eq "Y") {
        notepad .env
        Write-Host ""
        Read-Host "Press Enter when you're done editing .env"
    }
}
else {
    Write-Host "✅ .env file exists" -ForegroundColor Green
}

# Run tests
Write-Host ""
Write-Host "🧪 Running tests..." -ForegroundColor Yellow
python test_installation.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "⚠️  Some tests failed, but you can still try running the app" -ForegroundColor Yellow
}

# Ask to start server
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
$response = Read-Host "Start the server now? (y/n)"

if ($response -eq "y" -or $response -eq "Y") {
    Write-Host ""
    Write-Host "🚀 Starting CryptoMatch server..." -ForegroundColor Green
    Write-Host "   URL: http://localhost:8000" -ForegroundColor Cyan
    Write-Host "   Press Ctrl+C to stop" -ForegroundColor Yellow
    Write-Host ""
    
    python main.py
}
else {
    Write-Host ""
    Write-Host "To start the server later, run:" -ForegroundColor Yellow
    Write-Host "   conda activate cryptomatch" -ForegroundColor Cyan
    Write-Host "   python main.py" -ForegroundColor Cyan
    Write-Host ""
}
