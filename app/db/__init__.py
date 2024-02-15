import sys

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie


def _get_client():
    try:
        client = AsyncIOMotorClient("mongodb://mongodb:27017")
        return client
    except Exception:
        print("could not connect to database, try checking URL")
        sys.exit()


async def connect_db(db_name: str):
    client = _get_client()
    await init_beanie(
            database=client[db_name],
            document_models=[
                "app.user.models.User",
                "app.video.models.Video",
                "app.user.playlist.models.Playlist",
                "app.tweet.models.Tweet",
            ]
        )
