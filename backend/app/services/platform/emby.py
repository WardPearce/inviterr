from app.models.invite.internal import InviteEmbyModel
from app.models.platform import PlatformModel
from app.services.platform.base import PlatformBase, PlatformInviteBase


class EmbyInvite(PlatformInviteBase):
    def __init__(self, platform: PlatformBase, invite: InviteEmbyModel) -> None:
        super().__init__(platform, invite)

    async def create(self, username: str, password: str) -> str:
        assert isinstance(
            self._invite, InviteEmbyModel
        ), "EmbyInvite must be given InviteEmbyModel"

        self.validate_folders()

        created_user = await (
            await self._platform.request(
                "/Users/New",
                "POST",
                json={"Name": username},
            )
        ).json()

        permission_payload = {
            "AuthenticationProviderId": "Emby.Server.Implementations.Library.DefaultAuthenticationProvider",
            **self._invite.permissions.model_dump(exclude_none=True),
            "SimultaneousStreamLimit": self._invite.sessions,
        }

        if self._invite.folders:
            permission_payload["EnableAllFolders"] = False
            permission_payload["EnabledFolders"] = self._invite.folders
        else:
            permission_payload["EnableAllFolders"] = True

        await self._platform.request(
            f"/Users/{created_user['Id']}/Policy", "POST", json=permission_payload
        )

        await self._platform.request(
            f"/Users/{created_user['Id']}/Password", "POST", json={"NewPw": password}
        )

        return created_user["Id"]


class EmbyPlatform(PlatformBase):
    def __init__(self, platform: PlatformModel) -> None:
        assert platform.platform == "emby", f"Passed {platform.platform} on emby"

        super().__init__(platform)

    def invite(self, invite: InviteEmbyModel) -> EmbyInvite:
        return EmbyInvite(self, invite)

    async def login(self, username: str, password: str) -> bool:
        resp = await self.request(
            "/Users/AuthenticateByName",
            "POST",
            include_auth=False,
            headers={
                "X-Emby-Authorization": 'MediaBrowser Client="Jellyfin Web", Device="Firefox", DeviceId="TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NDsgcnY6ODUuMCkgR2Vja28vMjAxMDAxMDEgRmlyZWZveC84NS4wfDE2MTI5MjcyMDM5NzM1", Version="10.8.0"'
            },
            json={
                "Username": username,
                "Pw": password
            }
        )

        return resp.ok
