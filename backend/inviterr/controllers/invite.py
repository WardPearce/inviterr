import asyncio

import bcrypt
from inviterr.models.invite.internal import InviteModel
from inviterr.models.invite.redeem import RedeemInviteModel
from inviterr.models.platform import PlatformModel
from inviterr.resources import Session
from inviterr.services.platform.jellyfin import JellyfinPlatform
from litestar import Controller, Router, post
from litestar.exceptions import ClientException, NotAuthorizedException


class InviteController(Controller):
    path = "/public"

    @post(
        description="Allows for redeeming a invitation code", tags=["invite", "public"]
    )
    async def create(self, data: RedeemInviteModel) -> None:
        if not data.jellyfin_emby_auth and not data.plex_token:
            raise ClientException(
                detail="Must have at least jellyfin_emby_auth or plex_token defined"
            )

        try:
            id_, password = data.code.split("-", 1)
        except ValueError:
            raise NotAuthorizedException()

        result = await Session.mongo.invite.find_one({"_id": id_})
        if not result:
            raise NotAuthorizedException()

        invite = InviteModel(**result)

        if not bcrypt.checkpw(password.encode(), invite.password.encode()):
            raise NotAuthorizedException()

        if invite.jellyfin and not data.jellyfin_emby_auth:
            raise ClientException(detail="jellyfin_emby_auth must be included")

        if invite.emby and not data.jellyfin_emby_auth:
            raise ClientException(detail="jellyfin_emby_auth must be included")

        if invite.plex and not data.plex_token:
            raise ClientException("plex_token must be included")

        for invite_platform in invite.plex + invite.jellyfin + invite.emby:
            platform_result = await Session.mongo.platform.find_one(
                {"_id": invite_platform.platform_internal_id}
            )
            if not platform_result:
                continue

            platform = PlatformModel(**platform_result)

            match invite_platform.type:
                case "emby":
                    pass
                case "jellyfin":
                    asyncio.create_task(
                        JellyfinPlatform(platform)
                        .invite(invite_platform)
                        .create(
                            # Not possible to be None.
                            data.jellyfin_emby_auth.username,  # type: ignore
                            data.jellyfin_emby_auth.password,  # type: ignore
                        )
                    )
                case "plex":
                    pass


router = Router("/invite", route_handlers=[InviteController], tags=["invite"])
