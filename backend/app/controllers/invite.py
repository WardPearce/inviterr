import asyncio
import secrets
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from app.helpers.guards import user_roles_guard
from app.helpers.invite import Invite
from app.helpers.misc import PASSWORD_HASHER, url_safe_id
from app.helpers.user import username_exists
from app.models.invite.internal import (
    CreatedInviteModel,
    CreateInviteModel,
    InviteModel,
)
from app.models.invite.redeem import RedeemInviteModel
from app.models.platform import PlatformModel
from app.models.roles import ROLES
from app.models.user import UserModel
from app.resources import Session
from app.services.platform.emby import EmbyPlatform
from app.services.platform.jellyfin import JellyfinPlatform
from app.services.platform.plex import PlexPlatform
from argon2.exceptions import VerifyMismatchError
from litestar import Controller, Request, Router, delete, get, post, put
from litestar.exceptions import (
    ClientException,
    NotAuthorizedException,
    NotFoundException,
)
from plexapi.myplex import MyPlexAccount


class InviteIdController(Controller):
    path = "/{id_:str}"

    @get(
        description="Find an invite",
        tags=["invite", "find"],
        guards=[user_roles_guard([ROLES.invite_find])],
    )
    async def find(self, id_: str) -> InviteModel:
        return await Invite(id_).get()

    @put(
        description="Modify an invite",
        tags=["invite", "modify"],
        guards=[user_roles_guard([ROLES.invite_modify])],
    )
    async def modify(self, id_: str, data: CreateInviteModel) -> None:
        if not data.jellyfin and not data.emby and data.plex:
            raise ClientException(detail="Invite must include at least one platform")

        await Invite(id_).exists_raise()

        await Session.mongo.invite.update_one(
            {"_id": id_}, {"$set": data.model_dump(exclude_unset=True)}
        )

    @delete(
        path="/password-reset",
        description="Resets the password for an invite",
        tags=["invite", "reset"],
        guards=[user_roles_guard([ROLES.invite_reset])],
        status_code=200,
    )
    async def reset(self, id_: str) -> str:
        password = secrets.token_urlsafe(6)

        await Session.mongo.invite.update_one(
            {"_id": id_},
            {"$set": {"password": PASSWORD_HASHER.hash(password)}},
        )

        return password

    @delete(
        description="Deletes an invite",
        tags=["invite", "delete"],
        guards=[user_roles_guard([ROLES.invite_delete])],
    )
    async def delete_(self, id_: str) -> None:
        await Invite(id_).delete()


class InviteController(Controller):
    @post(
        description="Create an invite",
        tags=["invite", "create"],
        guards=[user_roles_guard([ROLES.invite_create])],
    )
    async def create(
        self, request: Request[UserModel, Any, Any], data: CreateInviteModel
    ) -> CreatedInviteModel:
        if not data.jellyfin and not data.emby and data.plex:
            raise ClientException(detail="Invite must include at least one platform")

        id_ = url_safe_id(6)

        # Ensure ID isn't currently in use.
        while await Invite(id_).exists():
            id_ = url_safe_id(6)
            await asyncio.sleep(0.01)

        password = secrets.token_urlsafe(16)

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
            user_id=request.user.id,
            id=id_,
            password=PASSWORD_HASHER.hash(password),
        )

        await Session.mongo.invite.insert_one(created_invite.model_dump())

        created_invite.password = password  # Set to raw password for response

        return created_invite

    @get(
        description="List 100 invites at a time",
        tags=["invite", "list"],
        guards=[user_roles_guard([ROLES.invite_list])],
        path="/page:int",
    )
    async def list_(self, page: int = 0) -> list[InviteModel]:
        results: list[InviteModel] = []

        async for invite in (
            Session.mongo.invite.find()
            .sort("expires", -1)
            .skip((page - 1) * 100)
            .limit(100)
        ):
            results.append(InviteModel(**invite))

        return results


