import uuid
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app
from models import User
from auth_service import get_current_user

# Підміна авторизованого користувача
def override_get_current_user():
    return User(
        id=1,
        username="testuser",
        email="test@example.com",
        password="hashed",
        is_active=True,
        is_verified=True,
        avatar_url=None
    )

app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


def test_read_contacts_empty():
    response = client.get("/contacts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_contact():
    data = {
        "first_name": "Test",
        "last_name": "User",
        "email": f"test_{uuid.uuid4().hex}@example.com", # test_create_001@example.com",
        "phone": "1234567890",
        "birthday": "2000-01-01"
    }
    response = client.post("/contacts/", json=data)
    assert response.status_code == 201
    contact = response.json()
    assert contact["first_name"] == "Test"
    assert contact["email"] == "test_create_001@example.com"


def test_get_created_contact():
    response = client.get("/contacts/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(contact["first_name"] == "Test" for contact in data)


def test_update_contact():
    data = {
        "first_name": "Old",
        "last_name": "Name",
        "email": f"test_{uuid.uuid4().hex}@example.com", # update_test@example.com",
        "phone": "0000000000",
        "birthday": "1990-01-01"
    }
    create_resp = client.post("/contacts/", json=data)
    contact_id = create_resp.json()["id"]

    update_data = {
        "first_name": "New"
    }
    response = client.put(f"/contacts/{contact_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["first_name"] == "New"


def test_delete_contact():
    data = {
        "first_name": "Delete",
        "last_name": "Me",
        "email": f"test_{uuid.uuid4().hex}@example.com", # delete_me@example.com",
        "phone": "1111111111",
        "birthday": "1999-01-01"
    }
    create_resp = client.post("/contacts/", json=data)
    contact_id = create_resp.json()["id"]

    response = client.delete(f"/contacts/{contact_id}")
    assert response.status_code == 200

    get_resp = client.get(f"/contacts/{contact_id}")
    assert get_resp.status_code == 404


def test_search_contacts():
    client.post("/contacts/", json={
        "first_name": "Olena",
        "last_name": "Test",
        "email": f"test_{uuid.uuid4().hex}@example.com", # olena_search@example.com",
        "phone": "1231231234",
        "birthday": "1995-05-05"
    })
    response = client.get("/contacts/search/?query=olena")
    assert response.status_code == 200
    assert any("olena" in contact["first_name"].lower() for contact in response.json())


def test_get_birthdays():
    today = "2000-04-22"  # Сьогодні
    client.post("/contacts/", json={
        "first_name": "Birthday",
        "last_name": "Soon",
        "email": f"test_{uuid.uuid4().hex}@example.com", # birthday_today@example.com",
        "phone": "8888888888",
        "birthday": today
    })
    response = client.get("/contacts/birthdays/")
    assert response.status_code == 200
    assert any(c["first_name"] == "Birthday" for c in response.json())

