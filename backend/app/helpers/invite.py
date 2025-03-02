from app.models.invite.internal import InviteModel
from app.resources import Session
from litestar.exceptions import NotFoundException


class Invite:
    def __init__(self, id_: str) -> None:
        self._id = id_

    @property
    def query(self) -> dict:
        return {"_id": self._id}

    async def get(self) -> InviteModel:
        result = await Session.mongo.invite.find_one(self.query)
        if not result:
            raise NotFoundException()

        return InviteModel(**result)

    async def exists(self) -> bool:
        return await Session.mongo.invite.count_documents(self.query) > 0

    async def exists_raise(self) -> None:
        if not await self.exists():
            raise NotFoundException()

    async def delete(self) -> None:
        await self.exists_raise()
        await Session.mongo.invite.delete_one(self.query)
