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
router2 = APIRouter(prefix="/v2")


@router2.get("/v1")
async def home2():
    return {"Message": "Hello World!"}


@router.get("/")
async def home():
    return {"Message": "Hello World!"}

router.include_router(router2)

app = FastAPI()
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
