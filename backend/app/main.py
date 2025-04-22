import glob
import os

import aiofiles
import aiohttp
from litestar import Litestar, Request
from litestar.config.cors import CORSConfig
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin
from litestar.openapi.spec import License, Server
from motor import motor_asyncio
from pydantic import BaseModel

from app import controllers
from app.env import SETTINGS
from app.helpers.jwt import JWT_AUTH
from app.resources import Session


class ScalarRenderPluginRouteFix(ScalarRenderPlugin):
    @staticmethod
    def get_openapi_json_route(request: Request) -> str:
        return "/schema/openapi.json"


async def startup_sessions(app: Litestar) -> None:
    Session.mongo = motor_asyncio.AsyncIOMotorClient(
        SETTINGS.mongo.host, SETTINGS.mongo.port
    )[SETTINGS.mongo.collection]

    await Session.mongo.client.server_info()

    Session.http = aiohttp.ClientSession()


async def shutdown_sessions(app: Litestar) -> None:
    if Session.http:
        await Session.http.close()


async def mongo_create_indexes(app: Litestar) -> None:
    await Session.mongo.session.create_index("expires", expireAfterSeconds=120)


async def load_onboarding_templates(app: Litestar) -> None:
    current_dir = os.path.dirname(os.path.realpath(__file__))

    onboarding_dir = os.path.join(current_dir, "onboarding", "*.md")

    for file in glob.glob(onboarding_dir):
        if file.endswith("README.md"):
            continue

        async with aiofiles.open(file, "r") as f_:
            contents = await f_.read()

        file_name = file.split("/")[-1]

        await Session.mongo.templates.update_one(
            {"name": file_name.removesuffix(".md")},
            {"$set": {"contents": contents}},
            upsert=True,
        )


app = Litestar(
    route_handlers=[controllers.router],
    openapi_config=OpenAPIConfig(
        title="Inviterr",
        version="0.0.1",
        render_plugins=[ScalarRenderPluginRouteFix()],
        description="OpenAPI specification for Inviterr.",
        servers=[Server(url="", description="Production server.")],
        license=License(
            name="GNU Affero General Public License v3.0",
            identifier="AGPL-3.0",
            url="https://github.com/WardPearce/inviterr/blob/main/LICENSE",
        ),
    ),
    debug=SETTINGS.proxy_urls.backend == "http://127.0.0.1:8000",
    cors_config=CORSConfig(
        allow_origins=[SETTINGS.proxy_urls.frontend],
        allow_credentials=True,
    ),
    type_encoders={BaseModel: lambda m: m.model_dump(by_alias=False)},
    on_startup=[startup_sessions, mongo_create_indexes, load_onboarding_templates],
    on_shutdown=[shutdown_sessions],
    middleware=[JWT_AUTH.middleware],
)
