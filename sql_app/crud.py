import bcrypt
from sqlalchemy.orm import Session
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
