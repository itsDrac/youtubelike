from app.video.models import Video as VideoModel
from app.video.schema import VideoOut, PublishVideoOut
from app.utils.fileHelper import save_file_on_disk, upload_on_cloudinary
from fastapi import HTTPException
from beanie.odm.enums import SortDirection
from beanie.odm.fields import PydanticObjectId


async def get_all_videos(
        query,
        skip=0,
        limit=10,
        sortBy="title",
        sortType=SortDirection.ASCENDING
        ):
    videos = await VideoModel.aggregate([
        {"$addFields": {
            "isqueryMatch": {
                "$regexMatch": {
                    "input": "$title",
                    "regex": r"\b{}\b".format(query),
                    "options": "i"
                    }
                }
            }
         },
        {"$match": {
            "isqueryMatch": True
            }
         },
        {"$skip": skip},
        {"$limit": limit},
        {"$sort": {
            sortBy: sortType
            }
         }
        ], projection_model=PublishVideoOut).to_list()
    return videos


async def upload_video(currentUser, title, description, videoFile, thumbnail):
    localVideoFilePath = await save_file_on_disk(videoFile)
    videoFileResult = await upload_on_cloudinary(
            localVideoFilePath,
            folder="video/"
            )
    localthumbnailFilePath = await save_file_on_disk(thumbnail)
    thumbnailFileResult = await upload_on_cloudinary(
            localthumbnailFilePath,
            folder="thumbnail/"
            )
    video = VideoModel(
            videoFile=videoFileResult.get("secure_url"),
            thumbnail=thumbnailFileResult.get("url"),
            title=title,
            description=description,
            duration=videoFileResult.get("duration"),
            isPublished=True,
            owner=currentUser
            )
    await video.insert()
    result = await VideoModel.find(
            VideoModel.id == PydanticObjectId(video.id)
            ).project(VideoOut).first_or_none()
    return result


async def get_video_by_id(videoId):
    video = await VideoModel.find(
            VideoModel.id == PydanticObjectId(videoId)
            ).project(PublishVideoOut).first_or_none()
    if not video:
        raise HTTPException(status_code=404, detail="Video doesn't exist")
    return video


async def update_video(userId, videoId, title, description, thumbnail):
    try:
        oldVideo = await VideoModel.get(videoId)
    except Exception:
        raise HTTPException(status_code=404, detail="Video doesn't exist")
    if not oldVideo.owner.id == PydanticObjectId(userId):
        raise HTTPException(status_code=402, detail="User is not same as Video's owner")
    if title:
        oldVideo.title = title
    if description:
        oldVideo.description = description
    if thumbnail:
        localthumbnailFilePath = await save_file_on_disk(thumbnail)
        thumbnailFileResult = await upload_on_cloudinary(
                localthumbnailFilePath,
                folder="thumbnail/"
                )
        oldVideo.thumbnail = thumbnailFileResult.get("url"),
    await oldVideo.save()
    newVideo = await VideoModel.find(
            VideoModel.id == PydanticObjectId(videoId)
            ).project(VideoOut).first_or_none()
    return newVideo


# Make controles for deleteing video
async def delete_video(userId, videoId):
    video = await VideoModel.find(
            VideoModel.id == PydanticObjectId(videoId)
            ).first_or_none()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    if not video.owner.id == PydanticObjectId(userId):
        raise HTTPException(status_code=402, detail="Video owner not same current user")
    await video.delete()
    return "deleted"


# Make controles for toggle publish
async def update_publish(userId, videoId, isPublished):
    video = await VideoModel.find(
            VideoModel.id == PydanticObjectId(videoId)
            ).first_or_none()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    if not video.owner.id == PydanticObjectId(userId):
        raise HTTPException(status_code=402, detail="Video owner not same current user")
    video.isPublished = isPublished
    await video.save()
    newVideo = await VideoModel.find(
            VideoModel.id == PydanticObjectId(videoId)
            ).project(VideoOut).first_or_none()
    return newVideo
