import datetime
from pydantic import BaseModel

from user import User


class Follow(BaseModel):
    id: int
    follower_id: int
    followee_id: int
    created_at: datetime.datetime
    user_follower: str[User]
    user_followee: str[User]

    class Config:
        orm_mode = True
