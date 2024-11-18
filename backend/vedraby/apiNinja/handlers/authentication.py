from ninja import Router

from common.containers import container
from authentication.commands import CreateTokenCommand, RefreshTokenCommand
from authentication.schemas import TokenInfoSchema, AccessTokenSchema

router = Router()


@router.post("/token", response=TokenInfoSchema, operation_id="create_token")
def create_token(request, email: str, password: str) -> TokenInfoSchema:
    command: CreateTokenCommand = container.resolve(CreateTokenCommand)
    token_info = command.execute(email=email, password=password)
    return TokenInfoSchema(**token_info)


@router.post("/refresh", response=AccessTokenSchema, operation_id="refresh_token")
def refresh_token(request, refresh_token: str) -> AccessTokenSchema:
    command: RefreshTokenCommand = container.resolve(RefreshTokenCommand)
    token_info = command.execute(refresh_token=refresh_token)
    return AccessTokenSchema(**token_info)
