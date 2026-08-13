# 333 Network Security Policy

## Purpose

This document describes the security posture and operating rules for the 333 Network repository. It is an engineering and incident-response reference, not a guarantee that every planned network service is already deployed.

The 333 Network combines public browser applications with a developing shared backend. Some applications remain local-first while authenticated server features are introduced progressively.

## Current trust boundaries

### Public frontend

The public HTML, CSS, JavaScript, manifest, icons, and service worker are inspectable client code. **No database password, SMTP password, deployment token, DNS/registrar credential, TURN secret, private signing key, administrative bearer token, or equivalent infrastructure secret may be embedded in these files.**

### Shared backend

The backend foundation uses FastAPI, PostgreSQL/SQLAlchemy, Alembic, Redis-backed rate limiting, authentication/session services, and audit records. Backend configuration must come from deployment environment variables or a secret manager, never committed production credentials.

### Local-first applications

HOLLO, KANSEE, E=Ven Mail, Bazaar Art Live, SIte, and Bunya contain browser-local capabilities. Local browser state is not equivalent to a verified server account, server-side authorization, live mailbox, live conferencing service, or completed deployment.

### OHMIC / Bunya infrastructure boundary

Future hosting, build, deployment, DNS, certificate, object-storage, backup, and provider operations must run behind authenticated server-side controls. Provider credentials must never be returned to public browser code.

## Security requirements

1. Production secrets stay outside Git.
2. Development, staging, and production use separate secrets and data stores.
3. Exact frontend origins are used for credentialed CORS; wildcard credentialed CORS is prohibited.
4. Authentication tokens and cookies use secure production settings.
5. Passwords are stored only through approved password-hashing functions.
6. Refresh/session credentials are revocable and rotated according to the authentication design.
7. Sensitive operations are rate limited and audited.
8. User-supplied HTML/applications are treated as untrusted unless explicitly reviewed and must be sandboxed or isolated appropriately.
9. Uploads must be type-, size-, and content-validated before public serving.
10. Deployment, DNS, registrar, mail, and conferencing credentials use narrowly scoped service permissions.
11. Backups are encrypted where practical and restoration is tested.
12. Logs redact secrets and avoid storing private message contents unless a documented service requirement requires them.
13. Forwarded client-IP headers are trusted only behind a configured trusted proxy boundary.
14. Destructive migrations or deployment changes require a recovery/rollback plan.

## Authentication and account safety

The backend authentication foundation includes hashed passwords, access/refresh session handling, account status controls, role checks, and audit logging. Browser-local profile/login simulations must not be presented as equivalent to this server-backed identity layer.

Administrator accounts should use strong unique credentials and multi-factor authentication when the deployed identity stack supports it. Administrative interfaces must not rely on secrecy of a public URL as their only access control.

## Network services still requiring production security review

Before public production enablement, each of the following must receive a service-specific threat review:

- KANSEE signaling, WebRTC, STUN/TURN, rooms, invitations, recordings, and files;
- Bazaar Art Live posts, media, moderation, reporting, groups, and events;
- E=Ven mailbox provisioning, SMTP/JMAP/IMAP or chosen mail interfaces, abuse controls, SPF, DKIM, and DMARC;
- SIte/OHMIC builds, user code isolation, static hosting, domains, certificates, and rollback;
- Bunya provider operations, DNS, deployment credentials, monitoring, and backups;
- upload/object-storage services;
- notifications and outbound messaging;
- any bridge to external telephone or carrier/SIP infrastructure.

## Dependency and release security

Production images should contain runtime dependencies only. Development/test tooling should remain outside the production image unless explicitly required.

Every production release should verify at minimum:

- automated tests;
- lint/type checks appropriate to the codebase;
- secret scanning;
- dependency review;
- migration review;
- exact environment configuration;
- health checks;
- rollback readiness.

## Vulnerability reporting

Please do not disclose a suspected vulnerability publicly before maintainers have had a reasonable opportunity to assess it.

When reporting, include:

- affected component or route;
- reproducible steps;
- observed and expected behavior;
- potential impact;
- relevant browser/runtime information;
- a suggested mitigation if known.

**Never include real credentials, access tokens, private user messages, or sensitive personal information in a public issue.**

If no private reporting channel is configured yet, provide only a minimal public notice asking maintainers for a secure disclosure channel rather than publishing exploit details.

## Incident principles

If a credential or secret may have been exposed:

1. revoke or rotate it first;
2. contain the affected service;
3. preserve relevant logs/evidence without spreading the secret;
4. assess data and account impact;
5. restore from a known-good state when necessary;
6. document remediation and prevention steps.

The repository's `INCIDENT_RESPONSE.md`, `DATA_RETENTION.md`, and `DEPLOYMENT.md` provide companion operational guidance.

## Current status

The 333 Network is under active development. A feature appearing in a frontend application does not by itself mean the corresponding server-side service is production-enabled. Public-facing copy and documentation should continue distinguishing local previews, application/request flows, and genuinely provisioned live services.
