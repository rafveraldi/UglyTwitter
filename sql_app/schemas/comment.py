import datetime
from typing import Optional
from pydantic import BaseModel


class Comment(BaseModel):
    id: int
    user_id: int
    tweet_id: int
    content: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True
