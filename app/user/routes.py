from typing import Annotated
from app.user import router
from app.user.schema import SignupUserIn, SignupUserOut
from app.user.controles import signup_user

from fastapi import UploadFile, Form, HTTPException


@router.post("/signup", status_code=201)
async def signup(
        userName: Annotated[str, Form()],
        email: Annotated[str, Form()],
        fullName: Annotated[str, Form()],
        password: Annotated[str, Form()],
        avatar: UploadFile,
        coverImage: UploadFile | None = None,
        ) -> SignupUserOut:
    try:
        userSchema = SignupUserIn(
                userName=userName,
                email=email,
                fullName=fullName,
                password=password,
                )
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid data provided")

    result = await signup_user(userSchema, avatar, coverImage)
    # return User pydantic model without password and refreshtoken
    return result
