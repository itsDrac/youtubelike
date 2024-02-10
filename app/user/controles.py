import os
from app.utils.fileHelper import save_file_on_disk, upload_on_cloudinary
from app.user.models import User as UserModel
from app.user.schema import ChannelInfo, WatchHistory
from beanie.operators import Or, Set
from fastapi import HTTPException
from jose import jwt

from beanie import UpdateResponse


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
    avatar_file = await upload_on_cloudinary(avatar_file, folder="avatar/")
    # Add avatar url and coverimage url in userSchema.
    userSchema.avatar = avatar_file.get("url")
    # check if coverimage is passed if yes upload it.
    if coverImage:
        coverImage = await save_file_on_disk(coverImage)
        coverImage = await upload_on_cloudinary(coverImage, folder="/coverImage")
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
    try:
        userData = jwt.decode(
                refreshToken,
                os.getenv("REFRESH_TOKEN_KEY"),
                algorithms=["HS256"]
                )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refersh token")
    user = await UserModel.get(userData.get("id"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid refersh token")
    if not (refreshToken == user.refreshToken):
        raise HTTPException(status_code=401, detail="Refresh token is expired or used")
    accessToken, refreshToken = await _get_access_referh_token(user.id)
    return (accessToken, refreshToken)


async def update_current_password(oldPassword, newPassword, userId):
    currentUser = await UserModel.get(userId)
    if not await currentUser.check_password_hash(oldPassword):
        raise HTTPException(status_code=401, detail="Incorrect password")

    currentUser.password = newPassword
    currentUser.genrate_password_hash()
    await currentUser.save()
    return currentUser


async def fetch_user(userId):
    user = await UserModel.get(userId)
    if not user:
        raise HTTPException(status_code=401, detail="User doesn't exist")
    return user


async def update_details(userId, email, fullName):
    user = await UserModel.get(userId)
    if not user:
        raise HTTPException(status_code=401, detail="User doesn't exist")
    updatedUser = await UserModel.find_one(
            UserModel.id == userId
            ).update(
                    Set({
                        UserModel.email: email,
                        UserModel.fullName: fullName
                        }),
                    response_type=UpdateResponse.NEW_DOCUMENT
                    )
    return updatedUser


async def update_avatar(userId, avatar):
    # Upload avatar first in server then in clodinary
    avatar_file = await save_file_on_disk(avatar)
    avatar_file = await upload_on_cloudinary(avatar_file)
    # userSchema.avatar = avatar_file.get("url")
    updatedUser = await UserModel.find_one(
            UserModel.id == userId
            ).update(
                    Set({
                        UserModel.avatar: avatar_file.get("url"),
                        }),
                    response_type=UpdateResponse.NEW_DOCUMENT
                    )
    return updatedUser


async def update_cover_image(userId, coverImage):
    # Upload avatar first in server then in clodinary
    coverImage = await save_file_on_disk(coverImage)
    coverImage = await upload_on_cloudinary(coverImage)
    # userSchema.avatar = avatar_file.get("url")
    updatedUser = await UserModel.find_one(
            UserModel.id == userId
            ).update(
                    Set({
                        UserModel.coverImage: coverImage.get("url"),
                        }),
                    response_type=UpdateResponse.NEW_DOCUMENT
                    )
    return updatedUser


async def get_channel_info(userName, currentUser):
    channel = await UserModel.find(
            UserModel.userName == userName).aggregate([
                {"$lookup": {
                    "from": "subscriptions",
                    "localField": "_id",
                    "foreignField": "channel",
                    "as": "subscribers"
                    }
                 },
                {"$lookup": {
                    "from": "subscriptions",
                    "localField": "_id",
                    "foreignField": "subscriber",
                    "as": "subscribedTo"
                    }
                 },
                {"$addFields": {
                    "subscriberCount": {
                        "$size": "$subscribers"
                        },
                    "subscribedToCount": {
                        "$size": "$subscribedTo"
                        },
                    "isSubscribed": {
                        "$cond": {
                            "if": {"$in": [currentUser.id, "$subscribers.subscriber"]},
                            "then": True,
                            "else": False
                            }
                        }
                    }
                 },
                {"$project": {
                    "userName": 1,
                    "email": 1,
                    "fullName": 1,
                    "avatar": 1,
                    "coverImage": 1,
                    "subscriberCount": 1,
                    "subscribedToCount": 1,
                    "isSubscribed": 1
                    }
                 }
                ], projection_model=ChannelInfo).to_list()
    return channel


async def get_watch_history(currentUser):
    print(await UserModel.find(UserModel.id == currentUser.id).to_list())
    history = await UserModel.find(
            UserModel.id == currentUser.id).aggregate([
                {"$lookup": {
                    "from": "videos",
                    "localField": "watchHistory",
                    "foreignField": "_id",
                    "as": "watchHistory",
                    "pipeline": [
                        {"$lookup": {
                            "from": "users",
                            "localField": "owner",
                            "foreignField": "_id",
                            "as": "owner",
                            "pipeline": [
                                {"$project": {
                                    "fullName": 1,
                                    "userName": 1,
                                    "avatar": 1
                                    }
                                 }
                                ]
                            }
                         },
                        {"$addFields": {
                            "owner": {
                                "$first": "$owner"
                                }
                            }
                         }
                        ]
                    }
                 }
                ], projection_model=WatchHistory).to_list()
    return history
