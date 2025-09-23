from typing import Optional, Protocol

from app.core.models.user import User


class UserRepositoryInterface(Protocol):
    """Interface for user repository - agnostic to database implementation"""

    async def find_by_username(self, username: str) -> Optional[User]:
        """Find a user by username"""
        pass

    async def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by email"""
        pass

    async def find_by_id(self, user_id: str) -> Optional[User]:
        """Find a user by ID"""
        pass

    async def create(self, user: User) -> User:
        """Create a new user"""
        pass

    async def update(self, user: User) -> User:
        """Update an existing user"""
        pass

    async def delete(self, user_id: str) -> bool:
        """Delete a user by ID"""
        pass
