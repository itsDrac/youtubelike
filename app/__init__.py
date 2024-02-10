import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.db import connect_db
from app.user import router as user_router
from app.video import router as video_router
from app.tweet import router as tweet_router

load_dotenv()


from fastapi import APIRouter
router = APIRouter(prefix="/v1")


@router.get("/")
async def home():
    return {"Message": "Hello World!"}


description = """
# YoutubeLike
--------------
This is a clone of youtube.com with similar features as youtube such as creating user, uploading videos, creating tweets, managing playlist, adding comment to video/tweet and likeing video/tweet/comment

All the CRUD operations are being performed for each functionility.
Please refer below listed routes/endpointer for better undestanding on how are routes working.

**Note**: Feel free to ask any question regarding below routes.

Thanks :)
"""

app = FastAPI(
        title="YoutubeLike",
        description=description,
        summary="API for YoutubeLike app",
        version="1.0.0",
        contact={
            "name": "Sahaj",
            "url": "https://www.linkedin.com/in/gpt-sahaj28/",
            "email": "sahajgupta28@gmail.com"
            }
        )
app.add_middleware(
        CORSMiddleware,
        allow_origins=os.getenv("CORS_ORIGIN").split("|"),
        allow_credentials=True
        )
app.include_router(router)
app.include_router(user_router)
app.include_router(video_router)
app.include_router(tweet_router)
app.mount("/public", StaticFiles(directory="public"), name="public")


@app.on_event("startup")
async def startup_app():
    try:
        await connect_db(os.getenv("DATABASE_NAME"))
    except Exception as e:
        print(f"Error in database connection Err: {e}")
