"""333 Network shared FastAPI application entry point."""

from __future__ import annotations

import importlib
import importlib.util
import logging
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

from app.core.config import Settings, settings
from app.core.database import database_health_check, dispose_engine
from app.core.exceptions import ServiceError
from app.core.rate_limits import rate_limiter
from app.core.logging import (
    configure_logging,
    reset_request_id,
    set_request_id,
)

APP_VERSION = "0.3.0"
configure_logging(settings)
LOGGER = logging.getLogger("network333")


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Attach request IDs, timing headers, and structured access logs."""

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        request_id = request.headers.get("x-request-id", "").strip()[:128] or str(
            uuid4()
        )
        request.state.request_id = request_id
        token = set_request_id(request_id)
        started = time.perf_counter()

        try:
            response = await call_next(request)
            elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
            response.headers["X-Request-ID"] = request_id
            response.headers["Server-Timing"] = f"app;dur={elapsed_ms}"

            LOGGER.info(
                "request_completed",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": elapsed_ms,
                },
            )
            return response
        except Exception:
            elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
            LOGGER.exception(
                "request_failed",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": elapsed_ms,
                },
            )
            raise
        finally:
            reset_request_id(token)


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
            "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
        )
        headers.setdefault(
            "Content-Security-Policy",
            "default-src 'none'; base-uri 'none'; form-action 'none'; "
            "frame-ancestors 'none'",
        )
        headers.setdefault("Cross-Origin-Resource-Policy", "same-site")
        headers.setdefault("X-Permitted-Cross-Domain-Policies", "none")

        forwarded_proto = request.headers.get("x-forwarded-proto", "")
        is_https = request.url.scheme == "https" or forwarded_proto == "https"
        if settings.is_production and is_https:
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
    try:
        return importlib.util.find_spec(module_name) is not None
    except (ImportError, ModuleNotFoundError, AttributeError):
        return False


def register_optional_routers(app: FastAPI) -> tuple[str, ...]:
    """Register each application router when its module exists."""
    loaded: list[str] = []

    for definition in ROUTER_DEFINITIONS:
        if not _module_exists(definition.module):
            LOGGER.info("router_pending", extra={"module_name": definition.module})
            continue

        module = importlib.import_module(definition.module)
        router = getattr(module, "router", None)
        if router is None:
            raise RuntimeError(
                f"{definition.module} exists but does not expose `router`."
            )

        app.include_router(
            router,
            prefix=f"{settings.api_prefix}{definition.prefix}",
            tags=list(definition.tags),
        )
        loaded.append(definition.module)
        LOGGER.info("router_registered", extra={"module_name": definition.module})

    return tuple(loaded)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Validate startup dependencies and dispose resources on shutdown."""
    app.state.started_at = time.time()
    app.state.instance_id = secrets.token_hex(8)

    LOGGER.info(
        "application_starting",
        extra={
            "version": APP_VERSION,
            "environment": settings.app_env,
            "instance_id": app.state.instance_id,
        },
    )

    health = await database_health_check()
    app.state.startup_database_health = health.to_dict()

    if not health.ok:
        LOGGER.warning(
            "database_not_ready_at_startup",
            extra={"database_status": health.status},
        )
        if settings.database_required_on_startup:
            raise RuntimeError("Database is required but unavailable at startup.")

    try:
        yield
    finally:
        await rate_limiter.close()
        await dispose_engine()
        LOGGER.info(
            "application_stopped",
            extra={"instance_id": app.state.instance_id},
        )


def create_app(application_settings: Settings = settings) -> FastAPI:
    docs_url = "/docs" if application_settings.docs_enabled else None
    redoc_url = "/redoc" if application_settings.docs_enabled else None
    openapi_url = "/openapi.json" if application_settings.docs_enabled else None

    app = FastAPI(
        title=application_settings.app_name,
        description=(
            "Shared backend for HOLLO, KANSEE, E=Ven Mail, Bazaar Art Live, "
            "SIte, and Bunya."
        ),
        version=APP_VERSION,
        debug=application_settings.app_debug,
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_url=openapi_url,
        lifespan=lifespan,
    )

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=application_settings.trusted_hosts,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=application_settings.frontend_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=[
            "Authorization",
            "Content-Type",
            "If-Match",
            "Idempotency-Key",
            "X-CSRF-Token",
            "X-Request-ID",
        ],
        expose_headers=["ETag", "Retry-After", "X-Request-ID"],
        max_age=600,
    )
    app.add_middleware(
        GZipMiddleware,
        minimum_size=application_settings.gzip_minimum_size,
    )
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestContextMiddleware)

    @app.exception_handler(ServiceError)
    async def service_error_handler(
        request: Request,
        exc: ServiceError,
    ) -> JSONResponse:
        headers: dict[str, str] = {}
        retry_after = exc.details.get("retry_after")
        if retry_after is not None:
            headers["Retry-After"] = str(retry_after)

        return JSONResponse(
            status_code=exc.status_code,
            headers=headers,
            content={
                "error": exc.code,
                "message": exc.message,
                "details": exc.details,
                "request_id": getattr(request.state, "request_id", None),
            },
        )

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
        LOGGER.exception("unhandled_exception", exc_info=exc)
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
            "service": application_settings.app_name,
            "version": APP_VERSION,
            "environment": application_settings.app_env,
            "status": "online",
            "api_prefix": application_settings.api_prefix,
            "documentation": docs_url,
        }

    @app.get("/health", tags=["System"])
    async def health() -> dict[str, Any]:
        """Lightweight process liveness check."""
        return {
            "status": "ok",
            "service": application_settings.app_name,
            "version": APP_VERSION,
        }

    @app.get("/ready", tags=["System"])
    async def readiness() -> JSONResponse:
        """Check configuration plus a live database connection."""
        configuration = application_settings.configuration_readiness()
        database = await database_health_check()

        configuration_ready = all(configuration.values())
        ready = database.ok and (
            configuration_ready if application_settings.is_production else True
        )

        return JSONResponse(
            status_code=200 if ready else 503,
            content={
                "ready": ready,
                "mode": (
                    "production"
                    if application_settings.is_production
                    else "development"
                ),
                "configuration": configuration,
                "database": database.to_dict(),
                "routers_loaded": list(app.state.routers_loaded),
            },
        )

    @app.get(f"{application_settings.api_prefix}/status", tags=["System"])
    async def api_status() -> dict[str, Any]:
        return {
            "status": "online",
            "applications": [
                "HOLLO",
                "KANSEE",
                "E=Ven Mail",
                "Bazaar Art Live",
                "SIte",
                "Bunya",
            ],
            "routers_loaded": list(app.state.routers_loaded),
        }

    app.state.routers_loaded = register_optional_routers(app)
    return app


app = create_app()
