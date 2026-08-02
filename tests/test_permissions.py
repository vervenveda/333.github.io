from app.core.permissions import Role, role_is_allowed


def test_administrator_inherits_access():
    assert role_is_allowed(
        Role.ADMINISTRATOR.value,
        {Role.MAIL_ADMIN},
    )


def test_member_does_not_receive_admin_access():
    assert not role_is_allowed(
        Role.MEMBER.value,
        {Role.MAIL_ADMIN, Role.ADMINISTRATOR},
    )
