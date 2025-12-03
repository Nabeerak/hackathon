@echo off
echo ========================================
echo Starting Physical AI Textbook Servers
echo ========================================

echo.
echo [1/2] Starting Backend Server...
cd backend
start "Backend Server" cmd /k "venv\Scripts\activate && python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend Server...
cd ..\docusaurus-book
start "Frontend Server" cmd /k "npm start"

echo.
echo ========================================
echo Servers Starting...
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo ========================================
echo.
echo Press any key to exit...
pause >nul
