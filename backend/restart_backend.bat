@echo off
echo ====================================
echo Restarting Backend Server
echo ====================================

echo.
echo [1/2] Killing all Python processes on port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do taskkill /F /PID %%a 2>nul

echo.
echo [2/2] Starting backend on port 8000...
cd /d "%~dp0"
call venv\Scripts\activate
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

pause
