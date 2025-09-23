"""
Abstract dependencies for the application.
This module provides dependency injection functions that are database-agnostic.
"""

from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.infrastructure.factories.repository_factory import RepositoryFactory
from app.infrastructure.services.authenticator_jwt import AuthenticatorJWT
from app.interfaces.repositories.review_repository_interface import (
    ReviewRepositoryInterface,
)
from app.interfaces.repositories.user_repository_interface import (
    UserRepositoryInterface,
)
from app.interfaces.services.authenticator_interface import AuthenticatorInterface

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token security
security = HTTPBearer()

# Rate limiter instance
limiter = Limiter(key_func=get_remote_address)


def get_user_repository() -> UserRepositoryInterface:
    """
    Get user repository instance using factory pattern.
    This function is database-agnostic and will use the configured database type.
    """
    return RepositoryFactory.create_user_repository()


def get_authenticator() -> AuthenticatorInterface:
    """
    Get authenticator instance with dependencies.
    This function is database-agnostic and will use the configured repository.
    """
    user_repository = get_user_repository()
    return AuthenticatorJWT(
        security=security, pwd_context=pwd_context, user_repository=user_repository
    )


def get_review_repository() -> ReviewRepositoryInterface:
    """
    Get review repository instance using factory pattern.
    This function is database-agnostic and will use the configured database type.
    """
    return RepositoryFactory.create_review_repository()


def get_rate_limiter():
    """
    Get rate limiter instance for IP-based rate limiting.
    """
    return limiter
