from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from backend.src.models.models import Conversation, Message, User

class ConversationService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_conversations(self, user_id: int, skip: int = 0, limit: int = 20) -> List[Conversation]:
        """Get all conversations for a user with pagination."""
        return self.db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(
            Conversation.last_updated_timestamp.desc()
        ).offset(skip).limit(limit).all()

    def get_conversation_by_id(self, conversation_id: str) -> Optional[Conversation]:
        """Get a specific conversation by ID."""
        return self.db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()

    def get_conversation_messages(self, conversation_id: str) -> List[Message]:
        """Get all messages for a specific conversation."""
        return self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp.asc()).all()

    def create_conversation(self, user_id: int, title: str = "New Conversation") -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(
            user_id=user_id,
            creation_timestamp=datetime.utcnow(),
            last_updated_timestamp=datetime.utcnow(),
            title=title,
            message_count=0
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def update_conversation_title(self, conversation_id: str, title: str):
        """Update conversation title."""
        conversation = self.get_conversation_by_id(conversation_id)
        if conversation:
            conversation.title = title
            conversation.last_updated_timestamp = datetime.utcnow()
            self.db.commit()

    def update_conversation_message_count(self, conversation_id: str):
        """Update message count for a conversation."""
        conversation = self.get_conversation_by_id(conversation_id)
        if conversation:
            message_count = self.db.query(Message).filter(
                Message.conversation_id == conversation_id
            ).count()
            conversation.message_count = message_count
            conversation.last_updated_timestamp = datetime.utcnow()
            self.db.commit()

    def delete_conversation(self, conversation_id: str):
        """Delete a conversation and its messages."""
        # Delete associated messages first
        self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).delete()
        
        # Then delete the conversation
        self.db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).delete()
        
        self.db.commit()

    def search_conversations(self, user_id: int, query: str, skip: int = 0, limit: int = 20) -> List[Conversation]:
        """Search conversations by keyword in messages."""
        # Find messages containing the query
        matching_messages = self.db.query(Message).filter(
            Message.content_text.ilike(f"%{query}%")
        ).all()
        
        # Get unique conversation IDs
        conversation_ids = list(set(msg.conversation_id for msg in matching_messages))
        
        # Get conversations for those IDs
        return self.db.query(Conversation).filter(
            Conversation.id.in_(conversation_ids),
            Conversation.user_id == user_id
        ).order_by(Conversation.last_updated_timestamp.desc()).offset(skip).limit(limit).all()

    def get_all_users_conversations(self, skip: int = 0, limit: int = 20) -> List[Conversation]:
        """Get all conversations from all users, ordered by last updated."""
        return self.db.query(Conversation).order_by(
            Conversation.last_updated_timestamp.desc()
        ).offset(skip).limit(limit).all()