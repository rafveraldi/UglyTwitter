from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    password = Column(String, nullable=False)
    bio = Column(Text)

    tweets = relationship("Tweet", cascade="all,delete", back_populates="owner")
    comments = relationship("Comment", cascade="all,delete", back_populates="owner")
    likes = relationship("Like", cascade="all,delete", back_populates="owner")
    followers = relationship(
        "Follow",
        cascade="all,delete",
        back_populates="user_followee",
        primaryjoin="Follow.followee_id==User.id",
    )
    following = relationship(
        "Follow",
        cascade="all,delete",
        back_populates="user_follower",
        primaryjoin="Follow.follower_id==User.id",
    )


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    owner = relationship("User", back_populates="tweets")
    comments = relationship("Comment", cascade="all,delete", back_populates="tweet")
    likes = relationship("Like", cascade="all,delete", back_populates="tweet")


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tweet_id = Column(Integer, ForeignKey("tweets.id"))
    created_at = Column(DateTime)

    owner = relationship("User", back_populates="likes")
    tweet = relationship("Tweet", back_populates="likes")


class Follow(Base):
    __tablename__ = "followage"

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id"))
    followee_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime)

    user_follower = relationship(
        "User", back_populates="following", primaryjoin="User.id==Follow.follower_id"
    )
    user_followee = relationship(
        "User", back_populates="followers", primaryjoin="User.id==Follow.followee_id"
    )


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tweet_id = Column(Integer, ForeignKey("tweets.id"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    owner = relationship("User", back_populates="comments")
    tweet = relationship("Tweet", back_populates="comments")
