#!/usr/bin/env python
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

try:
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )
    print("[OK] Connected to Qdrant successfully")

    # List collections
    collections = client.get_collections()
    print(f"[OK] Collections: {[c.name for c in collections.collections]}")

    # Check if book_content exists
    collection_names = [c.name for c in collections.collections]
    if "book_content" in collection_names:
        print("[OK] Collection 'book_content' exists")
        info = client.get_collection("book_content")
        print(f"  - Vectors count: {info.vectors_count}")
    else:
        print("[ERROR] Collection 'book_content' does NOT exist")
        print("  This is why chat is failing - no vector data to search!")

except Exception as e:
    print(f"[ERROR] {e}")
