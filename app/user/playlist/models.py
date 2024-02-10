from app.video.models import Video as VideoModel
from app.user.models import User as UserModel
from beanie import Document, Link
from typing import List


class Playlist(Document):
    name: str
    description: str | None
    videos: List[Link[VideoModel]] = []
    owner: Link[UserModel]
