from typing import Literal, Optional

from aiohttp.client import ClientResponse
from inviterr.models.invite.internal import (
    InviteEmbyModel,
    InviteJellyfinModel,
    InvitePlexModel,
)
from inviterr.models.platform import PlatformModel
from inviterr.resources import Session
from litestar.exceptions import NotFoundException


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
        self, username: Optional[str] = None, password: Optional[str] = None
    ) -> None: ...

    async def delete(self) -> None: ...

    async def modify(self) -> None: ...

    async def policy(self) -> None: ...


class PlatformBase:
    def __init__(self, platform: PlatformModel) -> None:
        self._platform = platform

    async def request(
        self, url: str, method: Literal["GET", "POST", "DELETE", "PUT"], **kwargs
    ) -> ClientResponse:

        if not self._platform.server.endswith("/"):
            self._platform.server += "/"

        if url.endswith("/"):
            url = url.removesuffix("/")

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
            kwargs["headers"] = {**kwargs["headers"], **headers}
        else:
            kwargs["headers"] = headers

        resp = await Session.http.request(method, self._platform.server + url, **kwargs)
        resp.raise_for_status()
        return resp

    def invite(
        self, invite: InviteJellyfinModel | InviteEmbyModel | InvitePlexModel
    ) -> PlatformInviteBase: ...