class InviteRedeemController(Controller):
    path = "/redeem"

    @post(
        description="Allows for redeeming a invitation code",
        tags=["invite", "redeem"],
        exclude_from_auth=True,
    )
    async def redeem(self, data: RedeemInviteModel) -> None:
        if not data.jellyfin_emby_auth and not data.plex_token:
            raise ClientException(
                detail="Must have at least jellyfin_emby_auth or plex_token defined"
            )

        try:
            id_, password = data.code.split("-", 1)
        except ValueError:
            raise NotAuthorizedException()

        invite = await Invite(id_).get()

        if invite.expires and datetime.now(tz=timezone.utc) > invite.expires:
            raise NotAuthorizedException()

        if invite.uses <= 0:
            raise NotAuthorizedException()

        if not invite.jellyfin and not invite.emby and invite.plex:
            raise ClientException(detail="Invite must include at least one platform")

        try:
            PASSWORD_HASHER.verify(invite.password, password)
        except VerifyMismatchError:
            raise NotAuthorizedException()

        await Session.mongo.invite.update_one({"_id": id_}, {"$inc": {"uses": -1}})

        if invite.jellyfin and not data.jellyfin_emby_auth:
            raise ClientException(detail="jellyfin_emby_auth must be included")

        if invite.emby and not data.jellyfin_emby_auth:
            raise ClientException(detail="jellyfin_emby_auth must be included")

        if invite.plex and not data.plex_token:
            raise ClientException(detail="plex_token must be included")

        if data.jellyfin_emby_auth:
            data.jellyfin_emby_auth.username = data.jellyfin_emby_auth.username.strip()

            if username_exists(data.jellyfin_emby_auth.username):
                raise ClientException(detail="Username taken")

            await Session.mongo.jellyfin_emby_taken.insert_one(
                {"username": data.jellyfin_emby_auth.username}
            )

        user_platform_access_ids: list[str] = []

        platform_tasks = []

        for invite_platform in invite.plex + invite.jellyfin + invite.emby:
            platform_result = await Session.mongo.platform.find_one(
                {"_id": invite_platform.platform_internal_id}
            )
            if not platform_result:
                continue

            user_platform_access_ids.append(invite_platform.platform_internal_id)

            platform = PlatformModel(**platform_result)

            match invite_platform.type:
                case "emby":
                    platform_tasks.append(
                        EmbyPlatform(platform)
                        .invite(invite_platform)
                        .create(
                            # Not possible to be None.
                            data.jellyfin_emby_auth.username,  # type: ignore
                            data.jellyfin_emby_auth.password,  # type: ignore
                        )
                    )
                case "jellyfin":
                    platform_tasks.append(
                        JellyfinPlatform(platform)
                        .invite(invite_platform)
                        .create(
                            # Not possible to be None.
                            data.jellyfin_emby_auth.username,  # type: ignore
                            data.jellyfin_emby_auth.password,  # type: ignore
                        )
                    )
                case "plex":
                    platform_tasks.append(
                        PlexPlatform(platform)
                        .invite(invite_platform)
                        .create(data.plex_token)  # type: ignore
                    )

        platform_tasks_results = await asyncio.gather(
            *platform_tasks, return_exceptions=True
        )

        # Use Plex auth over emby/jellyfin
        if data.plex_token:
            user_account = await asyncio.get_event_loop().run_in_executor(
                None, lambda: MyPlexAccount(token=data.plex_token)
            )
            await Session.mongo.user.insert_one(
                UserModel(
                    roles=invite.roles,
                    internal_platform_ids=user_platform_access_ids,
                    username=user_account.email,
                    password=None,
                    auth_type="plexOauth",
                    invite_id=id_,
                    id=str(uuid4()),
                ).model_dump()
            )
        elif data.jellyfin_emby_auth:
            await Session.mongo.user.insert_one(
                UserModel(
                    roles=invite.roles,
                    internal_platform_ids=user_platform_access_ids,
                    username=data.jellyfin_emby_auth.username,
                    password=PASSWORD_HASHER.hash(data.jellyfin_emby_auth.password),
                    auth_type="usernamePassword",
                    invite_id=id_,
                    id=str(uuid4()),
                ).model_dump()
            )


router = Router(
    "/invite",
    route_handlers=[InviteRedeemController, InviteIdController, InviteController],
    tags=["invite"],
)
