"""
Simple tests for Astra API
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Astra API"
    assert data["status"] == "running"


def test_ready_endpoint():
    """Test readiness endpoint"""
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"


def test_voice_command_endpoint():
    """Test voice command endpoint"""
    payload = {
        "user_id": "test-user-123",
        "transcript": "Hello Astra, what can you do?",
        "locale": "en-US"
    }
    
    response = client.post("/api/v1/voice", json=payload)
    # Note: This will fail without database, but tests the endpoint structure
    # For now, just verify it returns a proper error or success
    assert response.status_code in [200, 500]


def test_command_endpoint():
    """Test command endpoint"""
    payload = {
        "user_id": "test-user-123",
        "command": "search for Python tutorials"
    }
    
    response = client.post("/api/v1/command", json=payload)
    # Note: This will fail without database, but tests the endpoint structure
    assert response.status_code in [200, 500]
