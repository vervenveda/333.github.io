"""
333 Network shared FastAPI entry point.

This foundation runs before the feature routers are created. As router modules
are added under ``app/routers/``, they are discovered and registered
automatically.

Expected future modules:

    app.routers.auth
    app.routers.profiles
    app.routers.hollo
    app.routers.kansee
    app.routers.even_mail
    app.routers.bazaar
    app.routers.site
    app.routers.bunya
    app.routers.uploads
    app.routers.notifications
    app.routers.admin
"""

from __future__ import annotations

import importlib
import importlib.util
import logging
import os
import secrets
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, AsyncIterator
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

LOGGER = logging.getLogger("network333")
APP_VERSION = "0.1.0"


def _csv(value: str, *, default: tuple[str, ...] = ()) -> tuple[str, ...]:
    """Convert a comma-separated environment value into a clean tuple."""
    items = tuple(item.strip() for item in value.split(",") if item.strip())
    return items or default


def _bool(value: str | None, *, default: bool = False) -> bool:
    """Parse a conservative boolean environment value."""
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _int(value: str | None, *, default: int) -> int:
    """Parse an integer environment value with a safe fallback."""
    try:
        return int(value) if value is not None else default
    except (TypeError, ValueError):
        return default


def _is_placeholder(value: str | None) -> bool:
    """Detect unset or example-only secret values without revealing them."""
    if not value:
        return True

    lowered = value.strip().lower()
    markers = (
        "replace-",
        "example.invalid",
        "driver://",
        "changeme",
        "change-me",
        "placeholder",
    )
    return any(marker in lowered for marker in markers)


@dataclass(frozen=True, slots=True)
class Settings:
    """Small environment-backed settings object for the foundation app."""

    app_name: str
    app_env: str
    app_debug: bool
    api_prefix: str
    log_level: str
    frontend_origins: tuple[str, ...]
    trusted_hosts: tuple[str, ...]
    cookie_secure: bool
    enable_api_docs: bool
    gzip_minimum_size: int
    database_url: str
    redis_url: str
    jwt_secret: str
    session_secret: str

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"

    @classmethod
    def from_environment(cls) -> "Settings":
        app_env = os.getenv("APP_ENV", "development").strip().lower()
        api_prefix = os.getenv("API_PREFIX", "/api").strip() or "/api"
        if not api_prefix.startswith("/"):
            api_prefix = f"/{api_prefix}"
        api_prefix = api_prefix.rstrip("/") or "/api"

        default_origins = (
            "http://localhost:5500",
            "http://127.0.0.1:5500",
            "https://vervenveda.github.io",
        )
        default_hosts = ("localhost", "127.0.0.1", "testserver")

        return cls(
            app_name=os.getenv("APP_NAME", "333 Network API").strip()
            or "333 Network API",
            app_env=app_env,
            app_debug=_bool(os.getenv("APP_DEBUG"), default=False),
            api_prefix=api_prefix,
            log_level=os.getenv("LOG_LEVEL", "INFO").strip().upper() or "INFO",
            frontend_origins=_csv(
                os.getenv("FRONTEND_ORIGINS", ""),
                default=default_origins,
            ),
            trusted_hosts=_csv(
                os.getenv("TRUSTED_HOSTS", ""),
                default=default_hosts,
            ),
            cookie_secure=_bool(
                os.getenv("COOKIE_SECURE"),
                default=app_env == "production",
            ),
            enable_api_docs=_bool(
                os.getenv("ENABLE_API_DOCS"),
                default=app_env != "production",
            ),
            gzip_minimum_size=_int(
                os.getenv("GZIP_MINIMUM_SIZE"),
                default=1_024,
            ),
            database_url=os.getenv("DATABASE_URL", "").strip(),
            redis_url=os.getenv("REDIS_URL", "").strip(),
            jwt_secret=os.getenv("JWT_SECRET", "").strip(),
            session_secret=os.getenv("SESSION_SECRET", "").strip(),
        )

    def readiness(self) -> dict[str, Any]:
        """Return non-secret configuration readiness information."""
        checks = {
            "database_configured": not _is_placeholder(self.database_url),
            "redis_configured": not _is_placeholder(self.redis_url),
            "jwt_secret_configured": not _is_placeholder(self.jwt_secret),
            "session_secret_configured": not _is_placeholder(self.session_secret),
            "frontend_origins_configured": bool(self.frontend_origins),
            "trusted_hosts_configured": bool(self.trusted_hosts),
        }

        required_for_production = (
            checks["database_configured"],
            checks["redis_configured"],
            checks["jwt_secret_configured"],
            checks["session_secret_configured"],
            checks["frontend_origins_configured"],
            checks["trusted_hosts_configured"],
        )

        return {
            "ready": all(required_for_production)
            if self.is_production
            else True,
            "mode": "production" if self.is_production else "foundation",
            "checks": checks,
        }


