from qdrant_client import QdrantClient
from qdrant_client.async_qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict, Any, Optional
import os
import uuid
import logging

logger = logging.getLogger(__name__)

class QdrantService:
    def __init__(self):
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.client: Optional[QdrantClient] = None
        self.async_client: Optional[AsyncQdrantClient] = None
        self._connected = False

        if not self.qdrant_url:
            logger.warning("QDRANT_URL environment variable not set - Qdrant features will be unavailable")
            return

        try:
            # Initialize Qdrant clients (sync and async)
            if self.qdrant_api_key and self.qdrant_api_key != "your_qdrant_api_key_here":
                self.client = QdrantClient(url=self.qdrant_url, api_key=self.qdrant_api_key, timeout=10)
                self.async_client = AsyncQdrantClient(url=self.qdrant_url, api_key=self.qdrant_api_key, timeout=10)
            else:
                self.client = QdrantClient(url=self.qdrant_url, timeout=10)
                self.async_client = AsyncQdrantClient(url=self.qdrant_url, timeout=10)

            # Test connection
            self.client.get_collections()
            self._connected = True
            logger.info(f"Successfully connected to Qdrant at {self.qdrant_url}")
        except Exception as e:
            logger.warning(f"Failed to connect to Qdrant: {e}")
            self.client = None
            self.async_client = None
            self._connected = False

    def is_connected(self) -> bool:
        """Check if Qdrant client is connected"""
        return self._connected and self.client is not None

    def get_client(self) -> Optional[QdrantClient]:
        """Get the Qdrant client instance"""
        if not self.is_connected():
            logger.warning("Qdrant client is not connected")
            return None
        return self.client

    def ensure_collection_exists(self, collection_name: str, vector_size: int = 1536):
        """Ensure the Qdrant collection exists, create if not"""
        if not self.is_connected():
            logger.error("Cannot ensure collection - Qdrant not connected")
            raise RuntimeError("Qdrant service is not available")

        try:
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]

            if collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
                )
                logger.info(f"Collection '{collection_name}' created")
            else:
                logger.info(f"Collection '{collection_name}' already exists")
        except Exception as e:
            logger.error(f"Error ensuring collection exists: {e}")
            raise

    def upsert_documents(self, collection_name: str, documents: List[Dict[str, Any]]):
        """Insert or update documents in Qdrant

        Each document should have:
        - id: unique identifier
        - vector: embedding vector
        - payload: metadata (source, content, etc.)
        """
        if not self.is_connected():
            logger.error("Cannot upsert documents - Qdrant not connected")
            raise RuntimeError("Qdrant service is not available")

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
        """Search for similar vectors in Qdrant (sync version)

        Returns:
            List of search results with id, score, and payload
        """
        if not self.is_connected():
            logger.warning("Cannot search - Qdrant not connected")
            return []

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
            logger.error(f"Error searching Qdrant: {e}")
            return []

    async def search_async(self, collection_name: str, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar vectors in Qdrant (async - lower latency for production)

        Returns:
            List of search results with id, score, and payload
        """
        if not self.is_connected():
            logger.warning("Cannot search - Qdrant not connected")
            return []

        try:
            search_result = await self.async_client.query_points(
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
            logger.error(f"Error searching Qdrant async: {e}")
            return []


# Create singleton instance
qdrant_client = QdrantService()
