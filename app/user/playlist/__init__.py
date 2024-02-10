from app.middleware.auth import get_current_user
from fastapi import APIRouter, Security

router = APIRouter(
        prefix="/playlist",
        tags=["Playlist"],
        )

from app.user.playlist.routes import *
