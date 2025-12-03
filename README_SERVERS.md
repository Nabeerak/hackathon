# Server Startup Guide

## Quick Start

### Start Both Servers (Recommended)
Double-click `start_all.bat` to start both backend and frontend servers in separate windows.

- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

### Start Individual Servers

#### Backend Only
Double-click `start_backend.bat` or run:
```bash
cd backend
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Only
Double-click `start_frontend.bat` or run:
```bash
cd docusaurus-book
npm start
```

## Backend API Endpoints

### Main Endpoints
- `GET /` - API status
- `POST /api/chat` - Chat with RAG system
- `GET /api/health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)

### Chat API Example
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is Physical AI?",
    "selected_text": "Optional selected text for context",
    "user_id": 1
  }'
```

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
powershell -Command "Stop-Process -Id <PID> -Force"
```

**Database connection errors:**
- Check `.env` file has correct `NEON_DATABASE_URL`
- Run migrations: `cd backend && alembic upgrade head`

**Missing dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

### Frontend Issues

**Port 3000 already in use:**
- Docusaurus will automatically try port 3001, 3002, etc.
- Or kill the process using port 3000

**Missing dependencies:**
```bash
cd docusaurus-book
npm install
```

## Testing Backend Services

Run the backend test script to verify all services are working:
```bash
cd backend
python test_services.py
```

This will check:
- Environment variables
- Database connection
- OpenAI service
- Qdrant service
- Chat service
- Database tables

## Environment Variables

Required in `backend/.env`:
```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
NEON_DATABASE_URL=your_postgresql_url
```

## Features

### Text Selection Feature
1. Select any text on a documentation page
2. Click "Ask in Chat" button that appears
3. Chatbot opens with selected text as context
4. Ask questions about the selected text

### Conversation History
- All conversations are saved in the database
- Click "History" button to view past conversations
- Resume previous conversations

## Development

### Backend
- FastAPI with hot reload enabled
- Logs displayed in terminal
- Auto-reloads on code changes

### Frontend
- Docusaurus development server
- Hot Module Replacement (HMR)
- Opens browser automatically at http://localhost:3000

## Production Deployment

### Backend
```bash
cd backend
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend
```bash
cd docusaurus-book
npm run build
npm run serve
```
