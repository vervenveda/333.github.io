"""create identity foundation

Revision ID: 0001_identity
Revises:
Create Date: 2026-08-01
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "0001_identity"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), server_default="active", nullable=False),
        sa.Column("role", sa.String(length=32), server_default="member", nullable=False),
        sa.Column("email_verified", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("failed_login_attempts", sa.Integer(), server_default="0", nullable=False),
        sa.Column("locked_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_users"),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=False)
    op.create_index("ix_users_role", "users", ["role"], unique=False)
    op.create_index("ix_users_status", "users", ["status"], unique=False)

    op.create_table(
        "profiles",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("display_name", sa.String(length=120), nullable=False),
        sa.Column("handle", sa.String(length=40), nullable=False),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("avatar_url", sa.String(length=2048), nullable=True),
        sa.Column("visibility", sa.String(length=24), server_default="members", nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_profiles_user_id_users", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_profiles"),
        sa.UniqueConstraint("handle", name="uq_profiles_handle"),
        sa.UniqueConstraint("user_id", name="uq_profiles_user_id"),
    )
    op.create_index("ix_profiles_handle", "profiles", ["handle"], unique=False)
    op.create_index("ix_profiles_user_id", "profiles", ["user_id"], unique=False)

    op.create_table(
        "network_numbers",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("number", sa.String(length=20), nullable=False),
        sa.Column("kind", sa.String(length=24), server_default="network", nullable=False),
        sa.Column("status", sa.String(length=32), server_default="provisional", nullable=False),
        sa.Column("is_primary", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("verification_method", sa.String(length=40), nullable=True),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_network_numbers_user_id_users", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_network_numbers"),
        sa.UniqueConstraint("number", name="uq_network_numbers_number"),
    )
    op.create_index("ix_network_numbers_number", "network_numbers", ["number"], unique=False)
    op.create_index("ix_network_numbers_status", "network_numbers", ["status"], unique=False)
    op.create_index("ix_network_numbers_user_id", "network_numbers", ["user_id"], unique=False)

    op.create_table(
        "refresh_sessions",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("device_name", sa.String(length=120), nullable=True),
        sa.Column("user_agent_hash", sa.String(length=64), nullable=True),
        sa.Column("ip_address_hash", sa.String(length=64), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_refresh_sessions_user_id_users", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_refresh_sessions"),
        sa.UniqueConstraint("token_hash", name="uq_refresh_sessions_token_hash"),
    )
    op.create_index("ix_refresh_sessions_expires_at", "refresh_sessions", ["expires_at"], unique=False)
    op.create_index("ix_refresh_sessions_revoked_at", "refresh_sessions", ["revoked_at"], unique=False)
    op.create_index("ix_refresh_sessions_token_hash", "refresh_sessions", ["token_hash"], unique=False)
    op.create_index("ix_refresh_sessions_user_id", "refresh_sessions", ["user_id"], unique=False)

    op.create_table(
        "email_applications",
        sa.Column("reference", sa.String(length=32), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("requested_local_part", sa.String(length=64), nullable=False),
        sa.Column("requested_domain", sa.String(length=255), nullable=False),
        sa.Column("requested_address", sa.String(length=320), nullable=False),
        sa.Column("alternate_contact_email", sa.String(length=320), nullable=True),
        sa.Column("purpose", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=32), server_default="submitted", nullable=False),
        sa.Column("applicant_notes", sa.Text(), nullable=True),
        sa.Column("administrator_notes", sa.Text(), nullable=True),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("reviewed_by_user_id", sa.Uuid(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["reviewed_by_user_id"], ["users.id"], name="fk_email_applications_reviewed_by_user_id_users", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_email_applications_user_id_users", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_email_applications"),
        sa.UniqueConstraint("reference", name="uq_email_applications_reference"),
    )
    op.create_index("ix_email_applications_reference", "email_applications", ["reference"], unique=False)
    op.create_index("ix_email_applications_requested_address", "email_applications", ["requested_address"], unique=False)
    op.create_index("ix_email_applications_reviewed_by_user_id", "email_applications", ["reviewed_by_user_id"], unique=False)
    op.create_index("ix_email_applications_status", "email_applications", ["status"], unique=False)
    op.create_index("ix_email_applications_user_id", "email_applications", ["user_id"], unique=False)

    op.create_table(
        "audit_logs",
        sa.Column("actor_user_id", sa.Uuid(), nullable=True),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("resource_type", sa.String(length=100), nullable=False),
        sa.Column("resource_id", sa.String(length=128), nullable=True),
        sa.Column("outcome", sa.String(length=32), server_default="success", nullable=False),
        sa.Column("request_id", sa.String(length=128), nullable=True),
        sa.Column("ip_address_hash", sa.String(length=64), nullable=True),
        sa.Column("details", sa.JSON(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["actor_user_id"], ["users.id"], name="fk_audit_logs_actor_user_id_users", ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id", name="pk_audit_logs"),
    )
    op.create_index("ix_audit_logs_actor_user_id", "audit_logs", ["actor_user_id"], unique=False)
    op.create_index("ix_audit_logs_event_type", "audit_logs", ["event_type"], unique=False)
    op.create_index("ix_audit_logs_outcome", "audit_logs", ["outcome"], unique=False)
    op.create_index("ix_audit_logs_request_id", "audit_logs", ["request_id"], unique=False)
    op.create_index("ix_audit_logs_resource_id", "audit_logs", ["resource_id"], unique=False)
    op.create_index("ix_audit_logs_resource_type", "audit_logs", ["resource_type"], unique=False)


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("email_applications")
    op.drop_table("refresh_sessions")
    op.drop_table("network_numbers")
    op.drop_table("profiles")
    op.drop_table("users")
