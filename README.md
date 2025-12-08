# Physical AI & Humanoid Robotics - Backend API

FastAPI backend for the Physical AI & Humanoid Robotics textbook with RAG chatbot, user authentication, and personalization features.

## 🚀 Deployment on Render

This branch (`backend-deploy`) is configured for easy deployment on Render.

### Quick Deploy

1. **Create Web Service on Render**
   - Go to https://dashboard.render.com
   - Click **New+** → **Web Service**
   - Connect this GitHub repository
   - Select branch: `backend-deploy`

2. **Configure Build Settings**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
   - **Python Version:** `3.11`

3. **Add Environment Variables**

   Required variables:
   ```bash
   NEON_DATABASE_URL=postgresql://...
   JWT_SECRET_KEY=your-secret-key
   BETTER_AUTH_SECRET=your-auth-secret
   QDRANT_URL=https://...
   QDRANT_API_KEY=your-qdrant-key
   OPENAI_API_KEY=sk-...
   CORS_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
   ENVIRONMENT=production
   HOST=0.0.0.0
   ```

4. **Deploy**
   - Click **Create Web Service**
   - Render will automatically build and deploy

## 📋 Features

- **RAG Chatbot**: OpenAI-powered chatbot with Qdrant vector search
- **User Authentication**: Better-auth integration with session management
- **User Profiles**: Personalized learning paths and progress tracking
- **Conversation History**: Persistent chat history per user
- **PostgreSQL Database**: Neon serverless database
- **Vector Search**: Qdrant cloud for semantic search

## 🛠️ Technology Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (Neon)
- **Vector DB**: Qdrant Cloud
- **AI/LLM**: OpenAI GPT-4
- **Auth**: Better-auth
- **ORM**: SQLAlchemy
- **Migrations**: Alembic

## 📁 Project Structure

```
├── src/
│   ├── api/              # API endpoints
│   │   ├── auth_better.py
│   │   ├── chat.py
│   │   └── user_data.py
│   ├── models/           # Database models
│   ├── services/         # Business logic
│   │   ├── auth_service.py
│   │   ├── chat_service.py
│   │   ├── openai_service.py
│   │   └── qdrant_service.py
│   ├── database.py       # Database connection
│   └── main.py           # FastAPI app
├── alembic/              # Database migrations
├── scripts/              # Utility scripts
├── requirements.txt      # Python dependencies
└── .env                  # Environment variables (NOT in git)
```

## 🔧 Local Development

### Prerequisites

- Python 3.11+
- PostgreSQL database (or Neon)
- Qdrant instance (or Qdrant Cloud)
- OpenAI API key

### Setup

1. **Clone and install dependencies**
   ```bash
   git clone https://github.com/Nabeerak/hackathon.git
   cd hackathon
   git checkout backend-deploy
   pip install -r requirements.txt
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Run migrations**
   ```bash
   alembic upgrade head
   ```

4. **Start server**
   ```bash
   uvicorn src.main:app --reload
   ```

5. **Access API**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - Health: http://localhost:8000/api/health

## 📖 API Documentation

Once deployed, visit `/docs` for interactive API documentation.

### Main Endpoints

- `GET /api/health` - Health check
- `POST /api/auth/sign-up/email` - User registration
- `POST /api/auth/sign-in/email` - User login
- `POST /api/chat` - Send chat message
- `GET /api/conversations` - Get user conversations
- `GET /api/user/profile` - Get user profile

## 🔐 Security

- JWT-based authentication
- Session management with Better-auth
- CORS configuration for frontend domains
- Environment variables for secrets
- SQL injection protection via SQLAlchemy
- Rate limiting (configurable)

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/
```

## 📝 Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `NEON_DATABASE_URL` | PostgreSQL connection string | ✅ |
| `JWT_SECRET_KEY` | JWT token secret (32+ chars) | ✅ |
| `BETTER_AUTH_SECRET` | Better-auth session secret | ✅ |
| `QDRANT_URL` | Qdrant cloud URL | ✅ |
| `QDRANT_API_KEY` | Qdrant API key | ✅ |
| `OPENAI_API_KEY` | OpenAI API key | ✅ |
| `CORS_ORIGINS` | Comma-separated allowed origins | ✅ |
| `ENVIRONMENT` | `production` or `development` | ✅ |
| `HOST` | Server host (use `0.0.0.0`) | ✅ |
| `PORT` | Server port (Render provides this) | ❌ |

## 🚨 Troubleshooting

### Database Connection Issues
- Verify `NEON_DATABASE_URL` is correct
- Check if database is accessible
- Run migrations: `alembic upgrade head`

### CORS Errors
- Add your frontend URL to `CORS_ORIGINS`
- Format: `https://your-app.vercel.app,http://localhost:3000`

### Authentication Issues
- Check `JWT_SECRET_KEY` and `BETTER_AUTH_SECRET` are set
- Verify secrets match across deployments

## 📞 Support

For issues or questions:
- GitHub Issues: https://github.com/Nabeerak/hackathon/issues
- Documentation: See `/docs` endpoint when server is running

## 📜 License

Copyright © 2024 Panaversity. All rights reserved.
