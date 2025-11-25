from fastapi import FastAPI
import models
from database import engine
from routers import posts
from routers import users
from routers import auth
from utility import *

models.Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "hello world"}


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
