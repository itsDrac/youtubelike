from app.user.models import User as UserModel
from app.tweet.models import Tweet as TweetModel
from app.tweet.schema import CreateTweetOut
from beanie.odm.fields import PydanticObjectId
from fastapi import HTTPException


async def create_tweet(userId, details):
    user = await UserModel.get(userId)
    tweet = TweetModel(owner=user, **details.model_dump())
    await tweet.insert()
    newTweet = await TweetModel.find(
            TweetModel.id == tweet.id
            ).project(CreateTweetOut).first_or_none()
    return newTweet


async def user_tweets(userId):
    tweets = TweetModel.find(
            TweetModel.owner.id == userId
            ).project(CreateTweetOut).to_list()
    return tweets


async def update_tweet(userId, tweetId, details):
    tweet = TweetModel.find(
            TweetModel.id == PydanticObjectId(tweetId)
            ).first_or_none()
    if not tweet:
        raise HTTPException(status_code=404, details="Tweet not found")
    if not tweet.owner.id == PydanticObjectId(userId):
        raise HTTPException(status_code=402, details="User cant update tweet")
    tweet.content = details.content
    await tweet.save()
    newTweet = TweetModel.find(
            TweetModel.id == PydanticObjectId(tweetId)
            ).project(CreateTweetOut).first_or_none()
    return newTweet


async def delete_tweet(userId, tweetId):
    tweet = TweetModel.find(
            TweetModel.id == PydanticObjectId(tweetId)
            ).first_or_none()
    if not tweet:
        raise HTTPException(status_code=404, details="Tweet not found")
    if not tweet.owner.id == PydanticObjectId(userId):
        raise HTTPException(status_code=402, details="User cant delete tweet")
    await tweet.delete()
    return {"Message": "Tweet deleted"}
