#!/usr/bin/env python3
"""Create or promote the first 333 Network administrator."""

from __future__ import annotations

import argparse
import asyncio
import getpass

from sqlalchemy import select

from app.core.database import async_session_factory, dispose_engine
from app.core.permissions import Role
from app.core.security import hash_password
from app.models.enums import UserStatus
from app.models.user import User
from app.services.authentication_service import normalize_email


async def create_admin(email: str, password: str) -> None:
    normalized = normalize_email(email)
    async with async_session_factory() as session:
        user = await session.scalar(select(User).where(User.email == normalized))
        if user:
            user.role = Role.ADMINISTRATOR.value
            user.status = UserStatus.ACTIVE.value
            user.is_active = True
            if password:
                user.password_hash = hash_password(password)
            action = "promoted"
        else:
            user = User(
                email=normalized,
                password_hash=hash_password(password),
                role=Role.ADMINISTRATOR.value,
                status=UserStatus.ACTIVE.value,
                is_active=True,
                email_verified=True,
            )
            session.add(user)
            action = "created"

        await session.commit()
        print(f"Administrator {action}: {normalized}")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", required=True)
    parser.add_argument(
        "--password",
        help="Avoid shell history: omit this option to receive a hidden prompt.",
    )
    return parser.parse_args()


async def main() -> None:
    arguments = parse_arguments()
    password = arguments.password or getpass.getpass("Administrator password: ")
    confirmation = (
        arguments.password
        or getpass.getpass("Confirm administrator password: ")
    )
    if password != confirmation:
        raise SystemExit("Passwords do not match.")

    try:
        await create_admin(arguments.email, password)
    finally:
        await dispose_engine()


if __name__ == "__main__":
    asyncio.run(main())
