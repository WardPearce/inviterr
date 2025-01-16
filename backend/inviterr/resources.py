import aiohttp
from motor import motor_asyncio


class Session:
    http: aiohttp.ClientSession
    mongo: motor_asyncio.AsyncIOMotorCollection
