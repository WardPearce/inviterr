from typing import Any, List

from app.models.session import SessionModel
from app.models.user import UserModel
from app.resources import Session
from litestar import Controller, Request, Router, delete, get
from litestar.security.jwt import Token


class SessionController(Controller):
    @get("/", description="Lists all active sessions for myself", tags=["session"])
    async def sessions(
        self, request: Request[UserModel, Token, Any]
    ) -> List[SessionModel]:
        sessions = []
        async for session in Session.mongo.session.find(
            {"user_id": request.user.id}
        ).sort("created", -1):
            sessions.append(SessionModel(**session))

        return sessions

    @delete(
        "/{session_id:str}", description="Invalidates a given session", tags=["session"]
    )
    async def invalidate_session(
        self, request: Request[UserModel, Token, Any], session_id: str
    ) -> None:
        await Session.mongo.session.delete_one(
            {"id": session_id, "user_id": request.user.id}
        )


router = Router("/sessions", route_handlers=[SessionController])
