from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import os
from typing import List, Dict, Any

# Initialize Qdrant client
def get_qdrant_client():
    QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
    # QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None) # Uncomment if using Qdrant Cloud or authenticated Qdrant

    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    # client = QdrantClient(host=QDRANT_HOST, api_key=QDRANT_API_KEY) # For authenticated Qdrant
    return client

# Example function to ensure collection exists
def ensure_collection_exists(client: QdrantClient, collection_name: str, vector_size: int = 1536):
    collections = client.get_collections().collections
    if collection_name not in [c.name for c in collections]:
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )
        print(f"Collection '{collection_name}' created.")
    else:
        print(f"Collection '{collection_name}' already exists.")

# Placeholder for embedding generation (you'd integrate your embedding model here)
def generate_embedding(text: str) -> List[float]:
    # This is a mock function. In a real app, you'd use an actual embedding model (e.g., OpenAI, Sentence Transformers)
    # For OpenAI embeddings, the size is typically 1536
    print(f"Generating embedding for: {text[:50]}...")
    return [0.1] * 1536 # Return a dummy embedding for now

# Placeholder for search function
def search_qdrant(client: QdrantClient, collection_name: str, query_text: str, limit: int = 3) -> List[Dict[str, Any]]:
    query_vector = generate_embedding(query_text)
    search_result = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=limit,
        append_payload=True,
    )
    return [{
        "id": hit.id,
        "score": hit.score,
        "payload": hit.payload
    } for hit in search_result]
