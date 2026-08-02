from uuid import uuid4

import pytest

from app.core.exceptions import ValidationServiceError
from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hash_round_trip():
    password = "Strongly-Composed-333!"
    password_hash = hash_password(password)
    assert password_hash != password
    assert verify_password(password, password_hash)
    assert not verify_password("incorrect-password", password_hash)


def test_weak_password_rejected():
    with pytest.raises(ValidationServiceError):
        hash_password("password123")


def test_access_token_round_trip():
    user_id = uuid4()
    token, _ = create_access_token(user_id=user_id, role="member")
    payload = decode_access_token(token)
    assert payload["sub"] == str(user_id)
    assert payload["role"] == "member"
    assert payload["type"] == "access"
