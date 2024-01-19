from fastapi import APIRouter

router = APIRouter(
        prefix="/users",
        tags=["User"]
        )

from app.user.routes import *
