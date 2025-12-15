# Environment Setup Guide

Complete guide for setting up environment variables for local development and production deployment.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Production Deployment Setup](#production-deployment-setup)
4. [Environment Variables Reference](#environment-variables-reference)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before setting up environment variables, ensure you have accounts and API keys for:

- ✅ [Neon PostgreSQL](https://neon.tech) (or any PostgreSQL provider)
- ✅ [Qdrant Cloud](https://cloud.qdrant.io) (for vector database)
- ✅ [OpenAI](https://platform.openai.com) (for AI/LLM features)
- ✅ (Optional) [Render](https://render.com) (for deployment)

---

## 🏠 Local Development Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/nabeerak/hackathon.git
cd hackathon
```

### Step 2: Copy Environment Template

```bash
# Copy the example file to create your local .env
cp .env.example .env
```

### Step 3: Fill in Backend Environment Variables

Edit `backend/.env` with your actual credentials:

```bash
# Use your favorite text editor
code backend/.env
# or
nano backend/.env
# or
vim backend/.env
```

**Required Variables:**

```env
# 1. Database (Get from Neon dashboard)
NEON_DATABASE_URL="postgresql://user:password@host.region.aws.neon.tech/database?sslmode=require"

# 2. JWT Secret (Generate a secure random key)
JWT_SECRET_KEY="your-generated-secret-key-here"
BETTER_AUTH_SECRET="your-generated-secret-key-here"

# 3. Qdrant (Get from Qdrant Cloud dashboard)
QDRANT_URL="https://your-cluster.region.aws.cloud.qdrant.io"
QDRANT_API_KEY="your-qdrant-api-key"

# 4. OpenAI (Get from OpenAI dashboard)
OPENAI_API_KEY="sk-proj-your-openai-key-here"

# 5. Local settings
ENVIRONMENT="development"
CORS_ORIGINS="http://localhost:3000,http://localhost:3001"
```

### Step 4: Generate Secure Keys

```bash
# Generate JWT secret (Linux/Mac)
openssl rand -hex 32

# Generate JWT secret (Python)
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate JWT secret (Node.js)
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

### Step 5: Setup Frontend Environment

Create `docusaurus-book/.env.development`:

```bash
cd docusaurus-book
echo "REACT_APP_API_URL=http://localhost:8000/api" > .env.development
```

### Step 6: Install Dependencies

**Backend:**
```bash
cd backend

# Create virtual environment (optional but recommended)
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Frontend:**
```bash
cd docusaurus-book
npm install
```

### Step 7: Initialize Database

```bash
cd backend

# Run Alembic migrations
alembic upgrade head

# Verify connection
python -c "from src.database import engine; print('Database connected!' if engine else 'Failed')"
```

### Step 8: Start Development Servers

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd docusaurus-book
npm start
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/health

---

## 🚀 Production Deployment Setup

### Option 1: Deploy on Render

#### A. Backend Deployment

1. **Create Web Service:**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect GitHub repository

2. **Configure Service:**

```yaml
Name: your-backend-api
Environment: Python 3
Region: Oregon (US West)
Branch: main
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

3. **Add Environment Variables:**

Click "Environment" tab and add:

```
NEON_DATABASE_URL=postgresql://user:password@host.aws.neon.tech/db?sslmode=require
JWT_SECRET_KEY=your-production-secret-key
BETTER_AUTH_SECRET=your-production-auth-secret
QDRANT_URL=https://your-cluster.aws.cloud.qdrant.io
QDRANT_API_KEY=your-qdrant-key
OPENAI_API_KEY=sk-proj-your-openai-key
ENVIRONMENT=production
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
SESSION_DURATION_DAYS=7
HOST=0.0.0.0
PORT=$PORT
```

4. **Health Check:**
   - Path: `/api/health`
   - Expected Status: 200

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Copy your service URL: `https://hackathon-backend-rspn.onrender.com`

#### B. Frontend Deployment (GitHub Pages)

1. **Update Frontend Configuration:**

Edit `docusaurus-book/.env.production`:

```env
REACT_APP_API_URL=https://hackathon-backend-rspn.onrender.com/api
```

2. **Update docusaurus.config.js:**

```javascript
module.exports = {
  url: 'https://nabeerak.github.io',
  baseUrl: '/hackathon/',

  customFields: {
    apiUrl: process.env.REACT_APP_API_URL || 'https://hackathon-backend-rspn.onrender.com/api',
  },
};
```

3. **Build and Deploy:**

```bash
cd docusaurus-book
npm install
npm run build
npx gh-pages -d build
```

4. **GitHub Pages Setup:**
   - Go to Repository Settings → Pages
   - Source: `gh-pages` branch
   - URL: `https://nabeerak.github.io/hackathon/`

---

### Option 2: Deploy on Railway

#### Backend Deployment

1. **Create New Project:**
   - Go to [Railway Dashboard](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

2. **Configure Service:**

```bash
# Railway automatically detects Python
# Add environment variables in the Variables tab
```

3. **Add Environment Variables:**

Same as Render configuration above.

4. **Deploy:**
   - Railway auto-deploys on push
   - Get your URL: `https://your-app.up.railway.app`

---

### Option 3: Deploy on Vercel (Frontend Only)

```bash
cd docusaurus-book

# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Set environment variable
vercel env add REACT_APP_API_URL production
# Enter: https://your-backend-api.onrender.com/api

# Deploy production
vercel --prod
```

---

## 📚 Environment Variables Reference

### Backend Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NEON_DATABASE_URL` | ✅ Yes | - | PostgreSQL connection string |
| `JWT_SECRET_KEY` | ✅ Yes | - | JWT token signing key (min 32 chars) |
| `BETTER_AUTH_SECRET` | ✅ Yes | - | Session management secret |
| `QDRANT_URL` | ✅ Yes | - | Qdrant vector database URL |
| `QDRANT_API_KEY` | ✅ Yes | - | Qdrant API key |
| `OPENAI_API_KEY` | ✅ Yes | - | OpenAI API key |
| `ENVIRONMENT` | ⚠️ Optional | `development` | Environment mode |
| `CORS_ORIGINS` | ⚠️ Optional | `localhost:3000` | Allowed CORS origins |
| `SESSION_DURATION_DAYS` | ⚠️ Optional | `7` | Session expiry in days |
| `HOST` | ⚠️ Optional | `0.0.0.0` | Server bind host |
| `PORT` | ⚠️ Optional | `8000` | Server port |
| `RENDER_API_KEY` | ❌ No | - | Render deployment API key |

### Frontend Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `REACT_APP_API_URL` | ✅ Yes | `http://localhost:8000/api` | Backend API URL |

---

## 🔧 Troubleshooting

### Issue: Database Connection Error

**Error:** `NEON_DATABASE_URL environment variable is not set`

**Solution:**
```bash
# Check if .env file exists
ls -la backend/.env

# Verify .env is loaded
cd backend
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('NEON_DATABASE_URL'))"

# If None, check .env file format (no spaces around =)
# Correct: NEON_DATABASE_URL="postgresql://..."
# Wrong:   NEON_DATABASE_URL = "postgresql://..."
```

---

### Issue: Qdrant Connection Failed

**Error:** `Qdrant verification failed (non-critical)`

**Solution:**
```bash
# Check Qdrant credentials
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('URL:', os.getenv('QDRANT_URL')); print('Key:', os.getenv('QDRANT_API_KEY')[:10]+'...' if os.getenv('QDRANT_API_KEY') else 'NOT SET')"

# Test Qdrant connection
curl -X GET "https://your-cluster.aws.cloud.qdrant.io:6333/collections" \
  -H "api-key: your-qdrant-api-key"
```

---

### Issue: CORS Error in Browser

**Error:** `Access to fetch at 'http://localhost:8000/api/...' has been blocked by CORS policy`

**Solution:**
```bash
# Check backend CORS configuration in backend/src/main.py
# Ensure frontend URL is in allow_origins list

# For development, add:
allow_origins=[
    "http://localhost:3000",
    "http://localhost:3001",
]

# For production, add:
allow_origins=[
    "https://nabeerak.github.io",
    "https://your-frontend-domain.com",
]
```

---

### Issue: Frontend Can't Connect to Backend

**Error:** `NetworkError when attempting to fetch resource`

**Solution:**
```bash
# Check REACT_APP_API_URL in frontend
cd docusaurus-book
cat .env.development

# Verify backend is running
curl http://localhost:8000/api/health

# Check browser console for exact error
# Ensure no typos in API URL (trailing slash matters!)
# Correct: http://localhost:8000/api
# Wrong:   http://localhost:8000/api/
```

---

### Issue: OpenAI API Key Invalid

**Error:** `401 Unauthorized` from OpenAI

**Solution:**
```bash
# Test OpenAI key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# If error, regenerate key at:
# https://platform.openai.com/api-keys

# Ensure no spaces or quotes in key
# Correct: OPENAI_API_KEY="sk-proj-abc123"
# Wrong:   OPENAI_API_KEY=" sk-proj-abc123 "
```

---

### Issue: JWT Token Invalid

**Error:** `Invalid token` or `Token expired`

**Solution:**
```bash
# Regenerate JWT secret
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Update backend/.env with new key
JWT_SECRET_KEY="new-generated-key-here"

# Restart backend server
# All existing sessions will be invalidated
```

---

## 🎯 Quick Setup Checklist

### Local Development
- [ ] Copy `.env.example` to `.env`
- [ ] Fill in `NEON_DATABASE_URL`
- [ ] Generate and set `JWT_SECRET_KEY`
- [ ] Add `QDRANT_URL` and `QDRANT_API_KEY`
- [ ] Add `OPENAI_API_KEY`
- [ ] Create `docusaurus-book/.env.development`
- [ ] Install backend dependencies: `pip install -r requirements.txt`
- [ ] Install frontend dependencies: `npm install`
- [ ] Run migrations: `alembic upgrade head`
- [ ] Start backend: `uvicorn src.main:app --reload`
- [ ] Start frontend: `npm start`
- [ ] Test health: `curl http://localhost:8000/api/health`

### Production Deployment
- [ ] Create production database on Neon
- [ ] Create Qdrant cluster
- [ ] Generate production JWT secret
- [ ] Configure Render/Railway web service
- [ ] Add all environment variables
- [ ] Set `ENVIRONMENT=production`
- [ ] Update CORS_ORIGINS with frontend domain
- [ ] Deploy backend
- [ ] Update frontend `.env.production`
- [ ] Build and deploy frontend
- [ ] Test health: `curl https://your-backend.onrender.com/api/health`

---

## 📞 Support

If you encounter issues:

1. Check this guide's [Troubleshooting](#troubleshooting) section
2. Review `CLEANUP_REPORT.md` for common file issues
3. Check logs:
   - Backend: `uvicorn` console output
   - Frontend: Browser console (F12)
   - Render: Dashboard → Logs tab

---

**Last Updated:** December 7, 2025
**Project:** Book-Embedded RAG Chatbot
**Tech Stack:** FastAPI + Docusaurus + PostgreSQL + Qdrant + OpenAI
