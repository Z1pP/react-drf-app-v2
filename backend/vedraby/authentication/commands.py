from typing import Any
from ninja.errors import HttpError
from django.conf import settings

from authentication.services import TokenService
from user.services import UserService


class CreateTokenCommand:
    def __init__(self, token_service: TokenService, user_service: UserService):
        self.token_service = token_service
        self.user_service = user_service

    def execute(self, email: str, password: str) -> dict[str, Any]:
        user_dto = self.user_service.get_user_and_check_password(
            email=email, password=password
        )

        if not user_dto:
            raise HttpError(status_code=401, message="Invalid credentials")

        access_token = self.token_service.create_access_token(user=user_dto)
        refresh_token = self.token_service.create_refresh_token(user=user_dto)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": settings.AUTH_TOKEN_TYPE,
        }


class RefreshTokenCommand:
    def __init__(self, token_service: TokenService):
        self.token_service = token_service

    def execute(self, refresh_token: str) -> dict[str, Any]:
        new_access_token = self.token_service.refresh_token(refresh_token=refresh_token)
        return {
            "access_token": new_access_token,
            "token_type": settings.AUTH_TOKEN_TYPE,
        }
