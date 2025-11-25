from fastapi import Depends, HTTPException
from database import get_db
import sqlalchemy.orm.session as Session
import models
from schemas import UserCreate, UserResponse
from utility import hash_password
from fastapi import APIRouter

router = APIRouter(prefix="/users")


@router.post("/", status_code=201, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_passwd = hash_password(user.password)
    user.password = hashed_passwd
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{uid}", status_code=200, response_model=UserResponse)
def get_user(uid: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == uid).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
