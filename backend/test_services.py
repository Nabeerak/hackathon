"""Test script to verify all backend services are working"""
from dotenv import load_dotenv
load_dotenv()

import sys
import os

# Test 1: Environment Variables
print("=" * 50)
print("Test 1: Environment Variables")
print("=" * 50)
print(f"OPENAI_API_KEY: {'[OK] SET' if os.getenv('OPENAI_API_KEY') else '[ERROR] NOT SET'}")
print(f"QDRANT_URL: {'[OK] SET' if os.getenv('QDRANT_URL') else '[ERROR] NOT SET'}")
print(f"QDRANT_API_KEY: {'[OK] SET' if os.getenv('QDRANT_API_KEY') else '[ERROR] NOT SET'}")
print(f"NEON_DATABASE_URL: {'[OK] SET' if os.getenv('NEON_DATABASE_URL') else '[ERROR] NOT SET'}")

# Test 2: Database Connection
print("\n" + "=" * 50)
print("Test 2: Database Connection")
print("=" * 50)
try:
    from src.database import engine, SessionLocal
    with engine.connect() as conn:
        print("✓ Database connection successful")

    # Test session
    db = SessionLocal()
    db.close()
    print("✓ Database session creation successful")
except Exception as e:
    print(f"✗ Database connection failed: {e}")

# Test 3: OpenAI Service
print("\n" + "=" * 50)
print("Test 3: OpenAI Service")
print("=" * 50)
try:
    from src.services.openai_service import OpenAIService
    openai_service = OpenAIService()
    print("✓ OpenAI service initialized")

    # Test embedding
    test_text = "Hello world"
    embedding = openai_service.create_embedding(test_text)
    print(f"✓ Embedding created (dimension: {len(embedding)})")
except Exception as e:
    print(f"✗ OpenAI service failed: {e}")

# Test 4: Qdrant Service
print("\n" + "=" * 50)
print("Test 4: Qdrant Service")
print("=" * 50)
try:
    from src.services.qdrant_service import QdrantService
    qdrant_service = QdrantService()
    print("✓ Qdrant service initialized")

    # Check collection
    collection_name = "book_content"
    collections = qdrant_service.client.get_collections()
    collection_names = [c.name for c in collections.collections]

    if collection_name in collection_names:
        print(f"✓ Collection '{collection_name}' exists")

        # Get collection info
        collection_info = qdrant_service.client.get_collection(collection_name)
        print(f"  - Vector size: {collection_info.config.params.vectors.size}")
        print(f"  - Points count: {collection_info.points_count}")

        if collection_info.points_count == 0:
            print("  ⚠ WARNING: Collection is empty! No documents have been ingested.")
    else:
        print(f"⚠ WARNING: Collection '{collection_name}' does not exist")
        print("  Creating collection...")
        qdrant_service.ensure_collection_exists(collection_name)
        print(f"✓ Collection '{collection_name}' created (but empty)")
except Exception as e:
    print(f"✗ Qdrant service failed: {e}")

# Test 5: Chat Service
print("\n" + "=" * 50)
print("Test 5: Chat Service")
print("=" * 50)
try:
    from src.services.chat_service import ChatService
    chat_service = ChatService()
    print("✓ Chat service initialized")
except Exception as e:
    print(f"✗ Chat service failed: {e}")

# Test 6: Database Tables
print("\n" + "=" * 50)
print("Test 6: Database Tables")
print("=" * 50)
try:
    from src.models.models import User, Conversation, Message
    from src.database import SessionLocal

    db = SessionLocal()

    # Check if tables exist by querying them
    user_count = db.query(User).count()
    conv_count = db.query(Conversation).count()
    msg_count = db.query(Message).count()

    print(f"✓ Users table: {user_count} records")
    print(f"✓ Conversations table: {conv_count} records")
    print(f"✓ Messages table: {msg_count} records")

    db.close()
except Exception as e:
    print(f"✗ Database tables check failed: {e}")

print("\n" + "=" * 50)
print("Summary")
print("=" * 50)
print("If all tests passed with ✓, your backend is ready!")
print("If there are warnings (⚠), check the specific issues above.")
print("If there are errors (✗), fix them before starting the server.")
