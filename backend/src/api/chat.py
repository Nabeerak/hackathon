from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from ..services.chat_service import ChatService
from ..database import get_db
from ..models.models import User, Conversation, Message
from sqlalchemy.orm import Session
import json

router = APIRouter()

# Initialize ChatService
chat_service = ChatService()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str = Field(..., description="User's question")
    selected_text: Optional[str] = Field(None, description="Optional selected text for context")
    conversation_id: Optional[int] = Field(None, description="Optional conversation ID to continue")
    user_id: Optional[int] = Field(1, description="User ID (default 1 for demo)")

class ChatResponse(BaseModel):
    message: str
    conversation_id: int
    sources: List[str]
    timestamp: str
    processing_time: int
    off_topic: bool = False

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Main chat endpoint for RAG-based question answering

    - Accepts user questions about the book
    - Optionally accepts selected text for context
    - Maintains conversation history
    - Applies content guardrails
    """
    try:
        # Get or create user
        user = db.query(User).filter(User.id == request.user_id).first()
        if not user:
            user = User(id=request.user_id, username=f"user_{request.user_id}")
            db.add(user)
            db.commit()
            db.refresh(user)

        # Get or create conversation
        if request.conversation_id:
            conversation = db.query(Conversation).filter(
                Conversation.id == request.conversation_id,
                Conversation.user_id == user.id
            ).first()
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            # Create new conversation
            conversation = Conversation(
                user_id=user.id,
                title=request.message[:100]  # Use first part of message as title
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)

        # Get conversation history
        messages = db.query(Message).filter(
            Message.conversation_id == conversation.id
        ).order_by(Message.created_at).all()

        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

        # Save user message
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=request.message,
            selected_text=request.selected_text
        )
        db.add(user_message)

        # Get response from chat service
        result = chat_service.chat(
            question=request.message,
            selected_text=request.selected_text,
            conversation_history=conversation_history
        )

        # Save assistant message
        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=result["response"],
            sources=json.dumps(result["sources"]),
            processing_time=result["processing_time"]
        )
        db.add(assistant_message)
        db.commit()

        # Return response
        return ChatResponse(
            message=result["response"],
            conversation_id=conversation.id,
            sources=result["sources"],
            timestamp=datetime.utcnow().isoformat(),
            processing_time=result["processing_time"],
            off_topic=result.get("off_topic", False)
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "chatbot"}
