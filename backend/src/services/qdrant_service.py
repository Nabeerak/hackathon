import os
from qdrant_client import QdrantClient, models

class QdrantService:
    def __init__(self):
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
        )
        self.collection_name = "book_content"

    def recreate_collection(self):
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
        )

    def search_vectors(self, vector: list[float], limit: int = 5) -> list[models.ScoredPoint]:
        return self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=limit,
        )

    def upsert_vectors(self, points: list[models.PointStruct]):
        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
            wait=True,
        )
