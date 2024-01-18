from beanie import Document, Link
from app.models.user import User


class Video(Document):
    videofile: str  # clodinary url
    thumbnail: str  # clodinary url
    owner: Link[User]
    title: str
    description: str | None = None
    duration: int
    views: int = 0
    ispublished: bool = True
