from fastapi import FastAPI
import sqlalchemy.orm.session as Session
import models
from database import engine, get_db
from routers import posts
from routers import users
from utility import *

models.Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "hello world"}


app.include_router(posts.router)
app.include_router(users.router)
