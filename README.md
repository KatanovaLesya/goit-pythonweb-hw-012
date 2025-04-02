# Опис проєкту

## Contacts API

Цей проєкт реалізує REST API для збереження та управління контактами з використанням FastAPI, PostgreSQL та SQLAlchemy.

## 🚀 Технології

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic (міграції)
- Pydantic (валідація)
- Uvicorn (сервер)
- Email-validator

## 🛠 Функціонал API

- Створення нового контакту
- Отримання списку контактів
- Отримання одного контакту за ID
- Оновлення існуючого контакту
- Видалення контакту
- Пошук за ім ям, прізвищем або email (query параметри)
- Список контактів з днями народження у найближчі 7 днів

## ⚙️ Як запустити проєкт

1. Клонувати репозиторій
2. Створити та активувати віртуальне середовище
python3 -m venv venv
source venv/bin/activate
3. Встановити залежності
pip install -r requirements.txt
4. Налаштувати базу даних PostgreSQL (через pgAdmin або консоль). Назва бази: contacts_db.
5. Запустити сервер: uvicorn main:app --reload
6. Документація API доступна тут: Swagger UI: <http://127.0.0.1:8000/docs> Redoc: <http://127.0.0.1:8000/redoc>
7. Структура проєкту
goit-pythonweb-hw-08/
│
├── main.py                  Точка входу
├── models.py                SQLAlchemy моделі
├── schemas.py               Pydantic схеми
├── database.py              Підключення до БД
├── create_tables.py         Скрипт створення таблиць
├── routers/
│   └── contacts.py          CRUD роутери
├── requirements.txt         Залежності
└── README.md                Цей файл
8. Автор - Катановa Леся
