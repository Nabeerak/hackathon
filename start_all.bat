@echo off
echo ========================================
echo Starting All Servers
echo ========================================
echo.
echo Starting Backend Server in new window...
start "Backend Server" cmd /k "cd backend && python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"
echo.
echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak > nul
echo.
echo Starting Frontend Server in new window...
start "Frontend Server" cmd /k "cd docusaurus-book && npm start"
echo.
echo ========================================
echo Both servers are starting!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo ========================================
echo.
echo Close this window or press any key to exit...
pause > nul
