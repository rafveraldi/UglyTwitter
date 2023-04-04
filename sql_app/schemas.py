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


class Comment(BaseModel):
    id: int
    user_id: int
    tweet_id: int
    content: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True


class Tweet(BaseModel):
    id: int
    user_id: int
    content: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None
    comments: list[Comment] = []
    likes: list[Like] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    name: Optional[str] = None
    likes: list[Like] = []
    tweets: list[Tweet] = []
    comments: list[Comment] = []
    following: list[Follow] = []
    followers: list[Follow] = []

    class Config:
        orm_mode = True
