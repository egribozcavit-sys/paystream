"""
A.S.A.S Cloud - Basic Tests

Basic health and functionality tests for the payment infrastructure.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app, raise_server_exceptions=False)


def test_health_endpoint():
    """Test health check endpoint returns healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "timestamp" in response.json()


def test_root_endpoint():
    """Test root endpoint returns service information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "A.S.A.S" in data["name"]
    assert data["version"] == "1.0.0"
    assert data["status"] == "operational"


def test_invalid_endpoint():
    """Test that invalid endpoints return 404."""
    response = client.get("/invalid")
    assert response.status_code == 404
