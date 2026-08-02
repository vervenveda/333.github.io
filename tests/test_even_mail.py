import pytest

from app.schemas.even_mail import EmailApplicationCreate
from app.services.authentication_service import register_user
from app.services.email_application_service import submit_application


@pytest.mark.asyncio
async def test_even_mail_application(session):
    user = await register_user(
        session,
        email="mail@example.com",
        password="Email-Applicant-333!",
    )
    application = await submit_application(
        session,
        user=user,
        payload=EmailApplicationCreate(
            requested_local_part="jenny.pearl",
            requested_domain="evenmail.example.invalid",
            purpose="Personal correspondence",
        ),
    )

    assert application.reference.startswith("EVEN-")
    assert application.requested_address == (
        "jenny.pearl@evenmail.example.invalid"
    )
    assert application.status == "submitted"
