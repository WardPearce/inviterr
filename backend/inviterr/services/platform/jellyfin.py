from inviterr.models.invite.internal import InviteJellyfinModel
from inviterr.models.platform import PlatformModel
from inviterr.services.platform.base import PlatformBase, PlatformInviteBase


class JellyfinInvite(PlatformInviteBase):
    def __init__(self, platform: PlatformBase, invite: InviteJellyfinModel) -> None:
        super().__init__(platform, invite)

    async def create(self, username: str, password: str) -> str:
        assert isinstance(
            self._invite, InviteJellyfinModel
        ), "JellfinInvite must be given InviteJellyfinModel"

        self.validate_folders()

        created_user = await (
            await self._platform.request(
                "/Users/New",
                "POST",
                json={"Name": username, "Password": password},
            )
        ).json()

        permission_payload = {
            "AuthenticationProviderId": "Jellyfin.Server.Implementations.Users.DefaultAuthenticationProvider",
            **self._invite.permissions.model_dump(exclude_none=True),
            "MaxActiveSessions": self._invite.sessions,
        }

        if self._invite.folders:
            permission_payload["EnableAllFolders"] = False
            permission_payload["EnabledFolders"] = self._invite.folders
        else:
            permission_payload["EnableAllFolders"] = True

        await self._platform.request(
            f"/Users/{created_user['Id']}/Policy", "POST", json=permission_payload
        )

        return created_user["Id"]


class JellyfinPlatform(PlatformBase):
    def __init__(self, platform: PlatformModel) -> None:
        super().__init__(platform)

    def invite(self, invite: InviteJellyfinModel) -> JellyfinInvite:
        return JellyfinInvite(self, invite)
