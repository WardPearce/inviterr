from typing import Literal

from pydantic import BaseModel


class PlatformModel:
    platform: Literal["plex", "emby", "jellyfin"]
    api_key: str
    server: str
    alias: str
    description: str
    folders: list[str] = []
