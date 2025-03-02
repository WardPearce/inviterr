from typing import Literal, Optional

from pydantic import BaseModel, Field


class UserModel(BaseModel):
    id: str = Field(description="ID of user")
    roles: list[str] = Field(
        [], description="Defines what special permissions the user has"
    )
    internal_platform_ids: list[str] = Field(
        description="Internal platform IDs user can access"
    )
    username: str
    password: Optional[str] = Field(
        description="Hashed password if plexOauth isn't being used."
    )
    auth_type: Literal["usernamePassword", "plexOauth"]
    country: str = "Unknown"
    invite_id: str = Field(description="ID of invitation redeemed for access")
