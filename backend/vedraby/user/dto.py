from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserDTO:
    id: Optional[int] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_staff: Optional[bool] = None
    is_superuser: Optional[bool] = None
    date_joined: Optional[datetime] = None

    def to_dict(self, exclude_none: bool = False) -> dict:
        if exclude_none:
            return {k: v for k, v in self.__dict__.items() if v is not None}
        return self.__dict__
