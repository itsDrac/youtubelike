from typing import Annotated
from app.user import router
from app.user.models import UserModel
from app.middleware.auth import get_current_user
from app.user.schema import (
        SignupUserIn,
        SignupUserOut,
        LoginUserIn,
        LoginUserOut,
        ChannelInfo
        )
from app.user.controles import (
        signup_user,
        login_user,
        logout_user,
        refersh_access_token,
        update_current_password,
        fetch_user,
        update_details,
        update_avatar,
        update_cover_image,
        get_channel_info
        )

from fastapi import (
        UploadFile,
        Form,
        HTTPException,
        Response,
        Security,
        Cookie,
        Header,
        Depends
        )


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


# Add get route for logout which will check for access & refresh token in cookies
# and delete them.
@router.get("/logout", status_code=200)
async def logout(
        currentUser: Annotated[UserModel, Security(get_current_user)],
        res: Response
        ):
    await logout_user(currentUser.id)
    res.delete_cookie(key="accessToken", httponly=True, secure=True)
    res.delete_cookie(key="refreshToken", httponly=True, secure=True)
    return {"Message": "User logged out"}


@router.post("/refresh-token", status_code=200)
async def refresh_token(
        refreshToken: Annotated[str | None, Cookie(), Header()],
        res: Response
        ):
    refreshToken = refreshToken.replace("Bearer ", "")
    accessToken, refreshToken = await refersh_access_token(refreshToken)
    res.set_cookie(key="accessToken", value=accessToken, httponly=True, secure=True)
    res.set_cookie(key="refreshToken", value=refreshToken, httponly=True, secure=True)
    return {"Message": "Access token refershed."}


@router.post("/update-password", status_code=200)
async def update_password(
        currentUser: Annotated[UserModel, Security(get_current_user)],
        newPassword: str,
        oldPassword: str
        ):
    _ = await update_current_password(newPassword, currentUser.id)
    return {"Message": "Current user password changed."}


@router.get("/current-user", status_code=200)
async def current_user(
        currentUser: Annotated[UserModel, Security(get_current_user)]
        ) -> LoginUserOut:
    result = await fetch_user(currentUser.id)
    return result


@router.post("/update-details", status_code=200)
async def update_current_details(
        currentUser: Annotated[UserModel, Security(get_current_user)],
        email: str,
        fullName: str
        ) -> LoginUserOut:
    user = UserModel.get(currentUser.id)
    if not user:
        raise HTTPException(status_code=401, detail="User doesn't exist")
    updatedUser = await update_details(user.id, email, fullName)
    return updatedUser


@router.post("/update-avatar", status_code=200)
async def update_current_avatar(
        currentUser: Annotated[UserModel, Security(get_current_user)],
        avatar: UploadFile,
        ) -> LoginUserOut:
    user = UserModel.get(currentUser.id)
    if not user:
        raise HTTPException(status_code=401, detail="User doesn't exist")
    updatedUser = update_avatar(user.id, avatar)
    return updatedUser


@router.post("/update-coverimage", status_code=200)
async def update_current_cover_image(
        currentUser: Annotated[UserModel, Security(get_current_user)],
        coverImage: UploadFile,
        ) -> LoginUserOut:
    user = UserModel.get(currentUser.id)
    if not user:
        raise HTTPException(status_code=401, detail="User doesn't exist")
    updatedUser = update_cover_image(user.id, coverImage)
    return updatedUser


@router.get("/channel-info", status_code=200, response_model=list[ChannelInfo])
async def channel_info(
        userName: str,
        currentUser: Annotated[UserModel | None, Depends(get_current_user)] = None,
            ) -> Annotated[list, ChannelInfo]:
    result = await get_channel_info(userName, currentUser)
    return result
