from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseValidator(ABC):
    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> None:
        pass


class EmailValidatorService(BaseValidator):
    def validate(self, data: Dict[str, Any]) -> None:
        pass


class PasswordValidatorService(BaseValidator):
    def validate(self, data: Dict[str, Any]) -> None:
        pass
