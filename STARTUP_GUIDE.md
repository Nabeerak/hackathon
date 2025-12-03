# Complete Startup Guide - Get Your Chatbot Running!

## Overview

This guide will help you get the complete Physical AI chatbot running inside Docusaurus in **30-45 minutes**.

## Prerequisites

✅ You already have:
- Node.js 22.x installed
- Python 3.13 with venv
- Git repository cloned
- Dependencies installed (npm, pip)

## Step-by-Step Instructions

### Phase 1: Setup External Services (15-20 minutes)

#### 1A. Setup Neon PostgreSQL (5 minutes)

**Already done!** Your `.env.example` shows you have Neon configured:
```env
NEON_DATABASE_URL="postgresql://neondb_owner:npg_bn2H0AqWeNpv@ep-lingering-meadow-a1l67fjv-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
```

Copy this to your actual `.env`:

```bash
cd backend
# Copy .env.example to .env if you haven't
cp .env.example .env

# Run database migrations
./venv/Scripts/python.exe -m alembic upgrade head
```

Expected output:
```
INFO  [alembic.runtime.migration] Running upgrade  -> e4759d7755ca
```

#### 1B. Setup Qdrant Cloud (10 minutes)

📖 **Follow**: `backend/QDRANT_SETUP.md`

Quick summary:
1. Go to https://cloud.qdrant.io/
2. Sign up (free tier)
3. Create cluster named `hackathon-chatbot`
4. Copy URL and API Key
5. Update `backend/.env`:
   ```env
   QDRANT_URL="https://your-cluster-url.aws.cloud.qdrant.io"
   QDRANT_API_KEY="your-actual-api-key"
   ```
6. Test connection:
   ```bash
   cd backend
   ./venv/Scripts/python.exe -c "from qdrant_client import QdrantClient; import os; from dotenv import load_dotenv; load_dotenv(); client = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY')); print('✅ Connected!')"
   ```

#### 1C. Setup OpenAI API (5 minutes)

**IMPORTANT**: You need to rotate the exposed API key first!

1. Go to https://platform.openai.com/api-keys
2. Find and **delete/revoke** the old exposed key
3. Click "Create new secret key"
4. Name it: `hackathon-chatbot`
5. Copy the new key (starts with `sk-proj-...`)
6. Update `backend/.env`:
   ```env
   OPENAI_API_KEY="your-new-api-key-here"
   ```

### Phase 2: Ingest Book Content (10-15 minutes)

This creates the knowledge base for your chatbot:

```bash
cd backend

# This will read all markdown files and create embeddings
./venv/Scripts/python.exe scripts/ingest_book_content.py --book-path ../docusaurus-book/docs/physical-ai-textbook/
```

Expected output:
```
Collection 'book_content' ensured.
Ingested 15 chunks from docs/physical-ai-textbook/course-overview/overview.md
Ingested 22 chunks from docs/physical-ai-textbook/ros2-fundamentals/installation.md
...
Finished ingesting 50 documents from ../docusaurus-book/docs/physical-ai-textbook/
```

**Note**: This may take 5-15 minutes depending on:
- Number of markdown files
- OpenAI API rate limits
- Internet speed

**Troubleshooting**:
- If you see "Rate limit exceeded": Wait 1 minute and try again
- If ingestion fails midway: It's safe to re-run, it will skip existing chunks

### Phase 3: Start the Servers (2 minutes)

You'll need **two terminal windows**.

#### Terminal 1: Backend (FastAPI)

```bash
cd backend
./venv/Scripts/python.exe -m uvicorn src.main:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [67890]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Test it**: Open http://127.0.0.1:8000/health in your browser
- Should see: `{"status":"healthy"}`

#### Terminal 2: Frontend (Docusaurus)

```bash
cd docusaurus-book
npm start
```

Expected output:
```
[SUCCESS] Docusaurus website is running at: http://localhost:3000/
```

**The site will automatically open in your browser!**

### Phase 4: Test the Chatbot! (5 minutes)

1. **Open**: http://localhost:3000/
2. **Look for**: Purple chatbot button in bottom-right corner
3. **Click it**: Chat window opens
4. **Ask a question**: Try these:
   - "What is Physical AI?"
   - "Explain ROS 2"
   - "How do I install NVIDIA Isaac?"
5. **Verify**:
   - ✅ Bot responds within 3 seconds
   - ✅ Answers are relevant to the book
   - ✅ Sources are shown (if implemented)
   - ✅ Conversation history maintained

## Quick Test Checklist

After startup, verify each component:

### Backend Health Check

```bash
# Test health endpoint
curl http://127.0.0.1:8000/health

