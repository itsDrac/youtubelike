from fastapi import APIRouter

router = APIRouter(
        prefix="/users",
        tags=["User"]
        )

from app.user.routes import *
from app.user.playlist import router as playlistRouter


router.include_router(playlistRouter)
