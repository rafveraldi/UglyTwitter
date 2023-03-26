from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Time
from sqlalchemy.orm import relationship

from database import Base


class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    tweet_id = Column(Integer, ForeignKey('tweet.id'))
    created_at = Column(Time)

    owner = relationship('User', back_populates='likes')


# Like
# id (primary key)
# user_id (foreign key to User)
# tweet_id (foreign key to Tweet)
# created_at
