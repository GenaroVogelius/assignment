pytess# Test Suite

This directory contains all the tests for the FastAPI application using pytest.

## Test Structure

- `conftest.py` - Shared fixtures and test configuration
- `test_auth_registration.py` - Tests for user registration functionality
- `test_auth_logout.py` - Tests for logout and token blacklisting functionality
- `test_rate_limiting.py` - Tests for rate limiting functionality

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest app/tests/test_auth_registration.py
```

### Run tests with specific markers
```bash
# Run only integration tests (require running server)
pytest -m integration

# Run only authentication tests
pytest -m auth

# Run only rate limiting tests
pytest -m rate_limit

# Skip slow tests
pytest -m "not slow"
```

### Run tests with verbose output
```bash
pytest -v
```

### Run tests with coverage
```bash
pytest --cov=app
```

## Test Categories

### Unit Tests
- Test individual functions and components in isolation
- Use FastAPI TestClient for synchronous tests
- Use pytest fixtures for test data and setup

### Integration Tests
- Test complete workflows and API endpoints
- Require a running server (marked with `@pytest.mark.integration`)
- Use async httpx client for real HTTP requests

### Async Tests
- Tests that use `@pytest.mark.asyncio` for async functionality
- Use `httpx.AsyncClient` for async HTTP requests

## Fixtures

The following fixtures are available in `conftest.py`:

- `client` - FastAPI TestClient for synchronous tests
- `async_client` - httpx.AsyncClient for async tests
- `test_settings` - Application settings for testing
- `test_user_data` - Standard test user data
- `auth_headers` - Pre-authenticated headers for protected endpoints
- `base_url` - Base URL for the API
- `event_loop` - Event loop for async tests

## Test Data

Tests use consistent test data to avoid conflicts:
- Username: `test_user`, `rate_limit_test_user`, etc.
- Email: `test@example.com`, `rate_limit_test@example.com`, etc.
- Password: `testpass123`

## Notes

- Integration tests require the server to be running on `http://localhost:8000`
- Some tests may skip if authentication fails (user doesn't exist)
- Rate limiting tests make multiple requests and may take longer to run
- Tests are designed to be idempotent and can be run multiple times
