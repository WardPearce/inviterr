from litestar import Controller, Router


class AdminController(Controller):
    pass

router = Router(
    "/admin",
    route_handlers=[AdminController],
    tags=["admin"],
)
