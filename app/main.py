from fastapi import FastAPI

from .api import main
from .web import login, root, utils, views

app = FastAPI(title="Ugly")

app.include_router(root.router)
app.include_router(login.router)
app.include_router(views.router)
app.include_router(utils.router, prefix="/webutils")
app.include_router(main.router, prefix="/api")
