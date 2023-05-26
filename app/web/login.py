from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import templates
from app.api.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    TokenData,
    authenticate_user,
    create_access_token,
    get_bearer,
    get_user,
)
from app.api.crud import create_user
from app.api.main import get_db
from app.api.schemas import UserCreate

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def get_login(
    request: Request,
    invalid: Optional[bool] = None,
    logged_out: Optional[bool] = None,
    unauthorized: Optional[bool] = None,
    bearer: Optional[TokenData] = Depends(get_bearer),
):
    context = {
        "request": request,
        "invalid": invalid,
        "logged_out": logged_out,
        "unauthorized": unauthorized,
    }
    if bearer:
        return RedirectResponse("/home", status_code=302)
    else:
        return templates.TemplateResponse("/login.html", context)


@router.post("/login")
async def login_for_cookie(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        response = RedirectResponse("/login?invalid=True", status_code=302)
    if user:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        response = RedirectResponse("/home", status_code=302)
        response.set_cookie(key="bearer", value=access_token)
    return response


@router.get("/register")
async def read_register(
    request: Request,
    bearer: Optional[TokenData] = Depends(get_bearer),
    invalid: Optional[bool] = None,
):
    if bearer:
        return RedirectResponse("/home", status_code=302)
    else:
        context = {"request": request, "invalid": invalid}
        return templates.TemplateResponse("/registration.html", context)


@router.post("/register")
async def post_register(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    db_user = get_user(db, username=form_data.username)
    if db_user:
        return RedirectResponse("/register?invalid=True", status_code=302)
    else:
        user = UserCreate(username=form_data.username, password=form_data.password)
        create_user(db, user=user)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        response = RedirectResponse("/home", status_code=302)
        response.set_cookie(key="bearer", value=access_token)
        return response


@router.get("/logout")
@router.post("/logout")
async def post_logout(bearer: Optional[TokenData] = Depends(get_bearer)):
    if not bearer:
        response = RedirectResponse("/login?logged_out=True", status_code=302)

    response = RedirectResponse("/login?logged_out=True", status_code=302)
    response.delete_cookie(key="bearer")
    return response
