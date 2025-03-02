from typing import Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class MongoDB(BaseModel):
    host: str = "localhost"
    port: int = 27017
    collection: str = "inviterr"


class ProxiedUrls(BaseModel):
    frontend: str = "http://localhost"
    backend: str = "http://localhost/api"


class Settings(BaseSettings):
    mongo: MongoDB = MongoDB()
    proxy_urls: ProxiedUrls = ProxiedUrls()

    username_caching_interval: int = 160

    model_config = {"env_prefix": "inviterr_"}


SETTINGS = Settings()  # type: ignore
