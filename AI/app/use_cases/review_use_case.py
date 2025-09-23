from datetime import datetime
from typing import List, Optional

from app.core.models.review import Review
from app.interfaces.repositories.review_repository_interface import (
    ReviewRepositoryInterface,
)


class ReviewUseCase:
    def __init__(self, review_repository: ReviewRepositoryInterface):
        self.review_repository = review_repository

    async def create_review(self, review: Review) -> Review:
        return await self.review_repository.create(review)

    async def update_review(self, review: Review) -> Review:
        return await self.review_repository.update(review)

    async def delete_review(self, review_id: str) -> bool:
        return await self.review_repository.delete(review_id)

    async def get_review_by_id(self, review_id: str) -> Optional[Review]:
        return await self.review_repository.find_by_id(review_id)

    async def get_reviews_by_user(self, user_id: str) -> List[Review]:
        return await self.review_repository.find_by_user(user_id)

    async def get_reviews_by_status(self, status: str) -> List[Review]:
        return await self.review_repository.find_by_status(status)

    async def get_reviews_by_language(self, language: str) -> List[Review]:
        return await self.review_repository.find_by_language(language)

    async def get_reviews_by_user_with_filters(
        self,
        user_id: str,
        language: Optional[str] = None,
        status: Optional[str] = None,
        score: Optional[int] = None,
    ) -> List[Review]:
        return await self.review_repository.find_by_user_with_filters(
            user_id, language, status, score
        )
