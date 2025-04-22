from litestar import Router

from app.controllers import admin, invite, sessions, setup, user

router = Router(
    "/api/controllers/v1",
    route_handlers=[invite.router, setup.router, sessions.router, admin.router, user.router],
)