SETTINGS = Settings.from_environment()


def _configure_logging(settings: Settings) -> None:
    level = getattr(logging, settings.log_level, logging.INFO)
    logging.basicConfig(
        level=level,
        format=(
            "%(asctime)s %(levelname)s %(name)s "
            "%(message)s"
        ),
    )


_configure_logging(SETTINGS)


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Attach request IDs, timing, and safe request logs."""

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        request_id = (
            request.headers.get("x-request-id", "").strip()[:128]
            or str(uuid4())
        )
        request.state.request_id = request_id
        started = time.perf_counter()

        try:
            response = await call_next(request)
        except Exception:
            elapsed_ms = round((time.perf_counter() - started) * 1_000, 2)
            LOGGER.exception(
                "request_failed method=%s path=%s request_id=%s duration_ms=%s",
                request.method,
                request.url.path,
                request_id,
                elapsed_ms,
            )
            raise

        elapsed_ms = round((time.perf_counter() - started) * 1_000, 2)
        response.headers["X-Request-ID"] = request_id
        response.headers["Server-Timing"] = f"app;dur={elapsed_ms}"

        LOGGER.info(
            "request method=%s path=%s status=%s request_id=%s duration_ms=%s",
            request.method,
            request.url.path,
            response.status_code,
            request_id,
            elapsed_ms,
        )
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Apply conservative API security headers to every response."""

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        response = await call_next(request)

        headers = response.headers
        headers.setdefault("X-Content-Type-Options", "nosniff")
        headers.setdefault("X-Frame-Options", "DENY")
        headers.setdefault("Referrer-Policy", "no-referrer")
        headers.setdefault(
            "Permissions-Policy",
            (
                "camera=(), microphone=(), geolocation=(), "
                "payment=(), usb=(), interest-cohort=()"
            ),
        )
        headers.setdefault(
            "Content-Security-Policy",
            (
                "default-src 'none'; "
                "base-uri 'none'; "
                "form-action 'none'; "
                "frame-ancestors 'none'"
            ),
        )
        headers.setdefault("Cross-Origin-Resource-Policy", "same-site")
        headers.setdefault("X-Permitted-Cross-Domain-Policies", "none")

        forwarded_proto = request.headers.get("x-forwarded-proto", "")
        is_https = request.url.scheme == "https" or forwarded_proto == "https"
        if SETTINGS.is_production and is_https:
            headers.setdefault(
                "Strict-Transport-Security",
                "max-age=31536000; includeSubDomains",
            )

        return response


@dataclass(frozen=True, slots=True)
class RouterDefinition:
    module: str
    prefix: str
    tags: tuple[str, ...]


ROUTER_DEFINITIONS: tuple[RouterDefinition, ...] = (
    RouterDefinition("app.routers.auth", "/auth", ("Authentication",)),
    RouterDefinition("app.routers.profiles", "/profiles", ("Profiles",)),
    RouterDefinition("app.routers.hollo", "/hollo", ("HOLLO",)),
    RouterDefinition("app.routers.kansee", "/kansee", ("KANSEE",)),
    RouterDefinition("app.routers.even_mail", "/even-mail", ("E=Ven Mail",)),
    RouterDefinition("app.routers.bazaar", "/bazaar", ("Bazaar Art Live",)),
    RouterDefinition("app.routers.site", "/site", ("SIte",)),
    RouterDefinition("app.routers.bunya", "/bunya", ("Bunya",)),
    RouterDefinition("app.routers.uploads", "/uploads", ("Uploads",)),
    RouterDefinition(
        "app.routers.notifications",
        "/notifications",
        ("Notifications",),
    ),
    RouterDefinition("app.routers.admin", "/admin", ("Administration",)),
)


def _module_exists(module_name: str) -> bool:
    """Return True only when the requested optional module can be resolved."""
    try:
        return importlib.util.find_spec(module_name) is not None
    except (ImportError, ModuleNotFoundError, AttributeError):
        return False


