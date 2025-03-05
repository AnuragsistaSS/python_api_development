from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import models,schema,utils , oauth2
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/login",response_model=schema.Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends() ,db : Session = Depends(get_db)):

    User = db.query(models.Users).filter(models.Users.email==user_credentials.username).first()
    if not User:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"User with {User.email} not found")
    if not utils.verify_password(user_credentials.password,User.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid password")
    access_token = oauth2.create_access_token(data={"user_id":User.id})
    return {"access_token":access_token,"token_type":"bearer"}

