import bcrypt
import os
from typing import List
from beanie import Document, Indexed, Link
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.models.video import Video


_hash_salt = bcrypt.gensalt()


class UserModel(Document):
    userName: Indexed(str, unique=True)
    email: Indexed(str, unique=True)
    fullName: str
    avatar: str  # clodinary url
    coverImage: str | None = None  # clodinary url
    password: str  # Hashed password
    refreshToken: str | None = None  # JWT token
    watchHistory: List[Link[Video]] = []

    async def genrate_password_hash(self):
        hashed_password = bcrypt.hashpw(self.password.encode(), _hash_salt)
        self.password = hashed_password.decode()

    async def check_password_hash(self, text_password) -> bool:
        is_same = bcrypt.checkpw(text_password.encode(), self.password.encode())
        return is_same

    async def genrate_access_token(self):
        data = {
                "id": str(self.id),
                "email": self.email,
                "userName": self.userName
            }
        expire = datetime.now(timezone.utc)
        expire += timedelta(days=int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS")))
        data.update({"exp": expire})
        token = jwt.encode(data, os.getenv("ACCESS_TOKEN_KEY"), algorithm="HS256")
        return token

    async def genrate_refresh_token(self):
        data = {
                "id": str(self.id),
            }
        expire = datetime.now(timezone.utc)
        expire += timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")))
        data.update({"exp": expire})
        token = jwt.encode(data, os.getenv("REFRESH_TOKEN_KEY"), algorithm="HS256")
        return token
