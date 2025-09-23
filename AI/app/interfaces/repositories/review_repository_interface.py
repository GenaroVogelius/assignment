from datetime import datetime
from typing import List, Optional, Protocol

from app.core.models.review import Review


class ReviewRepositoryInterface(Protocol):
    """Interface for review repository - agnostic to database implementation"""

    async def find_by_id(self, review_id: str) -> Optional[Review]:
        """Find a review by ID"""
        pass

    async def create(self, review: Review) -> Review:
        """Create a new review"""
        pass

    async def update(self, review: Review) -> Review:
        """Update an existing review"""
        pass

    async def delete(self, review_id: str) -> bool:
        """Delete a review by ID"""
        pass

    async def find_by_user(self, user_id: str) -> List[Review]:
        """Find all reviews by user ID"""
        pass

    async def find_by_status(self, status: str) -> List[Review]:
        """Find all reviews by status"""
        pass

    async def find_by_language(self, language: str) -> List[Review]:
        """Find all reviews by language"""
        pass

    async def find_by_user_with_filters(
        self,
        user_id: str,
        language: Optional[str] = None,
        status: Optional[str] = None,
        score: Optional[int] = None,
    ) -> List[Review]:
        """Find reviews by user with optional filters"""
        pass
