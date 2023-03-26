import datetime
from pydantic import BaseModel

from user import User
from tweet import Tweet


class Like(BaseModel):
    id: int
    user_id: int
    tweet_id: int
    created_at: datetime.datetime
    owner: str[User]

    class Config:
        orm_mode = True
