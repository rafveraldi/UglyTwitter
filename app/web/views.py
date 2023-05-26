from datetime import timedelta
from typing import Optional, Union

from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import templates
from app.api.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    TokenData,
    create_access_token,
    get_bearer,
    get_user,
)
from app.api.crud import get_tweets_explore, get_tweets_home, get_tweets_user
from app.api.main import get_db
from app.api.schemas import UserCreate
from app.web.login import login_for_cookie

router = APIRouter()


@router.get("/home")
async def read_home(
    request: Request,
    bearer: Optional[TokenData] = Depends(get_bearer),
    db: Session = Depends(get_db),
    invalid: Optional[bool] = None,
):
    if bearer:
        user = get_user(db, bearer.username)
        tweets = get_tweets_home(user.id, db)
        context = {
            "request": request,
            "invalid": invalid,
            "user": user,
            "tweets": tweets,
        }
        return templates.TemplateResponse("/home.html", context)
    else:
        return RedirectResponse("/login?unauthorized=True", status_code=302)


@router.get("/explore")
async def read_explore(
    request: Request,
    bearer: Optional[TokenData] = Depends(get_bearer),
    db: Session = Depends(get_db),
    invalid: Optional[bool] = None,
):
    if bearer:
        user = get_user(db, bearer.username)
        tweets = get_tweets_explore(user.id, db)
        context = {
            "request": request,
            "invalid": invalid,
            "user": user,
            "tweets": tweets,
        }
        return templates.TemplateResponse("/home.html", context)
    else:
        return RedirectResponse("/login?unauthorized=True", status_code=302)


@router.get("/{username:str}")
async def read_profile(
    request: Request,
    username: str,
    follow: Optional[bool] = None,
    bearer: Optional[TokenData] = Depends(get_bearer),
    db: Session = Depends(get_db),
):
    if bearer:
        user = get_user(db, bearer.username)
        user_profile = get_user(db, username)
        if user_profile:
            user_profile = user_profile
            tweets = get_tweets_user(user_profile.id, db)
            follow = follow
            context = {
                "request": request,
                "follow": follow,
                "user": user,
                "user_profile": user_profile,
                "tweets": tweets,
            }
            return templates.TemplateResponse("/profile.html", context)
        else:
            return RedirectResponse("/home?invalid=True", status_code=302)
    else:
        return RedirectResponse("/login?unauthorized=True", status_code=302)
