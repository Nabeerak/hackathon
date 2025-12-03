#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
from src.services.chat_service import ChatService

load_dotenv()

try:
    print("[1/3] Initializing ChatService...")
    chat_service = ChatService()
    print("[OK] ChatService initialized")

    print("\n[2/3] Testing on-topic check...")
    is_on_topic = chat_service.is_on_topic("What is physical AI?")
    print(f"[OK] On-topic check: {is_on_topic}")

    print("\n[3/3] Testing RAG response...")
    response, sources = chat_service.get_rag_response("What is physical AI?")
    print(f"[OK] Response: {response[:100]}...")
    print(f"[OK] Sources: {sources}")

    print("\n[SUCCESS] All chat service tests passed!")

except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
