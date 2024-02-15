from app.video import router
from app.middleware.auth import get_current_user
from app.user.models import User as UserModel
from app.video.controles import (
        get_all_videos,
        upload_video,
        get_video_by_id,
        update_video,
        delete_video,
        update_publish
        )
from app.video.schema import VideoOut, PublishVideoOut, OwnerVideoOut
from fastapi import Security, UploadFile, Form
from beanie.odm.enums import SortDirection
from typing import Annotated


@router.get("/")
async def all_videos(
        query: str,
        page: int = 0,
        limit: int = 10,
        sortBy: str = "title",
        sortType: SortDirection = SortDirection.ASCENDING,
        ) -> list[PublishVideoOut]:
    result = await get_all_videos(query, page, limit, sortBy, sortType)
    return result


@router.post("/")
async def publish_video(
        currentUser: Annotated[UserModel, Security(get_current_user)],
        videoFile: UploadFile,
        thumbnail: UploadFile,
        title: Annotated[str, Form()],
        description: Annotated[str | None, Form()]
        ) -> OwnerVideoOut:
    result = await upload_video(currentUser, title, description, videoFile, thumbnail)
    return result


@router.get("/get_video_id")
async def get_video_id(videoId: str) -> PublishVideoOut:
    result = await get_video_by_id(videoId)
    return result


@router.patch("/update")
async def update(
        currentUser: Annotated[UserModel, Security(get_current_user)],
        videoId: str,
        title: str | None = None,
        description: str | None = None,
        thumbnail: UploadFile | None = None
        ) -> OwnerVideoOut:
    result = await update_video(currentUser.id, videoId, title, description, thumbnail)
    return result


# post route for deleteing video
@router.delete("/delete")
async def delete(
        currentUser: Annotated[UserModel, Security(get_current_user)],
        videoId: str,
        ):
    await delete_video(currentUser.id, videoId)
    return {"Message": "Video Deleted"}


# patch route to toggle publish
@router.patch("/publish")
async def publish(
        currentUser: Annotated[UserModel, Security(get_current_user)],
        videoId: str,
        isPublished: bool
        ) -> OwnerVideoOut:
    result = await update_publish(currentUser.id, videoId, isPublished)
    return result
