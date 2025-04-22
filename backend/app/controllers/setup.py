from uuid import uuid4

from litestar import Controller, Request, Response, Router, get, post
from litestar.exceptions import NotAuthorizedException

from app.helpers.jwt import login
from app.helpers.misc import PASSWORD_HASHER
from app.models.roles import ROLES
from app.models.setup import BasicSetupCompletedModel, BasicSetupCreateModel
from app.models.user import UserModel
from app.resources import Session


class SetupBasicController(Controller):

    @post(
        description="Setups the basic information for Inviterr, can only be called once.",
        tags=["setup"],
        exclude_from_auth=True,
    )
    async def setup(
        self, request: Request, data: BasicSetupCreateModel
    ) -> Response:
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
            }
        )

        user_id = str(uuid4())

        await Session.mongo.user.insert_one(
            UserModel(
                roles=[ROLES.root],
                internal_platform_ids=["*"],
                username=data.email,
                password=PASSWORD_HASHER.hash(data.password),
                supported_auth_type=["local"],
                invite_id=None,
                _id=user_id,
            ).model_dump()
        )

        return await login(user_id, request.headers.get("User-Agent", None))

    @get(
        description="Gets basic information for Inviterr, what's publicly available",
        tags=["setup", "public"],
        exclude_from_auth=True,
    )
    async def public(self) -> BasicSetupCompletedModel:
        result = await Session.mongo.basic_setup.find_one({"completed": True})
        if not result:
            return BasicSetupCompletedModel(
                site_title="Inviterr", theme="wintry", completed=False
            )

        return BasicSetupCompletedModel(**result)


router = Router("/setup", route_handlers=[SetupBasicController])
