from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import List,Dict,Any
import psycopg2 
import os
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from psycopg2 import DatabaseError
import models
from database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
app = FastAPI()
load_dotenv()

models.Base.metadata.create_all(bind=engine)


class Student(BaseModel):
    roll_no : int 
    name : str
    enrolled_courses : List[str]


# setting up databse conncetion 

# try:
#     Database_host = os.getenv("DATABASE_HOST")
#     Database_port = os.getenv("PORT")
#     Database_name = os.getenv('DATABASE')
#     User = os.getenv("USER")
#     Password = os.getenv("PASSWORD")
#     conn = psycopg2.connect(host = Database_host, port=Database_port, database = Database_name, user=User, password=Password, cursor_factory=RealDictCursor)
#     cursor = conn.cursor()

# except Exception as error:
#     print("Failed to connect to database \n")
#     print(f"Error:{error}")
    
def find_student(roll_no):
    index = 0 
    for data in sample_data:
        if data["roll_no"]==roll_no:
            return index
        else:
            index+=1
    return None

@app.get("/")
def get_all_students( db: Session = Depends(get_db)):
    all_students = db.query(models.Student).all()
    if all_students is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No records found")

    return {"Student Records": all_students}
    

@app.post("/add_student",status_code = status.HTTP_201_CREATED)
def add_student(student:Student, db: Session = Depends(get_db)):
   

    new_student = models.Student(**student.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {"New student":new_student}
    

@app.get("/get_student/{roll_no}")
def get_student(roll_no: int, db: Session = Depends(get_db)):

    student = db.query(models.Student).filter(models.Student.roll_no==roll_no).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"student with {roll_no} not found")

    return {"student": student}    
   

# deleting a post 
@app.delete("/get_student/{roll_no}", status_code=status.HTTP_204_NO_CONTENT)
def del_student(roll_no: int,db: Session = Depends(get_db)):
    
    student_query = db.query(models.Student).filter(models.Student.roll_no==roll_no)
    if not student_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"student with {roll_no} not found")
    student_query.delete(synchronize_session= False)
    db.commit()

    

# updating a student
@app.put("/get_student/{roll_no}", status_code=status.HTTP_201_CREATED)
def updated_student(roll_no:int, new_details : Student, db: Session = Depends(get_db)):
    student_query = db.query(models.Student).filter(models.Student.roll_no==roll_no)
    if not student_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"student with roll no {roll_no} not found")
    student_query.update(new_details.model_dump(), synchronize_session=False)
    db.commit()
    return{"message": f"Succesfully updated student with roll no {roll_no}"}

   