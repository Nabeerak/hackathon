1→# Data Model: Book-Embedded RAG Chatbot
2→
3→## Entities
4→
5→### User
6→- **Description**: Represents an individual interacting with the chatbot.
7→- **Attributes**:
8→  - `id`: Unique identifier (Primary Key)
9→  - `account_creation_timestamp`: Timestamp of user account creation
10→  - `total_interaction_count`: Total number of interactions with the chatbot
11→  - `preferences`: User-specific settings or preferences (e.g., personalization settings)
12→
13→### Conversation
14→- **Description**: Represents a chat session between a user and the chatbot.
15→- **Attributes**:
16→  - `id`: Unique conversation identifier (Primary Key)
17→  - `user_id`: Foreign Key referencing User.id
18→  - `creation_timestamp`: Timestamp when the conversation was initiated
19→  - `last_updated_timestamp`: Timestamp of the last message in the conversation
20→  - `title`: Optional title or topic for the conversation (for easy retrieval)
21→  - `message_count`: Number of messages in the conversation
22→
23→### Message
24→- **Description**: Represents a single exchange in a conversation.
25→- **Attributes**:
26→  - `id`: Unique message identifier (Primary Key)
27→  - `conversation_id`: Foreign Key referencing Conversation.id
28→  - `role`: Role of the sender (e.g., 'user', 'assistant')
29→  - `content_text`: The actual text content of the message
30→  - `timestamp`: Timestamp when the message was sent/received
31→  - `token_count_used`: Number of tokens used for this message (for cost tracking)
32→  - `processing_latency`: Latency in processing this message (for performance monitoring)
33→
34→### Knowledge Document
35→- **Description**: Represents a chunk of information from the book content.
36→- **Attributes**:
37→  - `id`: Unique document identifier (Primary Key)
38→  - `content_text`: The raw text content of the document chunk
39→  - `vector_embedding`: Numerical vector representation of the content
40→  - `metadata`: JSON object containing source, category, timestamp, chapter, page_number etc.
41→  - `relevance_score`: Score indicating relevance to a query (runtime attribute, not stored persistently with document)

## Relationships

- `User` 1:N `Conversation`: A user can have multiple conversations.
- `Conversation` 1:N `Message`: A conversation consists of multiple messages.

## Validation Rules

- All `_id` fields must be unique and non-null.
- `content_text` in `Message` and `Knowledge Document` must not be empty.
- `role` in `Message` must be one of ['user', 'assistant'].
- Timestamps must be valid date/time formats.

## State Transitions (Conceptual)

- `Conversation`:
    - `pending` -> `active` (first message)
    - `active` -> `archived` (after a period of inactivity or user action)
    - `active` -> `deleted` (user action)
