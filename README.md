# 📱 Contacts API — Final Project (GoIT Python Web)

This is the final project for the GoIT FullStack Web Development with Python course. It demonstrates implementation of a production-ready REST API with authentication, authorization, caching, testing, and more.

---

## 🚀 Features

- **JWT Authentication** with `access_token`
- **Password Reset** via email with token
- **Role-based Access Control** (user/admin)
- **Admin-only avatar upload** (via Cloudinary)
- **Contacts management**
- **Rate limiting** with `slowapi`
- **Caching** current user with Redis
- **Email delivery** with SMTP
- **Test coverage ≥ 75%** with `pytest` and `pytest-cov`
- **Environment variables** in `.env`

---

## 📂 Project Structure

```
.
├── auth_service.py
├── database.py
├── main.py
├── models.py
├── rate_limiter.py
├── repository/
│   └── contacts.py
├── routers/
│   ├── auth_router.py
│   └── contacts.py
├── schemas.py
├── services/
│   ├── cloudinary_service.py
│   ├── email_service.py
│   └── redis_service.py
├── tests/
│   ├── test_auth_router.py
│   ├── test_auth_service.py
│   ├── test_repository_contacts.py
│   ├── test_routes_contacts.py
│   └── ...
```

---

## ✅ How to Run

1. Setup PostgreSQL & Redis locally.
2. Create `.env` file:
```env
MAIL_USERNAME=your@mail.com
MAIL_PASSWORD=yourpassword
MAIL_FROM=your@mail.com
MAIL_PORT=587
MAIL_SERVER=smtp.yourserver.com
SECRET_KEY=your_secret_key
ALGORITHM=HS256
```
3. Run:
```bash
uvicorn main:app --reload
```

---

## 🧪 Run Tests

```bash
pytest --cov=./ --cov-report=term-missing
```

---

## 💻 Technologies Used

- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Cloudinary
- Pytest
- Sphinx
- Passlib (bcrypt)
- JWT (jose)

---

## 🏁 Author

Lesya Katanova — Final project for GoIT Python Web course