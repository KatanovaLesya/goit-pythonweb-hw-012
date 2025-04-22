"""
Сервіс авторизації та автентифікації користувачів.

Містить функції для хешування паролів,
створення та перевірки JWT токенів.
"""

from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
import jwt

# Зазвичай ключ і алгоритм зберігають у .env
SECRET_KEY = "super_mega_secret_key_123"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Перевіряє відповідність звичайного пароля та його хешу.

    Args:
        plain_password (str): Введений користувачем пароль.
        hashed_password (str): Хеш пароля з бази.

    Returns:
        bool: True якщо збігається, False інакше.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Хешує пароль для збереження у базі.

    Args:
        password (str): Пароль у відкритому вигляді.

    Returns:
        str: Хешований пароль.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Створює JWT access token з переданими даними.

    Args:
        data (dict): Дані, які будуть закодовані в токен.
        expires_delta (timedelta | None): Тривалість дії токена.

    Returns:
        str: Підписаний access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
