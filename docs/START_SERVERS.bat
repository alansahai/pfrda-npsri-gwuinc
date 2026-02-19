@echo off
REM NPS Retirement Intelligence Engine - Server Startup Script
REM This script starts both the backend and frontend servers

echo.
echo ================================================
echo  NPS Retirement Intelligence Engine
echo  Server Startup Script
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.9+
    pause
    exit /b 1
)

echo [1/2] Starting Backend Server...
echo.
echo Running: cd backend ^&^& python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.
echo Backend will be available at: http://localhost:8000
echo API Documentation at: http://localhost:8000/docs
echo.

REM Start backend server in new window
start "NPS Backend Server" cmd /k "cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment for backend to start
timeout /t 3 /nobreak 

echo.
echo [2/2] Starting Frontend Server...
echo.
echo Running: cd frontend ^&^& python -m http.server 8080 --directory .
echo.
echo Frontend will be available at: http://localhost:8080
echo.

REM Start frontend server in new window
start "NPS Frontend Server" cmd /k "cd frontend && python -m http.server 8080 --directory ."

echo.
echo ================================================
echo  Both servers are starting!
echo ================================================
echo.
echo Frontend: http://localhost:8080
echo Backend:  http://localhost:8000
echo.
echo If browsers don't open automatically:
echo   - Frontend: http://localhost:8080
echo   - API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C in either window to stop that server
echo.
pause
