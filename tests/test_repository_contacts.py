import uuid
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta

from models import Base, Contact
from schemas import ContactCreate, ContactUpdate
from repository.contacts import (
    create_contact,
    get_contacts,
    get_contact,
    update_contact,
    delete_contact,
    search_contacts,
    get_upcoming_birthdays,
)


# SQLite база в памʼяті для тестів
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_create_contact(db):
    contact_data = ContactCreate(
        first_name="Anna",
        last_name="Ivanova",
        email="anna@example.com",
        phone="1234567890",
        birthday=date(2000, 1, 1)
    )
    contact = create_contact(db, contact_data, user_id=1)
    assert contact.id is not None
    assert contact.first_name == "Anna"
    assert contact.user_id == 1


def test_get_contacts(db):
    for i in range(3):
        data = ContactCreate(
            first_name=f"User{i}",
            last_name="Test",
            email=f"user{i}@test.com",
            phone="0000000000",
            birthday=date(2000, 1, 1)
        )
        create_contact(db, data, user_id=1)
    results = get_contacts(db, skip=0, limit=10, user_id=1)
    assert len(results) == 3


def test_get_contact(db):
    contact = create_contact(
        db,
        ContactCreate(
            first_name="Oleg",
            last_name="Doe",
            email="oleg@example.com",
            phone="2222222222",
            birthday=date(1990, 5, 5)
        ),
        user_id=1
    )
    result = get_contact(db, contact.id, user_id=1)
    assert result.email == "oleg@example.com"


def test_update_contact(db):
    contact = create_contact(
        db,
        ContactCreate(
            first_name="Old",
            last_name="Name",
            email="old@example.com",
            phone="1111111111",
            birthday=date(1985, 6, 15)
        ),
        user_id=1
    )
    update = ContactUpdate(first_name="New")
    updated = update_contact(db, contact.id, update, user_id=1)
    assert updated.first_name == "New"


def test_delete_contact(db):
    contact = create_contact(
        db,
        ContactCreate(
            first_name="Del",
            last_name="Me",
            email="del@example.com",
            phone="1111111111",
            birthday=date(1980, 7, 20)
        ),
        user_id=1
    )
    deleted = delete_contact(db, contact.id, user_id=1)
    assert deleted.id == contact.id
    assert get_contact(db, contact.id, user_id=1) is None


def test_search_contacts(db):
    create_contact(
        db,
        ContactCreate(
            first_name="Julia",
            last_name="Roberts",
            email="julia@movie.com",
            phone="5555555555",
            birthday=date(1975, 10, 28)
        ),
        user_id=1
    )
    results = search_contacts(db, query="julia", user_id=1)
    assert len(results) == 1
    assert results[0].first_name == "Julia"


def test_get_upcoming_birthdays(db):
    today = date.today()
    birthday = today + timedelta(days=3)

    contact = Contact(
        first_name="Birthday",
        last_name="Soon",
        email="soon@bday.com",
        phone="9999999999",
        birthday=birthday,
        user_id=1
    )
    db.add(contact)
    db.commit()

    results = get_upcoming_birthdays(db, user_id=1)
    assert len(results) == 1
    assert results[0].first_name == "Birthday"

