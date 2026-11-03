from fastapi.testclient import TestClient
from main import app
 
client = TestClient(app)
 
def test_health():
    assert client.get("/health").json() == {"status": "ok"}
 
def test_add_and_list():
    client.post("/items?name=pain")
    assert "pain" in client.get("/items").json()