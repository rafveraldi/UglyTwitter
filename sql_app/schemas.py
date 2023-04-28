import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class Like(BaseModel):
    id: int
    user_id: int
    tweet_id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class Follow(BaseModel):
    id: int
    follower_id: int
    followee_id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    content: str


class Comment(CommentBase):
    id: int
    tweet_id: int
    user_id: int
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True


class TweetBase(BaseModel):
    content: str


class TweetBasic(TweetBase):
    id: int
    user_id: int
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None


class Tweet(TweetBasic):
    comments: list[Comment] = []
    likes: list[Like] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserBasic(UserBase):
    id: int
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    name: Optional[str] = None

    class Config:
        orm_mode = True


class User(UserBasic):
    likes: list[Like] = []
    tweets: list[Tweet] = []
    comments: list[CommentBase] = []
    following: list[Follow] = []
    followers: list[Follow] = []

    class Config:
        orm_mode = True
