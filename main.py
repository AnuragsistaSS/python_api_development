from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import List,Dict,Any
from passlib.context import CryptContext
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from psycopg2 import DatabaseError
import models,schema
from database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from routers import users, post, auth
import utils
app = FastAPI()
load_dotenv()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(post.router)
app.include_router(auth.router)