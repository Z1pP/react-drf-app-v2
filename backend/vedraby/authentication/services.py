from datetime import datetime, timedelta
from typing import Any, Literal
import jwt
from ninja.errors import HttpError
from ninja.security import HttpBearer
from django.conf import settings

from user.dto import UserDTO
from user.services import UserService

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


class TokenService:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service
        self.access_token_expire_minutes = settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_minutes = settings.AUTH_REFRESH_TOKEN_EXPIRE_MINUTES
        self.secret_key = settings.AUTH_JWT_SECRET_KEY
        self.algorithm = settings.AUTH_JWT_ALGORITHM

    def create_access_token(self, user: UserDTO) -> str:
        expire_delta = timedelta(minutes=self.access_token_expire_minutes)
        return self._create_token(
            subject=str(user.id),
            token_type=ACCESS_TOKEN_TYPE,
            expire_delta=expire_delta,
            extra_claims={"email": user.email},
        )

    def create_refresh_token(self, user: UserDTO) -> str:
        expire_delta = timedelta(minutes=self.refresh_token_expire_minutes)
        return self._create_token(
            subject=str(user.id),
            token_type=REFRESH_TOKEN_TYPE,
            expire_delta=expire_delta,
        )

    def _create_token(
        self,
        subject: str,
        token_type: Literal["access", "refresh"],
        expire_delta: timedelta,
        extra_claims: dict[str, Any] = None,
    ) -> str:

        now = datetime.utcnow()

        claims = {
            "sub": subject,
            "type": token_type,
            "iat": now,
            "exp": now + expire_delta,
        }

        if extra_claims:
            claims.update(extra_claims)

        return jwt.encode(claims, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HttpError(401, "Token has expired")
        except jwt.InvalidTokenError:
            raise HttpError(401, "Invalid token")

    def verify_token_type(self, payload: dict, expected_type: str) -> None:
        token_type = payload.get(TOKEN_TYPE_FIELD)
        if token_type != expected_type:
            raise HttpError(401, f"Invalid token type. Expected {expected_type}")

    def _get_user_id_from_token(self, payload: dict) -> int:
        user_id = payload.get("sub")
        if not user_id:
            raise HttpError(401, "Invalid token payload: missing user ID")
        return int(user_id)

    def refresh_token(self, refresh_token: str) -> str:
        payload = self.decode_token(refresh_token)
        self.verify_token_type(payload, REFRESH_TOKEN_TYPE)

        user_id = self._get_user_id_from_token(payload)
        user_db = self.user_service.get_user_by_id(user_id)

        return self.create_access_token(user_db)


class AuthBearerService(HttpBearer):
    def __init__(self, token_service: TokenService, user_service: UserService):
        self.token_service = token_service
        self.user_service = user_service

    def authenticate(self, request, token: str) -> UserDTO:
        try:
            payload = self.token_service.decode_token(token)
            self.token_service.verify_token_type(payload, ACCESS_TOKEN_TYPE)

            user_id = self.token_service._get_user_id_from_token(payload)
            return self.user_service.get_user_by_id(user_id)

        except HttpError as e:
            raise e
        except Exception as e:
            raise HttpError(401, f"Authentication failed: {str(e)}")
