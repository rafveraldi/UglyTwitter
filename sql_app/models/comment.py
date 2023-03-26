from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Time
from sqlalchemy.orm import relationship

from database import Base


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    tweet_id = Column(Integer, ForeignKey('tweets.id'))
    content = Column(Text, nullable=False)
    created_at = Column(Time)
    updated_at = Column(Time)

    owner = relationship("User", back_populates='comments')
    tweet = relationship('Tweet', back_populates='comments')

# Comment
# id (primary key)
# user_id (foreign key to User)
# tweet_id (foreign key to Tweet)
# content
# created_at
# updated_at
