"""
Unit tests for backend services
"""
import pytest
from backend.src.services.chat_service import ChatService
from backend.src.services.search_service import SearchService

def test_chat_service_initialization():
    """Test that ChatService initializes properly"""
    chat_service = ChatService()
    assert chat_service.openai_service is not None
    assert chat_service.qdrant_service is not None

def test_search_service_initialization():
    """Test that SearchService initializes properly"""
    search_service = SearchService()
    assert search_service.openai_service is not None
    assert search_service.qdrant_service is not None

def test_clean_text():
    """Test text cleaning functionality"""
    chat_service = ChatService()
    test_text = "Hello **world**! <script>alert('test')</script>"
    cleaned = chat_service.clean_text(test_text)
    # Should remove markdown and HTML tags
    assert "world" in cleaned
    assert "<script>" not in cleaned