from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from database import get_db
import models
from routers.oauth2 import create_access_token
from schemas import UserLogin
from utility import verify_password

router = APIRouter()


@router.post("/login")
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )
    if not user:
        raise HTTPException(status_code=403, detail="Invalid credentials")

    if not verify_password(
        user_credentials.password,
        user.password,
    ):
        raise HTTPException(status_code=403, detail="Invalid credentials")

    access_token = create_access_token(data={"user_id": user.id})

    return {"access token": access_token, "token_type": "Bearer"}
