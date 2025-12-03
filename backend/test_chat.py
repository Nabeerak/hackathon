import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

print("Testing chat service...")

try:
    from src.services.chat_service import ChatService
    print("[OK] ChatService imported successfully")

    chat_service = ChatService()
    print("[OK] ChatService initialized successfully")

    print("\nTesting RAG response...")
    response, sources = chat_service.get_rag_response("Hello, what is physical AI?")
    print(f"[OK] RAG response received: {response[:100]}...")
    print(f"[OK] Sources: {sources}")

except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
