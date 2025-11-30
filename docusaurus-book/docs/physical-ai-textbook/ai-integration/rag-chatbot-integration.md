---
title: RAG Chatbot Integration
sidebar_label: RAG Chatbot Integration
sidebar_position: 1
description: Building intelligent chatbots with Retrieval-Augmented Generation for Physical AI
keywords: [RAG, chatbot, OpenAI, FastAPI, Neon, Qdrant, retrieval-augmented generation]
---

# RAG Chatbot Integration

## Introduction

This chapter covers building an intelligent chatbot with Retrieval-Augmented Generation (RAG) that can answer questions about your Physical AI & Humanoid Robotics textbook content. The chatbot uses OpenAI's language models, FastAPI for the backend, Neon Serverless PostgreSQL for storage, and Qdrant for vector search.

## What is RAG?

Retrieval-Augmented Generation (RAG) enhances language models by:
- **Retrieving** relevant context from your textbook content
- **Augmenting** the query with this context
- **Generating** accurate responses based on both the context and the model's knowledge

### Benefits for Physical AI Education

- **Contextual answers**: Students get responses specific to textbook content
- **Up-to-date responses**: Chatbot knows about your course materials
- **Citation capability**: Can reference specific chapters, sections
- **Personalized learning**: Can adapt to user's background and progress

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │───▶│   FastAPI        │───▶│   OpenAI        │
│   (Docusaurus)  │    │   Backend        │    │   LLM API       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Vector Store    │
                    │   (Qdrant)       │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Database        │
                    │  (Neon Postgres) │
                    └──────────────────┘
```

## Technology Stack

### OpenAI API
- **Purpose**: Language model for generating responses
- **Model**: GPT-4 Turbo for best performance
- **Features**: Context understanding, code generation, explanation

### FastAPI
- **Purpose**: Backend API server
- **Features**: 
  - Async request handling
  - Automatic API documentation
  - Built-in validation
  - High performance

### Neon Serverless Postgres
- **Purpose**: Store user data, authentication, conversations
- **Features**:
  - Serverless scaling
  - Branching for development
  - PostgreSQL compatibility
  - Connection pooling

### Qdrant Vector Database
- **Purpose**: Store and search vector embeddings of textbook content
- **Features**:
  - High-performance similarity search
  - Filtering capabilities
  - REST/GRPC APIs
  - Local and cloud options

## Setting Up the Backend

### Project Structure

```bash
rag-chatbot/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User models
│   │   └── chat.py          # Chat models
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py          # Pydantic schemas
│   │   └── chat.py          # Chat schemas
│   ├── database/
│   │   ├── __init__.py
│   │   ├── database.py      # Database connection
│   │   └── models.py        # ORM models
│   ├── vector_store/
│   │   ├── __init__.py
│   │   ├── qdrant_client.py # Vector store operations
│   │   └── embeddings.py    # Text embedding functions
│   ├── services/
│   │   ├── __init__.py
│   │   ├── rag_service.py   # Core RAG logic
│   │   ├── chat_service.py  # Chat conversation logic
│   │   └── auth_service.py  # Authentication logic
│   └── utils/
│       └── text_splitter.py # Text processing utilities
├── requirements.txt
└── alembic/
    ├── env.py
    ├── script.py.mako
    └── versions/
```

### Requirements File

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
openai==1.3.6
qdrant-client==1.7.0
sqlalchemy==2.0.23
asyncpg==0.29.0
pydantic==2.5.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
tiktoken==0.5.2
aiofiles==23.2.1
cryptography==41.0.8
```

### Environment Configuration

Create `.env` file:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Qdrant Configuration
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_qdrant_api_key_here

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/rag_chatbot

