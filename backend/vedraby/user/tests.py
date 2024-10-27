from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import Mock, patch

from .dto import UserDTO
from .validators import UserCreateValidator, UserUpdateValidator
from .commands import (
    GetAllUsersCommand,
    CreateUserCommand,
    GetUserByIdCommand,
    UpdateUserCommand,
    DeleteUserCommand,
)
from .services import UserService
from .repository import UserRepository

User = get_user_model()


class UserValidatorTests(TestCase):
    def test_create_validator_valid_data(self):
        validator = UserCreateValidator()
        data = {"email": "test@example.com", "password": "password123"}
        try:
            validator.validate(data)
        except ValueError:
            self.fail("UserCreateValidator raised ValueError unexpectedly!")

    def test_create_validator_invalid_data(self):
        validator = UserCreateValidator()
        with self.assertRaises(ValueError):
            validator.validate({"email": "", "password": "short"})

    def test_update_validator_valid_data(self):
        validator = UserUpdateValidator()
        data = {"email": "new@example.com", "password": "newpassword123"}
        try:
            validator.validate(data)
        except ValueError:
            self.fail("UserUpdateValidator raised ValueError unexpectedly!")

    def test_update_validator_invalid_data(self):
        validator = UserUpdateValidator()
        with self.assertRaises(ValueError):
            validator.validate({"email": "", "password": "short"})


class UserCommandTests(TestCase):
    def setUp(self):
        self.repository = Mock(spec=UserRepository)

    def test_get_all_users_command(self):
        self.repository.get_all_users.return_value = [
            UserDTO(id=1, email="test@example.com")
        ]
        command = GetAllUsersCommand(self.repository)
        result = command.execute()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].email, "test@example.com")

    def test_create_user_command(self):
        validator = Mock(spec=UserCreateValidator)
        self.repository.create_user.return_value = UserDTO(
            id=1, email="new@example.com"
        )
        command = CreateUserCommand(self.repository, validator)
        user_dto = UserDTO(email="new@example.com", password="password123")
        result = command.execute(user_dto)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.email, "new@example.com")
        validator.validate.assert_called_once()

    def test_get_user_by_id_command(self):
        self.repository.get_user_by_id.return_value = UserDTO(
            id=1, email="test@example.com"
        )
        command = GetUserByIdCommand(self.repository)
        result = command.execute(1)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.email, "test@example.com")

    def test_update_user_command(self):
        validator = Mock(spec=UserUpdateValidator)
        self.repository.update_user.return_value = UserDTO(
            id=1, email="updated@example.com"
        )
        command = UpdateUserCommand(self.repository, validator)
        user_dto = UserDTO(email="updated@example.com")
        result = command.execute(1, user_dto)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.email, "updated@example.com")
        validator.validate.assert_called_once()

    def test_delete_user_command(self):
        command = DeleteUserCommand(self.repository)
        command.execute(1)
        self.repository.delete_user.assert_called_once_with(1)


class UserServiceTests(TestCase):
    def setUp(self):
        self.repository = Mock(spec=UserRepository)
        self.service = UserService(self.repository)

    @patch("user.commands.GetAllUsersCommand")
    def test_get_all_users(self, mock_command):
        mock_command.return_value.execute.return_value = [
            UserDTO(id=1, email="test@example.com")
        ]
        result = self.service.get_all_users()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].email, "test@example.com")

    @patch("user.commands.CreateUserCommand")
    def test_create_user(self, mock_command):
        mock_command.return_value.execute.return_value = UserDTO(
            id=1, email="new@example.com"
        )
        user_dto = UserDTO(email="new@example.com", password="password123")
        result = self.service.create_user(user_dto)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.email, "new@example.com")

    @patch("user.commands.GetUserByIdCommand")
    def test_get_user_by_id(self, mock_command):
        mock_command.return_value.execute.return_value = UserDTO(
            id=1, email="test@example.com"
        )
        result = self.service.get_user_by_id(1)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.email, "test@example.com")

    @patch("user.commands.UpdateUserCommand")
    def test_update_user(self, mock_command):
        mock_command.return_value.execute.return_value = UserDTO(
            id=1, email="updated@example.com"
        )
        user_dto = UserDTO(email="updated@example.com")
        result = self.service.update_user(1, user_dto)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.email, "updated@example.com")

    @patch("user.commands.DeleteUserCommand")
    def test_delete_user(self, mock_command):
        self.service.delete_user(1)
        mock_command.return_value.execute.assert_called_once_with(1)
