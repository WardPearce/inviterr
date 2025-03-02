from typing import Any

from app.env import SETTINGS
from app.models.user import UserModel
from app.resources import Session
from litestar.connection import ASGIConnection
from litestar.security.jwt import JWTCookieAuth, Token


async def retrieve_user_handler(
    token: Token, connection: ASGIConnection[Any, Any, Any, Any]
) -> UserModel | None:
    result = await Session.mongo.user.find_one({"id": token.sub})
    if not result:
        return

    return UserModel(**result)


JWT_AUTH = JWTCookieAuth[UserModel](
    token_secret=SETTINGS.jwt_secret, retrieve_user_handler=retrieve_user_handler
)
