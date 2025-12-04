from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from ..services.chat_service import ChatService
from ..database import get_db
from ..models.models import User, Conversation, Message, Session as DBSession
from sqlalchemy.orm import Session
import json
from datetime import datetime

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
    """Helper to get user from session cookie"""
    session_token = request.cookies.get("better-auth.session_token")
    if not session_token:
        return None

    session = db.query(DBSession).filter(DBSession.id == session_token).first()
    if not session or session.expires_at < datetime.utcnow():
        return None

    return db.query(User).filter(User.id == session.user_id).first()

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
async def delete_conversation_endpoint(conversation_id: int, user_id: int = 1, db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    db.delete(conversation)
    db.commit()
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
