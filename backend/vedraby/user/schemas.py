from dataclasses import asdict
from datetime import datetime
from typing import Optional, Self

from ninja.schema import Schema

from user.dto import UserDTO


class UserInSchema(Schema):
    email: str
    password: str

    def to_dto(self) -> UserDTO:
        return UserDTO(email=self.email, password=self.password)


class UserUpdateSchema(Schema):
    email: Optional[str] = None
    password: Optional[str] = None

    def to_dto(self) -> UserDTO:
        return UserDTO(email=self.email, password=self.password)


class UserResponseSchema(Schema):
    id: int
    email: str
    first_name: str
    last_name: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
    date_joined: datetime

    @classmethod
    def to_response(cls, dto: UserDTO) -> Self:
        return cls(**asdict(dto))
