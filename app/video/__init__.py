from app.middleware.auth import get_current_user
from fastapi import APIRouter, Security

router = APIRouter(
        prefix="/video",
        tags=["Video"],
        dependencies=[Security(get_current_user)],
        )


from app.video.routes import *
