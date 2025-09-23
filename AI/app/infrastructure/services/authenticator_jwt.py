from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config.settings import Settings
from app.core.models.user import TokenData, User
from app.infrastructure.db.mongo.models import BlackListToken
from app.interfaces.repositories.user_repository_interface import (
    UserRepositoryInterface,
)
from app.interfaces.services.authenticator_interface import AuthenticatorInterface


class AuthenticatorJWT(AuthenticatorInterface):
    def __init__(
        self,
        security: HTTPBearer,
        pwd_context: CryptContext,
        user_repository: UserRepositoryInterface,
    ):
        self.security = security
        self.pwd_context = pwd_context
        self.user_repository = user_repository
        self.settings = Settings()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        return self.pwd_context.hash(password)

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ):
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.settings.SECRET_KEY, algorithm=self.settings.HASH_ALGORITHM
        )
        return encoded_jwt

    async def verify_token(self, token: str) -> TokenData:
        """Verify and decode a JWT token"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        # Check if token is blacklisted
        if await self.is_token_blacklisted(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            payload = jwt.decode(
                token,
                self.settings.SECRET_KEY,
                algorithms=[self.settings.HASH_ALGORITHM],
            )
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception

        return token_data

    async def get_current_user(self, token: str) -> User:
        """Get the current authenticated user from token"""
        token_data = await self.verify_token(token)

        if token_data.username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token data",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = await self.user_repository.find_by_username(token_data.username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    async def get_current_active_user(self, current_user: User) -> User:
        """Get the current active user"""
        if not current_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
            )
        return current_user

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user with username and password"""
        user = await self.user_repository.find_by_username(username)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user

    async def blacklist_token(self, token: str) -> bool:
        """Add a token to the blacklist"""
        try:
            # Decode token to get expiration time
            payload = jwt.decode(
                token,
                self.settings.SECRET_KEY,
                algorithms=[self.settings.HASH_ALGORITHM],
            )
            expire_timestamp = payload.get("exp")
            if expire_timestamp:
                expire_datetime = datetime.fromtimestamp(expire_timestamp)
                await BlackListToken.add_token(token, expire_datetime)
                return True
            return False
        except JWTError:
            # If token is invalid, we can still blacklist it
            # Set a default expiration time (24 hours from now)
            expire_datetime = datetime.utcnow() + timedelta(hours=24)
            await BlackListToken.add_token(token, expire_datetime)
            return True
        except Exception:
            return False

    async def is_token_blacklisted(self, token: str) -> bool:
        """Check if a token is blacklisted"""
        try:
            return await BlackListToken.is_blacklisted(token)
        except Exception:
            return False
