from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schema, models, oauth2
from database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)
@router.get("/",response_model=List[schema.PostOut])
def get_all_Posts( db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.email)
    all_Posts = db.query(models.Post).all()
    if all_Posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No records found")

    return all_Posts
    

@router.post("/add_post",status_code = status.HTTP_201_CREATED, response_model=schema.PostOut)
def add_Post(post:schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    new_Post = models.Post(owner_id = current_user.id,**post.model_dump())
    db.add(new_Post)
    db.commit()
    db.refresh(new_Post)
    print(new_Post)
    return new_Post
    
@router.get("/get_post", response_model=schema.PostOut)
def get_Post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    Post = db.query(models.Post).filter(models.Post.id==id).first()
    if not Post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} not found")
    if not models.Post.id == current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"User with {current_user.id} not allowed to view this post")
    
    return Post
    
@router.get("/get_posts", response_model=List[schema.PostOut])
def get_Posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user), Limit: int = 10,skip: int = 0,search: Optional[str] = ""):

    Post = db.query(models.Post).filter(models.Post.owner_id == current_user.id,models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    if not Post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post not found")
    return Post
   

# deleting a post 
@router.delete("/get_post", status_code=status.HTTP_204_NO_CONTENT)
def del_Post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    Post_query = db.query(models.Post).filter(models.Post.id==id)
    if not Post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} not found")
    Post_query.delete(synchronize_session= False)
    db.commit()

    

# updating a Post
@router.put("/get_post", status_code=status.HTTP_201_CREATED, response_model= schema.PostOut)
def updated_Post(id:int, new_details : schema.UpdatePost, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    Post_query = db.query(models.Post).filter(models.Post.id==id)
    if not Post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} not found")
    Post_query.update(new_details.model_dump(), synchronize_session=False)
    upd_post = Post_query.first()
    db.commit()
    return upd_post 