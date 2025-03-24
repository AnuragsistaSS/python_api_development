from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
import app.models as models
import app.schema as schema
import app.oauth2 as oauth2
from app.database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.get("/", response_model=List[schema.PostWithVotes], status_code=status.HTTP_200_OK)
def get_Posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), Limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    try:
        results_query = db.query(models.Post, func.count(models.Votes.post_id).label('votes')).join(models.Votes, models.Post.id == models.Votes.post_id, isouter=True).group_by(models.Post.id)
        results = results_query.filter(models.Post.title.contains(search)).offset(skip).limit(Limit).all()
        if not results:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No records found")
        return results
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/get_post/{id}", response_model=schema.PostWithVotes, status_code=status.HTTP_200_OK)
def get_Post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    try:
        results_query = db.query(models.Post, func.count(models.Votes.post_id).label('votes')).join(models.Votes, models.Post.id == models.Votes.post_id, isouter=True).where(models.Post.id == id).group_by(models.Post.id)
        results = results_query.first()
        if not results:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found")
        return results
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/add_post", status_code=status.HTTP_201_CREATED, response_model=schema.PostOut)
def add_Post(post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    try:
        new_Post = models.Post(owner_id=current_user.id, **post.model_dump())
        db.add(new_Post)
        db.commit()
        db.refresh(new_Post)
        return new_Post
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/delete_post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_Post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    try:
        Post_query = db.query(models.Post).filter(models.Post.id == id)
        if not Post_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found")
        Post_query.delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/update_post/{id}", status_code=status.HTTP_201_CREATED, response_model=schema.PostOut)
def updated_Post(id: int, new_details: schema.UpdatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    try:
        Post_query = db.query(models.Post).filter(models.Post.id == id)
        if not Post_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found")
        if not Post_query.first().owner_id == current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this post")
        Post_query.update(new_details.model_dump(), synchronize_session=False)
        upd_post = Post_query.first()
        db.commit()
        return upd_post
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
