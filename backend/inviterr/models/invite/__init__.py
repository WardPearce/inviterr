from typing import List, Optional

from inviterr.models.invite.permssions import InviteJellyfinPermissions
from pydantic import BaseModel, Field


class InvitePlatformBaseModel(BaseModel):
    platform_internal_id: str = Field(
        description="Inviterr's internal ID of the server"
    )
    folders: Optional[List[str]] = Field(
        None,
        description="A list of folders enabled for the user, if None all folders will be provided.",
    )
    sessions: int = Field(
        default=0, description="Max allow sessions for user, if 0 is unlimited."
    )


class InviteJellyfinModel(InvitePlatformBaseModel):
    permissions: InviteJellyfinPermissions


class InvitePlexModel(InvitePlatformBaseModel):
    pass


class InviteEmbyModel(InvitePlatformBaseModel):
    pass


class InviteModel(BaseModel):
    """Describes a invite for media platforms & request portals"""

    id_: str = Field(alias="id", description="ID of the invitation code")
    password: str = Field(description="Invitation password hashed")

    jellyfin: List[InviteJellyfinModel] = []
    plex: List[InvitePlexModel] = []
    emby: List[InviteEmbyModel] = []
