from pydantic import BaseModel
from typing import Optional, List

class PostBase(BaseModel):
    title : str 
    content : str
    published: bool = True

class PostCreate(BaseModel):
    pass
class Post(BaseModel):
    title : str 
    content : str
    published: bool = True

    class Config:
        from_attributes = True
class UpdatePost(BaseModel):
    title: Optional[str]
    content: Optional[str]

    class Config:
        orm_mode = True




