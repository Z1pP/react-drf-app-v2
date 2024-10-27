from .dto import UserDTO
from .services import UserService
from .validators import BaseValidator


class GetAllUsersCommand:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def execute(self) -> list[UserDTO]:
        return self.user_service.get_all_users()


class CreateUserCommand:
    def __init__(self, user_service: UserService, validators: list[BaseValidator]):
        self.user_service = user_service
        self.validators = validators

    def execute(self, user: UserDTO) -> UserDTO:
        for validator in self.validators:
            validator.validate(user.__dict__)
        return self.user_service.create_user(user)


class GetUserByIdCommand:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def execute(self, user_id: int) -> UserDTO:
        return self.user_service.get_user_by_id(user_id)


class UpdateUserCommand:
    def __init__(self, user_service: UserService, validators: list[BaseValidator]):
        self.user_service = user_service
        self.validators = validators

    def execute(self, user_id: int, user: UserDTO) -> UserDTO:
        user_db = self.user_service.get_user_by_id(id=user_id)
        if not user_db:
            raise ValueError("User not found")
        for validator in self.validators:
            validator.validate(user.__dict__)
        return self.user_service.update_user(user_id, user)


class DeleteUserCommand:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def execute(self, user_id: int) -> None:
        user_db = self.user_service.get_user_by_id(id=user_id)
        if not user_db:
            raise ValueError("User not found")
        self.user_service.delete_user(user_id)
