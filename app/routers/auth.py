from fastapi import status, HTTPException, Depends, APIRouter
import app.models as models
import app.schema as schema
import app.utils as utils
import app.oauth2 as oauth2
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/login",response_model=schema.Token, status_code=status.HTTP_200_OK)
def login(user_credentials : OAuth2PasswordRequestForm = Depends() ,db : Session = Depends(get_db)):
    if user_credentials.username == "" or user_credentials.password == "":
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Invalid credentials")
    
    User = db.query(models.Users).filter(models.Users.email==user_credentials.username).first()
    if not User:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"User with {user_credentials.username} not found")
    if not utils.verify_password(user_credentials.password,User.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid password")
    access_token = oauth2.create_access_token(data={"user_id":User.id})
    return {"access_token":access_token,"token_type":"bearer"}

