from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """User domain model - agnostic to database implementation"""

    id: Optional[str] = None
    username: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    created_at: datetime = datetime.utcnow()


class UserCreate(BaseModel):
    """Model for user creation"""

    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """Model for user login"""

    username: str
    password: str


class UserResponse(BaseModel):
    """Model for user response (without password)"""

    id: str
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime


class Token(BaseModel):
    """Model for JWT token response"""
    username: str
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Model for token data"""

    username: Optional[str] = None
