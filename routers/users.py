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
@router.get("/",response_model=List[schema.UserCreate])
def get_all_users(db:Session = Depends(get_db)):
    try:

        all_users = db.query(models.Users).all()
        if all_users is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No records found")

        return all_users
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Error: {e}")



@router.post("/add_user",status_code = status.HTTP_201_CREATED, response_model=schema.UserOut)
def add_User(user:schema.UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_password = utils.hash_password(user.password)
        user.password = hashed_password
        new_User = models.Users(**user.model_dump())
        db.add(new_User)
        db.commit()
        db.refresh(new_User)
        return new_User
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Error: {e}")

@router.get("/get_user/{id}",response_model=schema.UserOut)
def get_user(id : int, db:Session = Depends(get_db)):
    try:
        user = db.query(models.Users).filter(models.Users.id==id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with {id} not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Error: {e}")

@router.delete("/delete_user/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_user(id: int,db: Session = Depends(get_db)):
    try:
        user_query = db.query(models.Users).filter(models.Users.id==id)
        if not user_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with {id} not found")
        user_query.delete(synchronize_session= False)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Error: {e}")

@router.put("/update_user/{id}",status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def update_user(id:int, updated_user: schema.UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_password = utils.hash_password(updated_user.password)
        updated_user.password = hashed_password
        print(updated_user.password)
        user_query = db.query(models.Users).filter(models.Users.id==id)
        if not user_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with {id} not found")
        user_query.update(updated_user.model_dump(), synchronize_session=False)
        db.commit()
        return user_query.first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Error: {e}")
# End of User routes