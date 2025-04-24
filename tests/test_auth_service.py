
from auth_service import create_access_token

def test_create_access_token():
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    assert isinstance(token, str)
    assert "." in token  # JWT must have 3 parts separated by dots
