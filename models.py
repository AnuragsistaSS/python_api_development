from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY

class Student(Base):
    __tablename__= "Student_details" 
    
    roll_no = Column(Integer,primary_key = True, nullable= False)
    name = Column(String,nullable=False)
    enrolled_courses = Column(ARRAY(String), nullable=True)
