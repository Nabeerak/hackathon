from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.sql import func
import os

DATABASE_URL = os.getenv("NEON_DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    account_creation_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    total_interaction_count = Column(Integer, default=0)
    preferences = Column(Text, nullable=True) # Storing as JSON string

    conversations = relationship("Conversation", back_populates="owner")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    creation_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    last_updated_timestamp = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    title = Column(String, nullable=True)
    message_count = Column(Integer, default=0)

    owner = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation_rel")

class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, index=True)
    conversation_id = Column(String, ForeignKey("conversations.id"))
    role = Column(String)
    content_text = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    token_count_used = Column(Integer, nullable=True)
    processing_latency = Column(Integer, nullable=True) # in milliseconds

    conversation_rel = relationship("Conversation", back_populates="messages")
