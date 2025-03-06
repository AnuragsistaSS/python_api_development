from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
import models, schema, oauth2
from sqlalchemy.orm import Session
from database import get_db
from typing import List
router = APIRouter(
    prefix="/vote",
    tags=["vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.VoteSchema, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_found = db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post with id {vote.post_id} not found")
    

    votes =db.query(models.Votes).filter(models.Votes.post_id==vote.post_id,models.Votes.user_id==current_user.id)
    vote_found = votes.first()
    print(vote_found)

    if vote.direction == 1 :
        if vote_found:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You have already voted")
        else:
            new_vote =models.Votes(user_id=current_user.id,post_id=vote.post_id)
            db.add(new_vote)
            db.commit()
            return {"message":"Voted successfully"}
    else:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You have not voted yet")
        else:
            db.delete(vote_found)
            db.commit()
            return {"message":"Vote removed"}
