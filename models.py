from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql.expression import text

class Student(Base):
    __tablename__= "Student_details" 
    
    roll_no = Column(Integer,primary_key = True, nullable= False)
    name = Column(String,nullable=False)
    enrolled_courses = Column(ARRAY(String), nullable=True)
    added_at = Column(TIMESTAMP(timezone=True),nullable= False, server_default = text('now()'))
