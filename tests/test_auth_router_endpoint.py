
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_auth_route_exists():
    response = client.get("/")
    assert response.status_code == 200
