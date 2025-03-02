from typing import Callable

from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.handlers.base import BaseRouteHandler


def user_roles_guard(required_roles: list[str]) -> Callable:
    def check(connection: ASGIConnection, _: BaseRouteHandler) -> None:
        if all(role in connection.user.roles for role in required_roles):
            raise NotAuthorizedException()

    return check
