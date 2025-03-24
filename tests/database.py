# from app.config import settings
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from app import models
# from fastapi.testclient import TestClient
# from app.main import app
# from app.database import get_db
# import pytest

# try:
#     print("Connecting to database")
#     password = settings.database_password.replace('@', '%40')
#     SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_user}:{password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
#     engine = create_engine(SQLALCHEMY_DATABASE_URL)
#     TestingSessionLocal = sessionmaker(autocommit=False , autoflush = False , bind = engine)
#     models.Base.metadata.create_all(bind=engine)
#     Base = declarative_base()
#     print("Succesfully connected to database")


# except Exception as e:
#     print("Failed to connect to database")
#     print(f"Error: {e}")



# @pytest.fixture
# def session():
#     print("Creating session")
#     models.Base.metadata.drop_all(bind=engine)
#     models.Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @pytest.fixture
# def client(session):
#     def override_get_db():
#         try:
#             yield session
#         finally:
#             session.close()
#     app.dependency_overrides[get_db] = override_get_db

#     yield TestClient(app)
