from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config.settings import Settings
from app.core.models.user import Token, User, UserCreate, UserLogin, UserResponse
from app.infrastructure.dependencies import get_authenticator, get_user_repository
from app.infrastructure.logger import logger
from app.interfaces.repositories.user_repository_interface import (
    UserRepositoryInterface,
)
from app.interfaces.services.authenticator_interface import AuthenticatorInterface


class AuthRoutes:
    def __init__(self):
        self.router = APIRouter()
        self.settings = Settings()
        self._setup_routes()

    async def get_current_active_user_dependency(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
        authenticator: AuthenticatorInterface = Depends(get_authenticator),
    ) -> User:
        """Dependency to get current active user using authenticator"""
        token = credentials.credentials
        current_user = await authenticator.get_current_user(token)
        return await authenticator.get_current_active_user(current_user)

    def _setup_routes(self):
        @self.router.post(
            "/register",
            response_model=UserResponse,
            status_code=status.HTTP_201_CREATED,
        )
        async def register(
            user_data: UserCreate,
            authenticator: AuthenticatorInterface = Depends(get_authenticator),
            user_repository: UserRepositoryInterface = Depends(get_user_repository),
        ):
            """Register a new user"""
            try:
                # Check if user already exists
                existing_user = await user_repository.find_by_username(
                    user_data.username
                )
                if existing_user:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Username already registered",
                    )

                # Check if email already exists
                existing_email = await user_repository.find_by_email(user_data.email)
                if existing_email:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already registered",
                    )

                # Create new user
                hashed_password = authenticator.get_password_hash(user_data.password)
                user = User(
                    username=user_data.username,
                    email=user_data.email,
                    hashed_password=hashed_password,
                )

                created_user = await user_repository.create(user)
                logger.info(f"New user registered: {user_data.username}")

                return UserResponse(
                    id=str(created_user.id),
                    username=created_user.username,
                    email=created_user.email,
                    is_active=created_user.is_active,
                    created_at=created_user.created_at,
                )

            except HTTPException:
                # Re-raise HTTPExceptions (like 400 for duplicate username/email)
                raise
            except Exception as e:
                logger.error(f"Error registering user: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error creating user",
                )

        @self.router.post("/login", response_model=Token)
        async def login(
            user_credentials: UserLogin,
            authenticator: AuthenticatorInterface = Depends(get_authenticator),
        ):
            """Login user and return access token"""
            try:
                user = await authenticator.authenticate_user(
                    user_credentials.username, user_credentials.password
                )
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Incorrect username or password",
                        headers={"WWW-Authenticate": "Bearer"},
                    )

                if not user.is_active:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
                    )

                access_token_expires = timedelta(
                    minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES
                )
                access_token = authenticator.create_access_token(
                    data={"sub": user.username}, expires_delta=access_token_expires
                )

                return Token(
                    username=user.username.capitalize(),
                    access_token=access_token,
                    token_type="bearer",
                    expires_in=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                )

            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Error during login: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error during authentication",
                )

        @self.router.post("/logout")
        async def logout(
            credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
            authenticator: AuthenticatorInterface = Depends(get_authenticator),
        ):
            """
            Logout user and blacklist token

            This endpoint:
            1. Extracts the JWT token from the Authorization header
            2. Adds the token to the blacklist in the database
            3. Returns a success message

            After logout, the token will be invalid for all future requests.

            Headers required:
            - Authorization: Bearer <token>

            Returns:
            - 200: Success message
            - 403: If token is missing (handled by HTTPBearer dependency)
            """
            try:
                token = credentials.credentials

                # Blacklist the token
                success = await authenticator.blacklist_token(token)

                if success:
                    logger.info("User logged out successfully - token blacklisted")
                    return {"message": "Successfully logged out"}
                else:
                    logger.warning("Failed to blacklist token during logout")
                    return {"message": "Logged out (token blacklist failed)"}

            except Exception as e:
                logger.error(f"Error during logout: {str(e)}")
                # Even if blacklisting fails, we can still return success
                # as the client should discard the token anyway
                return {"message": "Logged out"}
