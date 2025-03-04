from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import models,schema,utils
from sqlalchemy.orm import Session
from database import get_db
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/login")
def login(user:schema.UserLogin,db : Session = Depends(get_db)):
    User = db.query(models.Users).filter(models.Users.email==user.email).first()
    if not User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with {User.email} not found")
    if not utils.verify_password(user.password,User.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid password")
    return {"message":"Login successful"}