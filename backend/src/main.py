from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .router import chat_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)

@app.get("/")
async def read_root():
    return {"message": "Chatbot backend is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
