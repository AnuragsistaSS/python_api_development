from fastapi import FastAPI
from passlib.context import CryptContext
import models
from database import engine
from routers import users, post, auth,vote

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)