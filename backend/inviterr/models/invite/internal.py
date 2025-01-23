from datetime import datetime
from typing import List, Literal, Optional

from inviterr.models.invite import permssions
from inviterr.models.invite.permssions import (
    InviteEmbyPermissions,
    InviteJellyfinPermissions,
    InvitePlexPermissions,
)
from inviterr.models.onboarding import OnboardTemplateModel
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


class CreateInviteModel(BaseModel):
    jellyfin: List[InviteJellyfinModel] = []
    plex: List[InvitePlexModel] = []
    emby: List[InviteEmbyModel] = []

    roles: List[str] = []

    uses: int = 1

    expires: Optional[datetime] = None

    onboarding: list[OnboardTemplateModel] = Field([], ge=0, le=30)


class InviteModel(CreateInviteModel):
    """Describes a invite for media platforms & request portals"""

    id: str = Field(description="ID of the invitation code")
    password: str = Field(description="Invitation password hashed")


class CreatedInviteModel(InviteModel):
    """Describes whats returned on invitation creation to admin"""

    password: str = Field(description="Raw invitation password")
