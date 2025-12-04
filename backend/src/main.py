from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .api.chat import router as chat_router
from .api.auth_better import router as auth_router  # Better-auth compatible router

app = FastAPI(
    title="Book-Embedded RAG Chatbot API",
    description="RAG chatbot for 'Physical AI & Humanoid Robotics' book with better-auth integration",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://nabeerak.github.io/hackathon/",
        "https://nabeerak.github.io",  # GitHub Pages production URL
    ],
    allow_credentials=True,  # Required for cookies
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Set-Cookie"],  # Required for better-auth cookies
)

# Include API routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(chat_router, prefix="/api", tags=["chat"])

@app.get("/")
async def read_root():
    return {
        "message": "Book-Embedded RAG Chatbot API",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/favicon.ico")
async def favicon():
    return {"message": "No favicon"}

@app.get("/.well-known/appspecific/com.chrome.devtools.json")
async def devtools():
    return {"message": "Not available"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
