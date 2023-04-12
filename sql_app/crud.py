import bcrypt
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.encoders import jsonable_encoder


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
    db_user = db.query(models.User).filter(
        models.User.id == user.id).first().__dict__
    db_user_model = schemas.UserBasic(**db_user)
    update_data = user.dict(exclude_none=True)
    updated_user = db_user_model.copy(update=update_data)
    db.query(models.User).filter(
        models.User.id == user.id).update(updated_user.dict())
    db.commit()
    updated_user = jsonable_encoder(updated_user)
    return updated_user


def delete_user(db: Session, user_id: int):
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return 'User has been deleted.'


def get_followers(user_id: int, db: Session):
    return db.query(models.Follow).filter(models.Follow.followee_id == user_id).all()


def get_following(user_id: int, db: Session):
    return db.query(models.Follow).filter(models.Follow.follower_id == user_id).all()


def check_following(follower_user_id: int, followee_user_id: int, db: Session):
    return db.query(models.Follow).filter(models.Follow.follower_id == follower_user_id, models.Follow.followee_id == followee_user_id).all().__len__()


def create_follow(follower_user_id: int, followee_user_id: int, db: Session):
    creation_datetime = datetime.utcnow()
    db_follow = models.Follow(follower_id=follower_user_id,
                              followee_id=followee_user_id, created_at=creation_datetime)
    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)
    return db_follow


def delete_follow(follower_user_id: int, followee_user_id: int, db: Session):
    db.query(models.Follow).filter(models.Follow.follower_id ==
                                   follower_user_id, models.Follow.followee_id == followee_user_id).delete()
    db.commit()
    return 'Follow has been deleted.'
