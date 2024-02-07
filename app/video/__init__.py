from app.middleware.auth import get_current_user
from fastapi import APIRouter, Security

router = APIRouter(
        prefix="/video",
        tags=["Video"],
        )


from app.video.routes import *
