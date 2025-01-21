from typing import Optional

from pydantic import BaseModel, Field


class JellyfinEmbyAuth(BaseModel):
    username: str = Field(min_length=4)
    password: str = Field(min_length=8)


class RedeemInviteModel(BaseModel):
    """Describes the payload a public user posts for using a invite code"""

    code: str = Field(description="Raw invite code")

    jellyfin_emby_auth: Optional[JellyfinEmbyAuth] = None
    plex_token: Optional[str] = None
