# Deployment Guide

## Backend & Frontend Connectivity Status ✅

### Backend Verification
- ✅ Qdrant connection working properly
- ✅ Collection 'book_content' exists with data
- ✅ FastAPI upgraded to 0.123.5 with Pydantic v2 (Python 3.13 compatible)
- ✅ Chat endpoint tested successfully
- ✅ Health endpoint responding correctly

### Frontend-Backend Connectivity
- ✅ API endpoints configured
- ✅ CORS configured for development (localhost:3000, localhost:3001)
- ✅ CORS configured for production (GitHub Pages URLs)

## Pre-Deployment Checklist

### Backend Deployment

The backend needs to be deployed to a cloud service. Recommended options:

1. **Railway** (easiest)
2. **Render** (free tier available)
3. **Fly.io**
4. **Heroku**
5. **AWS/Azure/GCP**

#### Environment Variables Required:
```bash
OPENAI_API_KEY=your_key_here
QDRANT_URL=https://b52a32f4-94e8-4372-ae5a-e9d4a3662644.us-east-1-1.aws.cloud.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key_here
NEON_DATABASE_URL=your_neon_db_url_here
```

#### Backend Deployment Steps:
1. Choose a deployment platform
2. Connect your GitHub repository
3. Set root directory to `/backend`
4. Add all environment variables
5. Set start command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
6. Deploy
7. Note the deployed URL (e.g., `https://your-app.railway.app`)

### Frontend Deployment

#### Update API URL:
1. Edit `docusaurus-book/.env.production`
2. Replace `http://localhost:8000/api` with your deployed backend URL
   ```
   REACT_APP_API_URL=https://your-backend.railway.app/api
   ```

#### Update CORS on Backend:
Add your deployed backend URL to the CORS allowed origins in `backend/src/main.py`:
```python
allow_origins=[
    "http://localhost:3000",
    "http://localhost:3001",
    "https://nabeerak.github.io",
    "https://Nabeerak.github.io",
    "https://your-backend-url.com",  # Add your backend URL
],
```

#### Deploy Frontend to GitHub Pages:
```bash
cd docusaurus-book
npm run build
npm run deploy
```

## Database Migration

Before first deployment, run database migrations:
```bash
cd backend
alembic upgrade head
```

## Post-Deployment Testing

1. Test health endpoint: `https://your-backend.railway.app/health`
2. Test chat endpoint with curl or Postman
3. Open deployed frontend and test chatbot functionality
4. Verify conversation history works
5. Test search functionality

## Known Issues

1. **API URL Configuration**: Ensure frontend API URL matches deployed backend
2. **CORS**: Backend CORS must include all frontend URLs (dev + prod)
3. **Database**: Ensure Neon Postgres database is accessible from deployed backend
4. **Qdrant**: Ensure Qdrant Cloud is accessible from deployed backend

## Current Status

- ✅ Backend: Ready for deployment (compatible with Python 3.13)
- ✅ Frontend: Ready for GitHub Pages deployment
- ⚠️  Backend URL: Needs to be deployed and configured in frontend
- ⚠️  Database migrations: Need to be run on production database

## Next Steps

1. Deploy backend to Railway/Render
2. Update frontend `.env.production` with backend URL
3. Run database migrations on production
4. Deploy frontend to GitHub Pages
5. Test end-to-end functionality
