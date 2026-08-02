import pytest

from app.core.exceptions import ValidationServiceError
from app.schemas.profile import ProfileCreate
from app.services.authentication_service import register_user
from app.services.identity_service import create_profile
from app.services.number_service import (
    PROTECTED_SERVICE_ROUTES,
    register_existing_number,
    reserve_provisional_number,
)


@pytest.mark.asyncio
async def test_hollo_profile_and_provisional_number(session):
    user = await register_user(
        session,
        email="hollo@example.com",
        password="Hollo-Member-333!",
    )
    profile = await create_profile(
        session,
        user=user,
        payload=ProfileCreate(
            display_name="Hollo Member",
            handle="hollo.member",
        ),
    )
    number = await reserve_provisional_number(session, user=user)

    assert profile.handle == "hollo.member"
    assert number.number.startswith("333")
    assert number.number not in PROTECTED_SERVICE_ROUTES
    assert number.status == "provisional"


@pytest.mark.asyncio
async def test_service_route_cannot_be_existing_number(session):
    user = await register_user(
        session,
        email="route@example.com",
        password="Protected-Route-333!",
    )
    with pytest.raises(ValidationServiceError):
        await register_existing_number(
            session,
            user=user,
            number="333-222-7777",
        )
