from datetime import datetime

import bcrypt
from fastapi import status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_
from sqlalchemy.orm import Session

from . import auth, models, schemas


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_all_users(db: Session):
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.pwd_context.hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: schemas.UserBasic):
    db_user = db.query(models.User).filter(models.User.id == user.id).first().__dict__
    db_user_model = schemas.UserBasic(**db_user)
    update_data = user.dict(exclude_none=True)
    updated_user = db_user_model.copy(update=update_data)
    db.query(models.User).filter(models.User.id == user.id).update(updated_user.dict())
    db.commit()
    updated_user = jsonable_encoder(updated_user)
    return updated_user


def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(user)
    db.commit()
    return "User has been deleted."


def get_followers(user_id: int, db: Session):
    return db.query(models.Follow).filter(models.Follow.followee_id == user_id).all()


def get_following(user_id: int, db: Session):
    return db.query(models.Follow).filter(models.Follow.follower_id == user_id).all()


def check_following(follower_user_id: int, followee_user_id: int, db: Session):
    return (
        db.query(models.Follow)
        .filter(
            models.Follow.follower_id == follower_user_id,
            models.Follow.followee_id == followee_user_id,
        )
        .all()
        .__len__()
    )


def create_follow(follower_user_id: int, followee_user_id: int, db: Session):
    creation_datetime = datetime.utcnow()
    db_follow = models.Follow(
        follower_id=follower_user_id,
        followee_id=followee_user_id,
        created_at=creation_datetime,
    )
    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)
    return db_follow


def delete_follow(follower_user_id: int, followee_user_id: int, db: Session):
    follow = (
        db.query(models.Follow)
        .filter(
            models.Follow.follower_id == follower_user_id,
            models.Follow.followee_id == followee_user_id,
        )
        .first()
    )
    db.delete(follow)
    db.commit()
    return "Follow has been deleted."


def get_tweets_explore(user_id: int, db: Session):
    return (
        db.query(models.Tweet)
        .filter(models.Tweet.user_id != user_id)
        .order_by(models.Tweet.created_at.desc())
        .all()
    )


def get_tweets_user(user_id: int, db: Session):
    return db.query(models.Tweet).filter(models.Tweet.user_id == user_id).all()


def get_tweets_following(user_id: int, db: Session):
    query_following = db.query(models.Follow.followee_id).filter(
        models.Follow.follower_id == user_id
    )
    return (
        db.query(models.Tweet)
        .filter(models.Tweet.user_id.in_(query_following))
        .order_by(models.Tweet.created_at.desc())
        .all()
    )


def get_tweets_home(user_id: int, db: Session):
    query_following = db.query(models.Follow.followee_id).filter(
        models.Follow.follower_id == user_id
    )
    return (
        db.query(models.Tweet)
        .filter(
            or_(
                models.Tweet.user_id == user_id,
                models.Tweet.user_id.in_(query_following),
            )
        )
        .order_by(models.Tweet.created_at.desc())
        .all()
    )


def get_tweet_by_id(tweet_id: int, db: Session):
    return db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()


def create_tweet(current_user_id: int, tweet: schemas.TweetBase | str, db: Session):
    creation_datetime = datetime.utcnow()
    if type(tweet) == str:
        db_tweet = models.Tweet(
            content=tweet, user_id=current_user_id, created_at=creation_datetime
        )
    else:
        db_tweet = models.Tweet(
            content=tweet.content, user_id=current_user_id, created_at=creation_datetime
        )
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return db_tweet


def update_tweet(tweet_id: int, new_content: schemas.TweetBase | str, db: Session):
    db_tweet = get_tweet_by_id(tweet_id, db).__dict__
    db_tweet_model = schemas.TweetBasic(**db_tweet)
    if type(new_content) == str:
        update_data = {"content": new_content}
    else:
        update_data = new_content.dict()
    update_data["updated_at"] = datetime.utcnow()
    updated_tweet = db_tweet_model.copy(update=update_data)
    db.query(models.Tweet).filter(models.Tweet.id == tweet_id).update(
        updated_tweet.dict()
    )
    db.commit()
    updated_tweet = jsonable_encoder(updated_tweet)
    return updated_tweet


def delete_tweet(tweet_id: int, db: Session):
    tweet = db.query(models.Tweet).filter(models.Tweet.id == tweet_id).first()
    db.delete(tweet)
    db.commit()
    return "Tweet has been deleted."


def get_comments_tweet(tweet_id: int, db: Session):
    return db.query(models.Comment).filter(models.Comment.tweet_id == tweet_id).all()


def get_comment_by_id(comment_id: int, db: Session):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()


def create_comment(
    comment: schemas.CommentBase | str,
    current_tweet_id: int,
    current_user_id: int,
    db: Session,
):
    creation_datetime = datetime.utcnow()
    if type(comment) == str:
        db_comment = models.Comment(
            user_id=current_user_id,
            tweet_id=current_tweet_id,
            content=comment,
            created_at=creation_datetime,
        )
    else:
        db_comment = models.Comment(
            user_id=current_user_id,
            tweet_id=current_tweet_id,
            content=comment.content,
            created_at=creation_datetime,
        )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def update_comment(
    comment_id: int, new_content: schemas.CommentBase | str, db: Session
):
    db_comment = get_comment_by_id(comment_id, db).__dict__
    db_comment_model = schemas.Comment(**db_comment)
    if type(new_content) == str:
        update_data = {"content": new_content}
    else:
        update_data = new_content.dict()
    update_data["updated_at"] = datetime.utcnow()
    updated_comment = db_comment_model.copy(update=update_data)
    db.query(models.Comment).filter(models.Comment.id == comment_id).update(
        updated_comment.dict()
    )
    db.commit()
    updated_comment = jsonable_encoder(updated_comment)
    return updated_comment


def delete_comment(comment_id: int, db: Session):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    db.delete()
    db.commit()
    return "Comment has been deleted."


def check_like(current_tweet_id: int, current_user_id: int, db: Session):
    return (
        db.query(models.Like)
        .filter(
            models.Like.tweet_id == current_tweet_id,
            models.Like.user_id == current_user_id,
        )
        .all()
        .__len__()
    )


def create_like(current_tweet_id: int, current_user_id: int, db: Session):
    creation_datetime = datetime.utcnow()
    db_like = models.Like(
        user_id=current_user_id, tweet_id=current_tweet_id, created_at=creation_datetime
    )
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like


def delete_like(current_tweet_id: int, current_user_id: int, db: Session):
    like = (
        db.query(models.Like)
        .filter(
            models.Like.tweet_id == current_tweet_id,
            models.Like.user_id == current_user_id,
        )
        .first()
    )
    db.delete(like)
    db.commit()
    return dict()
