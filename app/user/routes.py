from typing import Annotated
from app.user import router
from app.user.schema import SignupUserIn, SignupUserOut, LoginUserIn, LoginUserOut
from app.user.controles import signup_user, login_user
from app.user.models import UserModel

from fastapi import UploadFile, Form, HTTPException, Response


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


# Add post route for login which will return user and access token & refersh token
# Set cookies for access token and refersh token
@router.post("/login", status_code=200)
async def login(user: LoginUserIn, res: Response) -> LoginUserOut:
    existedUser, accessToken, refreshToken = await login_user(user)
    loggedinUser = await UserModel.get(existedUser.id)
    res.set_cookie(key="accessToken", value=accessToken, httponly=True, secure=True)
    res.set_cookie(key="refreshToken", value=refreshToken, httponly=True, secure=True)

    result = LoginUserOut(**loggedinUser.model_dump(), accessToken=accessToken)

    return result
# TODO: Add get route for logout which will check for access & refresh token in cookies
#       and delete them.
