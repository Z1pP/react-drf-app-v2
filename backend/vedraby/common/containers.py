import punq

from user.repository import UserRepository, BaseUserRepository
from user.services import UserService
from authentication.services import TokenService, AuthBearerService
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
from authentication.commands import CreateTokenCommand, RefreshTokenCommand

container = punq.Container()

# Repositories
container.register(BaseUserRepository, UserRepository)
container.register(UserRepository)

# Services
container.register(UserService)
container.register(TokenService)
container.register(AuthBearerService)
# Validators
container.register(BaseValidator, EmailValidatorService)
container.register(BaseValidator, PasswordValidatorService)

# Commands
container.register(GetAllUsersCommand)
container.register(CreateUserCommand)
container.register(GetUserByIdCommand)
container.register(UpdateUserCommand)
container.register(DeleteUserCommand)
container.register(CreateTokenCommand)
container.register(RefreshTokenCommand)
