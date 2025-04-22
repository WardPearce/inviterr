from typing import Literal, Optional

from pydantic import BaseModel, Field


class UserPublicModel(BaseModel):
    supported_auth_type: list[Literal["emby", "jellyfin", "plex", "local"]]


class UserModel(UserPublicModel):
    id: str = Field(description="ID of user", alias="_id")
    roles: list[str] = Field(
        [], description="Defines what special permissions the user has"
    )
    internal_platform_ids: list[str] = Field(
        description="Internal platform IDs user can access"
    )
    username: str
    password: Optional[str] = Field(
        default=None, description="Only used for root admin"
    )
    country: str = "Unknown"
    invite_id: str | None = Field(
        description="ID of invitation redeemed for access"
    )


class LoginModel(BaseModel):
    username: Optional[str] = None
    password: str
    auth_type: Literal["jellyfinOrEmby", "plex", "local"]
