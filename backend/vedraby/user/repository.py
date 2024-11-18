from abc import ABC, abstractmethod

from .models import CustomUser


class BaseUserRepository(ABC):
    @abstractmethod
    def create(self, email: str, password: str) -> CustomUser:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> CustomUser:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> CustomUser:
        pass

    @abstractmethod
    def all(self) -> list[CustomUser]:
        pass

    @abstractmethod
    def update(self, id: int, **kwargs) -> CustomUser:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass


class UserRepository(BaseUserRepository):
    def all(self) -> list[CustomUser]:
        return CustomUser.objects.all()

    def create(self, email: str, password: str) -> CustomUser:
        return CustomUser.objects.create(email=email, password=password)

    def get_by_id(self, id: int) -> CustomUser | None:
        try:
            return CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            return None

    def get_by_email(self, email: str) -> CustomUser | None:
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None

    def update(self, id: int, **kwargs) -> CustomUser:
        user = self.get_by_id(id)
        for key, value in kwargs.items():
            if value is not None:
                setattr(user, key, value)
        user.save()
        return user

    def delete(self, id: int) -> None:
        CustomUser.objects.filter(id=id).delete()
