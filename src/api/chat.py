from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional, AsyncGenerator
from datetime import datetime, timezone
from ..services.chat_service import ChatService
from ..database import get_db
from ..models.models import User, Conversation, Message, Session as DBSession
from sqlalchemy.orm import Session
import json
import asyncio
import logging

logger = logging.getLogger(__name__)

class ConversationBase(BaseModel):
    id: int
    user_id: int
    title: Optional[str]
    created_at: datetime
    updated_at: datetime

class MessageBase(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    selected_text: Optional[str]
    sources: Optional[str]
    processing_time: Optional[int]
    created_at: datetime

class ConversationDetailResponse(ConversationBase):
    messages: List[MessageBase] = []

class CreateConversationRequest(BaseModel):
    title: Optional[str] = None
    user_id: Optional[int] = Field(1, description="User ID (default 1 for demo)")

class SearchResponseItem(BaseModel):
    id: str
    content: str
    source: str
    score: float

class SearchResponse(BaseModel):
    results: List[SearchResponseItem]
    total: int


router = APIRouter()

# Initialize ChatService
chat_service = ChatService()

def get_user_from_session(request: Request, db: Session) -> Optional[User]:
    """
    Helper to get user from session cookie or Authorization Bearer token

    Supports two authentication methods:
    1. Authorization: Bearer <token> header (recommended for cross-domain)
    2. better-auth.session_token cookie (for same-domain)
    """
    session_token = None

    # Try to get token from Authorization header first (for cross-domain requests)
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        session_token = auth_header.replace("Bearer ", "").strip()
        logger.debug(f"Auth: Using Bearer token from Authorization header")

    # Fallback to cookie-based auth (for same-domain requests)
    if not session_token:
        session_token = request.cookies.get("better-auth.session_token")
        if session_token:
            logger.debug(f"Auth: Using session token from cookie")

    if not session_token:
        logger.debug("Auth: No session token found in header or cookie")
        return None

    # Validate session token
    session = db.query(DBSession).filter(DBSession.id == session_token).first()
    if not session:
        logger.debug(f"Auth: Session not found for token")
        return None

    if session.expires_at < datetime.now(timezone.utc):
        logger.debug(f"Auth: Session expired for user {session.user_id}")
        return None

    user = db.query(User).filter(User.id == session.user_id).first()
    if user:
        logger.debug(f"Auth: Successfully authenticated user {user.id}")
    else:
        logger.debug(f"Auth: User not found for session")

    return user

@router.get("/conversations", response_model=List[ConversationBase])
async def get_conversations(request: Request, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    user = get_user_from_session(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    conversations = db.query(Conversation).filter(
        Conversation.user_id == user.id
    ).order_by(Conversation.updated_at.desc()).offset(skip).limit(limit).all()
    return conversations

@router.get("/conversations/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(conversation_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_user_from_session(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user.id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.post("/conversations", response_model=ConversationBase)
async def create_conversation_endpoint(request: CreateConversationRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        user = User(id=request.user_id, username=f"user_{request.user_id}")
        db.add(user)
        db.commit()
        db.refresh(user)

    conversation = Conversation(
        user_id=user.id,
        title=request.title
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

@router.delete("/conversations/{conversation_id}")
async def delete_conversation_endpoint(conversation_id: int, request: Request, db: Session = Depends(get_db)):
    print(f"[DEBUG] DELETE /api/conversations/{conversation_id} endpoint hit.")
    user = get_user_from_session(request, db)
    if not user:
        print("[DEBUG] User not authenticated for conversation deletion.")
        raise HTTPException(status_code=401, detail="Not authenticated")
    print(f"[DEBUG] Authenticated user ID: {user.id}")
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user.id
    ).first()
    if not conversation:
        print(f"[DEBUG] Conversation {conversation_id} not found for user {user.id}.")
        raise HTTPException(status_code=404, detail="Conversation not found")
    print(f"[DEBUG] Deleting conversation {conversation_id} for user {user.id}.")
    db.delete(conversation)
    db.commit()
    print(f"[DEBUG] Conversation {conversation_id} deleted successfully.")
    return {"message": "Conversation deleted successfully"}

@router.get("/conversations/search", response_model=List[ConversationBase])
async def search_conversations_endpoint(query: str, user_id: int = 1, db: Session = Depends(get_db)):
    conversations = db.query(Conversation).filter(
        Conversation.user_id == user_id,
        Conversation.title.ilike(f"%{query}%")
    ).all()
    return conversations

@router.get("/conversations/{conversation_id}/export", response_model=ConversationDetailResponse)
async def export_conversation_endpoint(conversation_id: int, user_id: int = 1, db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.get("/search", response_model=SearchResponse)
async def search_endpoint(query: str, limit: int = 10):
    """
    Search endpoint for retrieving relevant book content based on a query.
    """
    try:
        results = chat_service.retrieve_context(question=query, limit=limit)

        formatted_results = []
        for res in results:
            content = res["payload"].get("content", "")
            source = res["payload"].get("source", "Unknown")
            formatted_results.append(
                SearchResponseItem(
                    id=str(res.get("id", "no_id")),
                    content=content,
                    source=source,
                    score=res.get("score", 0.0)
                )
            )

        return SearchResponse(results=formatted_results, total=len(formatted_results))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


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
async def chat_endpoint(chat_request: ChatRequest, request: Request, db: Session = Depends(get_db)):
    """
    Main chat endpoint for RAG-based question answering

    - Accepts user questions about the book
    - Optionally accepts selected text for context
    - Maintains conversation history
    - Applies content guardrails
    """
    try:
        # Get authenticated user
        user = get_user_from_session(request, db)
        if not user:
            raise HTTPException(status_code=401, detail="Not authenticated")

        # Get or create conversation
        if chat_request.conversation_id:
            conversation = db.query(Conversation).filter(
                Conversation.id == chat_request.conversation_id,
                Conversation.user_id == user.id
            ).first()
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            # Create new conversation
            conversation = Conversation(
                user_id=user.id,
                title=chat_request.message[:100]  # Use first part of message as title
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
            content=chat_request.message,
            selected_text=chat_request.selected_text
        )
        db.add(user_message)

        # Get response from chat service with user personalization
        result = chat_service.chat(
            question=chat_request.message,
            selected_text=chat_request.selected_text,
            conversation_history=conversation_history,
            user_profile={
                "experience_level": user.experience_level,
                "software_background": user.software_background,
                "hardware_background": user.hardware_background,
                "preferred_language": user.preferred_language,
                "personalization_enabled": user.personalization_enabled
            } if user.personalization_enabled else None
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
            timestamp=datetime.now(timezone.utc).isoformat(),
            processing_time=result["processing_time"],
            off_topic=result.get("off_topic", False)
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/chat/stream")
async def chat_stream_endpoint(chat_request: ChatRequest, request: Request, db: Session = Depends(get_db)):
    """
    Streaming chat endpoint for real-time responses (Server-Sent Events)
    Provides lower perceived latency by streaming response tokens as they're generated
    """

    async def generate_stream() -> AsyncGenerator[str, None]:
        try:
            # Get authenticated user
            user = get_user_from_session(request, db)
            if not user:
                yield f"data: {json.dumps({'error': 'Not authenticated'})}\n\n"
                return

            # Get or create conversation
            if chat_request.conversation_id:
                conversation = db.query(Conversation).filter(
                    Conversation.id == chat_request.conversation_id,
                    Conversation.user_id == user.id
                ).first()
                if not conversation:
                    yield f"data: {json.dumps({'error': 'Conversation not found'})}\n\n"
                    return
            else:
                conversation = Conversation(
                    user_id=user.id,
                    title=chat_request.message[:100]
                )
                db.add(conversation)
                db.commit()
                db.refresh(conversation)

            # Send conversation_id first
            yield f"data: {json.dumps({'type': 'conversation_id', 'conversation_id': conversation.id})}\n\n"

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
                content=chat_request.message,
                selected_text=chat_request.selected_text
            )
            db.add(user_message)
            db.commit()

            # Get response from chat service
            result = chat_service.chat(
                question=chat_request.message,
                selected_text=chat_request.selected_text,
                conversation_history=conversation_history,
                user_profile={
                    "experience_level": user.experience_level,
                    "software_background": user.software_background,
                    "hardware_background": user.hardware_background,
                    "preferred_language": user.preferred_language,
                    "personalization_enabled": user.personalization_enabled
                } if user.personalization_enabled else None
            )

            # Stream response in chunks
            response_text = result["response"]
            chunk_size = 20  # Stream 20 characters at a time for smooth output

            for i in range(0, len(response_text), chunk_size):
                chunk = response_text[i:i + chunk_size]
                yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"
                await asyncio.sleep(0.01)  # Small delay for smooth streaming

            # Send sources and metadata
            yield f"data: {json.dumps({'type': 'sources', 'sources': result['sources']})}\n\n"
            yield f"data: {json.dumps({'type': 'metadata', 'processing_time': result['processing_time'], 'off_topic': result.get('off_topic', False)})}\n\n"

            # Save assistant message
            assistant_message = Message(
                conversation_id=conversation.id,
                role="assistant",
                content=response_text,
                sources=json.dumps(result["sources"]),
                processing_time=result["processing_time"]
            )
            db.add(assistant_message)
            db.commit()

            # End stream
            yield f"data: {json.dumps({'type': 'done'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "chatbot"}
