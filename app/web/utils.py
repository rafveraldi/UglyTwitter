import asyncio
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Form, Header, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app import templates
from app.api.auth import TokenData, get_bearer, get_user
from app.api.crud import (
    create_comment,
    create_follow,
    create_like,
    create_tweet,
    delete_comment,
    delete_follow,
    delete_like,
    delete_tweet,
    get_comment_by_id,
    get_tweet_by_id,
    update_comment,
    update_tweet,
)
from app.api.main import get_db
from app.api.schemas import TweetBase

router = APIRouter()


@router.post("/follow/{user_profile}")
async def post_follow(
    request: Request,
    user_profile: str,
    bearer: TokenData = Depends(get_bearer),
    db: Session = Depends(get_db),
):
    user = get_user(db, bearer.username)
    user_profile = get_user(db, user_profile)
    create_follow(user.id, user_profile.id, db)
    context = {
        "request": request,
        "user": user,
        "user_profile": user_profile,
    }
    return templates.TemplateResponse("/partials/follow.html", context)


@router.delete("/follow/{user_profile}")
async def remove_follow(
    request: Request,
    user_profile: str,
    bearer: TokenData = Depends(get_bearer),
    db: Session = Depends(get_db),
):
    user = get_user(db, bearer.username)
    user_profile = get_user(db, user_profile)
    delete_follow(user.id, user_profile.id, db)
    context = {
        "request": request,
        "user": user,
        "user_profile": user_profile,
    }
    return templates.TemplateResponse("/partials/follow.html", context)


@router.post("/tweet/{tweet_id:int}/like", response_class=HTMLResponse)
async def post_like(
    request: Request,
    tweet_id: int,
    bearer: TokenData = Depends(get_bearer),
    db: Session = Depends(get_db),
):
    user = get_user(db, bearer.username)
    create_like(tweet_id, user.id, db)
    tweet = get_tweet_by_id(tweet_id, db)
    context = {
        "request": request,
        "user": user,
        "tweet": tweet,
    }
    return templates.TemplateResponse("/partials/tweet.html", context)


@router.delete("/tweet/{tweet_id:int}/like", response_class=HTMLResponse)
async def remove_like(
    request: Request,
    tweet_id: int,
    bearer: TokenData = Depends(get_bearer),
    db: Session = Depends(get_db),
):
    user = get_user(db, bearer.username)
    delete_like(tweet_id, user.id, db)
    tweet = get_tweet_by_id(tweet_id, db)
    context = {
        "request": request,
        "user": user,
        "tweet": tweet,
    }
    return templates.TemplateResponse("/partials/tweet.html", context)


@router.post("/tweet", response_class=HTMLResponse)
async def post_tweet(
    request: Request,
    content: Annotated[str, Form()],
    bearer: TokenData = Depends(get_bearer),
    db: Session = Depends(get_db),
):
    user = get_user(db, bearer.username)
    tweet = create_tweet(user.id, content, db)
    context = {
        "request": request,
        "user": user,
        "tweet": tweet,
    }
    return templates.TemplateResponse("/partials/tweet.html", context)


@router.get("/tweet/{tweet_id:int}", response_class=HTMLResponse)
async def get_tweet(
    request: Request,
    tweet_id: int,
    bearer: TokenData = Depends(get_bearer),
    db: Session = Depends(get_db),
):
    user = get_user(db, bearer.username)
    tweet = get_tweet_by_id(tweet_id, db)
    context = {
        "request": request,
        "user": user,
        "tweet": tweet,
    }
    return templates.TemplateResponse("/partials/tweet.html", context)


@router.delete("/tweet/{tweet_id:int}", response_class=HTMLResponse)
async def remove_tweet(
    request: Request,
    tweet_id: int,
    bearer: TokenData = Depends(get_bearer),
    db: Session = Depends(get_db),
):
    user = get_user(db, bearer.username)
    delete_tweet(tweet_id, db)
    return ""


@router.get("/tweet/{tweet_id:int}/edit", response_class=HTMLResponse)
async def get_editable_tweet(
    request: Request,
    tweet_id: int,
    bearer: TokenData = Depends(get_bearer),
    db: Session = Depends(get_db),
):
    user = get_user(db, bearer.username)
    tweet = get_tweet_by_id(tweet_id, db)
    context = {
        "request": request,
        "user": user,
        "tweet": tweet,
    }
    return templates.TemplateResponse("/partials/tweet-edit.html", context)


@router.put("/tweet/{tweet_id:int}/edit", response_class=HTMLResponse)
async def post_edited_tweet(
    request: Request,
    content: Annotated[str, Form()],
    tweet_id: int,
    bearer: TokenData = Depends(get_bearer),
    db: Session = Depends(get_db),
):
    user = get_user(db, bearer.username)
    update_tweet(tweet_id, content, db)
    tweet = get_tweet_by_id(tweet_id, db)
    context = {
        "request": request,
        "user": user,
        "tweet": tweet,
    }
    return templates.TemplateResponse("/partials/tweet.html", context)


@router.post("/tweet/{tweet_id:int}/comment", response_class=HTMLResponse)
async def post_comment(
    request: Request,
    comment: Annotated[str, Form()],
    tweet_id: int,
    bearer: TokenData = Depends(get_bearer),
    db: Session = Depends(get_db),
):
    user = get_user(db, bearer.username)
    create_comment(comment, tweet_id, user.id, db)
    tweet = get_tweet_by_id(tweet_id, db)
    context = {
        "request": request,
        "user": user,
        "tweet": tweet,
    }
    return templates.TemplateResponse("/partials/tweet.html", context)


@router.get("/comment/{comment_id:int}", response_class=HTMLResponse)
async def get_comment(
    request: Request,
    comment_id: int,
    bearer: TokenData = Depends(get_bearer),
    db: Session = Depends(get_db),
):
    user = get_user(db, bearer.username)
    comment = get_comment_by_id(comment_id, db)
    context = {
        "request": request,
        "user": user,
        "comment": comment,
    }
    return templates.TemplateResponse("/partials/comment.html", context)


@router.delete("/comment/{comment_id:int}", response_class=HTMLResponse)
async def remove_comment(
    request: Request,
    comment_id: int,
    bearer: TokenData = Depends(get_bearer),
    db: Session = Depends(get_db),
):
    user = get_user(db, bearer.username)
    delete_comment(comment_id, db)
    return ""


@router.get("/comment/{comment_id:int}/edit", response_class=HTMLResponse)
async def get_editable_comment(
    request: Request,
    comment_id: int,
    bearer: TokenData = Depends(get_bearer),
    db: Session = Depends(get_db),
):
    user = get_user(db, bearer.username)
    comment = get_comment_by_id(comment_id, db)
    context = {
        "request": request,
        "user": user,
        "comment": comment,
    }
    return templates.TemplateResponse("/partials/comment-edit.html", context)


@router.put("/comment/{comment_id:int}/edit", response_class=HTMLResponse)
async def post_edited_comment(
    request: Request,
    content: Annotated[str, Form()],
    comment_id: int,
    bearer: TokenData = Depends(get_bearer),
    db: Session = Depends(get_db),
):
    user = get_user(db, bearer.username)
    update_comment(comment_id, content, db)
    comment = get_comment_by_id(comment_id, db)
    context = {
        "request": request,
        "user": user,
        "comment": comment,
    }
    return templates.TemplateResponse("/partials/comment.html", context)
