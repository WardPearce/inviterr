from typing import Any, Callable

from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.handlers.base import BaseRouteHandler

from app.models.roles import ROLES
from app.models.user import UserModel


def user_roles_guard(required_roles: list[str]) -> Callable[[ASGIConnection[Any, UserModel, Any, Any], BaseRouteHandler], None]:
    def check(
        connection: ASGIConnection[Any, UserModel, Any, Any], _: BaseRouteHandler
    ) -> None:
        # Allow root API access
        if ROLES.root in connection.user.roles:
            return

        if not all(role in connection.user.roles for role in required_roles):
            raise NotAuthorizedException()

    return check
