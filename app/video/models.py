from app.user.models import User as UserModel
from beanie import Document


class Video(Document):
    videoFile: str  # clodinary url
    thumbnail: str  # clodinary url
    title: str
    description: str | None = None
    duration: float
    isPublished: bool
    views: int = 0
    owner: UserModel
