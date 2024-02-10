from fastapi import APIRouter

router = APIRouter(
        prefix="/tweet",
        tags=["Tweet"]
        )

from app.tweet.routes import *
