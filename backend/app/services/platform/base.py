from typing import Any, Literal, Optional

from aiohttp.client import ClientResponse
from litestar.exceptions import NotAuthorizedException, NotFoundException

from app.models.invite.internal import (
    InviteEmbyModel,
    InviteJellyfinModel,
    InvitePlexModel,
)
from app.models.platform import PlatformModel
from app.resources import Session


class PlatformInviteBase:
    def __init__(
        self,
        platform: "PlatformBase",
        invite: InviteJellyfinModel | InviteEmbyModel | InvitePlexModel,
    ) -> None:
        self._platform = platform
        self._invite = invite

    def validate_folders(self) -> None:
        if self._invite.folders and sorted(self._platform._platform.folders) != sorted(
            self._invite.folders
        ):
            raise NotFoundException(detail="Folders don't match instance.")

    async def create(
        self, username: Optional[str], password: Optional[str]
    ) -> Any: ...

    async def delete(self) -> None: ...

    async def modify(self) -> None: ...

    async def policy(self) -> None: ...


class PlatformBase:
    def __init__(self, platform: PlatformModel) -> None:
        self._platform = platform

    async def request(
        self,
        url: str,
        method: Literal["GET", "POST", "DELETE", "PUT"],
        include_auth: bool = True,
        **kwargs
    ) -> ClientResponse:

        if not self._platform.server.endswith("/"):
            self._platform.server += "/"

        if url.endswith("/"):
            url = url.removesuffix("/")

        if include_auth:
            if self._platform.platform in ("emby", "jellyfin"):
                headers = {
                    "X-Emby-Token": self._platform.api_key,
                    "Accept": (
                        "application/json"
                        if self._platform.platform == "emby"
                        else 'application/json, profile="PascalCase"'
                    ),
                }
            else:
                headers = {"X-Plex-Token": self._platform.api_key}

            if "headers" in kwargs:
                kwargs["headers"] = {**headers, **kwargs["headers"]}
            else:
                kwargs["headers"] = headers

        resp = await Session.http.request(method, self._platform.server + url, **kwargs)

        match resp.status:
            case 401:
                raise NotAuthorizedException()
            case 404:
                raise NotFoundException()
            case _:
                resp.raise_for_status()

        return resp

    async def login(self, username: str, password: str) -> bool: ...

    def invite(
        self, invite: InviteJellyfinModel | InviteEmbyModel | InvitePlexModel
    ) -> PlatformInviteBase: ...
