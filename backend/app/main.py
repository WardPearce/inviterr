import aiohttp
import pkg_resources
from app import controllers
from app.env import SETTINGS
from app.resources import Session
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from litestar import Litestar, Request
from litestar.config.cors import CORSConfig
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin
from litestar.openapi.spec import License, Server
from motor import motor_asyncio
from pydantic import BaseModel
from pymongo import AsyncMongoClient


class ScalarRenderPluginRouteFix(ScalarRenderPlugin):
    @staticmethod
    def get_openapi_json_route(request: Request) -> str:
        return f"/schema/openapi.json"


async def startup_sessions(app: Litestar) -> None:
    Session.mongo = motor_asyncio.AsyncIOMotorClient(
        SETTINGS.mongo.host, SETTINGS.mongo.port
    )[SETTINGS.mongo.collection]

    await Session.mongo.client.server_info()

    Session.http = aiohttp.ClientSession()

    scheduler = AsyncIOScheduler(
        gconfig={
            "jobstores": {
                "default",
                MongoDBJobStore(
                    database=f"{SETTINGS.mongo.collection}_apscheduler",
                    client=AsyncMongoClient(
                        host=SETTINGS.mongo.host, port=SETTINGS.mongo.port
                    ),
                ),
            }
        }
    )

    scheduler.start()


async def shutdown_sessions(app: Litestar) -> None:
    if Session.http:
        await Session.http.close()


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
    on_startup=[startup_sessions],
    on_shutdown=[],
)
