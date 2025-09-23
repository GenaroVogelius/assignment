from unittest.mock import AsyncMock

import httpx
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.config.settings import Settings


@pytest.fixture
def test_app():
    """Create a test FastAPI app with minimal routes."""
    app = FastAPI(title="Test App", version="0.1")

    # Create minimal test routes without heavy dependencies
    from fastapi import APIRouter

    # Auth routes
    auth_router = APIRouter()

    @auth_router.post("/register", status_code=201)
    async def register():
        return {"message": "Registration endpoint"}

    @auth_router.post("/login")
    async def login():
        return {"access_token": "test_token", "token_type": "bearer"}

    @auth_router.post("/logout")
    async def logout():
        return {"message": "Logged out"}

    # Main routes
    main_router = APIRouter()

    @main_router.get("/reviews")
    async def get_reviews():
        return {"reviews": []}

    app.include_router(auth_router, prefix="/api", tags=["auth"])
    app.include_router(main_router, prefix="/api", tags=["api rest"])

    return app


@pytest.fixture
def real_app():
    """Create the real FastAPI app for integration tests."""
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from slowapi.errors import RateLimitExceeded

    from app.config.settings import Settings
    from app.infrastructure.api.auth_routes import AuthRoutes
    from app.infrastructure.api.main_routes import MainRoutes
    from app.infrastructure.dependencies import limiter

    settings = Settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        debug=settings.DEBUG,
        description="AI Service with database integration",
    )

    # Add rate limiter to the app
    app.state.limiter = limiter
    app.add_exception_handler(
        RateLimitExceeded,
        lambda request, exc: JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded", "status_code": 429},
        ),
    )

    # Configuración de CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.ALLOW_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Manejo global de errores
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail, "status_code": exc.status_code},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "status_code": 500},
        )

    # Add routes without database initialization
    main_routes = MainRoutes()
    app.include_router(main_routes.router, prefix="/api", tags=["api rest"])

    auth_routes = AuthRoutes()
    app.include_router(auth_routes.router, prefix="/api", tags=["auth"])

    return app


@pytest.fixture
def client(test_app):
    """FastAPI TestClient fixture for synchronous tests."""
    return TestClient(test_app)


@pytest.fixture
def real_client(real_app):
    """FastAPI TestClient fixture for real app tests."""
    return TestClient(real_app)


@pytest.fixture
def async_client():
    """Async httpx client fixture for asynchronous tests."""
    return httpx.AsyncClient()


@pytest.fixture
def test_settings():
    """Test settings fixture."""

    return Settings()


@pytest.fixture
def test_user_data():
    """Test user data for registration and login tests."""
    return {
        "username": "test_user",
        "email": "test@example.com",
        "password": "testpass123",
    }


@pytest.fixture
def mock_user():
    """Mock user object for testing."""
    from datetime import datetime

    from app.core.models.user import User

    user = User(
        id="test_user_id",
        username="test_user",
        email="test@example.com",
        hashed_password="hashed_password",
        is_active=True,
        created_at=datetime.now(),
    )
    return user


@pytest.fixture
def mock_authenticator():
    """Mock authenticator for testing."""
    authenticator = AsyncMock()
    authenticator.authenticate_user.return_value = None
    authenticator.get_current_user.return_value = None
    authenticator.get_current_active_user.return_value = None
    authenticator.get_password_hash.return_value = "hashed_password"
    authenticator.create_access_token.return_value = "mock_access_token"
    authenticator.blacklist_token.return_value = True
    return authenticator


@pytest.fixture
def mock_user_repository():
    """Mock user repository for testing."""
    repository = AsyncMock()
    repository.find_by_username.return_value = None
    repository.find_by_email.return_value = None
    repository.create.return_value = None
    return repository


@pytest.fixture
def mock_review_repository():
    """Mock review repository for testing."""
    repository = AsyncMock()
    repository.find_by_user_id.return_value = []
    repository.create.return_value = None
    repository.find_by_id.return_value = None
    return repository


@pytest.fixture
def auth_headers():
    """Mock authenticated headers for protected endpoints."""
    return {"Authorization": "Bearer mock_access_token"}


@pytest.fixture
def base_url():
    """Base URL for the API."""
    return "http://localhost:8000"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    import asyncio

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
