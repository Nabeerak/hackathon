import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, field_validator
from pydantic import ValidationError
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from slowapi import Limiter
from slowapi.util import get_remote_address
import time
import html

from src.services.chat_service import ChatService
from src.database import get_db
from src.models.models import User, Conversation, Message

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str
    selected_text: Optional[str] = None

    @field_validator('message')
    def validate_message(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Message cannot be empty')
        if len(v) > 2000:  # Max length check
            raise ValueError('Message too long')
        # Sanitize the message
        v = html.escape(v)
        return v

    @field_validator('selected_text', mode='before')
    def validate_selected_text(cls, v):
        if v is not None:
            if len(v) > 2000:  # Max length check
                raise ValueError('Selected text too long')
            # Sanitize the selected text
            v = html.escape(v)
        return v

class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    sources: list[str]
    timestamp: str
    processing_time: float
    metadata: dict = {}

@router.post("/chat", response_model=ChatResponse)
@limiter.limit("30/minute")
async def chat_endpoint(
    request_data: ChatRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Send a message to the chatbot and get a response."""
    start_time = time.time()
    client_ip = request.client.host if request.client else "unknown"

    logger.info(f"Chat request from {client_ip} for conversation {request_data.conversation_id}")

    try:
        # Initialize ChatService
        chat_service = ChatService()

        # Get or create conversation
        conversation = None
        if request_data.conversation_id:
            conversation = db.query(Conversation).filter(
                Conversation.id == request_data.conversation_id
            ).first()
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            # Create new conversation with default user
            user = db.query(User).first()
            if not user:
                user = User(
                    account_creation_timestamp=datetime.utcnow(),
                    total_interaction_count=0,
                    preferences={}
                )
                db.add(user)
                db.commit()
                db.refresh(user)

            conversation = Conversation(
                user_id=user.id,
                creation_timestamp=datetime.utcnow(),
                last_updated_timestamp=datetime.utcnow(),
                title=request_data.message[:50],
                message_count=0
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)

        # Save user message
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content_text=request_data.message,
            timestamp=datetime.utcnow(),
            token_count_used=0,
            processing_latency=0.0
        )
        db.add(user_message)

        # Get RAG response
        if request_data.selected_text:
            response_content, sources = chat_service.get_rag_response_with_selection(
                request_data.message,
                request_data.selected_text
            )
        else:
            response_content, sources = chat_service.get_rag_response(request_data.message)

        # Save assistant message
        processing_time = time.time() - start_time
        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content_text=response_content,
            timestamp=datetime.utcnow(),
            token_count_used=0,
            processing_latency=processing_time
        )
        db.add(assistant_message)

        # Update conversation
        conversation.last_updated_timestamp = datetime.utcnow()
        conversation.message_count += 2
        db.commit()

        # Prepare metadata
        metadata = {
            "processing_time": processing_time,
            "sources_count": len(sources),
            "timestamp": datetime.utcnow().isoformat(),
            "client_ip": client_ip
        }

        logger.info(f"Chat response generated successfully in {processing_time:.2f}s for conversation {conversation.id}")

        return ChatResponse(
            message=response_content,
            conversation_id=str(conversation.id),
            sources=sources,
            timestamp=datetime.utcnow().isoformat(),
            processing_time=processing_time,
            metadata=metadata
        )
    except ValidationError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(status_code=400, detail=f"Validation error: {str(ve)}")
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
