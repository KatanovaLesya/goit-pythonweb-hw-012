# Опис проєкту

## Contacts API (FastAPI + PostgreSQL + Docker)

REST API для зберігання, пошуку та управління контактами. Реалізовано аутентифікацію, авторизацію, підтвердження email, аватар користувача та Docker-контейнеризацію.

## Стек технологій

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT (JSON Web Tokens)
- Cloudinary (аватарки)
- Mailtrap (лист підтвердження)
- Docker, Docker Compose

## Швидкий запуск (Docker)

docker-compose up --build

## Основні фічі

- Реєстрація користувача з перевіркою пошти
- Авторизація через JWT токени
- Верифікація email
- CRUD операції з контактами
- Пошук контактів (ім'я, прізвище, email)
- Найближчі дні народження
- Обмеження запитів `/me` (rate limit 5/minute)
- Оновлення аватара (Cloudinary)
- CORS enabled
- Dockerized

## Структура проекту

├── main.py
├── models.py
├── routers/
├── services/
├── repository/
├── database.py
├── auth_service.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

## Swagger UI

- Доступно після запуску: [http://localhost:8002/docs](http://localhost:8002/docs)

## Автор

Lesya Katanova
