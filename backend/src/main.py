from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from api import chat
from api import conversations
from api import search
from database import engine
from models import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["30/minute"])

# Create FastAPI app
app = FastAPI(title="Chatbot API", version="1.0.0")

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Docusaurus default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(conversations.router, prefix="/api", tags=["conversations"])
app.include_router(search.router, prefix="/api", tags=["search"])

@app.get("/")
async def root():
    return {"message": "Chatbot API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
