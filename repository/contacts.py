"""
Модуль для обробки CRUD операцій із контактами користувача.

Містить функції для створення, читання, оновлення та видалення контактів.
"""

from sqlalchemy.orm import Session
from models import Contact
from schemas import ContactCreate, ContactUpdate
from datetime import date, timedelta


def create_contact(db: Session, contact: ContactCreate, user_id: int):
    """
    Створює новий контакт для заданого користувача.

    Args:
        db (Session): Сесія бази даних SQLAlchemy.
        contact (ContactCreate): Дані нового контакту.
        user_id (int): ID користувача.

    Returns:
        Contact: Створений контакт.
    """
    db_contact = Contact(**contact.dict(), user_id=user_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contacts(db: Session, skip: int, limit: int, user_id: int):
    """
    Отримує список контактів користувача з пагінацією.

    Args:
        db (Session): Сесія бази даних.
        skip (int): Кількість записів для пропуску.
        limit (int): Максимальна кількість записів для повернення.
        user_id (int): ID користувача.

    Returns:
        List[Contact]: Список контактів.
    """
    return db.query(Contact).filter(Contact.user_id == user_id).offset(skip).limit(limit).all()


def get_contact(db: Session, contact_id: int, user_id: int):
    """
    Отримує контакт за його ID, лише якщо він належить користувачу.

    Args:
        db (Session): Сесія бази даних.
        contact_id (int): ID контакту.
        user_id (int): ID користувача.

    Returns:
        Contact | None: Знайдений контакт або None.
    """
    return db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user_id).first()


def update_contact(db: Session, contact_id: int, contact: ContactUpdate, user_id: int):
    """
    Оновлює контакт користувача.

    Args:
        db (Session): Сесія бази даних.
        contact_id (int): ID контакту для оновлення.
        contact (ContactUpdate): Нові дані контакту.
        user_id (int): ID користувача.

    Returns:
        Contact | None: Оновлений контакт або None, якщо не знайдено.
    """
    db_contact = get_contact(db, contact_id, user_id)
    if not db_contact:
        return None
    for field, value in contact.dict(exclude_unset=True).items():
        setattr(db_contact, field, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int, user_id: int):
    """
    Видаляє контакт користувача.

    Args:
        db (Session): Сесія бази даних.
        contact_id (int): ID контакту.
        user_id (int): ID користувача.

    Returns:
        Contact | None: Видалений контакт або None, якщо не знайдено.
    """
    db_contact = get_contact(db, contact_id, user_id)
    if not db_contact:
        return None
    db.delete(db_contact)
    db.commit()
    return db_contact


def search_contacts(db: Session, query: str, user_id: int):
    """
    Пошук контактів користувача за ім'ям, прізвищем або email.

    Args:
        db (Session): Сесія бази даних.
        query (str): Пошуковий запит.
        user_id (int): ID користувача.

    Returns:
        List[Contact]: Список знайдених контактів.
    """
    return db.query(Contact).filter(
        Contact.user_id == user_id,
        (
            Contact.first_name.ilike(f"%{query}%") |
            Contact.last_name.ilike(f"%{query}%") |
            Contact.email.ilike(f"%{query}%")
        )
    ).all()


def get_upcoming_birthdays(db: Session, user_id: int):
    """
    Отримує контакти з днями народження протягом наступних 7 днів.

    Args:
        db (Session): Сесія бази даних.
        user_id (int): ID користувача.

    Returns:
        List[Contact]: Контакти з наближеними днями народження.
    """
    today = date.today()
    next_week = today + timedelta(days=7)

    contacts = db.query(Contact).filter(Contact.user_id == user_id).all()
    result = []
    for contact in contacts:
        if contact.birthday:
            birthday_this_year = contact.birthday.replace(year=today.year)
            if today <= birthday_this_year <= next_week:
                result.append(contact)
    return result
