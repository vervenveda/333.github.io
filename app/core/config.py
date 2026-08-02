"""Environment-backed settings for the 333 Network backend."""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


PLACEHOLDER_MARKERS = (
    "replace-",
    "change-me",
    "changeme",
    "example.invalid",
    "placeholder",
    "driver://",
)


def _contains_placeholder(value: str) -> bool:
    lowered = value.strip().lower()
    return not lowered or any(marker in lowered for marker in PLACEHOLDER_MARKERS)


def _split_csv(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    if isinstance(value, (list, tuple, set)):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()]


class Settings(BaseSettings):
    """Validated application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "333 Network API"
    app_env: str = "development"
    app_debug: bool = False
    app_module: str = "app.main:app"
    api_prefix: str = "/api"
    host: str = "0.0.0.0"
    port: int = Field(default=8000, ge=1, le=65535)
    log_level: str = "INFO"
    log_format: str = "json"

    jwt_issuer: str = "333-network"
    jwt_audience: str = "333-network-api"
    minimum_password_length: int = Field(default=12, ge=10, le=128)
    login_max_attempts: int = Field(default=5, ge=3, le=20)
    login_lock_minutes: int = Field(default=15, ge=1, le=1440)
    registration_rate_limit: int = Field(default=5, ge=1, le=100)
    login_rate_limit: int = Field(default=20, ge=1, le=500)
    refresh_rate_limit: int = Field(default=60, ge=1, le=1000)
    email_application_rate_limit: int = Field(default=5, ge=1, le=100)
    rate_limit_fail_closed: bool = False

    network_number_prefix: str = "333"
    network_number_total_digits: int = Field(default=10, ge=7, le=15)
    even_mail_allowed_domains: list[str] = Field(
        default_factory=lambda: ["evenmail.example.invalid"]
    )

    api_public_url: str = "http://localhost:8000"
    frontend_public_url: str = "http://localhost:5500"
    frontend_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:5500",
            "http://127.0.0.1:5500",
            "https://vervenveda.github.io",
        ]
    )
    trusted_hosts: list[str] = Field(
        default_factory=lambda: ["localhost", "127.0.0.1", "testserver"]
    )

    database_url: str = (
        "postgresql+asyncpg://network333:replace-with-a-long-random-local-password"
        "@localhost:5432/network333"
    )
    database_echo: bool = False
    database_pool_size: int = Field(default=5, ge=1, le=50)
    database_max_overflow: int = Field(default=10, ge=0, le=100)
    database_pool_timeout_seconds: int = Field(default=30, ge=1, le=300)
    database_health_timeout_seconds: float = Field(default=3.0, gt=0, le=30)
    database_required_on_startup: bool = False

    redis_url: str = "redis://localhost:6379/0"

    jwt_secret: SecretStr = SecretStr("replace-with-at-least-64-random-characters")
    session_secret: SecretStr = SecretStr(
        "replace-with-at-least-64-random-characters"
    )
    token_signing_algorithm: str = "HS256"
    access_token_minutes: int = Field(default=15, ge=5, le=1440)
    refresh_token_days: int = Field(default=30, ge=1, le=365)

    cookie_name: str = "network333_session"
    cookie_secure: bool = False
    cookie_samesite: str = "lax"
    cookie_domain: str | None = None

    enable_api_docs: bool | None = None
    gzip_minimum_size: int = Field(default=1024, ge=0)

    @field_validator("app_env", mode="before")
    @classmethod
    def normalize_environment(cls, value: Any) -> str:
        normalized = str(value or "development").strip().lower()
        allowed = {"development", "test", "staging", "production"}
        if normalized not in allowed:
            raise ValueError(f"APP_ENV must be one of: {', '.join(sorted(allowed))}")
        return normalized

    @field_validator("api_prefix", mode="before")
    @classmethod
    def normalize_api_prefix(cls, value: Any) -> str:
        prefix = str(value or "/api").strip()
        if not prefix.startswith("/"):
            prefix = f"/{prefix}"
        return prefix.rstrip("/") or "/api"

    @field_validator("frontend_origins", "trusted_hosts", "even_mail_allowed_domains", mode="before")
    @classmethod
    def parse_csv_lists(cls, value: Any) -> list[str]:
        return _split_csv(value)

    @field_validator("frontend_origins")
    @classmethod
    def normalize_origins(cls, values: list[str]) -> list[str]:
        cleaned: list[str] = []
        for value in values:
            origin = value.strip().rstrip("/")
            if origin and origin not in cleaned:
                cleaned.append(origin)
        if not cleaned:
            raise ValueError("At least one FRONTEND_ORIGINS value is required.")
        return cleaned

    @field_validator("trusted_hosts")
    @classmethod
    def normalize_hosts(cls, values: list[str]) -> list[str]:
        cleaned: list[str] = []
        for value in values:
            host = value.strip().lower()
            if host and host not in cleaned:
                cleaned.append(host)
        if not cleaned:
            raise ValueError("At least one TRUSTED_HOSTS value is required.")
        return cleaned

    @field_validator("log_level", mode="before")
    @classmethod
    def normalize_log_level(cls, value: Any) -> str:
        level = str(value or "INFO").strip().upper()
        allowed = {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"}
        if level not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of: {', '.join(sorted(allowed))}")
        return level

    @field_validator("log_format", mode="before")
    @classmethod
    def normalize_log_format(cls, value: Any) -> str:
        output = str(value or "json").strip().lower()
        if output not in {"json", "text"}:
            raise ValueError("LOG_FORMAT must be json or text.")
        return output

    @field_validator("cookie_samesite", mode="before")
    @classmethod
    def normalize_samesite(cls, value: Any) -> str:
        output = str(value or "lax").strip().lower()
        if output not in {"lax", "strict", "none"}:
            raise ValueError("COOKIE_SAMESITE must be lax, strict, or none.")
        return output

    @model_validator(mode="after")
    def validate_runtime_safety(self) -> "Settings":
        if self.enable_api_docs is None:
            self.enable_api_docs = self.app_env != "production"

        if self.app_env != "production":
            return self

        problems: list[str] = []
        jwt = self.jwt_secret.get_secret_value()
        session = self.session_secret.get_secret_value()

        if self.app_debug:
            problems.append("APP_DEBUG must be false")
        if not self.cookie_secure:
            problems.append("COOKIE_SECURE must be true")
        if self.cookie_samesite == "none" and not self.cookie_secure:
            problems.append("SameSite=None requires secure cookies")
        if _contains_placeholder(self.database_url):
            problems.append("DATABASE_URL contains a placeholder")
        if _contains_placeholder(jwt) or len(jwt) < 64:
            problems.append("JWT_SECRET must contain at least 64 non-placeholder characters")
        if _contains_placeholder(session) or len(session) < 64:
            problems.append(
                "SESSION_SECRET must contain at least 64 non-placeholder characters"
            )
        if "*" in self.frontend_origins:
            problems.append("wildcard FRONTEND_ORIGINS is not allowed")
        if "*" in self.trusted_hosts:
            problems.append("wildcard TRUSTED_HOSTS is not allowed")
        if any(_contains_placeholder(domain) for domain in self.even_mail_allowed_domains):
            problems.append("EVEN_MAIL_ALLOWED_DOMAINS contains a placeholder")
        if not self.network_number_prefix.isdigit():
            problems.append("NETWORK_NUMBER_PREFIX must contain only digits")

        if problems:
            raise ValueError(
                "Unsafe production configuration: " + "; ".join(problems)
            )
        return self

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def docs_enabled(self) -> bool:
        return bool(self.enable_api_docs)

    def configuration_readiness(self) -> dict[str, bool]:
        """Return a non-secret description of critical configuration state."""
        return {
            "database_url_configured": not _contains_placeholder(self.database_url),
            "redis_url_configured": not _contains_placeholder(self.redis_url),
            "jwt_secret_configured": not _contains_placeholder(
                self.jwt_secret.get_secret_value()
            ),
            "session_secret_configured": not _contains_placeholder(
                self.session_secret.get_secret_value()
            ),
            "frontend_origins_configured": bool(self.frontend_origins),
            "trusted_hosts_configured": bool(self.trusted_hosts),
        }


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Create and cache the process-wide settings object."""
    return Settings()


settings = get_settings()
