from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse, RedirectResponse

from app.api.auth import TokenData, get_bearer

router = APIRouter()


@router.get("/")
async def read_root(bearer: Optional[TokenData] = Depends(get_bearer)):
    if bearer:
        path = "/home"
    else:
        path = "/login"
    return RedirectResponse(path, status_code=302)
