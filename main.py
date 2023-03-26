from fastapi import FastAPI

from sql_app import main
from frontend import frontend


app = FastAPI(title='UglyTwitter')


app.include_router(frontend.router)
app.include_router(main.router, prefix='/api')
