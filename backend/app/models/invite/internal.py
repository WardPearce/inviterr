from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

from app.models.invite.permissions import (
    InviteEmbyPermissions,
    InviteJellyfinPermissions,
    InvitePlexPermissions,
)
from app.models.onboarding import OnboardTemplateOrderModel


class InvitePlatformBaseModel(BaseModel):
    platform_internal_id: str = Field(
        description="Inviterr's internal ID of the server"
    )
    folders: Optional[list[str]] = Field(
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
    jellyfin: list[InviteJellyfinModel] = []
    plex: list[InvitePlexModel] = []
    emby: list[InviteEmbyModel] = []

    roles: list[str] = Field(
        [], description="Any special permissions said user should be given"
    )

    uses: int = Field(1, description="How many times can a invite code be redeemed")

    expires: Optional[datetime] = Field(
        None, description="Optional datetime to stop accepting code"
    )

    onboarding: list[OnboardTemplateOrderModel] = Field([], ge=0, le=30)


class InviteModel(CreateInviteModel):
    """Describes a invite for media platforms & request portals"""

    id: str = Field(description="ID of the invitation code")
    password: str = Field(description="Invitation password hashed")

    user_id: str = Field(description="User ID who created the invite")


class CreatedInviteModel(InviteModel):
    """Describes whats returned on invitation creation to admin"""

    password: str = Field(description="Raw invitation password")
