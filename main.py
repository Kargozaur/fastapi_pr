from fastapi import FastAPI, HTTPException, Depends, Response
import sqlalchemy.orm.session as Session
import models
from database import engine, get_db
from sqlalchemy import delete
from schemas import (
    PostBase,
    PostCreate,
    PostUpdate,
    PostResponse,
    UserCreate,
    UserResponse,
)
from typing import List
from pwdlib import PasswordHash
import jwt
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

Password_hash = PasswordHash.recommended()

models.Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "hello world"}


@app.get("/posts", response_model=List[PostBase])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=201, response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/latest")
def get_latest(db: Session = Depends(get_db)):
    query = db.query(models.Post).order_by(models.Post.id.desc()).first()
    return query


@app.get("/posts/{post_id}", response_model=PostBase)
def get_post(post_id: int, db: Session = Depends(get_db)):
    test_id = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not test_id:
        raise HTTPException(status_code=404, detail="post not found")
    return test_id


@app.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning * """, (str(post_id)))
    # deleted_post = cursor.fetchone()
    deleted_post = db.query(models.Post).filter(models.Post.id == post_id)
    if not deleted_post.first():
        raise HTTPException(status_code=404, detail="post not found")
    # conn.commit()
    deleted_post.delete(synchronize_session=False)
    db.commit()
    # return statement doesnt do anything
    return deleted_post


@app.put("/posts/{post_id}", status_code=205)
def update_post(post_id: int, post: PostUpdate, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    db_post = post_query.first()
    if not db_post:
        raise HTTPException(status_code=404, detail="post not found")
    post_query.update(
        post.model_dump(),
        synchronize_session=False,
    )
    db.commit()
    return Response(status_code=205)


@app.post("/users", status_code=201, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_passwd = "pass"
    user.password = hashed_passwd
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
