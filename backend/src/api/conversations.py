import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
import html

from backend.src.database import get_db
from backend.src.models.models import Conversation, Message, User

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int

class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    timestamp: datetime

class ConversationDetailResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse]

class CreateConversationRequest(BaseModel):
    title: Optional[str] = None

    @validator('title', pre=True)
    def validate_title(cls, v):
        if v is not None:
            if len(v) > 100:  # Max length check
                raise ValueError('Title too long')
            # Sanitize the title
            v = html.escape(v)
        return v

@router.get("/conversations", response_model=List[ConversationResponse])
def list_conversations(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """List all conversations with pagination."""
    try:
        logger.info(f"Listing conversations with skip={skip}, limit={limit}")

        # Validate inputs
        if skip < 0:
            raise HTTPException(status_code=400, detail="Skip parameter must be non-negative")
        if limit <= 0 or limit > 100:  # Limit max limit to prevent abuse
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")

        conversations = db.query(Conversation).order_by(
            Conversation.last_updated_timestamp.desc()
        ).offset(skip).limit(limit).all()

        result = [
            ConversationResponse(
                id=str(conv.id),
                title=conv.title,
                created_at=conv.creation_timestamp,
                updated_at=conv.last_updated_timestamp,
                message_count=conv.message_count
            )
            for conv in conversations
        ]

        logger.info(f"Returned {len(result)} conversations")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing conversations: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/conversations", response_model=ConversationResponse)
def create_conversation(
    request: CreateConversationRequest,
    db: Session = Depends(get_db)
):
    """Create a new conversation."""
    try:
        logger.info("Creating new conversation")

        # Get or create default user
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
            title=request.title or "New Conversation",
            message_count=0
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        logger.info(f"Created conversation with ID: {conversation.id}")
        return ConversationResponse(
            id=str(conversation.id),
            title=conversation.title,
            created_at=conversation.creation_timestamp,
            updated_at=conversation.last_updated_timestamp,
            message_count=conversation.message_count
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating conversation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/conversations/{conversation_id}", response_model=ConversationDetailResponse)
def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific conversation with all its messages."""
    try:
        logger.info(f"Retrieving conversation: {conversation_id}")

        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp.asc()).all()

        result = ConversationDetailResponse(
            id=str(conversation.id),
            title=conversation.title,
            created_at=conversation.creation_timestamp,
            updated_at=conversation.last_updated_timestamp,
            messages=[
                MessageResponse(
                    id=str(msg.id),
                    role=msg.role,
                    content=msg.content_text,
                    timestamp=msg.timestamp
                )
                for msg in messages
            ]
        )

        logger.info(f"Retrieved conversation {conversation_id} with {len(messages)} messages")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving conversation {conversation_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """Delete a specific conversation."""
    try:
        logger.info(f"Deleting conversation: {conversation_id}")

        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Delete associated messages first (due to foreign key constraints)
        db.query(Message).filter(Message.conversation_id == conversation_id).delete()

        # Then delete the conversation
        db.delete(conversation)
        db.commit()

        logger.info(f"Deleted conversation {conversation_id}")
        return {"message": "Conversation deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting conversation {conversation_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Add search functionality for conversation history
@router.get("/conversations/search")
def search_conversations(
    query: str = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Search conversations by keyword in messages."""
    try:
        logger.info(f"Searching conversations with query: {query}")

        if not query or len(query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query parameter is required")

        # Sanitize the query
        query = html.escape(query.strip())

        # Validate inputs
        if skip < 0:
            raise HTTPException(status_code=400, detail="Skip parameter must be non-negative")
        if limit <= 0 or limit > 100:  # Limit max limit to prevent abuse
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")

        # Search through message content for the query term
        matching_messages = db.query(Message).filter(
            Message.content_text.ilike(f"%{query}%")
        ).all()

        # Get unique conversation IDs that contain the query
        conversation_ids = list(set(msg.conversation_id for msg in matching_messages))

        # Get the conversations
        conversations = db.query(Conversation).filter(
            Conversation.id.in_(conversation_ids)
        ).order_by(Conversation.last_updated_timestamp.desc()).offset(skip).limit(limit).all()

        result = [
            ConversationResponse(
                id=str(conv.id),
                title=conv.title,
                created_at=conv.creation_timestamp,
                updated_at=conv.last_updated_timestamp,
                message_count=conv.message_count
            )
            for conv in conversations
        ]

        logger.info(f"Found {len(result)} conversations matching query: {query}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching conversations: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Add export functionality for conversation
@router.get("/conversations/{conversation_id}/export")
def export_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """Export a conversation in JSON format."""
    try:
        logger.info(f"Exporting conversation: {conversation_id}")

        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp.asc()).all()

        # Format as JSON
        conversation_data = {
            "id": str(conversation.id),
            "title": conversation.title,
            "created_at": conversation.creation_timestamp.isoformat(),
            "updated_at": conversation.last_updated_timestamp.isoformat(),
            "message_count": conversation.message_count,
            "messages": [
                {
                    "id": str(msg.id),
                    "role": msg.role,
                    "content": msg.content_text,
                    "timestamp": msg.timestamp.isoformat()
                }
                for msg in messages
            ]
        }

        from fastapi.responses import JSONResponse
        response = JSONResponse(
            content=conversation_data,
            headers={
                "Content-Disposition": f"attachment; filename=conversation_{conversation_id}.json"
            }
        )

        logger.info(f"Exported conversation {conversation_id} with {len(messages)} messages")
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting conversation {conversation_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")