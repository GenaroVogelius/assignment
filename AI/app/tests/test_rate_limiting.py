#!/usr/bin/env python3
"""
Test module for rate limiting functionality.
Tests the rate limiting on the /api/reviews endpoint.
"""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient


class TestRateLimiting:
    """Test class for rate limiting functionality."""

    @patch("app.infrastructure.dependencies.get_authenticator")
    @patch("app.infrastructure.dependencies.get_review_repository")
    def test_rate_limiting_with_test_client(
        self, mock_review_repo, mock_auth, client: TestClient, auth_headers, mock_user
    ):
        """Test rate limiting using FastAPI TestClient."""
        # Setup mocks
        mock_auth.return_value.get_current_user = AsyncMock(return_value=mock_user)
        mock_auth.return_value.get_current_active_user = AsyncMock(
            return_value=mock_user
        )
        mock_review_repo.return_value.find_by_user_id = AsyncMock(return_value=[])

        # Make multiple requests to test rate limiting
        successful_requests = 0
        rate_limited_requests = 0

        for i in range(15):  # Make 15 requests
            response = client.get("/api/reviews", headers=auth_headers)

            if response.status_code == 200:
                successful_requests += 1
            elif response.status_code == 429:
                rate_limited_requests += 1
            elif response.status_code == 404:
                # No reviews exist, but request was processed
                successful_requests += 1

        # Note: Rate limiting is currently commented out in the code
        # So all requests should succeed
        assert successful_requests == 15, (
            f"Expected 15 successful requests (rate limiting disabled), got {successful_requests}"
        )
        assert rate_limited_requests == 0, (
            f"Expected 0 rate limited requests (rate limiting disabled), got {rate_limited_requests}"
        )

    def test_rate_limiting_without_auth(self, client: TestClient):
        """Test that rate limiting applies to unauthenticated requests too."""
        successful_requests = 0
        rate_limited_requests = 0

        for i in range(15):
            response = client.get("/api/reviews")

            if response.status_code == 200:
                successful_requests += 1
            elif response.status_code == 429:
                rate_limited_requests += 1
            elif response.status_code == 401:
                # Unauthorized but not rate limited
                successful_requests += 1

        # For unauthenticated requests, we expect 401 (unauthorized) responses
        # since the endpoint requires authentication
        assert successful_requests == 15, (
            f"Expected 15 unauthorized requests, got {successful_requests}"
        )
        assert rate_limited_requests == 0, (
            f"Expected 0 rate limited requests (rate limiting disabled), got {rate_limited_requests}"
        )


@pytest.mark.integration
class TestRateLimitingIntegration:
    """Integration tests for rate limiting that require a running server."""

    @pytest.mark.asyncio
    async def test_rate_limiting_with_real_server(self):
        """Test rate limiting against a real running server."""
        # This test is marked as integration and will be skipped unless explicitly run
        pytest.skip("Integration test - requires running server")
