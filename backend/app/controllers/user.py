import asyncio
from typing import Any

from argon2.exceptions import VerifyMismatchError
from litestar import Controller, Request, Router, get, post
from litestar.exceptions import NotAuthorizedException
from litestar.response import Response
from litestar.security.jwt import Token
from plexapi.myplex import MyPlexAccount
from plexapi.myplex import Unauthorized as PlexUnauthorized

from app.helpers.jwt import login
from app.helpers.misc import PASSWORD_HASHER
from app.helpers.user import User, user_from_name
from app.models.user import LoginModel, UserModel
from app.services.platform.emby import EmbyPlatform
from app.services.platform.jellyfin import JellyfinPlatform


class UserController(Controller):
    @post("/login", description="User login")
    async def login(self, request: Request, data: LoginModel) -> Response:
        if data.auth_type in ("jellyfinOrEmby", "local"):
            if not data.username:
                raise NotAuthorizedException()

            user_obj = await user_from_name(data.username)
            user = await user_obj.get()

            if data.auth_type == "local":
                if not user.password:
                    raise NotAuthorizedException()

                try:
                    PASSWORD_HASHER.verify(user.password, data.password)
                except VerifyMismatchError:
                    raise NotAuthorizedException()
            else:
                auth_checks = []

                async for platform in user_obj.platforms():
                    match platform.platform:
                        case "jellyfin":
                            auth_checks.append(
                                JellyfinPlatform(platform).login(
                                    data.username, data.password
                                )
                            )
                        case "emby":
                            auth_checks.append(
                                EmbyPlatform(platform).login(
                                    data.username, data.password
                                )
                            )

                auth_check_results = await asyncio.gather(
                    *auth_checks, return_exceptions=False
                )

                # Any failed checks won't be returned
                if not auth_check_results:
                    raise NotAuthorizedException()

        else:
            loop = asyncio.get_event_loop()

            try:
                user_account = await loop.run_in_executor(
                    None, lambda: MyPlexAccount(token=data.password)
                )
            except PlexUnauthorized:
                raise NotAuthorizedException()

            user = await User(user_account.email).get()

        return await login(user.id, request.headers.get("User-Agent", None))

    @get("/me", description="Get info about myself")
    async def me(self, request: Request[UserModel, Token, Any]) -> UserModel:
        return await User(request.user.id).get()


router = Router(
    "/user",
    route_handlers=[UserController],
    tags=["user"],
)
