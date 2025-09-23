#!/usr/bin/env python3
"""
Test module for user registration functionality.
Tests the registration endpoint with the new format (without full_name).
"""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient


class TestRegistration:
    """Test class for registration endpoint functionality."""

    @patch(
        "app.infrastructure.factories.repository_factory.RepositoryFactory.create_user_repository"
    )
    @patch("app.infrastructure.dependencies.get_authenticator")
    def test_registration_success(
        self,
        mock_auth,
        mock_user_repo,
        real_client: TestClient,
        test_user_data,
        mock_user,
    ):
        """Test successful user registration."""
        # Setup mocks
        mock_user_repo.return_value.find_by_username = AsyncMock(return_value=None)
        mock_user_repo.return_value.find_by_email = AsyncMock(return_value=None)
        mock_user_repo.return_value.create = AsyncMock(return_value=mock_user)
        mock_auth.return_value.get_password_hash.return_value = "hashed_password"

        response = real_client.post("/api/register", json=test_user_data)

        if response.status_code != 201:
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.text}")

        assert response.status_code == 201
        user_data = response.json()
        assert user_data["username"] == test_user_data["username"]
        assert user_data["email"] == test_user_data["email"]
        assert user_data["is_active"] is True
        assert "id" in user_data
        assert "created_at" in user_data
        # Verify full_name is not in response
        assert "full_name" not in user_data

    def test_registration_missing_fields(self, real_client: TestClient):
        """Test registration with missing required fields."""
        # Test missing username
        response = real_client.post(
            "/api/register",
            json={"email": "test@example.com", "password": "testpass"},
        )
        assert response.status_code == 422

        # Test missing email
        response = real_client.post(
            "/api/register",
            json={"username": "testuser", "password": "testpass"},
        )
        assert response.status_code == 422

        # Test missing password
        response = real_client.post(
            "/api/register",
            json={"username": "testuser", "email": "test@example.com"},
        )
        assert response.status_code == 422

    def test_registration_invalid_email(self, real_client: TestClient):
        """Test registration with invalid email format."""
        registration_data = {
            "username": "testuser",
            "email": "invalid-email",
            "password": "testpass",
        }

        response = real_client.post("/api/register", json=registration_data)
        assert response.status_code == 422

    @patch(
        "app.infrastructure.factories.repository_factory.RepositoryFactory.create_user_repository"
    )
    @patch("app.infrastructure.dependencies.get_authenticator")
    def test_registration_duplicate_username(
        self,
        mock_auth,
        mock_user_repo,
        real_client: TestClient,
        test_user_data,
        mock_user,
    ):
        """Test registration with duplicate username."""
        # Setup mocks - user already exists
        mock_user_repo.return_value.find_by_username = AsyncMock(return_value=mock_user)
        mock_user_repo.return_value.find_by_email = AsyncMock(return_value=None)
        mock_user_repo.return_value.create = AsyncMock(return_value=mock_user)
        mock_auth.return_value.get_password_hash.return_value = "hashed_password"

        response = real_client.post("/api/register", json=test_user_data)
        assert response.status_code == 400
        error_data = response.json()
        assert "Username already registered" in error_data["error"]

    @patch(
        "app.infrastructure.factories.repository_factory.RepositoryFactory.create_user_repository"
    )
    @patch("app.infrastructure.dependencies.get_authenticator")
    def test_registration_duplicate_email(
        self,
        mock_auth,
        mock_user_repo,
        real_client: TestClient,
        test_user_data,
        mock_user,
    ):
        """Test registration with duplicate email."""
        # Setup mocks - email already exists
        mock_user_repo.return_value.find_by_username = AsyncMock(return_value=None)
        mock_user_repo.return_value.find_by_email = AsyncMock(return_value=mock_user)
        mock_user_repo.return_value.create = AsyncMock(return_value=mock_user)
        mock_auth.return_value.get_password_hash.return_value = "hashed_password"

        response = real_client.post("/api/register", json=test_user_data)
        assert response.status_code == 400
        error_data = response.json()
        assert "Email already registered" in error_data["error"]


@pytest.mark.asyncio
class TestRegistrationAsync:
    """Async tests for registration functionality."""

    @patch(
        "app.infrastructure.factories.repository_factory.RepositoryFactory.create_user_repository"
    )
    @patch("app.infrastructure.dependencies.get_authenticator")
    async def test_registration_async(
        self,
        mock_auth,
        mock_user_repo,
        real_client: TestClient,
        test_user_data,
        mock_user,
    ):
        """Test registration using async httpx client."""
        # Setup mocks
        mock_user_repo.return_value.find_by_username = AsyncMock(return_value=None)
        mock_user_repo.return_value.find_by_email = AsyncMock(return_value=None)
        mock_user_repo.return_value.create = AsyncMock(return_value=mock_user)
        mock_auth.return_value.get_password_hash.return_value = "hashed_password"

        # Use the real client instead of httpx.AsyncClient
        response = real_client.post("/api/register", json=test_user_data)

        assert response.status_code == 201
        user_data = response.json()
        assert user_data["username"] == test_user_data["username"]
        assert user_data["email"] == test_user_data["email"]
        assert "full_name" not in user_data
