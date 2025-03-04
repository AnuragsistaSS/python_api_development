from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class PostBase(BaseModel):
    title : str 
    content : str
    published: bool = True

class PostCreate(BaseModel):
    pass
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UpdatePost(BaseModel):
    title: Optional[str]
    content: Optional[str]

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    id: int
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
