from inviterr.controllers import invite
from litestar import Router

router = Router(
    "/api/controllers",
    route_handlers=[
        invite.router,
    ],
)
