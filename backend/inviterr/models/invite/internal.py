from datetime import datetime
from typing import List, Literal, Optional

from inviterr.models.invite import permssions
from inviterr.models.invite.permssions import (
    InviteEmbyPermissions,
    InviteJellyfinPermissions,
    InvitePlexPermissions,
)
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
        default=0,
        description="Max allow sessions for user, if 0 is unlimited. For Plex this must be implemented with an external system.",
        ge=0,
        le=1000,
    )


class InviteJellyfinModel(InvitePlatformBaseModel):
    permissions: InviteJellyfinPermissions
    type: Literal["jellyfin"] = "jellyfin"


class InvitePlexModel(InvitePlatformBaseModel):
    permissions: InvitePlexPermissions
    type: Literal["plex"] = "plex"


class InviteEmbyModel(InvitePlatformBaseModel):
    permissions: InviteEmbyPermissions
    type: Literal["emby"] = "emby"


class InviteModel(BaseModel):
    """Describes a invite for media platforms & request portals"""

    id_: str = Field(description="ID of the invitation code")
    password: str = Field(description="Invitation password hashed")

    jellyfin: List[InviteJellyfinModel] = []
    plex: List[InvitePlexModel] = []
    emby: List[InviteEmbyModel] = []

    expires: datetime


class CreatedInviteModel(InviteModel):
    password: str = Field(description="Raw invitation password")


class CreateInviteModel(BaseModel):
    jellyfin: List[InviteJellyfinModel] = []
    plex: List[InvitePlexModel] = []
    emby: List[InviteEmbyModel] = []

    expires: datetime
    emby: List[InviteEmbyModel] = []

    expires: datetime
