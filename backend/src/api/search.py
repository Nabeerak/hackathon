import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import html

from backend.src.services.search_service import SearchService

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class SearchResponseItem(BaseModel):
    id: str
    content: str
    source: str
    score: float

class SearchResponse(BaseModel):
    results: List[SearchResponseItem]
    total: int
    metadata: dict = {}

@router.get("/search")
def search_content(
    query: str,
    limit: int = 10
):
    """Search book content directly using vector similarity."""
    try:
        logger.info(f"Searching content with query: {query}, limit: {limit}")

        if not query or len(query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query parameter is required")

        # Sanitize the query
        query = html.escape(query.strip())

        # Validate inputs
        if limit <= 0 or limit > 50:  # Limit max limit to prevent abuse
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 50")

        # Use Search service
        search_service = SearchService()
        raw_results = search_service.search_content(query, limit)

        # Format results
        formatted_results = []
        for i, (content, source, score) in enumerate(raw_results):
            # Use a simple ID based on position since we're not storing the original point ID in the service
            formatted_results.append(SearchResponseItem(
                id=f"result_{i}",
                content=content,
                source=source,
                score=score
            ))

        # Prepare metadata
        metadata = {
            "query": query,
            "limit": limit,
            "results_count": len(formatted_results),
            "timestamp": "2025-11-30T00:00:00Z"  # Note: In real implementation, use actual timestamp
        }

        logger.info(f"Search completed successfully, returned {len(formatted_results)} results")
        return SearchResponse(
            results=formatted_results,
            total=len(formatted_results),
            metadata=metadata
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in search content: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")