from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import List,Dict,Any
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from psycopg2 import DatabaseError
import models,schema
from database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
app = FastAPI()
load_dotenv()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def get_all_Posts( db: Session = Depends(get_db)):
    all_Posts = db.query(models.Post).all()
    if all_Posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No records found")

    return {"Post Records": all_Posts}
    

@app.post("/add_post",status_code = status.HTTP_201_CREATED, response_model=schema.Post)
def add_Post(post:schema.Post, db: Session = Depends(get_db)):
    new_Post = models.Post(**post.model_dump())
    db.add(new_Post)
    db.commit()
    db.refresh(new_Post)
    print(new_Post)
    return new_Post
    

@app.get("/get_post/{id}")
def get_Post(id: int, db: Session = Depends(get_db)):

    Post = db.query(models.Post).filter(models.Post.id==id).first()
    if not Post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} not found")

    return {"Post": Post}    
   

# deleting a post 
@app.delete("/get_post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_Post(id: int,db: Session = Depends(get_db)):
    
    Post_query = db.query(models.Post).filter(models.Post.id==id)
    if not Post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} not found")
    Post_query.delete(synchronize_session= False)
    db.commit()

    

# updating a Post
@app.put("/get_post/{id}", status_code=status.HTTP_201_CREATED, response_model= schema.Post)
def updated_Post(id:int, new_details : schema.Post, db: Session = Depends(get_db)):
    Post_query = db.query(models.Post).filter(models.Post.id==id)
    if not Post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} not found")
    Post_query.update(new_details.model_dump(), synchronize_session=False)
    db.commit()
    return Post_query.first()


