from typing import Optional

from app.core.models.user import User
from app.interfaces.services.authenticator_interface import AuthenticatorInterface


class AuthenticateUseCase:
    def __init__(self, authenticator: AuthenticatorInterface):
        self.authenticator = authenticator

    async def execute(self, username: str, password: str) -> Optional[User]:
        return await self.authenticator.authenticate_user(username, password)
