from typing import AsyncGenerator

from litestar.exceptions import NotFoundException

from app.models.platform import PlatformModel
from app.models.user import UserModel
from app.resources import Session


async def username_exists(username: str) -> bool:
    return (
        await Session.mongo.jellyfin_emby_taken.count_documents({"username": username})
        > 0
    )

class User:
    def __init__(self, id_: str) -> None:
        self._id = id_

    def __str__(self) -> str:
        return f"User(id={self._id})"

    async def get(self) -> UserModel:
        result = await Session.mongo.user.find_one({"_id": self._id})
        if not result:
            raise NotFoundException(detail="User not found")

        return result

    async def platforms(self) -> AsyncGenerator[PlatformModel]:
        """Yields platforms a user can access.
        """

        user = await self.get()

        platforms = []
        async for platform in Session.mongo.platform.find({"_id": {"$in": user.internal_platform_ids}}):
            yield PlatformModel(**platform)
