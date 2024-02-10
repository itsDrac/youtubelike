from app.video.schema import PublishVideoOut
from pydantic import BaseModel, Field
from beanie.odm.fields import PydanticObjectId
from typing import List


class PlaylistIn(BaseModel):
    name: str
    description: str | None = None


class PlaylistOut(PlaylistIn):
    id: PydanticObjectId = Field(alias="_id")
    videos: List[PublishVideoOut] = []
