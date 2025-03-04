from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
load_dotenv()
try:
    username = os.getenv("USER")
    password = os.getenv("PASSSWORD")
    hostname = os.getenv("DATABASE_HOST")
    database_name = os.getenv("DATABASE")
    
    
    SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
    engine = create_engine

except Exception as e:
    print("Failed to connect to database")
    print(f"Error: {e}")
