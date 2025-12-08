from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import uvicorn
import logging
from sqlalchemy import text

from .api.chat import router as chat_router
from .api.auth_better import router as auth_router  # Better-auth compatible router
from .api.user_data import router as user_data_router
from .database import engine, Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize backend services on startup"""
    logger.info("Starting backend initialization...")

    try:
        # Create database tables if they don't exist
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")

        # Test database connection
        logger.info("Testing database connection...")
        from .database import SessionLocal
        db = SessionLocal()
        try:
            db.execute(text("SELECT 1"))
            logger.info("Database connection verified")
        finally:
            db.close()

        # Verify Qdrant connection (optional - will not fail startup)
        try:
            logger.info("Verifying Qdrant connection...")
            from .services.qdrant_service import qdrant_client
            if qdrant_client.is_connected():
                client = qdrant_client.get_client()
                collections = client.get_collections()
                logger.info(f"Qdrant connection verified. Collections: {len(collections.collections)}")
            else:
                logger.warning("Qdrant is not connected - vector search features will be unavailable")
        except Exception as e:
            logger.warning(f"Qdrant verification failed (non-critical): {e}")

        logger.info("Backend initialization completed successfully")

    except Exception as e:
        logger.error(f"Backend initialization failed: {e}")
        raise

    yield

    # Cleanup on shutdown
    logger.info("Shutting down backend...")

app = FastAPI(
    title="Book-Embedded RAG Chatbot API",
    description="RAG chatbot for 'Physical AI & Humanoid Robotics' book with better-auth integration",
    version="2.0.0",
    lifespan=lifespan
)

# Add GZIP compression for responses > 1000 bytes
app.add_middleware(GZIPMiddleware, minimum_size=1000)

# CORS with optimized settings for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://nabeerak.github.io/hackathon/",
        "https://nabeerak.github.io",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Set-Cookie"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Include API routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(user_data_router, prefix="/api/user", tags=["user-data"])

@app.get("/")
async def read_root():
    return {
        "message": "Book-Embedded RAG Chatbot API",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint for frontend initialization"""
    from .database import SessionLocal

    health_status = {
        "status": "healthy",
        "services": {}
    }

    # Check database
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        health_status["services"]["database"] = "connected"
    except Exception as e:
        health_status["services"]["database"] = f"error: {str(e)}"
        health_status["status"] = "degraded"

    # Check Qdrant (optional)
    try:
        from .services.qdrant_service import qdrant_client
        if qdrant_client.is_connected():
            client = qdrant_client.get_client()
            collections = client.get_collections()
            health_status["services"]["qdrant"] = f"connected ({len(collections.collections)} collections)"
        else:
            health_status["services"]["qdrant"] = "not connected"
    except Exception as e:
        health_status["services"]["qdrant"] = f"unavailable: {str(e)}"
        # Don't mark as degraded for Qdrant issues

    return health_status

@app.get("/favicon.ico")
async def favicon():
    return {"message": "No favicon"}

@app.get("/.well-known/appspecific/com.chrome.devtools.json")
async def devtools():
    return {"message": "Not available"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
