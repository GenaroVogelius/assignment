from typing import List, Optional

from beanie import PydanticObjectId

from app.core.models.review import CodeReviewIAResponse, Review
from app.core.models.user import User
from app.infrastructure.db.mongo.models import Review as MongoReview
from app.infrastructure.db.mongo.models import User as MongoUser
from app.interfaces.repositories.review_repository_interface import (
    ReviewRepositoryInterface,
)
from app.interfaces.repositories.user_repository_interface import (
    UserRepositoryInterface,
)


class MongoUserRepository(UserRepositoryInterface):
    """MongoDB implementation of UserRepositoryInterface"""

    async def find_by_username(self, username: str) -> Optional[User]:
        """Find a user by username"""
        mongo_user = await MongoUser.find_one(MongoUser.username == username)
        if not mongo_user:
            return None

        return self._mongo_to_domain(mongo_user)

    async def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by email"""
        mongo_user = await MongoUser.find_one(MongoUser.email == email)
        if not mongo_user:
            return None

        return self._mongo_to_domain(mongo_user)

    async def find_by_id(self, user_id: str) -> Optional[User]:
        """Find a user by ID"""
        mongo_user = await MongoUser.get(user_id)
        if not mongo_user:
            return None

        return self._mongo_to_domain(mongo_user)

    async def create(self, user: User) -> User:
        """Create a new user"""
        mongo_user = MongoUser(
            username=user.username,
            email=user.email,
            password=user.hashed_password,
            is_active=user.is_active,
            created_at=user.created_at,
        )
        await mongo_user.insert()

        return self._mongo_to_domain(mongo_user)

    async def update(self, user: User) -> User:
        """Update an existing user"""
        mongo_user = await MongoUser.get(user.id)
        if not mongo_user:
            raise ValueError(f"User with id {user.id} not found")

        mongo_user.username = user.username
        mongo_user.email = user.email
        mongo_user.password = user.hashed_password
        mongo_user.is_active = user.is_active

        await mongo_user.save()

        return self._mongo_to_domain(mongo_user)

    async def delete(self, user_id: str) -> bool:
        """Delete a user by ID"""
        mongo_user = await MongoUser.get(user_id)
        if not mongo_user:
            return False

        await mongo_user.delete()
        return True

    def _mongo_to_domain(self, mongo_user: MongoUser) -> User:
        """Convert MongoDB user to domain user"""
        return User(
            id=str(mongo_user.id),
            username=mongo_user.username,
            email=mongo_user.email,
            hashed_password=mongo_user.password,
            is_active=mongo_user.is_active,
            created_at=mongo_user.created_at,
        )


class MongoReviewRepository(ReviewRepositoryInterface):
    """MongoDB implementation of ReviewRepositoryInterface"""

    async def find_by_id(self, review_id: str) -> Optional[Review]:
        """Find a review by ID"""
        try:
            # Convert string to PydanticObjectId
            object_id = PydanticObjectId(review_id)
            mongo_review = await MongoReview.get(object_id)
            if not mongo_review:
                return None

            return self._mongo_to_domain(mongo_review)
        except Exception:
            # If conversion fails or review not found, return None
            return None

    async def create(self, review: Review) -> Review:
        """Create a new review"""
        try:
            # Convert user string to PydanticObjectId
            user_object_id = PydanticObjectId(review.user)
            mongo_review = MongoReview(
                user=user_object_id,
                language=review.language.lower().strip(),  # Normalize language to lowercase and trim whitespace
                status=review.status,
                code_submission=review.code_submission,
                code_review=review.code_review.model_dump()
                if review.code_review
                else None,
                created_at=review.created_at,
            )
            await mongo_review.insert()

            return self._mongo_to_domain(mongo_review)
        except Exception as e:
            raise ValueError(f"Failed to create review: {str(e)}")

    async def update(self, review: Review) -> Review:
        """Update an existing review"""
        try:
            object_id = PydanticObjectId(review.id)
            mongo_review = await MongoReview.get(object_id)
            if not mongo_review:
                raise ValueError(f"Review with id {review.id} not found")

            mongo_review.user = PydanticObjectId(review.user)
            mongo_review.language = review.language
            mongo_review.status = review.status
            mongo_review.code_submission = review.code_submission
            mongo_review.code_review = (
                review.code_review.model_dump() if review.code_review else None
            )

            await mongo_review.save()

            return self._mongo_to_domain(mongo_review)
        except Exception as e:
            raise ValueError(f"Review with id {review.id} not found: {str(e)}")

    async def delete(self, review_id: str) -> bool:
        """Delete a review by ID"""
        try:
            object_id = PydanticObjectId(review_id)
            mongo_review = await MongoReview.get(object_id)
            if not mongo_review:
                return False

            await mongo_review.delete()
            return True
        except Exception:
            return False

    async def find_by_user(self, user_id: str) -> List[Review]:
        """Find all reviews by user ID"""
        try:
            object_id = PydanticObjectId(user_id)
            mongo_reviews = await MongoReview.find(
                MongoReview.user == object_id
            ).to_list()
            return [self._mongo_to_domain(review) for review in mongo_reviews]
        except Exception:
            return []

    async def find_by_status(self, status: str) -> List[Review]:
        """Find all reviews by status"""
        mongo_reviews = await MongoReview.find(MongoReview.status == status).to_list()
        return [self._mongo_to_domain(review) for review in mongo_reviews]

    async def find_by_language(self, language: str) -> List[Review]:
        """Find all reviews by language"""
        normalized_language = language.lower().strip()
        mongo_reviews = await MongoReview.find(
            MongoReview.language == normalized_language
        ).to_list()
        return [self._mongo_to_domain(review) for review in mongo_reviews]

    async def find_by_user_with_filters(
        self,
        user_id: str,
        language: Optional[str] = None,
        status: Optional[str] = None,
        score: Optional[int] = None,
    ) -> List[Review]:
        """Find reviews by user with optional filters"""
        try:
            object_id = PydanticObjectId(user_id)

            # Build query dictionary
            query_dict: dict = {"user": object_id}

            # Add optional filters
            if language:
                normalized_language = language.lower().strip()
                query_dict["language"] = normalized_language

            if status:
                query_dict["status"] = status

            if score:
                query_dict["code_review.overall_score"] = score

            # Execute query using dictionary
            mongo_reviews = await MongoReview.find(query_dict).to_list()
            return [self._mongo_to_domain(review) for review in mongo_reviews]
        except Exception as e:
            print(f"Error in find_by_user_with_filters: {e}")
            return []

    def _mongo_to_domain(self, mongo_review: MongoReview) -> Review:
        """Convert MongoDB review to domain review"""
        # Convert code_review dict back to CodeReviewIAResponse if it exists
        code_review = None
        if mongo_review.code_review and isinstance(mongo_review.code_review, dict):
            try:
                code_review = CodeReviewIAResponse(**mongo_review.code_review)
            except Exception:
                # If conversion fails, keep as None
                code_review = None

        return Review(
            id=str(mongo_review.id),
            user=str(mongo_review.user),
            language=mongo_review.language,
            status=mongo_review.status,
            code_submission=mongo_review.code_submission,
            code_review=code_review,
            created_at=mongo_review.created_at,
            updated_at=mongo_review.updated_at,
        )
