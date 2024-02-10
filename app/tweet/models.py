from app.user.models import User as UserModel
from beanie import Document, Link


class Tweet(Document):
    owner: Link[UserModel]
    content: str
