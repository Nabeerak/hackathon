# Claude Code Subagent: Book-Embedded RAG Chatbot

## Overview

This subagent provides a Retrieval-Augmented Generation (RAG) chatbot that can answer questions about book content, support text selection for context-specific questions, and apply guardrails to prevent off-topic queries.

## Architecture

The chatbot subagent consists of:

1. **Backend Services**:
   - FastAPI-based REST API
   - RAG logic with OpenAI and Qdrant integration
   - Conversation management with PostgreSQL
   - Content search capabilities

2. **Frontend Components**:
   - React-based chat interface
   - Text selection functionality
   - Conversation history management

## Reusability

The chatbot is designed to be reusable in other Claude Code projects:

### Backend Integration
- The API endpoints can be mounted in other FastAPI applications
- Services can be instantiated independently
- Database models can be integrated into other schemas

### Frontend Components
- React components can be imported and used in other applications
- API service clients can be reused with different base URLs
- CSS can be customized with theme variables

## API Endpoints

### Chat
- `POST /api/chat` - Send messages and receive responses
- Includes support for selected text context

### Conversations
- `GET /api/conversations` - List conversations
- `POST /api/conversations` - Create conversation
- `GET /api/conversations/{id}` - Get conversation details
- `DELETE /api/conversations/{id}` - Delete conversation
- `GET /api/conversations/search` - Search conversations
- `GET /api/conversations/{id}/export` - Export conversation

### Search
- `GET /api/search` - Search book content

## Configuration

The subagent requires the following environment variables:
- `OPENAI_API_KEY`
- `NEON_DATABASE_URL`
- `QDRANT_URL`
- `QDRANT_API_KEY`

## Usage in Other Projects

To integrate this subagent into another Claude Code project:

1. Add the backend as a dependency
2. Mount the API routers in your main application
3. Include the frontend components in your UI
4. Configure the environment variables

## Deployment

1. Set up the required services (PostgreSQL, Qdrant, OpenAI)
2. Configure environment variables
3. Run database migrations
4. Start the FastAPI server
5. Build and serve the frontend

## Testing

Run the unit tests:
```bash
cd backend
python -m pytest tests/unit/
```

Run the integration tests:
```bash
cd backend
python -m pytest tests/integration/
```

## Security Considerations

- Input validation and sanitization
- Rate limiting (30 requests per minute per IP)
- SQL injection prevention
- XSS prevention through HTML escaping
- Proper authentication (though not implemented in this MVP)

## Performance

- Vector search for fast content retrieval
- Caching mechanisms (to be enhanced)
- Optimized database queries
- Asynchronous processing where appropriate