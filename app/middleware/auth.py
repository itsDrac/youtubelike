import os
from typing import Annotated
from fastapi import Header, Cookie, HTTPException
from app.user.models import UserModel
from jose import jwt


# Add middleware to get current user.
async def get_current_user(accessToken: Annotated[str | None, Cookie(), Header()]):
    if not accessToken:
        raise HTTPException(status_code=404, detail="Access Token not found")
    accessToken = accessToken.replace("Bearer ", "")
    userData = jwt.decode(
            accessToken,
            os.getenv("ACCESS_TOKEN_KEY"),
            algorithms=["HS256"]
            )

    currentUser = await UserModel.get(userData.get("id"))
    return currentUser
