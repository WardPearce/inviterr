import secrets
from typing import Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class MongoDB(BaseModel):
    host: str = "localhost"
    port: int = 27017
    collection: str = "inviterr"


class ProxiedUrls(BaseModel):
    frontend: str = "http://localhost:5173"
    backend: str = "http://127.0.0.1:8000"


class Settings(BaseSettings):
    mongo: MongoDB = MongoDB()
    proxy_urls: ProxiedUrls = ProxiedUrls()

    jwt_secret: str = Field(secrets.token_urlsafe(), min_length=32)

    model_config = {"env_prefix": "inviterr_"}


SETTINGS = Settings()  # type: ignore
