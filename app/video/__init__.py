from fastapi import APIRouter

router = APIRouter(
        prefix="/video",
        tags=["Video"],
        )


from app.video.routes import *
