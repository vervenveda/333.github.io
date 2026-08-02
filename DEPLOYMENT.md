# Deployment Guide

## Deployment model

The public HTML applications may remain on GitHub Pages. The backend must run on infrastructure that supports:

- Python application processes
- PostgreSQL
- Redis
- HTTPS
- Secret management
- Persistent object storage
- Background workers
- Scheduled backups
- Monitoring and logs

Use separate environments:

```text
development
staging
production
```

Never share databases, signing secrets, upload buckets, or provider tokens between environments.

## Before deployment

The package now includes the runnable application entry point, validated settings, asynchronous database sessions, base model metadata, and the Alembic environment. Add the feature models, schemas, routers, services, security module, and tests before public use:

```text
app/core/security.py
app/models/user.py
app/models/profile.py
app/models/network_number.py
app/models/email_application.py
app/models/refresh_session.py
app/models/audit_log.py
app/schemas/
app/routers/
app/services/
tests/
```

The API must expose a health endpoint expected by the Docker image:

```text
GET /health
```

## Environment preparation

1. Copy `.env.example` into the hosting platform’s secret system.
2. Replace every placeholder secret.
3. Use an HTTPS public API URL.
4. Set exact GitHub Pages frontend origins.
5. Set `COOKIE_SECURE=true` in production.
6. Set trusted hosts explicitly.
7. Configure PostgreSQL with automated backups.
8. Configure Redis persistence appropriately.
9. Configure object storage for uploads.
10. Configure monitoring and alerting.

## Database migrations

Run migrations as a controlled deployment step:

```bash
alembic upgrade head
```

Do not run schema-changing migrations automatically from every web process.

Before a risky migration:

- Back up the database
- Test against a staging copy
- Document rollback behavior
- Confirm application compatibility
- Schedule maintenance when required

## Docker deployment

Build:

```bash
docker build -t network333-backend:0.1.0 .
```

Run locally:

```bash
docker compose up --build
```

For production, use a managed PostgreSQL service when possible. Do not expose PostgreSQL or Redis directly to the public internet.

## CORS and frontend origins

Set exact origins, for example:

```text
https://vervenveda.github.io
https://www.example.com
```

Do not use `*` with cookies or credentialed requests.

The frontend should call only the public API hostname. It must never receive database, SMTP, object-storage, DNS, registrar, deployment, or TURN administrative secrets.

## Reverse proxy

Terminate TLS through the hosting provider or a reverse proxy. Forward only required headers. Enforce:

- HTTPS redirects
- HSTS after testing
- Request-size limits
- Timeouts
- Rate limits
- Security headers
- WebSocket upgrade support for KANSEE signaling

## Workers

Run background workers separately from the web API for:

- Email notifications
- Media inspection and thumbnails
- Cleanup and retention
- Backups
- SIte builds
- Bunya deployments
- DNS or provider operations

Workers should use narrowly scoped credentials.

## Backups

At minimum:

- Daily PostgreSQL backups
- Encrypted backup storage
- A 30-day rolling retention period
- Regular restore tests
- Object-storage versioning or equivalent protection
- A documented recovery-time objective
- A documented recovery-point objective

A backup is not reliable until a restore has been tested.

## Monitoring

Monitor:

- Health endpoint
- Error rate
- Request latency
- Database connections
- Redis availability
- Worker queue depth
- Failed sign-ins
- Rate-limit events
- Upload failures
- Mail application failures
- Meeting-signaling errors
- Deployment failures
- Backup age and restore-test status

## Release checklist

- [ ] Tests pass
- [ ] Dependency and secret scans pass
- [ ] Migration reviewed
- [ ] Backup completed
- [ ] Environment variables verified
- [ ] CORS origins verified
- [ ] Admin multi-factor authentication verified
- [ ] Rate limits verified
- [ ] Upload restrictions verified
- [ ] Logs redact secrets
- [ ] Health check succeeds
- [ ] Rollback procedure documented
- [ ] Privacy and retention changes reviewed
- [ ] Incident contact confirmed

## Rollback

A rollback plan should identify:

- Previous application image
- Database compatibility
- Migration downgrade or forward-fix approach
- Feature flags to disable new behavior
- Cache invalidation steps
- Member communication responsibilities

Avoid irreversible database migrations without a tested recovery strategy.
