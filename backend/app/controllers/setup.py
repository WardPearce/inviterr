from datetime import timedelta
from uuid import uuid4

import bcrypt
from app.helpers.jwt import JWT_AUTH, login
from app.models.roles import ROLES
from app.models.setup import BasicSetupCreateModel, BasicSetupModel
from app.models.user import UserModel
from app.resources import Session
from litestar import Controller, Request, Response, Router, get, post
from litestar.exceptions import NotAuthorizedException


class SetupBasicController(Controller):

    @post(
        description="Setups the basic information for Inviterr, can only be called once.",
        tags=["setup"],
        exclude_from_auth=True,
    )
    async def setup(
        self, request: Request, data: BasicSetupCreateModel
    ) -> Response[UserModel]:
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
                password=bcrypt.hashpw(
                    data.password.encode(),
                    bcrypt.gensalt(rounds=16),
                ).decode(),
                auth_type="usernamePassword",
                invite_id=None,
                id=user_id,
            ).model_dump()
        )

        return await login(user_id, request.headers.get("User-Agent", None))

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
