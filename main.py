from fastapi import FastAPI

from frontend import frontend
from sql_app import main

app = FastAPI(title='uglyTwitter')


app.include_router(frontend.router)
app.include_router(main.router, prefix='/api')
