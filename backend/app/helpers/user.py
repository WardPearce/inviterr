from app.resources import Session


async def username_exists(username: str) -> bool:
    return (
        await Session.mongo.jellyfin_emby_taken.count_documents({"username": username})
        > 0
    )
