# 333 Network Changelog

Meaningful public repository changes are recorded here. Dates use `YYYY-MM-DD`.

## Unreleased

### Integrity and governance

- Added `BUILD_LOG.md` as a sanitized record of major technical and architectural milestones.
- Replaced stale Polyglot governance text with 333-specific security, accessibility, and roadmap documentation.
- Prepared replacement privacy and changelog documents for the 333 Network.
- Identified accidental Python bytecode and a duplicate root Alembic environment file for removal.
- Prepared production dependency separation and `.dockerignore` hardening.

### PWA

- Corrected the service-worker registration contract to use 333-native update events.
- Added update-ready detection for waiting/installing service workers.
- Added one-time controller-change signaling so the gateway can reload after an accepted update.
- Advanced the 333 PWA cache version and removed obsolete Polyglot cache-name cleanup.

### Backend audit

- Confirmed the shared FastAPI foundation for authentication, profiles, HOLLO, E=Ven Mail applications, administration, PostgreSQL/Alembic, Redis-backed rate limiting, Docker deployment, and structured logging.
- Confirmed KANSEE, Bazaar, SIte, Bunya, uploads, and notifications are intended service families but are not all implemented yet.
- Confirmed the browser applications remain substantially local-first and must be integrated with the shared backend deliberately.

## 0.3.0 — 2026-08

### Backend foundation

- Shared FastAPI application entry point and optional-router model.
- Asynchronous PostgreSQL/SQLAlchemy and Alembic foundation.
- Authentication, profiles, HOLLO, E=Ven Mail application, and administrative API foundations.
- Argon2 password hashing, token support, refresh rotation, audit logging, and role checks.
- Docker, Redis, deployment, retention, incident-response, and operational documentation foundations.

### Applications

- Continued development of HOLLO, KANSEE, E=Ven Mail, Bazaar Art Live, SIte, and Bunya as local-first browser applications.
- 333 Network PWA shell, manifest, install helper, offline fallback, and service-worker caching.

## Documentation rule

This changelog distinguishes implemented backend services, local-first browser capabilities, and planned hosted services. A local interface or planning console is not labeled as a live network service until its backend contract is implemented and verified.
