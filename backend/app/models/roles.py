from pydantic import BaseModel, Field


class RolesModel(BaseModel):
    root: str = Field(".root.all", description="Gives the user access to everything")

    invite_find: str = Field(
        "invite.find", description="Allows someone to read every detail of an invite"
    )
    invite_modify: str = Field(
        "invite.modify",
        description="Allows someone to modify every aspect of any invite",
    )
    invite_reset: str = Field(
        "invite.reset", description="Allows someone to reset password for any invite"
    )
    invite_delete: str = Field(
        "invite.delete", description="Allows someone to delete any invite"
    )
    invite_create: str = Field(
        "invite.create",
        description="Allows someone to create any invite for any platform",
    )
    invite_list: str = Field(
        "invite.list", description="Allows someone to list all invites"
    )


ROLES = RolesModel()  # type: ignore
