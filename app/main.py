from fastapi import FastAPI
from passlib.context import CryptContext
from app.models import Base
from app.database import engine
from app.routers import users, post, auth,vote
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status
app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
Base.metadata.create_all(bind=engine)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/", status_code= status.HTTP_200_OK)
def read_root():
    return {"Message": "Hello World"}