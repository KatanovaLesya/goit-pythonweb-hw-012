"""
Маршрути API для роботи з контактами користувача.

Містить ендпоінти для створення, читання, оновлення, видалення контактів,
пошуку по імені/прізвищу/email, та отримання днів народження.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from schemas import Contact, ContactCreate, ContactUpdate
from repository import contacts as repository_contacts
from models import User
from auth_service import get_current_user

router = APIRouter(prefix="/contacts", tags=["contacts"])

def get_db():
    """
    Отримання сесії бази даних для кожного запиту.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=Contact, status_code=status.HTTP_201_CREATED)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Створення нового контакту для поточного користувача.

    Args:
        contact (ContactCreate): Дані нового контакту.
        db (Session): Сесія бази даних.
        current_user (User): Авторизований користувач.

    Returns:
        Contact: Створений контакт.
    """
    return repository_contacts.create_contact(db, contact, current_user.id)


@router.get("/", response_model=List[Contact])
def read_contacts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Отримання всіх контактів користувача з пагінацією.

    Args:
        skip (int): Скільки записів пропустити.
        limit (int): Максимальна кількість записів.
        db (Session): Сесія бази даних.
        current_user (User): Авторизований користувач.

    Returns:
        List[Contact]: Список контактів.
    """
    return repository_contacts.get_contacts(db, skip, limit, current_user.id)


@router.get("/{contact_id}", response_model=Contact)
def read_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Отримання конкретного контакту за ID.

    Args:
        contact_id (int): Ідентифікатор контакту.
        db (Session): Сесія бази даних.
        current_user (User): Авторизований користувач.

    Returns:
        Contact: Знайдений контакт або HTTP 404.
    """
    contact = repository_contacts.get_contact(db, contact_id, current_user.id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=Contact)
def update_contact(
    contact_id: int,
    contact: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Оновлення існуючого контакту.

    Args:
        contact_id (int): Ідентифікатор контакту.
        contact (ContactUpdate): Нові дані контакту.
        db (Session): Сесія бази даних.
        current_user (User): Авторизований користувач.

    Returns:
        Contact: Оновлений контакт або HTTP 404.
    """
    updated_contact = repository_contacts.update_contact(db, contact_id, contact, current_user.id)
    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact


@router.delete("/{contact_id}", response_model=Contact)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Видалення контакту за ID.

    Args:
        contact_id (int): Ідентифікатор контакту.
        db (Session): Сесія бази даних.
        current_user (User): Авторизований користувач.

    Returns:
        Contact: Видалений контакт або HTTP 404.
    """
    deleted = repository_contacts.delete_contact(db, contact_id, current_user.id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return deleted

@router.get("/search/", response_model=List[Contact])
def search_contacts(
    query: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Пошук контактів за іменем, прізвищем або email.

    Args:
        query (str): Пошуковий запит.
        db (Session): Сесія бази даних.
        current_user (User): Авторизований користувач.

    Returns:
        List[Contact]: Список знайдених контактів.
    """
    return repository_contacts.search_contacts(db, query, current_user.id)

@router.get("/birthdays/", response_model=List[Contact])
def upcoming_birthdays(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Отримання контактів, у яких день народження протягом 7 днів.

    Args:
        db (Session): Сесія бази даних.
        current_user (User): Авторизований користувач.

    Returns:
        List[Contact]: Список контактів з наближеними днями народження.
    """
    return repository_contacts.get_upcoming_birthdays(db, current_user.id)
