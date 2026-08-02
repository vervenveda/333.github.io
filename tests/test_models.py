from app.models import Base


def test_identity_tables_are_registered():
    assert {
        "users",
        "profiles",
        "network_numbers",
        "email_applications",
        "refresh_sessions",
        "audit_logs",
    }.issubset(Base.metadata.tables)
