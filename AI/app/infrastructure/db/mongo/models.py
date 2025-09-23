import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from beanie import Document, Indexed, PydanticObjectId
from pydantic import EmailStr, Field
from pymongo import IndexModel

from app.infrastructure.utils.hash import hash_password, verify_password


class User(Document):
    """User model for authentication"""

    id: Optional[PydanticObjectId] = Field(default_factory=PydanticObjectId)
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    password: str
    is_active: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Optional: Store user roles/permissions
    roles: List[str] = Field(default_factory=list)

    class Settings:
        name = "users"
        indexes = [
            IndexModel([("username", 1)], unique=True),
            IndexModel([("email", 1)], unique=True),
            IndexModel([("is_active", 1)]),
            IndexModel([("created_at", -1)]),
        ]

    def set_password(self, password: str) -> None:
        """Hash and set password"""
        self.password = hash_password(password)
        self.updated_at = datetime.utcnow()

    def check_password(self, password: str) -> bool:
        """Check if provided password matches stored hash"""
        return verify_password(password, self.password)

    @classmethod
    async def find_by_username(cls, username: str) -> Optional["User"]:
        """Find user by username"""
        return await cls.find_one(cls.username == username)

    @classmethod
    async def find_by_email(cls, email: str) -> Optional["User"]:
        """Find user by email"""
        return await cls.find_one(cls.email == email)

    @classmethod
    async def authenticate(cls, email: str, password: str) -> Optional["User"]:
        """Authenticate user with email and password"""
        user = await cls.find_by_email(email)
        if not user or not user.check_password(password):
            return None
        return user

    @classmethod
    async def create_user(
        cls, username: str, email: str, password: str, **kwargs
    ) -> "User":
        """Create a new user with hashed password"""
        user = cls(username=username, email=email, **kwargs)
        user.set_password(password)
        await user.insert()
        return user

    def __str__(self) -> str:
        return f"User(username={self.username}, email={self.email})"


class BlackListToken(Document):
    """Blacklisted JWT tokens model"""

    id: Optional[PydanticObjectId] = Field(default_factory=PydanticObjectId)
    token: Indexed(str, unique=True)
    expire: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "blacklist_tokens"
        indexes = [
            IndexModel([("token", 1)], unique=True),
            IndexModel([("expire", 1)]),
            IndexModel([("created_at", -1)]),
        ]

    @classmethod
    async def add_token(cls, token: str, expire: datetime) -> "BlackListToken":
        """Add a token to blacklist"""
        blacklist_token = cls(token=token, expire=expire)
        await blacklist_token.insert()
        return blacklist_token

    @classmethod
    async def is_blacklisted(cls, token: str) -> bool:
        """Check if token is blacklisted"""
        blacklist_token = await cls.find_one(cls.token == token)
        return blacklist_token is not None

    @classmethod
    async def cleanup_expired_tokens(cls) -> int:
        """Remove expired tokens from blacklist"""
        result = await cls.find(cls.expire < datetime.utcnow()).delete()
        return result.deleted_count




class Review(Document):
    """Review model for code reviews"""

    id: Optional[PydanticObjectId] = Field(default_factory=PydanticObjectId)
    user: PydanticObjectId  # Reference to User who created the review
    language: str
    status: str = Field(default="pending")  # pending, in_progress, completed, rejected
    created_at: datetime = Field(default_factory=datetime.utcnow)
    code_submission: str
    code_review: Optional[Dict[str, Any]] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "reviews"
        indexes = [
            IndexModel([("user", 1)]),  # Find reviews by user
            IndexModel([("language", 1)]),  # Find reviews by language
            IndexModel([("status", 1)]),  # Find reviews by status
            IndexModel([("created_at", -1)]),  # Sort by creation date (newest first)
            IndexModel([("updated_at", -1)]),  # Sort by update date (newest first)
            IndexModel([("user", 1), ("status", 1)]),  # Compound: user + status
            IndexModel([("language", 1), ("status", 1)]),  # Compound: language + status
            IndexModel([("user", 1), ("language", 1)]),  # Compound: user + language
        ]

    @classmethod
    async def find_by_user(cls, user_id: uuid.UUID) -> List["Review"]:
        """Find reviews by user"""
        return await cls.find(cls.user == user_id).to_list()

    @classmethod
    async def find_by_status(cls, status: str) -> List["Review"]:
        """Find reviews by status"""
        return await cls.find(cls.status == status).to_list()

    @classmethod
    async def find_by_language(cls, language: str) -> List["Review"]:
        """Find reviews by programming language"""
        return await cls.find(cls.language == language).to_list()

    @classmethod
    async def find_by_user_and_status(
        cls, user_id: uuid.UUID, status: str
    ) -> List["Review"]:
        """Find reviews by user and status"""
        return await cls.find((cls.user == user_id) & (cls.status == status)).to_list()

    @classmethod
    async def find_by_language_and_status(
        cls, language: str, status: str
    ) -> List["Review"]:
        """Find reviews by language and status"""
        return await cls.find(
            (cls.language == language) & (cls.status == status)
        ).to_list()

    @classmethod
    async def find_pending_reviews(cls) -> List["Review"]:
        """Find all pending reviews"""
        return await cls.find_by_status("pending")

    @classmethod
    async def find_completed_reviews(cls) -> List["Review"]:
        """Find all completed reviews"""
        return await cls.find_by_status("completed")

    def update_status(self, status: str) -> None:
        """Update review status"""
        self.status = status
        self.updated_at = datetime.utcnow()

    def add_review(self, code_review: dict) -> None:
        """Add review comments as JSON object"""
        self.code_review = code_review
        self.updated_at = datetime.utcnow()
        if self.status == "pending":
            self.status = "completed"

    def __str__(self) -> str:
        return f"Review(id={self.id}, user={self.user}, language={self.language}, status={self.status})"
