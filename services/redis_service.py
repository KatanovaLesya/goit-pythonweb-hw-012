import redis
import os
import json

# Завантажуємо .env змінні
from dotenv import load_dotenv
load_dotenv()

# Параметри Redis з .env або дефолтні
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# Підключення до Redis
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True  # Щоб не повертало байти
)

def cache_user(token: str, user_data: dict, expire: int = 1800):
    """Зберігає дані користувача в Redis з таймером життя."""
    redis_client.setex(token, expire, json.dumps(user_data))

def get_cached_user(token: str):
    """Повертає користувача з Redis або None."""
    cached = redis_client.get(token)
    return json.loads(cached) if cached else None