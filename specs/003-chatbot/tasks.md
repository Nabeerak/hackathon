# Tasks: Book-Embedded RAG Chatbot

**Feature**: Book-Embedded RAG Chatbot
**Branch**: `003-chatbot`
**Date**: 2025-11-30

This document outlines the tasks required to implement the Book-Embedded RAG Chatbot, organized by user story priority and development phase.

## Dependencies

The user stories are prioritized as follows, indicating their completion order:
1.  User Story 1: Ask Questions About Book Content (P1)
2.  User Story 2: Ask Questions About Selected Text (P2)
3.  User Story 3: View and Resume Conversation History (P3)
4.  User Story 4: Search Book Content Directly (P4)

Each user story is designed to be independently testable.

## Implementation Strategy

The implementation will follow an incremental delivery approach, focusing on completing User Story 1 (P1) as the Minimum Viable Product (MVP). Subsequent user stories will be built upon the foundation established in earlier phases.

## Phase 1: Setup and Infrastructure (Foundational)

**Goal**: Establish the core project structure, environment, and foundational services.

-   [X] T001 Create backend directory and initial FastAPI project structure at `backend/`
-   [X] T002 Create frontend directory (within `docusaurus-book`) and initial React components structure at `docusaurus-book/frontend/`
-   [X] T003 Set up Python virtual environment and install backend dependencies (FastAPI, uvicorn, openai, qdrant-client, psycopg2-binary, sqlalchemy, alembic) in `backend/requirements.txt`
-   [X] T004 Set up Node.js environment and install frontend dependencies (React, Docusaurus, Axios, state management library) in `docusaurus-book/package.json`
-   [X] T005 Configure `.env` for backend with `OPENAI_API_KEY`, `NEON_DATABASE_URL`, `QDRANT_URL`, `QDRANT_API_KEY` in `backend/.env`
-   [X] T006 Initialize Alembic for database migrations at `backend/alembic/`
-   [X] T007 Create `scripts/ingest_book_content.py` script for indexing Docusaurus book content into Qdrant at `backend/scripts/ingest_book_content.py`

## Phase 2: User Story 1 - Ask Questions About Book Content (P1)

**Goal**: Implement the core RAG chatbot functionality to answer questions about the entire book content.

**Independent Test**: Submit various questions about book topics (e.g., "What is physical AI?", "How do humanoid robots work?") and verify that relevant answers are returned within 3 seconds, sourced from book content only. Off-topic questions should be gracefully rejected.

-   [X] T008 [US1] Create database models for `User`, `Conversation`, `Message` in `backend/src/models/`
-   [X] T009 [US1] Implement database migration for `User`, `Conversation`, `Message` models in `backend/alembic/versions/`
-   [X] T010 [US1] Implement `QdrantService` for interaction with Qdrant Cloud (initialization, vector search) in `backend/src/services/qdrant_service.py`
-   [X] T011 [US1] Implement `OpenAIService` for interaction with OpenAI API (embeddings, chat completions) in `backend/src/services/openai_service.py`
-   [X] T012 [US1] Implement `ChatService` for RAG logic, combining `QdrantService` and `OpenAIService` in `backend/src/services/chat_service.py`
-   [X] T013 [US1] Create FastAPI endpoint `/chat` for receiving user questions and returning chatbot responses in `backend/src/api/chat.py`
-   [X] T014 [US1] Implement content guardrails in `backend/src/services/chat_service.py` to prevent off-topic questions
-   [X] T015 [US1] Develop basic React chatbot UI component (input, display messages) in `docusaurus-book/frontend/src/components/Chatbot.tsx`
-   [X] T016 [US1] Integrate chatbot UI component into a Docusaurus page/layout in `docusaurus-book/src/pages/index.tsx` (or similar)
-   [X] T017 [US1] Implement API client in frontend to communicate with backend `/chat` endpoint in `docusaurus-book/frontend/src/services/chat_api.ts`
-   [X] T018 [US1] Run `backend/scripts/ingest_book_content.py` to populate Qdrant with book content.

## Phase 3: User Story 2 - Ask Questions About Selected Text (P2)

**Goal**: Enable users to ask questions specifically about selected text, with intelligent context expansion.

**Independent Test**: Select various text passages in the book, ask questions about those selections, and verify that answers prioritize the selected text while incorporating relevant context from related book sections when helpful.

