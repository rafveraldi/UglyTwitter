from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Time
from sqlalchemy.orm import relationship

from database import Base


class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(Text, nullable=False)
    created_at = Column(Time)
    updated_at = Column(Time)

    owner = relationship('User', back_populates='tweets')
    comments = relationship('Comments', back_populates='tweet')
    likes = relationship('Like', back_populates='liked_tweets')

# Tweet
# id (primary key)
# user_id (foreign key to User)
# content
# created_at
# updated_at
