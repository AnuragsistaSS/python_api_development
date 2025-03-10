from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.config import settings 
load_dotenv(dotenv_path=".env")

try:
    print("Connecting to database")
    password = settings.database_password.replace('@', '%40')
    SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_user}:{password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False , autoflush = False , bind = engine)
    Base = declarative_base()
    print("Succesfully connected to database")


except Exception as e:
    print("Failed to connect to database")
    print(f"Error: {e}")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()