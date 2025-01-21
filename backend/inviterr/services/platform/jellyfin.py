import asyncio
from typing import Optional

from inviterr.models.invite import InviteJellyfinModel
from inviterr.models.platform import PlatformModel
from inviterr.services.platform.base import PlatformBase, PlatformInviteBase
from litestar.exceptions import NotFoundException


class JellfinInvite(PlatformInviteBase):
    def __init__(self, platform: PlatformBase, identifier: str) -> None:
        super().__init__(platform, identifier)

    async def __create(
        self,
        username: Optional[str],
        password: Optional[str],
        invite_platform: InviteJellyfinModel,
    ) -> None:
        created_user = await (
            await self._platform.request(
                "/Users/New",
                "POST",
                json={"Name": username, "Password": password},
            )
        ).json()

        permission_payload = {
            "AuthenticationProviderId": "Jellyfin.Server.Implementations.Users.DefaultAuthenticationProvider",
            **invite_platform.permissions.model_dump(exclude_none=True),
            "MaxActiveSessions": invite_platform.sessions,
        }

        if invite_platform.folders:
            permission_payload["EnableAllFolders"] = False
            permission_payload["EnabledFolders"] = invite_platform.folders
        else:
            permission_payload["EnableAllFolders"] = True

        await self._platform.request(
            f"/Users/{created_user['Id']}/Policy", "POST", json=permission_payload
        )

    async def create(self, username: Optional[str], password: Optional[str]) -> None:
        invite = await self.validate()

        if not invite.jellyfin:
            raise NotFoundException(detail="No jellyfin config for that invite")

        for jellyfin in invite.jellyfin:
            asyncio.create_task(self.__create(username, password, jellyfin))


class JellyfinPlatform(PlatformBase):
    def __init__(self, platform: PlatformModel) -> None:
        super().__init__(platform)

    def invite(self, code: str) -> JellfinInvite:
        return JellfinInvite(self, code)
