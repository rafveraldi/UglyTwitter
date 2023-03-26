import datetime
from typing import Optional
from pydantic import BaseModel

from user import User
from comment import Comment
from like import Like


class Tweet(BaseModel):
    id: int
    user_id: int
    content: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None
    owner: str[User]
    comments: list[Comment] = []
    likes: list[Like] = []

    class Config:
        orm_mode = True
