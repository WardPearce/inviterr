from typing import Literal

from pydantic import BaseModel, Field


class BasicSetupModel(BaseModel):
    site_title: str = Field(max_length=34)
    theme: (
        Literal["catppuccin"]
        | Literal["cerberus"]
        | Literal["concord"]
        | Literal["crimson"]
        | Literal["fennec"]
        | Literal["hamlindigo"]
        | Literal["legacy"]
        | Literal["mint"]
        | Literal["modern"]
        | Literal["mona"]
        | Literal["nosh"]
        | Literal["nouveau"]
        | Literal["pine"]
        | Literal["reign"]
        | Literal["rocket"]
        | Literal["rose"]
        | Literal["sahara"]
        | Literal["seafoam"]
        | Literal["terminus"]
        | Literal["vintage"]
        | Literal["vox"]
        | Literal["wintry"]
    )


class BasicSetupCreateModel(BasicSetupModel):
    email: str = Field(max_length=255)
    password: str = Field(max_length=255)
