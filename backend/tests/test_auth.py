import pytest
from passlib.context import CryptContext
from src.infrastructure.security.password import hash_password, verify_password
from src.infrastructure.security.jwt import create_access_token, decode_access_token


def test_password_hash():
    password = "senha_secreta_123"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("senha_errada", hashed) is False


def test_jwt_token_create_and_decode():
    token = create_access_token({"sub": "test-user-id", "papel": "admin"})
    payload = decode_access_token(token)
    assert payload is not None
    assert payload["sub"] == "test-user-id"
    assert payload["papel"] == "admin"


def test_jwt_roundtrip():
    token = create_access_token({"sub": "uuid-example"})
    payload = decode_access_token(token)
    assert payload["sub"] == "uuid-example"


def test_invalid_token():
    payload = decode_access_token("invalid.token.value")
    assert payload is None