# Quick Check - Is Backend Running?

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "NPS Backend Health Check" -ForegroundColor Cyan  
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Test if backend is running
Write-Host "Testing backend connection..." -ForegroundColor Yellow

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "✅ BACKEND IS RUNNING!" -ForegroundColor Green
    Write-Host ""
    Write-Host "API Base URL: http://localhost:8000" -ForegroundColor Green
    Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Green
    Write-Host "Health: http://localhost:8000/health" -ForegroundColor Green
    Write-Host ""
    
    if ($response.StatusCode -eq 200) {
        Write-Host "Status: " -NoNewline
        Write-Host "✅ OK" -ForegroundColor Green
        $version = $response.Content | ConvertFrom-Json
        Write-Host "Version: " -NoNewline
        Write-Host $version.version -ForegroundColor Cyan
    }
} catch {
    Write-Host "❌ BACKEND IS NOT RUNNING" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error: " -NoNewline
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "To start the backend, run:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  cd d:\PFRDA\backend" -ForegroundColor White
    Write-Host "  python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -ForegroundColor White
    Write-Host ""
    Write-Host "Or use the startup script:" -ForegroundColor Yellow
    Write-Host "  .\START_SERVERS.ps1" -ForegroundColor White
    Write-Host ""
}

Write-Host ""
Write-Host "Testing frontend connection..." -ForegroundColor Yellow

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "✅ FRONTEND IS RUNNING!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Frontend URL: http://localhost:8080" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "❌ FRONTEND IS NOT RUNNING" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error: " -NoNewline
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "To start the frontend, run:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  cd d:\PFRDA\frontend" -ForegroundColor White
    Write-Host "  python -m http.server 8080 --directory ." -ForegroundColor White
    Write-Host ""
    Write-Host "Or use the startup script:" -ForegroundColor Yellow
    Write-Host "  .\START_SERVERS.ps1" -ForegroundColor White
    Write-Host ""
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. If BOTH are running:" -ForegroundColor White
Write-Host "   Open browser: http://localhost:8080" -ForegroundColor Green
Write-Host "   Try clicking 'Calculate ➤' button" -ForegroundColor Green
Write-Host ""
Write-Host "2. If BACKEND is missing:" -ForegroundColor White
Write-Host "   Run: .\START_SERVERS.ps1" -ForegroundColor Yellow
Write-Host "   Wait for both to start" -ForegroundColor Yellow
Write-Host "   Reload browser" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Open browser console for debugging:" -ForegroundColor White
Write-Host "   Press: F12" -ForegroundColor Yellow
Write-Host "   Look for red ❌ errors" -ForegroundColor Yellow
Write-Host ""
