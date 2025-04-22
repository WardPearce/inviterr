from typing import Any
from litestar.security.jwt import Token
from litestar.exceptions import NotFoundException
from app.resources import Session
from app.models.user import UserModel
from litestar import Controller, Request, Router, get


class UserController(Controller):
    @get("/me", description="Get info about myself")
    async def me(self, request: Request[UserModel, Token, Any]) -> UserModel:
        result = await Session.mongo.user.find_one({"_id": request.user.id})
        if not result:
            raise NotFoundException(detail="User not found")

        return result


router = Router(
    "/user",
    route_handlers=[UserController],
    tags=["user"],
)
