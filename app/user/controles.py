from app.utils.fileHelper import save_file_on_disk, upload_on_cloudinary
from app.user.models import UserModel
from beanie.operators import Or
from fastapi import HTTPException


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
