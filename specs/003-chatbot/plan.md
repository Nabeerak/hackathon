# Implementation Plan: Book-Embedded RAG Chatbot

**Branch**: `003-chatbot` | **Date**: 2025-11-30 | **Spec**: D:/hackathon/specs/003-chatbot/spec.md
**Input**: Feature specification from `/specs/003-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the implementation of a Retrieval-Augmented Generation (RAG) chatbot embedded within the "Physical AI & Humanoid Robotics" Docusaurus book. The chatbot will answer user questions about the book's content, support context-specific questions based on user-selected text, and utilize guardrails to prevent off-topic queries. The technical approach involves leveraging OpenAI Agents/ChatKit SDKs, FastAPI for the backend, Neon Serverless Postgres for relational data, and Qdrant Cloud Free Tier for vector similarity search.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11+ (for FastAPI), TypeScript (for Docusaurus frontend)  
**Primary Dependencies**: OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres, Qdrant Cloud Free Tier, Docusaurus  
**Storage**: Neon Serverless Postgres (for conversation history, user data), Qdrant Cloud Free Tier (for vector embeddings of book content)  
**Testing**: pytest (for backend API), Playwright/Cypress (for frontend E2E/integration), Jest/React Testing Library (for frontend unit/component)  
**Target Platform**: Web (embedded within Docusaurus book)
**Project Type**: Web application (backend API for chatbot logic, frontend for Docusaurus integration and UI)  
**Performance Goals**: 95% of requests complete in under 3 seconds (SC-001), conversation history search returns results within 1 second for 95% of queries (SC-009).  
**Constraints**: Rate limiting of 30 requests per minute per user (FR-009), responses within 3 seconds for 95% of requests (FR-012).  
**Scale/Scope**: Initial deployment targets up to 500 concurrent users (SC-004 implies 100 concurrent users without degradation, spec mentions initial deployment targets up to 500).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **II. Integrated RAG Chatbot Development**: This project directly implements this principle by building and embedding a RAG chatbot using the specified technologies (OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres, Qdrant Cloud Free Tier) and functionalities (answering book content questions, text selection, guardrails). **PASS**

## Project Structure

### Documentation (this feature)

```text
specs/003-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
```text
backend/
├── src/
│   ├── models/            # Pydantic models for data, ORM models for Postgres
│   ├── services/          # Core chatbot logic, RAG pipeline, OpenAI/ChatKit integration, Qdrant interaction
│   └── api/               # FastAPI endpoints for chat, history, health checks
└── tests/                 # Unit, integration, and E2E tests for the backend

frontend/ (within docusaurus-book directory)
├── src/
│   ├── components/        # React components for chatbot UI, message display, text selection
│   ├── pages/             # Docusaurus page for chatbot integration
│   └── services/          # Frontend API interaction, state management for chat
└── tests/                 # Frontend tests
```

**Structure Decision**: The project will adopt a web application structure, separating the backend (FastAPI) for chatbot logic and data management from the frontend (Docusaurus/React) for the user interface and book embedding. This aligns with "Option 2: Web application" and facilitates clear separation of concerns and independent development/deployment of the services. The frontend will reside within the existing `docusaurus-book` directory.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
