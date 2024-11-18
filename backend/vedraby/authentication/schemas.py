from ninja import Schema


class AccessTokenSchema(Schema):
    access_token: str
    token_type: str


class TokenInfoSchema(AccessTokenSchema):
    refresh_token: str | None = None
