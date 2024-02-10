from app.user.models import User as UserModel
from app.user.playlist.models import Playlist as PlaylistModel
from app.user.playlist.schema import PlaylistOut
from app.video.models import Video as VideoModel
from beanie.odm.fields import PydanticObjectId
from fastapi import HTTPException


async def get_playlists(userId):
    playlists = await PlaylistModel.find(
            PlaylistModel.owner.id == userId
            ).project(PlaylistOut).to_list()
    return playlists


async def create_playlist(userId, details):
    user = await UserModel.get(userId)
    playlist = PlaylistModel(**details.model_dump(), owner=user)
    await playlist.create()
    newPlaylist = await PlaylistModel.find(
            PlaylistModel.id == playlist.id
            ).project(PlaylistOut).first_or_none()
    return newPlaylist


async def get_playlist(playlistId):
    playlist = await PlaylistModel.find(
            PlaylistModel.id == PydanticObjectId(playlistId)
            ).project(PlaylistOut).first_or_none()
    return playlist


async def update_playlist(userId, playlistId, details):
    playlist = await PlaylistModel.get(playlistId)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist dont exist")
    if not playlist.owner.id == PydanticObjectId(userId):
        raise HTTPException(status_code=401, detail="User doesnt own this playlist.")
    playlist.name = details.get("name")
    playlist.description = details.get("description")
    await playlist.save()
    newplaylist = await PlaylistModel.get(playlist.id)
    return newplaylist


async def delete_playlist(userId, playlistId):
    playlist = await PlaylistModel.get(playlistId)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist dont exist")
    if not playlist.owner.id == PydanticObjectId(userId):
        raise HTTPException(status_code=401, detail="User doesnt own this playlist.")
    await playlist.delete()
    return {"Message": "Playlist deleted"}


async def add_video(userId, videoId, playlistId):
    playlist = await PlaylistModel.get(playlistId)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist dont exist")
    if not playlist.owner.id == PydanticObjectId(userId):
        raise HTTPException(status_code=401, detail="User doesnt own this playlist.")
    video = await VideoModel.get(videoId)
    if not video:
        raise HTTPException(status_code=404, details="Video doesnt exist")
    playlist.videos.append(video)
    await playlist.save()
    newPlaylist = await PlaylistModel.get(playlist.id)
    return newPlaylist


async def remove_video(userId, videoId, playlistId):
    playlist = await PlaylistModel.get(playlistId)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist dont exist")
    if not playlist.owner.id == PydanticObjectId(userId):
        raise HTTPException(status_code=401, detail="User doesnt own this playlist.")
    video = await VideoModel.get(videoId)
    if not video:
        raise HTTPException(status_code=404, details="Video doesnt exist")
    playlist.videos.remove(video)
    await playlist.save()
    newPlaylist = await PlaylistModel.get(playlist.id)
    return newPlaylist