-   [X] T019 [P] [US2] Enhance frontend UI to allow text selection within Docusaurus content in `docusaurus-book/frontend/src/components/Chatbot.tsx` (or new component)
-   [X] T020 [US2] Modify `/chat` API endpoint to accept optional `selected_text` parameter in `backend/src/api/chat.py`
-   [X] T021 [US2] Update `ChatService` to prioritize `selected_text` for context retrieval and intelligently expand with related book sections in `backend/src/services/chat_service.py`
-   [X] T022 [US2] Refine guardrails to handle off-topic questions related to selected text in `backend/src/services/chat_service.py`

## Phase 4: User Story 3 - View and Resume Conversation History (P3)

**Goal**: Implement functionality for users to view, search, and resume past conversations.

**Independent Test**: Create multiple conversation sessions, log out/close the app, return later, and verify all previous conversations are accessible and can be continued with maintained context.

-   [X] T023 [US3] Create FastAPI endpoints for `GET /conversations` (list), `POST /conversations` (new), `GET /conversations/{id}` (retrieve), `DELETE /conversations/{id}` in `backend/src/api/conversations.py`
-   [X] T024 [US3] Implement `ConversationService` for managing conversation persistence and retrieval from Neon Postgres in `backend/src/services/conversation_service.py`
-   [X] T025 [US3] Develop React components for displaying conversation list and individual conversation history in `docusaurus-book/frontend/src/components/ConversationHistory.tsx`
-   [X] T026 [US3] Integrate conversation history UI into Docusaurus frontend, enabling selection and continuation of past chats in `docusaurus-book/src/pages/index.tsx` (or similar)
-   [X] T027 [US3] Implement frontend API client for `conversations` endpoints in `docusaurus-book/frontend/src/services/conversation_api.ts`

## Phase 5: User Story 4 - Search Book Content Directly (P4)

**Goal**: Allow users to perform keyword-based searches directly within the book content.

**Independent Test**: Enter book-related search keywords (e.g., "neural networks", "actuators") and verify that relevant book passages are returned ranked by relevance score, with highlighting of matching terms.

-   [X] T028 [US4] Create FastAPI endpoint `GET /search` for keyword-based book content search in `backend/src/api/search.py`
-   [X] T029 [US4] Implement `SearchService` utilizing `QdrantService` for direct keyword search on book content in `backend/src/services/search_service.py`
-   [X] T030 [US4] Develop React component for a search interface and displaying search results in `docusaurus-book/frontend/src/components/BookSearch.tsx`
-   [X] T031 [US4] Integrate book search UI into Docusaurus frontend in `docusaurus-book/src/pages/index.tsx` (or similar)
-   [X] T032 [US4] Implement frontend API client for `/search` endpoint in `docusaurus-book/frontend/src/services/search_api.ts`

## Phase 6: Polish and Cross-Cutting Concerns

**Goal**: Address remaining non-functional requirements and overall system quality.

-   [X] T033 Implement comprehensive error handling and logging across backend services in `backend/src/`
-   [X] T034 Implement rate limiting (FR-009) for API endpoints in `backend/src/api/` (using FastAPI dependencies)
-   [X] T035 Implement input sanitization and validation (FR-011) for all API endpoints in `backend/src/api/`
-   [X] T036 Set up unit tests for backend services (P1-P4) using `pytest` in `backend/tests/unit/`
-   [X] T037 Set up integration tests for backend API endpoints (P1-P4) in `backend/tests/integration/`
-   [X] T038 Set up E2E tests for chatbot functionality (P1-P4) using Playwright/Cypress in `docusaurus-book/tests/e2e/`
-   [X] T039 Ensure all responses include metadata (timestamp, sources, processing time) (FR-014) in `backend/src/api/`
-   [X] T040 Implement conversation export functionality (FR-015) in `backend/src/api/conversations.py` and `docusaurus-book/frontend/src/components/ConversationHistory.tsx`
-   [X] T041 Ensure chatbot is designed as a reusable Claude Code Subagent (FR-016) by defining a clear interface and packaging it appropriately.

## Next Steps

-   **Suggested MVP Scope**: Focus on completing Phase 1 and Phase 2 (User Story 1) to get the core chatbot functionality working.
-   **Parallel Opportunities**: Tasks marked with [P] can be worked on concurrently if resources allow, especially frontend and backend development within a user story phase after core API contracts are established.
-   **ADR Suggestion**: A decision was made to design the chatbot as a reusable Claude Code Subagent. This is an architecturally significant decision.
    📋 Architectural decision detected: Chatbot as Reusable Claude Code Subagent — Document reasoning and tradeoffs? Run `/sp.adr ChatbotReusableSubagent`
