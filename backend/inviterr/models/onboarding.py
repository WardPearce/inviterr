from typing import List, Literal

from pydantic import BaseModel, Field


class OnboardTemplateOrderModel(BaseModel):
    order: int = Field(
        description="What step order should this template be displayed in, if -1 will only be viewable in user guides"
    )
    hide_after_onboard: bool = Field(
        False,
        description="Hide this documentation after onboarding",
    )
    template_id: str = Field(description="The internal ID for said template")
    only_for: List[Literal["plex", "jellyfin", "emby"]] = Field(
        ["plex", "jellyfin", "emby"],
        description="Only show template if invite includes following platforms or requests",
    )


class CreateOnboardTemplateModel(BaseModel):
    markdown: str = Field(le=1000000, description="Markdown for documentation")


class OnboardTemplate(CreateOnboardTemplateModel):
    template_id: str
