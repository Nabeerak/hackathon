from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict, Any
import os
import uuid

class QdrantService:
    def __init__(self):
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if not self.qdrant_url:
            raise ValueError("QDRANT_URL environment variable not set")

        # Initialize Qdrant client
        if self.qdrant_api_key and self.qdrant_api_key != "your_qdrant_api_key_here":
            self.client = QdrantClient(url=self.qdrant_url, api_key=self.qdrant_api_key)
        else:
            self.client = QdrantClient(url=self.qdrant_url)

    def ensure_collection_exists(self, collection_name: str, vector_size: int = 1536):
        """Ensure the Qdrant collection exists, create if not"""
        try:
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]

            if collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
                )
                print(f"Collection '{collection_name}' created")
            else:
                print(f"Collection '{collection_name}' already exists")
        except Exception as e:
            print(f"Error ensuring collection exists: {e}")
            raise

    def upsert_documents(self, collection_name: str, documents: List[Dict[str, Any]]):
        """Insert or update documents in Qdrant

        Each document should have:
        - id: unique identifier
        - vector: embedding vector
        - payload: metadata (source, content, etc.)
        """
        points = [
            PointStruct(
                id=doc.get("id", str(uuid.uuid4())),
                vector=doc["vector"],
                payload=doc.get("payload", {})
            )
            for doc in documents
        ]

        self.client.upsert(
            collection_name=collection_name,
            points=points
        )

    def search(self, collection_name: str, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar vectors in Qdrant

        Returns:
            List of search results with id, score, and payload
        """
        try:
            from qdrant_client.models import SearchRequest

            search_result = self.client.query_points(
                collection_name=collection_name,
                query=query_vector,
                limit=limit,
                with_payload=True
            )

            return [
                {
                    "id": hit.id,
                    "score": hit.score,
                    "payload": hit.payload
                }
                for hit in search_result.points
            ]
        except Exception as e:
            print(f"Error searching Qdrant: {e}")
            return []
