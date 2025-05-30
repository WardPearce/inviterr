import asyncio

from litestar.exceptions import ClientException, NotAuthorizedException
from plexapi.myplex import MyPlexAccount, PlexServer
from plexapi.myplex import Unauthorized as PlexUnauthorized

from app.models.invite.internal import InvitePlexModel
from app.models.platform import PlatformModel
from app.services.platform.base import PlatformBase, PlatformInviteBase


class PlexInvite(PlatformInviteBase):
    def __init__(self, platform: PlatformBase, invite: InvitePlexModel) -> None:
        super().__init__(platform, invite)

    async def create(self, password: str) -> None:
        assert isinstance(
            self._invite, InvitePlexModel
        ), "PlexInvite must be given InvitePlexModel"

        self.validate_folders()

        loop = asyncio.get_event_loop()

        plex = await loop.run_in_executor(
            None,
            lambda: PlexServer(
                self._platform._platform.server, self._platform._platform.api_key
            ),
        )

        # Is long running synchronous so must be ran in executor
        server_account = await loop.run_in_executor(None, plex.myPlexAccount)
        try:
            user_account = await loop.run_in_executor(
                None, lambda: MyPlexAccount(token=password)
            )
        except PlexUnauthorized:
            raise NotAuthorizedException()

        invite = await loop.run_in_executor(
            None,
            lambda: server_account.inviteFriend(
                user=user_account.email,
                sections=self._invite.folders if self._invite.folders else None,
                **self._invite.permissions.model_dump(exclude_none=True),
            ),
        )

        if invite is None:
            raise ClientException(detail="Unable to invite user")

        await loop.run_in_executor(
            None, user_account.acceptInvite, server_account.email
        )
        await loop.run_in_executor(None, server_account.enableViewStateSync)


class PlexPlatform(PlatformBase):
    def __init__(self, platform: PlatformModel) -> None:
        assert platform.platform == "plex", f"Passed {platform.platform} on plex"

        super().__init__(platform)

    async def login(self, username: str, password: str) -> bool:
        raise NotImplementedError()

    def invite(self, invite: InvitePlexModel) -> PlexInvite:
        return PlexInvite(self, invite)
