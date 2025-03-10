from fastapi.testclient import TestClient
from app.main import app
from app.schema import UserOut
client = TestClient(app)


def test_read_root():
    res = client.get("/")
    print(res.json())
    assert res.json().get("Message") == "Hello World"
    assert res.status_code == 200


def test_create_user():
    res = client.post("/users/add_user",json={"id":"3","email":"user3@example.com","password":"password3"})
    new_user = UserOut(**res.json())
    assert new_user.email == "user3@example.com"
    assert res.status_code == 201
