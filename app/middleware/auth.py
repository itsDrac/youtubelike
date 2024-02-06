import os
from typing import Annotated
from fastapi import Header, Cookie, HTTPException
from app.user.models import User as UserModel
from jose import jwt


# Add middleware to get current user.
async def get_current_user(accessToken: Annotated[str | None, Cookie(), Header()]):
    if not accessToken:
        raise HTTPException(status_code=404, detail="Access Token not found")
    accessToken = accessToken.replace("Bearer ", "")
    try:
        userData = jwt.decode(
                accessToken,
                os.getenv("ACCESS_TOKEN_KEY"),
                algorithms=["HS256"]
                )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid access token")

    currentUser = await UserModel.get(userData.get("id"))
    return currentUser