# JWT Configuration
SECRET_KEY=your_super_secret_jwt_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Settings
UPLOAD_DIR=uploads
MAX_CONTENT_SIZE=10485760  # 10MB
```

## FastAPI Application Setup

### Main Application (`app/main.py`)

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import logging

from app.database.database import init_db
from app.routers import chat, auth, documents
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Initializing database...")
    await init_db()
    logger.info("Database initialized")
    
    # Shutdown
    yield
    
    # Any cleanup code can go here
    logger.info("Shutting down...")

app = FastAPI(
    title="Physical AI RAG Chatbot",
    description="Intelligent chatbot for Physical AI & Humanoid Robotics textbook",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])

@app.get("/")
async def root():
    return {"message": "Physical AI RAG Chatbot API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Vector Store Integration (`app/vector_store/qdrant_client.py`)

```python
from typing import List, Dict, Optional
import uuid
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, Batch, Distance, VectorParams, Filter, FieldCondition, Match
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)

class QdrantVectorStore:
    def __init__(self, url: str, api_key: str, collection_name: str = "textbook_content"):
        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection_name = collection_name
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight embedding model
        
        # Ensure collection exists
        self._init_collection()
    
    def _init_collection(self):
        """Initialize the Qdrant collection if it doesn't exist."""
        try:
            collections = self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)
            
            if not collection_exists:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
                )
                logger.info(f"Created collection: {self.collection_name}")
            else:
                logger.info(f"Collection {self.collection_name} already exists")
        except Exception as e:
            logger.error(f"Error initializing collection: {e}")
            raise
    
    def add_text_chunks(self, chunks: List[Dict[str, str]], doc_id: str) -> bool:
        """
        Add text chunks to the vector store.
        
        Args:
            chunks: List of dictionaries with 'text', 'metadata' keys
            doc_id: Document identifier
        
        Returns:
            bool: True if successful
        """
        try:
            # Create embeddings for each chunk
            texts = [chunk['text'] for chunk in chunks]
            embeddings = self.encoder.encode(texts).tolist()
            
            # Prepare points for insertion
            points = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                point_id = str(uuid.uuid4())
                
                # Create payload with text and metadata
                payload = {
                    "text": chunk['text'],
                    "doc_id": doc_id,
                    "chunk_id": i,
                    "metadata": chunk.get('metadata', {}),
                    "source": chunk.get('source', 'unknown')
                }
                
                point = PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=payload
                )
                
                points.append(point)
            
            # Batch insert
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            logger.info(f"Added {len(chunks)} chunks to collection")
            return True
            
        except Exception as e:
            logger.error(f"Error adding chunks to vector store: {e}")
            return False
    
    def search_similar(self, query: str, limit: int = 5, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Search for similar text chunks to the query.
        
        Args:
            query: Query text
            limit: Number of results to return
            filters: Optional filters (e.g., {"source": "chapter_1.md"})
        
        Returns:
            List of similar text chunks with metadata
        """
        try:
            query_embedding = self.encoder.encode(query).tolist()
            
            # Build filter if provided
            qdrant_filter = None
            if filters:
                conditions = []
                for key, value in filters.items():
                    conditions.append(
                        FieldCondition(key=f"metadata.{key}", match=Match(value=value))
                    )
                
                if conditions:
                    qdrant_filter = Filter(must=conditions)
            
            # Search for similar vectors
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                query_filter=qdrant_filter,
                with_payload=True
            )
            
            # Process results
            similar_chunks = []
            for result in results:
                chunk_data = {
                    "id": result.id,
                    "text": result.payload["text"],
                    "doc_id": result.payload["doc_id"],
                    "chunk_id": result.payload["chunk_id"],
                    "metadata": result.payload["metadata"],
                    "score": result.score
                }
                similar_chunks.append(chunk_data)
            
            return similar_chunks
            
        except Exception as e:
            logger.error(f"Error searching vector store: {e}")
            return []

# Global instance - in production, use dependency injection
vector_store = None
```

### RAG Service (`app/services/rag_service.py`)

```python
from typing import List, Dict, Optional
import openai
from app.vector_store.qdrant_client import vector_store
import logging

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self, openai_api_key: str):
        openai.api_key = openai_api_key
        self.vector_store = vector_store
    
    async def get_answer(self, query: str, user_context: Optional[Dict] = None, 
                        max_context_length: int = 3000) -> Dict[str, any]:
        """
        Get answer to query using RAG approach.
        
        Args:
            query: User question
            user_context: User-specific context (profile, progress, etc.)
            max_context_length: Maximum length of context to include
        
        Returns:
            Dict with answer and metadata
        """
        try:
            # Step 1: Search vector store for relevant context
            relevant_chunks = self.vector_store.search_similar(query, limit=5)
            
            if not relevant_chunks:
                # If no relevant chunks found, use general knowledge
                response = await self._get_general_response(query)
                return {
                    "answer": response,
                    "sources": [],
                    "confidence": "low",
                    "method": "general"
                }
            
            # Step 2: Prepare context from retrieved chunks
            context_parts = []
            total_length = 0
            sources = []
            
            for chunk in relevant_chunks:
                chunk_text = chunk["text"]
                
                # Check if adding this chunk would exceed max length
                if total_length + len(chunk_text) > max_context_length:
                    break
                
                context_parts.append(chunk_text)
                total_length += len(chunk_text)
                
                # Track source for citations
                sources.append({
                    "text": chunk_text[:100] + "...",
                    "source": chunk.get("metadata", {}).get("source", "unknown"),
                    "score": chunk["score"]
                })
            
            context = "\n\n".join(context_parts)
            
            # Step 3: Prepare system message with user context
            system_message = self._build_system_message(user_context)
            
            # Step 4: Prepare messages for OpenAI
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
            ]
            
            # Step 5: Call OpenAI API
            response = await openai.ChatCompletion.acreate(
                model="gpt-4-turbo",
                messages=messages,
                temperature=0.3,  # Lower temperature for more consistent answers
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            
            return {
                "answer": answer,
                "sources": sources,
                "confidence": "high" if len(sources) > 0 else "medium",
                "method": "rag"
            }
            
        except Exception as e:
            logger.error(f"Error in RAG service: {e}")
            return {
                "answer": "I encountered an error while processing your question. Please try again.",
                "sources": [],
                "confidence": "error",
                "method": "error"
            }
    
    def _build_system_message(self, user_context: Optional[Dict]) -> str:
        """Build system message with user context."""
        base_system = (
            "You are an AI assistant for the Physical AI & Humanoid Robotics textbook. "
            "Your role is to help students understand concepts related to robotics, "
            "AI, ROS 2, NVIDIA Isaac, vision-language-action models, and humanoid robotics. "
            "Use the provided context to answer questions accurately and in an educational manner. "
            "If the context doesn't contain the answer, say so and offer general knowledge where appropriate."
        )
        
        if user_context:
            background = user_context.get("background", "general")
            experience = user_context.get("experience", "beginner")
            
            context_addition = (
                f"\n\nUser context: This student has a background in {background} "
                f"and is at {experience} level in robotics/AI. "
                f"Adjust your explanations accordingly."
            )
            
            return base_system + context_addition
        
        return base_system
    
    async def _get_general_response(self, query: str) -> str:
        """Get response without specific context when no relevant chunks found."""
        try:
            messages = [
                {
                    "role": "system", 
                    "content": (
                        "You are an AI assistant for Physical AI & Humanoid Robotics education. "
                        "The user's question didn't match any specific textbook content, "
                        "but you can still provide general information about robotics, AI, "
                        "and related topics. Be helpful but acknowledge the limitations."
                    )
                },
                {"role": "user", "content": query}
            ]
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4-turbo",
                messages=messages,
                temperature=0.5,
                max_tokens=300
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error in general response: {e}")
            return "I'm having trouble processing your question right now. Please try rephrasing it."
```

## API Endpoints

### Chat Router (`app/routers/chat.py`)

```python
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from pydantic import BaseModel

from app.services.rag_service import RAGService
from app.core.config import settings
from app.dependencies import get_current_user  # Assuming auth is implemented

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_context: Optional[dict] = None

class ChatResponse(BaseModel):
    answer: str
    sources: list
    confidence: str
    method: str

@router.post("/query", response_model=ChatResponse)
async def chat_query(request: ChatRequest):
    """Process a chat query using RAG."""
    try:
        rag_service = RAGService(settings.OPENAI_API_KEY)
        result = await rag_service.get_answer(
            query=request.message,
            user_context=request.user_context
        )
        
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat query: {str(e)}"
        )

class DocumentUploadRequest(BaseModel):
    content: str
    source: str  # e.g., "ros2-fundamentals/nodes-topics.md"

@router.post("/upload-document")
async def upload_document(request: DocumentUploadRequest, user=Depends(get_current_user)):
    """Upload document content for RAG indexing."""
    try:
        # Process and split the document content
        from app.utils.text_splitter import split_text
        chunks = split_text(request.content, source=request.source)
        
        # Add to vector store
        success = vector_store.add_text_chunks(chunks, doc_id=user.id)
        
        if success:
            return {"message": "Document uploaded and indexed successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to index document"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading document: {str(e)}"
        )
```

## Frontend Integration in Docusaurus

### Creating a Chat Component

Create `docusaurus-book/src/components/ChatbotWidget.jsx`:

```jsx
import React, { useState, useEffect, useRef } from 'react';
import { useColorMode } from '@docusaurus/theme-common';
import styles from './ChatbotWidget.module.css';

const ChatbotWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [userContext, setUserContext] = useState(null);
  const messagesEndRef = useRef(null);
  const { colorMode } = useColorMode();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Load user context from localStorage or auth system
    const storedContext = localStorage.getItem('userContext');
    if (storedContext) {
      setUserContext(JSON.parse(storedContext));
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = { role: 'user', content: input, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/v1/chat/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: input,
          user_context: userContext
        }),
      });

      const data = await response.json();
      
      const botMessage = {
        role: 'assistant',
        content: data.answer,
        sources: data.sources || [],
        confidence: data.confidence,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your question. Please try again.',
        error: true,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      <button 
        className={`${styles.chatButton} ${isOpen ? styles.open : ''}`}
        onClick={toggleChat}
        aria-label="Open chat"
      >
        💬
      </button>

      {isOpen && (
        <div className={`${styles.chatContainer} ${colorMode === 'dark' ? styles.dark : styles.light}`}>
          <div className={styles.chatHeader}>
            <h3>Physical AI Assistant</h3>
            <button onClick={toggleChat} className={styles.closeButton}>
              ×
            </button>
          </div>
          
          <div className={styles.chatMessages}>
            {messages.length === 0 ? (
              <div className={styles.welcomeMessage}>
                <p>Hello! I'm your Physical AI & Humanoid Robotics assistant.</p>
                <p>Ask me about ROS 2, NVIDIA Isaac, Humanoid Robotics, VLA models, or any topic from the textbook.</p>
              </div>
            ) : (
              messages.map((msg, index) => (
                <div 
                  key={index} 
                  className={`${styles.message} ${styles[msg.role]}`}
                >
                  <div className={styles.messageContent}>
                    {msg.content}
                    {msg.sources && msg.sources.length > 0 && (
                      <div className={styles.sources}>
                        <strong>Sources:</strong>
                        <ul>
                          {msg.sources.slice(0, 3).map((source, idx) => (
                            <li key={idx}>{source.source}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className={`${styles.message} ${styles.assistant}`}>
                <div className={styles.messageContent}>
                  <div className={styles.typingIndicator}>
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleSubmit} className={styles.chatInputForm}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about Physical AI concepts..."
              disabled={isLoading}
              className={styles.chatInput}
            />
            <button 
              type="submit" 
              disabled={isLoading || !input.trim()}
              className={styles.sendButton}
            >
              Send
            </button>
          </form>
        </div>
      )}
    </>
  );
};

export default ChatbotWidget;
```

### Styling the Chat Widget

Create `docusaurus-book/src/components/ChatbotWidget.module.css`:

```css
.chatButton {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: none;
  background-color: #007acc;
  color: white;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  transition: all 0.3s ease;
}

.chatButton:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.chatButton.open {
  transform: scale(0.95);
}

.chatContainer {
  position: fixed;
  bottom: 90px;
  right: 20px;
  width: 380px;
  height: 500px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  z-index: 1000;
  max-height: 80vh;
}

.light {
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
}

.dark {
  background-color: #1a1a1a;
  border: 1px solid #333333;
}

.chatHeader {
  padding: 16px;
  border-bottom: 1px solid;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.light .chatHeader {
  border-bottom-color: #e0e0e0;
  background-color: #f8f9fa;
}

.dark .chatHeader {
  border-bottom-color: #333333;
  background-color: #222222;
}

.chatHeader h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.closeButton {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.light .closeButton {
  color: #666;
}

.dark .closeButton {
  color: #aaa;
}

.chatMessages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.welcomeMessage {
  text-align: center;
  color: #666;
  font-style: italic;
  padding: 20px 0;
}

.message {
  max-width: 85%;
  padding: 12px 16px;
  border-radius: 18px;
  position: relative;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.user {
  align-self: flex-end;
  background-color: #007acc;
  color: white;
  border-bottom-right-radius: 4px;
}

.light .user {
  background-color: #007acc;
}

.dark .user {
  background-color: #005a9e;
}

.assistant {
  align-self: flex-start;
  background-color: #f0f2f5;
  color: #333;
  border-bottom-left-radius: 4px;
}

.light .assistant {
  background-color: #f0f2f5;
}

.dark .assistant {
  background-color: #2d2d2d;
  color: #e0e0e0;
}

.messageContent {
  line-height: 1.5;
}

.sources {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid;
  font-size: 0.85em;
}

.light .sources {
  border-top-color: #ddd;
}

.dark .sources {
  border-top-color: #444;
}

.sources ul {
  margin: 4px 0;
  padding-left: 20px;
}

.sources li {
  margin-bottom: 4px;
}

.typingIndicator {
  display: flex;
  align-items: center;
}

.typingIndicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #666;
  margin: 0 2px;
  animation: bounce 1.4s infinite ease-in-out both;
}

.typingIndicator span:nth-child(1) {
  animation-delay: -0.32s;
}

.typingIndicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

.chatInputForm {
  padding: 16px;
  border-top: 1px solid;
  display: flex;
  gap: 8px;
}

.light .chatInputForm {
  border-top-color: #e0e0e0;
  background-color: #f8f9fa;
}

.dark .chatInputForm {
  border-top-color: #333333;
  background-color: #222222;
}

.chatInput {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid;
  border-radius: 24px;
  outline: none;
  font-size: 14px;
}

.light .chatInput {
  border-color: #ddd;
  background-color: white;
  color: #333;
}

.dark .chatInput {
  border-color: #444;
  background-color: #333;
  color: #e0e0e0;
}

.sendButton {
  padding: 12px 20px;
  border: none;
  border-radius: 20px;
  background-color: #007acc;
  color: white;
  cursor: pointer;
  font-weight: 500;
}

.light .sendButton {
  background-color: #007acc;
}

.dark .sendButton {
  background-color: #005a9e;
}

.sendButton:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Responsive design */
@media (max-width: 480px) {
  .chatContainer {
    width: calc(100vw - 40px);
    height: 50vh;
    bottom: 80px;
    right: 20px;
    left: 20px;
  }
}
```

### Integrating the Chat Widget

To use the chatbot in your Docusaurus site, add it to your layout. For example, in `docusaurus.config.ts`:

```ts
// In the theme config section of docusaurus.config.ts
themeConfig: {
  // ... other config
  navbar: {
    // ... other navbar config
  },
  footer: {
    // ... other footer config
  },
  // Add a custom footer component that includes the chatbot
}
```

And in your main layout file (`src/pages/index.js` or as a layout component):

```jsx
import ChatbotWidget from '@site/src/components/ChatbotWidget';

function LayoutWrapper(props) {
  return (
    <>
      {props.children}
      <ChatbotWidget />
    </>
  );
}
```

## Advanced RAG Features

### Personalized Responses

The RAG system can provide personalized content based on user profiles:

```python
# Example of how to use user context for personalization
user_profile = {
    "background": "computer science",
    "experience": "intermediate",
    "learning_style": "visual_learner",  # visual, auditory, kinesthetic
    "current_chapter": "ros2-fundamentals/nodes-topics",
    "progress": 0.45  # 45% complete
}

# This context is passed to the RAG service to customize responses
```

### Content Selection and Filtering

The system can filter content based on user level and preferences:

```python
# In the RAG service, implement content filtering
def filter_content_by_level(content, user_level):
    """Filter content complexity based on user level."""
    if user_level == "beginner":
        return [item for item in content if item.get("difficulty", "medium") in ["beginner", "medium"]]
    elif user_level == "advanced":
        return content  # Show all content
    else:
        return [item for item in content if item.get("difficulty", "medium") == user_level]
```

## Deployment Configuration

### Docker Setup

Create `Dockerfile` for backend:

```Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose for Development

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - QDRANT_URL=http://qdrant:6333
      - DATABASE_URL=postgresql://user:password@db:5432/rag_chatbot
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
      - qdrant
    volumes:
      - ./uploads:/app/uploads

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: rag_chatbot
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage

volumes:
  postgres_data:
  qdrant_data:
```

## Security Considerations

### API Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# Apply rate limiting to endpoints
@router.post("/query")
@limiter.limit("10/minute")
async def chat_query(request: ChatRequest, request: Request):
    # ... implementation
```

### Input Sanitization

```python
import re

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent injection attacks."""
    # Remove potentially dangerous characters/sequences
    # Only allow alphanumeric, basic punctuation, and spaces
    sanitized = re.sub(r'[<>"\']', '', text)
    return sanitized.strip()

# Use in the API route
@router.post("/query")
async def chat_query(request: ChatRequest):
    request.message = sanitize_input(request.message)
    # ... rest of implementation
```

## Performance Optimization

### Caching Strategies

```python
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from fastapi_cache.backends.inmemory import InMemoryBackend

# Initialize cache
FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

# Cache frequently asked questions
@cache(expire=300)  # Cache for 5 minutes
async def get_cached_answer(query: str):
    # Implementation
    pass
```

## Summary

You now have a comprehensive RAG chatbot system that:

- ✅ Integrates with OpenAI for natural language processing
- ✅ Uses Qdrant for efficient vector similarity search
- ✅ Stores data in Neon Serverless Postgres
- ✅ Provides personalized responses based on user context
- ✅ Runs on FastAPI for high performance
- ✅ Includes frontend integration with Docusaurus
- ✅ Implements security best practices
- ✅ Provides proper error handling and logging

## Implementation Steps

1. **Environment Setup**: Configure API keys and connection strings
2. **Database and Vector Store**: Set up Neon Postgres and Qdrant
3. **Backend Development**: Implement the FastAPI application
4. **Frontend Integration**: Add the chat widget to your Docusaurus site
5. **Content Indexing**: Process your textbook content for RAG
6. **Testing**: Verify functionality and security
7. **Deployment**: Deploy the full stack to production

## Next Steps

- Implement the authentication layer for personalized content
- Add the multilingual support functionality
- Create Claude Code subagents for specific textbook topics
- Integrate with the existing ROS 2, NVIDIA Isaac, and other textbook content