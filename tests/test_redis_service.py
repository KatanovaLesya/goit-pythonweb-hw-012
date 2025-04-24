
from services.redis_service import cache_user, get_cached_user
import fakeredis
import json

def test_cache_and_get_user(monkeypatch):
    r = fakeredis.FakeStrictRedis()
    monkeypatch.setattr("services.redis_service.redis_client", r)

    email = "user@example.com"
    user_data = {"email": email, "username": "user"}
    cache_user(email, user_data)

    result = get_cached_user(email)
    assert result == user_data
