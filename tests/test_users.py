import pytest
from app import schema
from app.config import settings
from jose import jwt
def test_read_root(client):
    res = client.get("/")
    print(res.json())
    assert res.json().get("Message") == "Hello World"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/add_user",json={"email":"example@gmail.com","password":"password123"})
    assert res.status_code == 201


def test_login(client,test_create_user):
    res = client.post("/auth/login",data= {"username":test_create_user['email'],"password":test_create_user['password']})
    login_res = schema.Token(**res.json())
    payload = jwt.decode(login_res.access_token,settings.secret_key,algorithms=[settings.algorithm])
    id = payload["user_id"]
    assert id == test_create_user["id"] , "User id does not match"
    assert login_res.token_type == "bearer"
    assert res.status_code == 200



@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post(
        "/auth/login", data={"username": email, "password": password})
    assert res.status_code == status_code