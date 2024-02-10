from app.middleware.auth import get_current_user
from app.user.playlist import router
from app.user.playlist.schema import PlaylistOut, PlaylistIn
from app.user.playlist.controles import (
        get_playlists,
        create_playlist,
        get_playlist,
        update_playlist,
        delete_playlist,
        add_video,
        remove_video
        )
from app.user.models import User as UserModel
from fastapi import Security
from typing import Annotated, List


# Post route to "/" for creating playlist
# get route to "/" to return all playlists of currentUser
# Get route to /{playlistId} to return playlist of given id
# patch route to /{playlistId} to update playlist of given id
# delete route to /{playlistId} to delete playlist of given id
# patch route to /add/{videoId}/{playlistId} to add video in playlist of given id
# patch route to /remove/{videoId}/{playlistId} to add video in playlist


@router.get("/")
async def current_user_playlists(
        currentUser: Annotated[UserModel, Security(get_current_user)],
        ) -> List[PlaylistOut]:
    result = await get_playlists(currentUser.id)
    return result


@router.post("/")
async def create_user_playlist(
        currentUser: Annotated[UserModel, Security(get_current_user)],
        details: PlaylistIn
        ) -> PlaylistOut:
    result = await create_playlist(currentUser.id, details)
    return result


@router.get("/{playlistId}")
async def get_playlist_by_id(playlistId: str) -> PlaylistOut:
    result = await get_playlist(playlistId)
    return result


@router.patch("/{playlistId}")
async def update_playlist_by_id(
        playlistId: str,
        currentUser: Annotated[UserModel, Security(get_current_user)],
        details: PlaylistIn
        ) -> PlaylistOut:
    result = await update_playlist(currentUser.id, playlistId, details)
    return result


@router.delete("/{playlistId}")
async def delete_playlist_by_id(
        playlistId: str,
        currentUser: Annotated[UserModel, Security(get_current_user)],
        ):
    result = await delete_playlist(currentUser.id, playlistId)
    return result


@router.patch("/add/{videoId}/{playlistId}")
async def add_video_in_playlist(
        videoId: str,
        playlistId: str,
        currentUser: Annotated[UserModel, Security(get_current_user)],
        ) -> PlaylistOut:
    result = await add_video(currentUser.id, videoId, playlistId)
    return result


@router.patch("/remove/{videoId}/{playlistId}")
async def remove_video_in_playlist(
        videoId: str,
        playlistId: str,
        currentUser: Annotated[UserModel, Security(get_current_user)],
        ) -> PlaylistOut:
    result = await remove_video(currentUser.id, videoId, playlistId)
    return result
