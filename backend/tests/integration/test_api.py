"""
Integration tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from backend.src.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["message"] == "Chatbot API is running"

def test_chat_endpoint_validation():
    """Test validation on chat endpoint"""
    # Test with empty message
    response = client.post("/api/chat", json={
        "message": "",
        "conversation_id": None
    })
    assert response.status_code == 400  # Should return validation error
    
    # Test with very long message
    long_message = "A" * 2500  # Exceeds our 2000 char limit
    response = client.post("/api/chat", json={
        "message": long_message,
        "conversation_id": None
    })
    assert response.status_code == 400  # Should return validation error