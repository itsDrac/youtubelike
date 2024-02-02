from pydantic import BaseModel, field_validator, EmailStr


class SignupUserOut(BaseModel):
    userName: str
    email: EmailStr
    fullName: str
    avatar: str = ""
    coverImage: str | None = None


class SignupUserIn(SignupUserOut):
    password: str

    @field_validator("userName", "email", "fullName", "password")
    @classmethod
    def check_value(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Data should be provided")
        return value

    @field_validator("userName")
    @classmethod
    def username_to_lower(cls, value):
        return value.lower()


# Add Schema for login user In
class LoginUserIn(BaseModel):
    userName: str | None = None
    email: EmailStr | None = None
    password: str


# TODO: Add Schema for login user out
class LoginUserOut(SignupUserOut):
    accessToken: str
    refreshToken: str


class ChannelInfo(SignupUserOut):
    subscriberCount: int
    subscribedToCount: int
    isSubscribed: bool
