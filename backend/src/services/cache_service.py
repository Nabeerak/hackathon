"""
Cache service for embeddings and conversation memory
Reduces latency by caching frequently accessed data
"""
from typing import Optional, List, Dict, Any
import hashlib
import json
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

class CacheService:
    """
    In-memory LRU cache for embeddings and conversation context
    For production: consider Redis or Memcached for distributed caching
    """

    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self._embedding_cache = {}
        self._conversation_cache = {}

    def _generate_key(self, text: str) -> str:
        """Generate cache key from text using SHA-256 hash"""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def get_embedding(self, text: str) -> Optional[List[float]]:
        """Get cached embedding vector for text"""
        key = self._generate_key(text)
        embedding = self._embedding_cache.get(key)
        if embedding:
            logger.debug(f"Cache HIT for embedding: {key[:16]}...")
        return embedding

    def set_embedding(self, text: str, embedding: List[float]) -> None:
        """Cache embedding vector for text"""
        key = self._generate_key(text)

        # Simple LRU eviction: remove oldest if cache is full
        if len(self._embedding_cache) >= self.max_size:
            # Remove first (oldest) item
            oldest_key = next(iter(self._embedding_cache))
            del self._embedding_cache[oldest_key]
            logger.debug(f"Cache EVICT: {oldest_key[:16]}...")

        self._embedding_cache[key] = embedding
        logger.debug(f"Cache SET for embedding: {key[:16]}...")

    def get_conversation_context(self, conversation_id: int) -> Optional[List[Dict[str, Any]]]:
        """Get cached conversation messages"""
        context = self._conversation_cache.get(conversation_id)
        if context:
            logger.debug(f"Cache HIT for conversation: {conversation_id}")
        return context

    def set_conversation_context(self, conversation_id: int, messages: List[Dict[str, Any]]) -> None:
        """Cache conversation messages (last N messages for context)"""
        # Simple LRU eviction
        if len(self._conversation_cache) >= self.max_size:
            oldest_key = next(iter(self._conversation_cache))
            del self._conversation_cache[oldest_key]
            logger.debug(f"Cache EVICT conversation: {oldest_key}")

        # Store only last 10 messages to limit memory usage
        self._conversation_cache[conversation_id] = messages[-10:]
        logger.debug(f"Cache SET for conversation: {conversation_id}")

    def invalidate_conversation(self, conversation_id: int) -> None:
        """Invalidate cached conversation (e.g., after new message)"""
        if conversation_id in self._conversation_cache:
            del self._conversation_cache[conversation_id]
            logger.debug(f"Cache INVALIDATE conversation: {conversation_id}")

    def clear_all(self) -> None:
        """Clear all caches"""
        self._embedding_cache.clear()
        self._conversation_cache.clear()
        logger.info("All caches cleared")

    def get_stats(self) -> Dict[str, int]:
        """Get cache statistics"""
        return {
            "embeddings_cached": len(self._embedding_cache),
            "conversations_cached": len(self._conversation_cache),
            "max_size": self.max_size
        }


# Global cache instance
cache_service = CacheService(max_size=1000)


# Decorator for caching function results
def cached_embedding(func):
    """Decorator to cache embedding generation"""
    async def wrapper(text: str, *args, **kwargs):
        # Check cache first
        cached = cache_service.get_embedding(text)
        if cached is not None:
            return cached

        # Generate embedding if not cached
        embedding = await func(text, *args, **kwargs)

        # Store in cache
        if embedding:
            cache_service.set_embedding(text, embedding)

        return embedding

    return wrapper
