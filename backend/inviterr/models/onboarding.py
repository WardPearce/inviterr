from pydantic import BaseModel, Field


class OnboardTemplateModel(BaseModel):
    order: int = Field(
        description="What step order should this template be displayed in, if -1 will only be viewable in user guides"
    )
    hide_after_onboard: bool = Field(
        False,
        description="Should the user be able to view this documentation after onboarding",
    )
    template_id: str = Field(description="The internal ID for said template")
