from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Time
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    bio = Column(Text)
    # profile_picture = ??

    tweets = relationship('Tweet', back_populates='owner')
    comments = relationship('Comment', back_populates='owner')
    likes = relationship('Like', back_populates='owner')
    followers = relationship('Follow', back_populates='user_followee')
    following = relationship('Follow', back_populates='user_follower')

# User
# id (primary key)
# username (unique)
# email (unique)
# password
# bio
# profile_picture
