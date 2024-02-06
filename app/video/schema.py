from pydantic import BaseModel, Field
from beanie.odm.fields import PydanticObjectId


class VideoOwner(BaseModel):
    fullName: str
    userName: str
    avatar: str


class VideoOut(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    videoFile: str
    thumbnail: str
    title: str
    description: str
    duration: float
    views: int = 0
    isPublished: bool


class PublishVideoOut(VideoOut):
    owner: VideoOwner
