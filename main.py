from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import sqlalchemy.orm.session as Session
import models
from database import engine, get_db


models.Base.metadata.create_all(engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="1234",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Connected to db")
        break
    except Exception as e:
        print(e)
        time.sleep(2)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/")
def root():
    return {"message": "hello world"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts; """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    return {"status": "success"}


@app.post("/posts", status_code=201)
def create_post(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING * """,
        (post.title, post.content),
    )
    post_dict = cursor.fetchone()
    conn.commit()
    return {"data": post_dict}


@app.get("/posts/latest")
def get_latest():
    cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1""")
    latest = cursor.fetchall()
    return {"data": latest}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(post_id)))
    test_id = cursor.fetchone()
    if not test_id:
        raise HTTPException(status_code=404, detail="post not found")
    return {"data": test_id}


@app.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning * """, (str(post_id)))
    deleted_post = cursor.fetchone()
    if not deleted_post:
        raise HTTPException(status_code=404, detail="post not found")
    conn.commit()
    return deleted_post


@app.put("/posts/{post_id}", status_code=205)
def update_post(post_id: int, updated_post: Post):
    cursor.execute(
        """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning * """,
        (
            updated_post.title,
            updated_post.content,
            updated_post.published,
            str(post_id),
        ),
    )
    update_posts = cursor.fetchone()
    if not update_posts:
        raise HTTPException(status_code=404, detail="post not found")
    conn.commit()
    return {"detail": update_posts}
