from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schema
class UserCreate(BaseModel):
    id: int
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Post schema
class PostBase(BaseModel):
    title : str 
    content : str
    published: bool = True

class PostCreate(PostBase):
    pass
class PostOut(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner : UserOut
    class Config:
        from_attributes = True

class UpdatePost(BaseModel):
    #title: Optional[str]
    content: Optional[str]
    #published: Optional[bool]

# Token schema
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None