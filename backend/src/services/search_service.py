from typing import List, Tuple
from backend.src.services.qdrant_service import QdrantService
from backend.src.services.openai_service import OpenAIService

class SearchService:
    def __init__(self):
        self.qdrant_service = QdrantService()
        self.openai_service = OpenAIService()

    def search_content(self, query: str, limit: int = 10) -> List[Tuple[str, str, float]]:
        """Search book content using vector similarity."""
        # Generate embedding for the query
        query_embedding = self.openai_service.get_embedding(query)
        
        # Search in Qdrant
        search_results = self.qdrant_service.search_vectors(query_embedding, limit=limit)
        
        # Format results as (content, source, score)
        formatted_results = []
        for point in search_results:
            content = point.payload.get("text_preview", "")
            source = point.payload.get("source_file", "Unknown")
            score = point.score or 0.0
            formatted_results.append((content, source, score))
        
        return formatted_results