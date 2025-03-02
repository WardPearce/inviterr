from app.controllers import invite, setup
from litestar import Router

router = Router(
    "/api/controllers/v1",
    route_handlers=[invite.router, setup.router],
)
