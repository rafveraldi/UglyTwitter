from pydantic import BaseModel, EmailStr

from typing import Optional

from tweet import Tweet
from comment import Comment
from follow import Follow


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    username: str
    bio: Optional[str] = None
    tweets: list[Tweet] = []
    comments: list[Comment] = []
    followers: list[Follow] = []
    following: list[Follow] = []

    class Config:
        orm_mode = True
