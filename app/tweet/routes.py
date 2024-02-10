from app.middleware.auth import get_current_user
from app.user.models import User as UserModel
from app.tweet import router
from app.tweet.schema import CreateTweetIn, CreateTweetOut
from app.tweet.controles import create_tweet, user_tweets, update_tweet, delete_tweet
from fastapi import Security
from typing import Annotated

# post route to "/" to create tweet
# get route to "/user/{userId}/" to get all tweets of user
# patch route to "/{tweetId}" to update tweet
# delete route to "/{tweetId}" to delete tweet


@router.post("/")
async def create_tweet_for_user(
        currentUser: Annotated[UserModel, Security(get_current_user)],
        details: CreateTweetIn
        ) -> CreateTweetOut:
    result = await create_tweet(currentUser.id, details)
    return result


@router.get("/user/{userId}")
async def all_user_tweet(userId: str) -> list[CreateTweetOut]:
    result = await user_tweets(userId)
    return result


@router.patch("/{tweetId}")
async def update_user_tweet(
        tweetId: str,
        currentUser: Annotated[UserModel, Security(get_current_user)],
        details: CreateTweetIn
        ) -> CreateTweetOut:
    result = await update_tweet(currentUser.id, tweetId, details)
    return result


@router.delete("/{tweetId}")
async def delete_user_tweet(
        tweetId: str,
        currentUser: Annotated[UserModel, Security(get_current_user)]
        ):
    result = await delete_tweet(currentUser.id, tweetId)
    return result
