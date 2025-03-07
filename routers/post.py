from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
import schema, models, oauth2
from database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)
@router.get("/",response_model=List[schema.PostWithVotes])
def get_Posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user), Limit: int = 10,skip: int = 0,search: Optional[str] = ""):

    results_query = db.query(models.Post,func.count(models.Votes.post_id).label('votes')).join(models.Votes,models.Post.id==models.Votes.post_id,isouter=True).group_by(models.Post.id)
    results = results_query.filter(models.Post.title.contains(search)).offset(skip).limit(Limit).all()
    print("results_query:",results_query)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No records found")
    return results
    
@router.get("/get_post/{id}", response_model=schema.PostWithVotes)
def get_Post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    results_query = db.query(models.Post,func.count(models.Votes.post_id).label('votes')).join(models.Votes,models.Post.id==models.Votes.post_id,isouter=True).where(models.Post.id==id).group_by(models.Post.id)
    results = results_query.first()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} not found")
    return results
    

@router.post("/add_post",status_code = status.HTTP_201_CREATED, response_model=schema.PostOut)
def add_Post(post:schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    new_Post = models.Post(owner_id = current_user.id,**post.model_dump())
    db.add(new_Post)
    db.commit()
    db.refresh(new_Post)
    print(new_Post)
    return new_Post

# deleting a post 
@router.delete("/delete_post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_Post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    Post_query = db.query(models.Post).filter(models.Post.id==id)
    if not Post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} not found")
    Post_query.delete(synchronize_session= False)
    db.commit()

    

# updating a Post
@router.put("/update_post/{id}", status_code=status.HTTP_201_CREATED, response_model= schema.PostOut)
def updated_Post(id:int, new_details : schema.UpdatePost, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    Post_query = db.query(models.Post).filter(models.Post.id==id)
    if not Post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} not found")
    Post_query.update(new_details.model_dump(), synchronize_session=False)
    upd_post = Post_query.first()
    db.commit()
    return upd_post 