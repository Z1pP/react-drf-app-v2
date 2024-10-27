from user.dto import UserDTO
from user.repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_all_users(self) -> list[UserDTO]:
        users_db = self.repository.all()
        return [user.to_dto() for user in users_db]

    def create_user(self, user: UserDTO) -> UserDTO:
        user_db = self.repository.create(user)
        return user_db.to_dto()

    def get_user_by_id(self, id: int) -> UserDTO:
        user_db = self.repository.get(id=id)
        return user_db.to_dto()

    def update_user(self, user_id: int, user: UserDTO) -> UserDTO:
        updated_data = user.to_dict(exclude_none=True)
        user_db = self.repository.update(id=user_id, **updated_data)
        return user_db.to_dto()

    def delete_user(self, user_id: int) -> None:
        self.repository.delete(user_id)
