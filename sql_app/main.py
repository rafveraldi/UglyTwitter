from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import auth, crud, models, schemas
from .database import Base, SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.post('/token', response_model=auth.Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect username or password', headers={'WWW-Authenticate': 'Bearer'})
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = auth.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered.")
    return crud.create_user(db=db, user=user)


@router.get('/users/me', response_model=schemas.User)
def read_users_me(db: Session = Depends(get_db), username: str = Depends(auth.get_current_username)):
    current_user = auth.get_user(db, username)
    return current_user


@router.put('/users/me', response_model=schemas.UserBasic)
def update_user_me(db: Session = Depends(get_db), current_user: schemas.UserBasic = Depends(read_users_me), new_details: schemas.UserBasic = Depends()):
    if new_details.id != current_user.id:
        raise HTTPException(
            status_code=400, detail="Id does not match authenticated user.")
    updated_user = crud.update_user(db, new_details)
    return updated_user


@router.delete('/users/me')
def delete_user_me(user_credentials: schemas.UserCreate, current_user: schemas.UserBasic = Depends(read_users_me), db: Session = Depends(get_db)):
    if not auth.get_user(db, user_credentials.username):
        raise HTTPException(
            status_code=400, detail="1 Username or password does not match authenticated user.")
    if current_user.id != auth.get_user(db, user_credentials.username).id:
        raise HTTPException(
            status_code=400, detail="2 Username or password does not match authenticated user.")
    if not auth.verify_password(user_credentials.password, current_user.password):
        raise HTTPException(
            status_code=400, detail="3 Username or password does not match authenticated user.")
    return crud.delete_user(db, current_user.id)

# @router.get('/tweets')
# def read_tweets():
#     return 'This are all tweets.'


# @router.post('/tweets')
# def create_tweet():
#     return 'Tweet has been created.'


# @router.put('/tweets/{id}')
# def update_tweet():
#     return 'Tweet {id} has been updated.'


# @router.delete('/tweets/{id}')
# def delete_tweet():
#     return 'Tweet {id} has been deleted.'
