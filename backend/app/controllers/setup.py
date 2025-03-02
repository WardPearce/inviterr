import bcrypt
from app.models.roles import ROLES
from app.models.setup import BasicSetupCreateModel, BasicSetupModel
from app.resources import Session
from litestar import Controller, Router, get, post
from litestar.exceptions import NotAuthorizedException


class SetupBasicController(Controller):
    @post(
        description="Setups the basic information for Inviterr, can only be called once.",
        tags=["setup"],
    )
    async def setup(self, data: BasicSetupCreateModel) -> None:
        is_completed = (
            await Session.mongo.basic_setup.count_documents({"completed": True}) > 0
        )
        if is_completed:
            raise NotAuthorizedException(detail="Setup already completed")

        await Session.mongo.basic_setup.insert_one(
            {
                "completed": True,
                "theme": data.theme,
                "site_title": data.site_title,
                "email": data.email,
                "password": bcrypt.hashpw(
                    data.password.encode(), bcrypt.gensalt(rounds=16)
                ),
                "roles": [ROLES.root],
            }
        )

    @get(
        description="Gets basic information for Inviterr, what's publicly available",
        tags=["setup", "public"],
    )
    async def public(self) -> BasicSetupModel:
        result = await Session.mongo.basic_setup.find_one({"completed": True})
        if not result:
            return BasicSetupModel(site_title="Inviterr", theme="wintry")

        return BasicSetupModel(**result)


router = Router("/setup", route_handlers=[SetupBasicController])
