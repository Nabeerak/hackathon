@echo off
echo ========================================
echo Starting Backend Server
echo ========================================
cd backend
echo Loading environment variables...
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
