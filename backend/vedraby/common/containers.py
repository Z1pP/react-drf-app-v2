import punq

from user.repository import UserRepository, BaseUserRepository
from user.services import UserService
from user.validators import (
    BaseValidator,
    EmailValidatorService,
    PasswordValidatorService,
)
from user.commands import (
    GetAllUsersCommand,
    CreateUserCommand,
    GetUserByIdCommand,
    UpdateUserCommand,
    DeleteUserCommand,
)

container = punq.Container()

# Repositories
container.register(BaseUserRepository, UserRepository)
container.register(UserRepository)

# Services
container.register(UserService)

# Validators
container.register(BaseValidator, EmailValidatorService)
container.register(BaseValidator, PasswordValidatorService)

# Commands
container.register(GetAllUsersCommand)
container.register(CreateUserCommand)
container.register(GetUserByIdCommand)
container.register(UpdateUserCommand)
container.register(DeleteUserCommand)
