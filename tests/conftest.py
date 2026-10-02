"""
A.S.A.S Cloud - Pytest Fixtures

Shared fixtures and configuration for all tests.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base, engine
from app.models import User, Account
from app.auth import get_password_hash
import uuid


@pytest.fixture
def client():
    """Create test client."""
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client


@pytest.fixture
def test_user():
    """Create test user data."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }


@pytest.fixture
def test_account():
    """Create test account data."""
    return {
        "user_id": "test-user-id",
        "currency": "USD"
    }


@pytest.fixture(scope="function")
def db_session():
    """Create fresh database session for each test."""
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()
    transaction = connection.begin()
    SessionLocal = get_db()
    session = SessionLocal()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()
