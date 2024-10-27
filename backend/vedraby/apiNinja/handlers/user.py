from ninja import Router
from ninja.errors import HttpError

from user.models import CustomUser
from user.schemas import UserInSchema, UserResponseSchema, UserUpdateSchema
from user.commands import (
    GetAllUsersCommand,
    CreateUserCommand,
    GetUserByIdCommand,
    UpdateUserCommand,
    DeleteUserCommand,
)
from common.containers import container

router = Router()


@router.get("/", response=list[UserResponseSchema], operation_id="get_all_users")
def get_users(request) -> list[UserResponseSchema]:
    command: GetAllUsersCommand = container.resolve(GetAllUsersCommand)
    try:
        users_dto = command.execute()
        return [UserResponseSchema.to_response(user) for user in users_dto]
    except ValueError as e:
        raise HttpError(400, str(e))


@router.post(
    "/",
    response=UserResponseSchema,
    operation_id="create_new_user",
)
def create_user(request, user: UserInSchema) -> UserResponseSchema:
    command: CreateUserCommand = container.resolve(CreateUserCommand)
    try:
        user_dto = command.execute(user=user.to_dto())
        return UserResponseSchema.to_response(user_dto)
    except ValueError as e:
        raise HttpError(400, str(e))


@router.get("/{user_id}", response=UserResponseSchema, operation_id="get_current_user")
def get_user_by_id(request, user_id: int) -> UserResponseSchema:
    command: GetUserByIdCommand = container.resolve(GetUserByIdCommand)
    try:
        user_dto = command.execute(user_id=user_id)
        return UserResponseSchema.to_response(user_dto)
    except CustomUser.DoesNotExist:
        raise HttpError(404, "User not found")


@router.patch(
    "/{user_id}", response=UserResponseSchema, operation_id="update_current_user"
)
def update_user(request, user_id: int, user: UserUpdateSchema) -> UserResponseSchema:
    command: UpdateUserCommand = container.resolve(UpdateUserCommand)
    try:
        user_dto = command.execute(user_id=user_id, user=user.to_dto())
        return UserResponseSchema.to_response(user_dto)
    except CustomUser.DoesNotExist:
        raise HttpError(404, "User not found")


@router.delete("/{user_id}", operation_id="delete_user")
def delete_user(request, user_id: int) -> None:
    command: DeleteUserCommand = container.resolve(DeleteUserCommand)
    try:
        command.execute(user_id=user_id)
    except CustomUser.DoesNotExist:
        raise HttpError(404, "User not found")
