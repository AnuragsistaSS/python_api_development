from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schema, models , utils
from database import get_db
from typing import List
# User routes
router = APIRouter(
    prefix="/users",
    tags=["users"],
)
@router.get("/get_users",response_model=List[schema.UserCreate])
def get_all_users(db:Session = Depends(get_db)):
    all_users = db.query(models.Users).all()
    if all_users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No records found")

    return all_users



@router.post("/add_user",status_code = status.HTTP_201_CREATED, response_model=schema.UserOut)
def add_User(user:schema.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_User = models.Users(**user.model_dump())
    db.add(new_User)
    db.commit()
    db.refresh(new_User)
    return new_User

@router.get("/get_user/{id}",response_model=schema.UserOut)
def get_user(id : int, db:Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with {id} not found")
    return user

@router.delete("/get_user/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_user(id: int,db: Session = Depends(get_db)):
    
    user_query = db.query(models.Users).filter(models.Users.id==id)
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with {id} not found")
    user_query.delete(synchronize_session= False)
    db.commit()

@router.put("/get_user/{id}",status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def update_user(id:int, updated_user: schema.UserCreate, db: Session = Depends(get_db)):
    user_query = db.query(models.Users).filter(models.Users.id==id)
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with {id} not found")
    user_query.udate(updated_user.model_dump(), synchronize_session=False)
    db.commit()
   