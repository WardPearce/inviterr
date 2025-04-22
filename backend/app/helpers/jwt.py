from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

from litestar import Response
from litestar.connection import ASGIConnection
from litestar.security.jwt import JWTCookieAuth, Token

from app.env import SETTINGS
from app.models.session import SessionModel
from app.models.user import UserModel
from app.resources import Session


async def retrieve_user_handler(
    token: Token, connection: ASGIConnection[Any, Any, Any, Any]
) -> UserModel | None:
    valid_session = (
        await Session.mongo.session.count_documents(
            {"id": token.jti, "user_id": token.sub}
        )
        > 0
    )
    if not valid_session:
        return

    result = await Session.mongo.user.find_one({"id": token.sub})
    if not result:
        return

    return UserModel(**result)


async def login(identifier: str, user_agent: str | None) -> Response:
    token_expires = timedelta(days=31)
    now = datetime.now(tz=timezone.utc)

    session_id = str(uuid4())

    await Session.mongo.session.insert_one(
        SessionModel(
            expires=now + token_expires,
            created=now,
            device=user_agent,
            user_id=identifier,
            id=session_id,
        ).model_dump()
    )

    return JWT_AUTH.login(
        identifier=identifier,
        token_expiration=token_expires,
        token_unique_jwt_id=session_id,
    )


JWT_AUTH = JWTCookieAuth[UserModel](
    token_secret=SETTINGS.jwt_secret, retrieve_user_handler=retrieve_user_handler
)
