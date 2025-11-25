from typing import List
from fastapi import Depends, HTTPException, Response
import sqlalchemy.orm.session as Session
from database import get_db
import models
from schemas import PostBase, PostCreate, PostResponse, PostUpdate
from fastapi import APIRouter

router = APIRouter(prefix="/posts", tags=["posts"])

# CRUD realirealization


@router.get("/", response_model=List[PostBase])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=201, response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/latest")
def get_latest(db: Session = Depends(get_db)):
    query = db.query(models.Post).order_by(models.Post.id.desc()).first()
    return query


@router.get("/{post_id}", response_model=PostBase)
def get_post(post_id: int, db: Session = Depends(get_db)):
    test_id = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not test_id:
        raise HTTPException(status_code=404, detail="post not found")
    return test_id


@router.delete("/{post_id}", status_code=204)
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


@router.put("/{post_id}", status_code=205)
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
