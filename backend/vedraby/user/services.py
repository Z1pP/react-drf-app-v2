from user.dto import UserDTO
from user.repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user_and_check_password(self, email: str, password: str) -> UserDTO | None:
        user_db = self.repository.get_by_email(email=email)
        if not user_db:
            return None
        if user_db.check_password(raw_password=password):
            return user_db.to_dto()

    def get_all_users(self) -> list[UserDTO]:
        users_db = self.repository.all()
        return [user.to_dto() for user in users_db]

    def create_user(self, user: UserDTO) -> UserDTO:
        user_db = self.repository.create(user)
        return user_db.to_dto()

    def get_user_by_id(self, id: int) -> UserDTO:
        user_db = self.repository.get_by_id(id=id)
        if not user_db:
            return None
        return user_db.to_dto()

    def update_user(self, user_id: int, user: UserDTO) -> UserDTO:
        updated_data = user.to_dict(exclude_none=True)
        user_db = self.repository.update(id=user_id, **updated_data)
        return user_db.to_dto()

    def delete_user(self, user_id: int) -> None:
        self.repository.delete(user_id)
