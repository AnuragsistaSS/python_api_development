from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import models
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.oauth2 import create_access_token
import pytest

try:
    print("Connecting to database")
    password = settings.database_password.replace('@', '%40')
    SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_user}:{password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False , autoflush = False , bind = engine)
    models.Base.metadata.create_all(bind=engine)
    Base = declarative_base()
    print("Succesfully connected to database")


except Exception as e:
    print("Failed to connect to database")
    print(f"Error: {e}")



@pytest.fixture
def session():
    print("Creating session")
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

@pytest.fixture
def test_user(client):
    res = client.post("/users/add_user",json={"id":"5","email":"user5@example.com","password":"password5"})
    new_user = res.json()
    new_user["password"] = "password5"
    assert new_user['email'] == "user5@example.com"
    assert res.status_code == 201
    return new_user

@pytest.fixture
def test_user2(client):
    res = client.post("/users/add_user",json={"id":"6","email":"user6@example.com","password":"password6"})
    new_user = res.json()  
    new_user["password"] = "password6"
    assert new_user['email'] == "user6@example.com"
    assert res.status_code == 201
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id":test_user["id"]})

@pytest.fixture
def authorized_client(client,token):
    client.headers= {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client
    


@pytest.fixture
def tests_posts(test_user,test_user2, session):
    posts_data = [{"title":"Post 1","content":"Content of post 1","owner_id":test_user["id"]},
                  {"title":"Post 2","content":"Content of post 2","owner_id":test_user2["id"]},
                  {"title":"Post 3","content":"Content of post 3","owner_id":test_user["id"]},
                  {"title":"Post 4","content":"Content of post 4","owner_id":test_user2["id"]},]
    def validate(post):
        return models.Post(**post)
    post_list = list(map(validate,posts_data))
    session.add_all(post_list)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
