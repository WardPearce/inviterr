from typing import Literal, Optional, Tuple

import bcrypt
from aiohttp.client import ClientResponse
from inviterr.models.invite import InviteModel
from inviterr.models.platform import PlatformModel
from inviterr.resources import Session
from litestar.exceptions import NotAuthorizedException


class PlatformInviteBase:
    def __init__(self, platform: "PlatformBase", code: str) -> None:
        self._platform = platform
        self._code = code

    @property
    def extracted_code(self) -> Tuple[str, str]:
        try:
            id_, password = self._code.split("-")
        except ValueError:
            raise NotAuthorizedException()

        return id_, password

    async def get(self) -> InviteModel:
        id_, _ = self.extracted_code

        result = await Session.mongo.find_one({"_id": id_})
        if not result:
            raise NotAuthorizedException()

        return InviteModel(**result)

    async def validate(self) -> InviteModel:
        _, password = self.extracted_code

        invite = await self.get()

        if not bcrypt.checkpw(password.encode(), invite.password.encode()):
            raise NotAuthorizedException()

        return invite

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

    def invite(self, code: str) -> PlatformInviteBase: ...
