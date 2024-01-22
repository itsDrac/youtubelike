import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.db import connect_db
from app.user import router as user_router

load_dotenv()


from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def home():
    return {"Message": "Hello World!"}


app = FastAPI()
app.add_middleware(
        CORSMiddleware,
        allow_origins=os.getenv("CORS_ORIGIN").split("|"),
        allow_credentials=True
        )
app.include_router(router)
app.include_router(user_router)
app.mount("/public", StaticFiles(directory="public"), name="public")


@app.on_event("startup")
async def startup_app():
    try:
        await connect_db(os.getenv("DATABASE_NAME"))
    except Exception as e:
        print(f"Error in database connection Err: {e}")
