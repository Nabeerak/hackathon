from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List, Dict, Any
from openai import OpenAI
from .llm_factory import get_llm_client
from .qdrant_client import get_qdrant_client, search_qdrant

chat_router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    conversation_id: str | None = None
    message: str
    selected_text: str | None = None
    history: List[Message] = []

class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    sources: List[str] | None = None
    timestamp: str | None = None
    processing_time: float | None = None

@chat_router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    llm_client = get_llm_client()
    qdrant_client = get_qdrant_client()
    collection_name = "chatbot_collection" # Define your Qdrant collection name

    # Ensure Qdrant collection exists (optional, could be done on startup)
    # from .qdrant_client import ensure_collection_exists # Temporary import for this example
    # ensure_collection_exists(qdrant_client, collection_name)

    # 1. Retrieve relevant context from Qdrant
    retrieved_docs = search_qdrant(qdrant_client, collection_name, request.message)
    retrieved_sources = [doc["payload"]["source"] for doc in retrieved_docs if "source" in doc["payload"]]

    # Add retrieved context to the message history for the LLM
    context_messages = []
    if retrieved_sources:
        context_content = "\n\nRelevant context:\n" + "\n".join(retrieved_sources)
        context_messages.append({"role": "system", "content": context_content})

    # 2. Construct the conversation history for OpenAI
    messages_for_openai = []
    messages_for_openai.extend(context_messages)
    if request.history:
        messages_for_openai.extend(request.history)
    messages_for_openai.append({"role": "user", "content": request.message})

    # 3. Call OpenAI Chat Completions API
    try:
        completion = llm_client.chat.completions.create(
            model="gpt-3.5-turbo", # Or another appropriate model
            messages=messages_for_openai
        )
        assistant_message = completion.choices[0].message.content
    except Exception as e:
        # Basic error handling
        print(f"OpenAI API error: {e}")
        assistant_message = "Sorry, I'm having trouble connecting to the AI. Please try again later."

    return ChatResponse(
        message=assistant_message,
        conversation_id=request.conversation_id or "new-conversation", # Generate or use existing ID
        sources=retrieved_sources,
        timestamp="", # Populate with actual timestamp
        processing_time=0.0 # Populate with actual processing time
    )
