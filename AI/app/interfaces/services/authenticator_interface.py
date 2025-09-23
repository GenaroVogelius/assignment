from datetime import timedelta
from typing import Optional, Protocol

from app.core.models.user import TokenData, User


class AuthenticatorInterface(Protocol):
    """Interface defining the contract for authentication operations"""

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user with username and password"""
        pass

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        pass

    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        pass

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ):
        """Create a JWT access token"""
        pass

    async def verify_token(self, token: str) -> TokenData:
        """Verify and decode a JWT token"""
        pass

    async def get_current_user(self, token: str) -> User:
        """Get the current authenticated user from token"""
        pass

    async def get_current_active_user(self, current_user: User) -> User:
        """Get the current active user"""
        pass

    async def blacklist_token(self, token: str) -> bool:
        """Add a token to the blacklist"""
        pass

    async def is_token_blacklisted(self, token: str) -> bool:
        """Check if a token is blacklisted"""
        pass
