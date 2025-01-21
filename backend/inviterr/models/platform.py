from typing import Literal

from bson import ObjectId
from pydantic import BaseModel, Field


class PlatformModel(BaseModel):
    """Describes a media platform, e.g. jellyfin, plex or emby."""

    id_: str = Field(description="Inviterr's internal ID of the server")
    platform: Literal["plex", "emby", "jellyfin"]
    api_key: str = Field(description="API key to access external media server")
    server: str = Field(description="Endpoint for the media server")
    alias: str = Field(min_length=4, description="Human friendly name of the server")
    description: str = Field(
        min_length=4, description="Description of the media server"
    )
    folders: list[str] = Field(default=[], description="Folder IDs for media server")
