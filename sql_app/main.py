from datetime import datetime, timedelta
from typing import Annotated, List

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


@router.get('/followers/{user_id:int}', response_model=List[schemas.Follow])
def read_followers(user_id: int, db: Session = Depends(get_db)):
    return crud.get_followers(user_id, db)


@router.get('/following/{user_id:int}', response_model=List[schemas.Follow])
def read_following(user_id: int, db: Session = Depends(get_db)):
    return crud.get_following(user_id, db)


@router.post('/follow/{followee_user_id:int}', response_model=schemas.Follow)
def create_follow(followee_user_id: int, current_user: schemas.User = Depends(read_users_me), db: Session = Depends(get_db)):
    if followee_user_id == current_user.id:
        raise HTTPException(
            status_code=400, detail="You can't follow yourself.")
    db_followee_id = crud.get_user_by_id(db, followee_user_id)
    if not db_followee_id:
        raise HTTPException(
            status_code=400, detail="Followee id does not exist.")
    following_check = crud.check_following(
        current_user.id, followee_user_id, db)
    if following_check != 0:
        raise HTTPException(
            status_code=400, detail="Already following this person.")
    return crud.create_follow(current_user.id, followee_user_id, db)


@router.delete('/follow/{followee_user_id:int}')
def delete_follow(followee_user_id: int, current_user: schemas.User = Depends(read_users_me), db: Session = Depends(get_db)):
    db_followee_id = crud.get_user_by_id(db, followee_user_id)
    if not db_followee_id:
        raise HTTPException(
            status_code=400, detail="Followee id does not exist.")
    following_check = crud.check_following(
        current_user.id, followee_user_id, db)
    if following_check == 0:
        raise HTTPException(
            status_code=400, detail="You're not following this person.")
    return crud.delete_follow(current_user.id, followee_user_id, db)


@router.get('/tweets', response_model=List[schemas.Tweet])
def read_tweets_explore(current_user: schemas.User = Depends(read_users_me), db: Session = Depends(get_db)):
    return crud.get_tweets_explore(current_user.id, db)


@router.get('/tweets/{user_id:int}', response_model=List[schemas.Tweet])
def read_tweets_user(user_id: int, current_user: schemas.User = Depends(read_users_me), db: Session = Depends(get_db)):
    return crud.get_tweets_user(user_id, db)


@router.get('/tweets/following', response_model=List[schemas.Tweet])
def read_tweets_following(current_user: schemas.User = Depends(read_users_me), db: Session = Depends(get_db)):
    return crud.get_tweets_following(current_user.id, db)


@router.post('/tweets', response_model=schemas.Tweet)
def create_tweet(tweet: schemas.TweetBase, current_user: schemas.User = Depends(read_users_me), db: Session = Depends(get_db)):
    return crud.create_tweet(current_user.id, tweet, db)


@router.put('/tweets/{tweet_id:int}', response_model=schemas.Tweet)
def update_tweet(tweet_id, new_content: schemas.TweetBase, current_user: schemas.User = Depends(read_users_me), db: Session = Depends(get_db)):
    current_tweet = crud.get_tweet_by_id(tweet_id, db)
    if current_tweet.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail="Tweet not owned by autheticated user.")
    updated_tweet = crud.update_tweet(tweet_id, new_content, db)
    return updated_tweet


@router.delete('/tweets/{tweet_id:int}')
def delete_tweet(tweet_id, current_user: schemas.User = Depends(read_users_me), db: Session = Depends(get_db)):
    current_tweet = crud.get_tweet_by_id(tweet_id, db)
    if not current_tweet:
        raise HTTPException(
            status_code=400, detail="Tweet id does not exist.")
    if current_tweet.user_id != current_user.id:
        raise HTTPException(
            status_code=400, detail="Tweet not owned by autheticated user.")
    return crud.delete_tweet(tweet_id, db)
