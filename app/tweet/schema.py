from app.user.schema import SignupUserOut
from pydantic import BaseModel, Field
from beanie.odm.fields import PydanticObjectId


class CreateTweetIn(BaseModel):
    content: str


class CreateTweetOut(CreateTweetIn):
    id: PydanticObjectId = Field(alias="_id")
    owner: SignupUserOut
