import os
from app.utils.fileHelper import save_file_on_disk, upload_on_cloudinary
from app.user.models import UserModel
from beanie.operators import Or, Set
from fastapi import HTTPException
from jose import jwt


async def signup_user(userSchema, avatar, coverImage):
    # Check if user already exist in  database If yes throw error.
    existedUser = await UserModel.find(
            Or(
                UserModel.userName == userSchema.userName,
                UserModel.email == userSchema.email,
              )
            ).first_or_none()
    if existedUser:
        raise HTTPException(status_code=403, detail="User Already exist")

    # Upload avatar first in server then in clodinary
    avatar_file = await save_file_on_disk(avatar)
    avatar_file = await upload_on_cloudinary(avatar_file)
    # Add avatar url and coverimage url in userSchema.
    userSchema.avatar = avatar_file.get("url")
    # check if coverimage is passed if yes upload it.
    if coverImage:
        coverImage = await save_file_on_disk(coverImage)
        coverImage = await upload_on_cloudinary(coverImage)
        userSchema.coverImage = coverImage.get("url")
    # Make UserModel instance from userSchema.
    user = UserModel(
            userName=userSchema.userName,
            email=userSchema.email,
            fullName=userSchema.fullName,
            avatar=userSchema.avatar,
            coverImage=userSchema.coverImage,
            password=userSchema.password,
            )
    # Genrate password hash and add in UserModel instance.
    await user.genrate_password_hash()
    # Insert UserModel instance in DB.
    try:
        await user.insert()
    except Exception:
        raise HTTPException(status_code=500, detail="Error in adding user")
    createdUser = await UserModel.get(user.id)
    return createdUser


# make access and refersh token for user.
async def _get_access_referh_token(userId):
    try:
        user = await UserModel.get(userId)
        accessToken = await user.genrate_access_token()
        refreshToken = await user.genrate_refresh_token()
        user.refreshToken = refreshToken
        # store refresh token in db
        await user.save()
        return (accessToken, refreshToken)
    except Exception:
        raise HTTPException(status_code=500,
                            detail="Error while genrating access and refresh token")


# Make login controler.
async def login_user(userSchema):
    # Accept userSchema and check if user with username or email exist in DB.
    existedUser = await UserModel.find(
            Or(
                UserModel.userName == userSchema.userName,
                UserModel.email == userSchema.email,
              )
            ).first_or_none()
    if not existedUser:
        raise HTTPException(status_code=403, detail="User does not exist")
    # check for password.
    isPasswordSame = await existedUser.check_password_hash(userSchema.password)
    if not isPasswordSame:
        raise HTTPException(status_code=403, detail="Incorrect password")
    accessToken, refreshToken = await _get_access_referh_token(existedUser.id)
    # return existedUser + access token + refresh token
    return (existedUser, accessToken, refreshToken)


# Add logout controler, wherein delete refresh token from current user.
async def logout_user(userId):
    _ = await UserModel.find_one(
            UserModel.id == userId
            ).update(
                    Set({
                        UserModel.refreshToken: None
                        })
                    )


async def refersh_access_token(refreshToken):
    if not refreshToken:
        raise HTTPException(status_code=401, detail="Unauthorized Request")
    userData = jwt.decode(
            refreshToken,
            os.getenv("REFRESH_TOKEN_KEY"),
            algorithms=["HS256"]
            )
    user = await UserModel.get(userData.get("id"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid refersh token")
    if not (refreshToken == user.refreshToken):
        raise HTTPException(status_code=401, detail="Refresh token is expired or used")
    accessToken, refreshToken = await _get_access_referh_token(user.id)
    return (accessToken, refreshToken)
