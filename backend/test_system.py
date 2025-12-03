#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick System Test Script
Tests all components of the chatbot system
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Windows console compatibility
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def test_env_variables():
    """Check all required environment variables"""
    print("=" * 60)
    print("1. Testing Environment Variables")
    print("=" * 60)

    required_vars = {
        'OPENAI_API_KEY': 'OpenAI API',
        'QDRANT_URL': 'Qdrant Vector DB',
        'QDRANT_API_KEY': 'Qdrant API Key',
        'NEON_DATABASE_URL': 'Neon PostgreSQL (or DATABASE_URL for SQLite)'
    }

    all_good = True
    for var, description in required_vars.items():
        value = os.getenv(var) or os.getenv(var.replace('NEON_', ''))
        if value:
            # Mask sensitive data
            if 'KEY' in var or 'URL' in var:
                display_value = value[:20] + '...' if len(value) > 20 else value
            else:
                display_value = value
            print(f"  ✅ {description}: {display_value}")
        else:
            print(f"  ❌ {description}: NOT SET")
            all_good = False

    print()
    return all_good


def test_database():
    """Test database connection"""
    print("=" * 60)
    print("2. Testing Database Connection")
    print("=" * 60)

    try:
        from src.database import engine
        print(f"  ✅ Database engine created")
        print(f"  📊 Database type: {engine.url.drivername}")

        # Try to connect
        with engine.connect() as conn:
            print(f"  ✅ Successfully connected to database!")

        print()
        return True
    except Exception as e:
        print(f"  ❌ Database error: {str(e)}")
        print()
        return False


def test_qdrant():
    """Test Qdrant connection and check collection"""
    print("=" * 60)
    print("3. Testing Qdrant Connection")
    print("=" * 60)

    try:
        from src.services.qdrant_service import QdrantService

        qdrant = QdrantService()
        print(f"  ✅ Qdrant client created")

        # Check collection
        collection = qdrant.client.get_collection('book_content')
        print(f"  ✅ Collection 'book_content' exists")
        print(f"  📊 Total chunks: {collection.points_count}")

        if collection.points_count == 0:
            print(f"  ⚠️  WARNING: No data ingested yet!")
            print(f"      Run: python scripts/ingest_book_content.py --book-path ../docusaurus-book/docs/physical-ai-textbook/")
        elif collection.points_count < 100:
            print(f"  ⚠️  WARNING: Only {collection.points_count} chunks. Expected 500+")
        else:
            print(f"  ✅ Sufficient data for chatbot")

        print()
        return True
    except Exception as e:
        print(f"  ❌ Qdrant error: {str(e)}")
        print(f"      Make sure Qdrant cluster is running and credentials are correct")
        print()
        return False


def test_openai():
    """Test OpenAI connection"""
    print("=" * 60)
    print("4. Testing OpenAI Connection")
    print("=" * 60)

    try:
        from src.services.openai_service import OpenAIService

        openai = OpenAIService()
        print(f"  ✅ OpenAI client created")

        # Try a simple embedding
        test_text = "test"
        embedding = openai.get_embedding(test_text)
        print(f"  ✅ Successfully generated embedding")
        print(f"  📊 Embedding size: {len(embedding)} dimensions")

        print()
        return True
    except Exception as e:
        print(f"  ❌ OpenAI error: {str(e)}")
        print(f"      Check your API key and billing status")
        print()
        return False


def test_chat_service():
    """Test the chat service integration"""
    print("=" * 60)
    print("5. Testing Chat Service")
    print("=" * 60)

    try:
        from src.services.chat_service import ChatService

        chat = ChatService()
        print(f"  ✅ Chat service created")
        print(f"  📊 Qdrant available: {chat.qdrant_available}")

        if not chat.qdrant_available:
            print(f"  ⚠️  WARNING: Qdrant not available - chatbot will work without RAG")

        # Try a simple response (without RAG if Qdrant unavailable)
        print(f"  🧪 Testing simple chat response...")
        response, sources = chat.get_rag_response("What is AI?")
        print(f"  ✅ Got response: {response[:100]}...")
        print(f"  📊 Sources found: {len(sources)}")

        print()
        return True
    except Exception as e:
        print(f"  ❌ Chat service error: {str(e)}")
        print()
        return False


def test_api_server():
    """Test if the API server is running"""
    print("=" * 60)
    print("6. Testing API Server")
    print("=" * 60)

    try:
        import requests

        # Try to connect to health endpoint
        response = requests.get('http://127.0.0.1:8000/health', timeout=2)

        if response.status_code == 200:
            print(f"  ✅ API server is running!")
            print(f"  📊 Health status: {response.json()}")
        else:
            print(f"  ⚠️  API server returned status {response.status_code}")

        print()
        return True
    except requests.exceptions.ConnectionError:
        print(f"  ⚠️  API server not running")
        print(f"      Start it with: uvicorn src.main:app --reload --port 8000")
        print()
        return False
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        print()
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("CHATBOT SYSTEM TEST")
    print("=" * 60 + "\n")

    results = {
        'Environment Variables': test_env_variables(),
        'Database': test_database(),
        'Qdrant': test_qdrant(),
        'OpenAI': test_openai(),
        'Chat Service': test_chat_service(),
        'API Server': test_api_server()
    }

    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {test_name}")

    total = len(results)
    passed = sum(1 for r in results.values() if r)

    print()
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)

    if passed == total:
        print("\n🎉 All tests passed! Your chatbot is ready to use!")
        print("\nNext steps:")
        print("  1. Start backend: cd backend && uvicorn src.main:app --reload")
        print("  2. Start frontend: cd docusaurus-book && npm start")
        print("  3. Open http://localhost:3000 and test the chatbot!")
    else:
        print("\n⚠️  Some tests failed. Check the errors above and fix them.")
        print("\nQuick fixes:")
        print("  - Missing env vars: Check backend/.env file")
        print("  - Qdrant error: See backend/QDRANT_SETUP.md")
        print("  - Database error: See backend/NEON_SETUP.md")
        print("  - OpenAI error: Check API key and billing")

    print()
    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main())
