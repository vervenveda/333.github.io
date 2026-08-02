import pytest

from app.core.exceptions import AuthenticationError, ConflictError
from app.services.authentication_service import (
    authenticate_user,
    register_user,
)


@pytest.mark.asyncio
async def test_registration_and_authentication(session):
    user = await register_user(
        session,
        email="Member@Example.com",
        password="Member-Safety-333!",
    )
    assert user.email == "member@example.com"

    authenticated = await authenticate_user(
        session,
        email="member@example.com",
        password="Member-Safety-333!",
    )
    assert authenticated.id == user.id


@pytest.mark.asyncio
async def test_duplicate_email_rejected(session):
    await register_user(
        session,
        email="member@example.com",
        password="Member-Safety-333!",
    )
    with pytest.raises(ConflictError):
        await register_user(
            session,
            email="MEMBER@example.com",
            password="Another-Safe-333!",
        )


@pytest.mark.asyncio
async def test_incorrect_password_rejected(session):
    await register_user(
        session,
        email="member@example.com",
        password="Member-Safety-333!",
    )
    with pytest.raises(AuthenticationError):
        await authenticate_user(
            session,
            email="member@example.com",
            password="wrong-password",
        )
