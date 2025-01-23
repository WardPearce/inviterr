import asyncio
import secrets

import bcrypt
from inviterr.guards import user_roles_guard
from inviterr.misc import url_safe_id
from inviterr.models.invite.internal import (
    CreatedInviteModel,
    CreateInviteModel,
    InviteModel,
)
from inviterr.models.invite.redeem import RedeemInviteModel
from inviterr.models.platform import PlatformModel
from inviterr.resources import Session
from inviterr.services.platform.jellyfin import JellyfinPlatform
from litestar import Controller, Router, delete, get, post
from litestar.exceptions import (
    ClientException,
    NotAuthorizedException,
    NotFoundException,
)


class InviteController(Controller):
    path = "/{id_:str}"

    @get(
        description="Find an invite",
        tags=["invite", "find"],
        guards=[user_roles_guard(["invite.find"])],
    )
    async def find(self, id_: str) -> InviteModel:
        result = await Session.mongo.invite.find_one({"_id": id_})
        if not result:
            raise NotFoundException()

        return InviteModel(**result)

    @delete(
        description="Deletes an invite",
        tags=["invite", "delete"],
        guards=[user_roles_guard(["invite.delete"])],
    )
    async def delete_(self, id_: str) -> None:
        await Session.mongo.invite.delete_one({"_id": id_})


class InviteCreateController(Controller):
    @post(
        description="Create an invite",
        tags=["invite", "create"],
        guards=[user_roles_guard(["invite.create"])],
    )
    async def create(self, data: CreateInviteModel) -> CreatedInviteModel:
        id_ = url_safe_id(6)

        # Ensure ID isn't currently in use.
        while await Session.mongo.invite.count_documents({"_id": id_}) > 0:
            id_ = url_safe_id(6)
            await asyncio.sleep(0.1)

        password = secrets.token_urlsafe(6)

        for platform in data.jellyfin + data.plex + data.emby:
            if (
                await Session.mongo.platform.count_documents(
                    {
                        "_id": platform.platform_internal_id,
                        "folders": {"$in": platform.folders},
                    }
                )
                == 0
            ):
                raise NotFoundException(
                    detail=f"Platform ID {platform.platform_internal_id} or folders {platform.folders} is invalid"
                )

        created_invite = CreatedInviteModel(
            **data.model_dump(),
            id_=id_,
            password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(),
        )

        await Session.mongo.invite.insert_one(created_invite.model_dump())

        created_invite.password = password  # Set to raw password for response

        return created_invite


class InviteRedeemController(Controller):
    path = "/redeem"

    @post(
        description="Allows for redeeming a invitation code",
        tags=["invite", "redeem"],
        exclude_from_auth=True,
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


router = Router(
    "/invite",
    route_handlers=[InviteRedeemController, InviteCreateController, InviteController],
    tags=["invite"],
)
