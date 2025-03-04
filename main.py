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
from models import Base
from database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
app = FastAPI()
load_dotenv()

models.Base.metadata.create_all(bind=engine)

sample_data = [
    {
        "roll_no": 101,
        "name": "Alice Johnson",
        "courses": ["Mathematics", "Physics", "Computer Science"]
    },
    {
        "roll_no": 102,
        "name": "Bob Smith",
        "courses": ["History", "Philosophy", "English"]
    },
    {
        "roll_no": 103,
        "name": "Charlie Brown",
        "courses": ["Biology", "Chemistry", "Mathematics"]
    },
    {
        "roll_no": 104,
        "name": "David Clark",
        "courses": ["Psychology", "Sociology", "Statistics"]
    },
    {
        "roll_no": 105,
        "name": "Eve White",
        "courses": ["Art", "Music", "Literature"]
    }
]


class Student(BaseModel):
    #student details 
    roll_no:int
    name:str
    courses: List[str]


# setting up databse conncetion 

try:
    Database_host = os.getenv("DATABASE_HOST")
    Database_port = os.getenv("PORT")
    Database_name = os.getenv('DATABASE')
    User = os.getenv("USER")
    Password = os.getenv("PASSWORD")
    conn = psycopg2.connect(host = Database_host, port=Database_port, database = Database_name, user=User, password=Password, cursor_factory=RealDictCursor)
    cursor = conn.cursor()

except Exception as error:
    print("Failed to connect to database \n")
    print(f"Error:{error}")
    


def find_student(roll_no):
    index = 0 
    for data in sample_data:
        if data["roll_no"]==roll_no:
            return index
        else:
            index+=1
    return None

@app.get("/")
def get_all_students():
    cursor.execute("""select * from public."Student Details" """)
    all_details = cursor.fetchall()
    if all_details is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No records available")

    return{"Student_details":all_details}


@app.post("/add_student",status_code = status.HTTP_201_CREATED)
def add_student(student:Student):
    try:

        cursor.execute(""" insert into public."Student Details" (roll_no,name,courses) values(%s,%s,%s);
                   select * from public."Student Details" """,(student.roll_no,student.name,student.courses))
        conn.commit()
        student_details = cursor.fetchall()
        return {"student_details ": student_details}
    except Exception as e:
        #conn.rollback()
        print("Error occurred:", e)
        raise HTTPException(status_code=500, detail=f"Exception: {e}")
        
    
    # student_details = student.model_dump()
    # sample_data.append(student_details)
    # print(sample_data)
    

@app.get("/get_student/{roll_no}")
def get_student(roll_no: int):
    cursor.execute(""" select from public."Student Details" where roll_no = %s""",str(roll_no))
    student_detail = cursor.fetchone()
    if student_detail is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    return {f"Details of student with {roll_no}": student_detail}
    # index = find_student(roll_no)
    # if index is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail = f"post with id: {roll_no} was not found")
    # return {"student_details": sample_data[index]}

# deleting a post 
@app.delete("/get_student/{roll_no}", status_code=status.HTTP_204_NO_CONTENT)
def del_student(roll_no: int ):
    cursor.execute("""delete from public."Student Details" where roll_no = %s ;
                   select * from public."Student Details" """, str(roll_no))
    conn.commit()

    # index = find_student(roll_no)
    # if index is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail = f"post with id: {roll_no} was not found")
    # else:
    #     sample_data.pop(index)

# updating a student
@app.put("/get_student/{roll_no}", status_code=status.HTTP_201_CREATED)
def updated_student(roll_no:int, new_details : Student):
    # now working on ORM
    cursor.execute(""" UPDATE public."Student Details" set roll_no = %s, name = %s, courses = %s where roll_no  = %s ;
                   select * from public."Student Details" """ , (new_details.roll_no,new_details.name,new_details.courses, str(roll_no)))
    updated_details = cursor.fetchall()
    conn.commit()
    return{"Updated Student details": updated_details}


    
# checking sqlaclhemy functionality

@app.get("/sqlalchemy")
def test_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return {"Students": students}

