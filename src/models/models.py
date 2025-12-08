from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    image = Column(String(500), nullable=True)  # User profile image URL

    # Profile fields for personalization
    software_background = Column(Text, nullable=True)  # User's software experience (Python, JavaScript, etc.)
    hardware_background = Column(Text, nullable=True)  # User's hardware experience (Arduino, Raspberry Pi, etc.)
    learning_goals = Column(Text, nullable=True)  # What they want to learn
    experience_level = Column(String(50), nullable=True)  # beginner, intermediate, advanced

    # Preferences
    personalization_enabled = Column(Boolean, default=True)
    preferred_language = Column(String(10), default='en')  # 'en' or 'ur' for Urdu

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")

class Session(Base):
    """User session for better-auth compatibility"""
    __tablename__ = "sessions"

    id = Column(String(255), primary_key=True, index=True)  # Session token
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    user_agent = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="sessions")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String(50), nullable=False)  # 'user', 'assistant', 'system'
    content = Column(Text, nullable=False)
    selected_text = Column(Text, nullable=True)
    sources = Column(Text, nullable=True)  # JSON string of source references
    processing_time = Column(Integer, nullable=True)  # milliseconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    conversation = relationship("Conversation", back_populates="messages")

class ReadingProgress(Base):
    __tablename__ = "reading_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    page_path = Column(String(500), nullable=False)  # e.g., /docs/ros2/basics
    progress_percentage = Column(Integer, default=0)  # 0-100
    last_position = Column(String(100), nullable=True)  # Section/heading ID
    completed = Column(Boolean, default=False)
    time_spent_seconds = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", backref="reading_progress")

class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    page_path = Column(String(500), nullable=False)
    page_title = Column(String(500), nullable=False)
    section = Column(String(500), nullable=True)  # Specific section/heading
    note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="bookmarks")

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    page_path = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    highlighted_text = Column(Text, nullable=True)
    position = Column(String(100), nullable=True)  # Section/paragraph ID
    color = Column(String(20), default='yellow')  # Highlight color
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", backref="notes")