def register_optional_routers(app: FastAPI) -> tuple[str, ...]:
    """
    Register feature routers that currently exist.

    A missing router is expected during the foundation phase. Import failures
    inside an existing router are not hidden and will stop startup.
    """
    loaded: list[str] = []

    for definition in ROUTER_DEFINITIONS:
        if not _module_exists(definition.module):
            LOGGER.info("router_pending module=%s", definition.module)
            continue

        module = importlib.import_module(definition.module)
        router = getattr(module, "router", None)
        if router is None:
            raise RuntimeError(
                f"{definition.module} exists but does not expose `router`."
            )

        app.include_router(
            router,
            prefix=f"{SETTINGS.api_prefix}{definition.prefix}",
            tags=list(definition.tags),
        )
        loaded.append(definition.module)
        LOGGER.info("router_registered module=%s", definition.module)

    return tuple(loaded)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application startup and shutdown boundary."""
    LOGGER.info(
        "startup app=%s version=%s environment=%s",
        SETTINGS.app_name,
        APP_VERSION,
        SETTINGS.app_env,
    )

    app.state.started_at = time.time()
    app.state.instance_id = secrets.token_hex(8)

    yield

    LOGGER.info(
        "shutdown app=%s instance_id=%s",
        SETTINGS.app_name,
        getattr(app.state, "instance_id", "unknown"),
    )


def create_app(settings: Settings = SETTINGS) -> FastAPI:
    """Application factory used by Uvicorn and tests."""
    docs_url = "/docs" if settings.enable_api_docs else None
    redoc_url = "/redoc" if settings.enable_api_docs else None
    openapi_url = "/openapi.json" if settings.enable_api_docs else None

    app = FastAPI(
        title=settings.app_name,
        description=(
            "Shared backend foundation for HOLLO, KANSEE, E=Ven Mail, "
            "Bazaar Art Live, SIte, and Bunya."
        ),
        version=APP_VERSION,
        debug=settings.app_debug,
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_url=openapi_url,
        lifespan=lifespan,
    )

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=list(settings.trusted_hosts),
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.frontend_origins),
        allow_credentials=True,
        allow_methods=[
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
            "OPTIONS",
        ],
        allow_headers=[
            "Authorization",
            "Content-Type",
            "If-Match",
            "Idempotency-Key",
            "X-CSRF-Token",
            "X-Request-ID",
        ],
        expose_headers=[
            "ETag",
            "Retry-After",
            "X-Request-ID",
        ],
        max_age=600,
    )
    app.add_middleware(
        GZipMiddleware,
        minimum_size=settings.gzip_minimum_size,
    )
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestContextMiddleware)

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "error": "validation_error",
                "message": "The request did not pass validation.",
                "details": exc.errors(),
                "request_id": getattr(request.state, "request_id", None),
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        LOGGER.exception(
            "unhandled_exception request_id=%s",
            getattr(request.state, "request_id", None),
            exc_info=exc,
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": "internal_server_error",
                "message": "The request could not be completed.",
                "request_id": getattr(request.state, "request_id", None),
            },
        )

    @app.get("/", tags=["System"])
    async def root() -> dict[str, Any]:
        return {
            "service": settings.app_name,
            "version": APP_VERSION,
            "environment": settings.app_env,
            "status": "online",
            "api_prefix": settings.api_prefix,
            "documentation": docs_url,
        }

    @app.get("/health", tags=["System"])
    async def health() -> dict[str, Any]:
        """Liveness check used by Docker and external monitors."""
        return {
            "status": "ok",
            "service": settings.app_name,
            "version": APP_VERSION,
        }

    @app.get("/ready", tags=["System"])
    async def readiness() -> JSONResponse:
        """
        Configuration readiness check.

        Development foundation mode remains runnable while modules are being
        built. Production mode returns 503 when required configuration is
        missing or still uses placeholder values.
        """
        report = settings.readiness()
        report["routers_loaded"] = list(
            getattr(app.state, "routers_loaded", ())
        )

        return JSONResponse(
            status_code=200 if report["ready"] else 503,
            content=report,
        )

    @app.get(f"{settings.api_prefix}/status", tags=["System"])
    async def api_status() -> dict[str, Any]:
        """Public, non-secret summary of the API foundation."""
        return {
            "status": "online",
            "mode": settings.readiness()["mode"],
            "applications": [
                "HOLLO",
                "KANSEE",
                "E=Ven Mail",
                "Bazaar Art Live",
                "SIte",
                "Bunya",
            ],
            "routers_loaded": list(
                getattr(app.state, "routers_loaded", ())
            ),
        }

    app.state.routers_loaded = register_optional_routers(app)
    return app


app = create_app()