# Expected: {"status":"healthy"}
```

### Database Connection

```bash
cd backend
./venv/Scripts/python.exe -c "from src.database import engine; print('✅ Database OK')"
```

### Qdrant Connection

```bash
./venv/Scripts/python.exe -c "from src.services.qdrant_service import QdrantService; qs = QdrantService(); print('✅ Qdrant OK')"
```

### OpenAI Connection

```bash
./venv/Scripts/python.exe -c "from src.services.openai_service import OpenAIService; os = OpenAIService(); print('✅ OpenAI OK')"
```

### Chatbot API Test

```bash
# Test chat endpoint
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is ROS 2?", "conversation_id": null}'
```

Expected: JSON response with chatbot answer

### Frontend Test

1. Open http://localhost:3000/
2. Check console for errors (F12)
3. Click chatbot button
4. Send a message
5. Verify response appears

## Responsive Design Testing

Test on different screen sizes:

### Desktop (1920x1080)
- Chatbot: 400px wide, bottom-right corner
- Should have nice shadow and rounded corners

### Tablet (768x1024)
- Chatbot: Slightly smaller, max 450px
- Still bottom-right positioned

### Mobile (375x667)
- Chatbot: **Full screen** when open
- Toggle button stays visible in bottom-right
- No border-radius on mobile (full coverage)
- Font size adjusted for readability

**Test in browser**:
1. Press F12 (Dev Tools)
2. Click "Toggle Device Toolbar" icon
3. Select different devices (iPhone, iPad, etc.)
4. Test chatbot interaction

## Troubleshooting

### Backend won't start

**Error**: `"No database URL found!"`
- **Fix**: Check `backend/.env` has `NEON_DATABASE_URL` set

**Error**: `"Connection refused"` (Qdrant)
- **Fix**: Verify Qdrant cluster is running in dashboard
- **Fix**: Check `QDRANT_URL` and `QDRANT_API_KEY` in `.env`

**Error**: `"OpenAI authentication failed"`
- **Fix**: Verify `OPENAI_API_KEY` is correct and not expired

### Frontend won't start

**Error**: `"Module not found"`
- **Fix**: Run `npm install` in `docusaurus-book/`

**Error**: `"Port 3000 already in use"`
- **Fix**: Kill existing process or use different port:
  ```bash
  npm start -- --port 3001
  ```

### Chatbot not responding

**Symptom**: Button shows but no response when clicking
- **Fix**: Check if backend is running (http://127.0.0.1:8000/health)
- **Fix**: Check browser console for CORS errors
- **Fix**: Verify `CORS` in `backend/src/main.py` includes `http://localhost:3000`

**Symptom**: Bot says "Error connecting to backend"
- **Fix**: Backend might be down - check Terminal 1
- **Fix**: Check `docusaurus-book/src/services/chat_api.ts` has correct API URL

**Symptom**: Bot responds but answers are irrelevant
- **Fix**: Data might not be ingested - re-run ingestion script
- **Fix**: Check Qdrant has data:
  ```bash
  ./venv/Scripts/python.exe -c "from qdrant_client import QdrantClient; import os; from dotenv import load_dotenv; load_dotenv(); client = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY')); coll = client.get_collection('book_content'); print(f'Chunks: {coll.points_count}')"
  ```

### Mobile Responsiveness Issues

**Symptom**: Chatbot too small on mobile
- **Fix**: Clear browser cache
- **Fix**: Hard reload (Ctrl+Shift+R)

**Symptom**: Text zooms in when typing on iOS
- **Fix**: Already handled with `font-size: 16px` in inputs

## Production Deployment (Future)

Once everything works locally, deploy to:

### Frontend (Docusaurus)
- **GitHub Pages**: `npm run build && npm run deploy`
- **Vercel**: Connect repo and deploy
- **Netlify**: Drag-and-drop `build/` folder

### Backend (FastAPI)
- **Render.com** (recommended - free tier)
- **Railway.app**
- **Fly.io**
- **AWS/Azure/GCP**

**Update frontend** to use production API:
- Edit `docusaurus-book/src/services/chat_api.ts`
- Change `API_BASE_URL` to your deployed backend URL

## What's Next?

After getting the chatbot running:

1. ✅ Test thoroughly with different questions
2. ✅ Check mobile responsiveness
3. ⏭️ Implement authentication (better-auth.com)
4. ⏭️ Add personalization features
5. ⏭️ Add Urdu translation
6. ⏭️ Deploy to production

## Need Help?

- **Neon Issues**: See `backend/NEON_SETUP.md`
- **Qdrant Issues**: See `backend/QDRANT_SETUP.md`
- **Backend Errors**: Check `backend/src/` code
- **Frontend Errors**: Check browser console (F12)

## Success Criteria

You'll know everything is working when:

✅ Backend health check returns `{"status":"healthy"}`
✅ Qdrant has 500+ chunks ingested
✅ Frontend loads without console errors
✅ Chatbot button appears in bottom-right
✅ Chatbot responds to questions within 3 seconds
✅ Answers are relevant to your book content
✅ Mobile view shows full-screen chatbot
✅ Tablet view shows appropriate sizing
✅ Desktop view shows elegant floating chat window

## Time Investment Summary

- **Setup services**: 15-20 min (one-time)
- **Ingest data**: 10-15 min (one-time)
- **Start servers**: 2 min (every session)
- **Test chatbot**: 5 min
- **Total first-time**: ~45 min
- **Total subsequent**: ~7 min

🎉 **Congratulations!** Once complete, you have a fully functional RAG chatbot embedded in your Docusaurus site!
