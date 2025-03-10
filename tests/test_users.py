from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_read_root():
    res = client.get("/")
    print(res.json())