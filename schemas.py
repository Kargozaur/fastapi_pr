from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    published: bool


class PostResponse(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attribute = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attribute = True


class UserLogin(UserCreate):
    pass


class Token(BaseModel):
    access_token: set
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
