# NPS Retirement Intelligence Engine - Server Startup (PowerShell)
# Run this in PowerShell to start both backend and frontend servers

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host " NPS Retirement Intelligence Engine" -ForegroundColor Cyan
Write-Host " Server Startup Script (PowerShell)" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[✓] Python found: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "[✗] ERROR: Python not found! Please install Python 3.9+" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[1/2] Starting Backend Server..." -ForegroundColor Yellow
Write-Host "      Command: cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -ForegroundColor Gray
Write-Host "      URL: http://localhost:8000" -ForegroundColor Green
Write-Host "      API Docs: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""

# Start backend in a new PowerShell window
Start-Process powershell -ArgumentList {
    cd d:\PFRDA\backend
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
} -WindowStyle Normal

# Wait for backend to start
Write-Host "      Waiting 3 seconds for backend to initialize..." -ForegroundColor Gray
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "[2/2] Starting Frontend Server..." -ForegroundColor Yellow
Write-Host "      Command: cd frontend && python -m http.server 8080 --directory ." -ForegroundColor Gray
Write-Host "      URL: http://localhost:8080" -ForegroundColor Green
Write-Host ""

# Start frontend in a new PowerShell window
Start-Process powershell -ArgumentList {
    cd d:\PFRDA\frontend
    python -m http.server 8080 --directory .
} -WindowStyle Normal

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host " Both servers are starting!" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📱 Frontend: http://localhost:8080" -ForegroundColor Green
Write-Host "🔧 Backend:  http://localhost:8000" -ForegroundColor Green
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  You can now close this window. The servers will continue running in their own windows." -ForegroundColor Yellow
Write-Host ""
