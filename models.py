from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__= "Posts" 
    
    title = Column(String,nullable=False)
    content = Column(String,nullable=False) 
    published = Column(Boolean, server_default='TRUE', nullable=False)
    id = Column(Integer,primary_key = True, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True),nullable= False, server_default = text('now()'))
    owner_id = Column(Integer,ForeignKey('Users.id',ondelete='CASCADE'),nullable=False)
    owner = relationship("Users")
class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),nullable= False, server_default = text('now()'))
    