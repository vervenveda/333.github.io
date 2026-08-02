# Security Policy

## Scope

This policy applies to the 333 Network backend, its administrative interfaces, APIs, databases, background workers, object storage, and integrations supporting HOLLO, KANSEE, E=Ven Mail, Bazaar Art Live, SIte, and Bunya.

## Security principles

1. **Least privilege:** users, services, workers, and administrators receive only the permissions needed for their current role.
2. **Server-side secrets:** credentials, signing keys, provider tokens, database passwords, TURN secrets, and mail passwords never enter frontend code.
3. **Explicit boundaries:** local browser records are not treated as verified server identities.
4. **Defense in depth:** authentication, authorization, validation, rate limiting, logging, encryption, and backups work together.
5. **Safe failure:** errors must not expose stack traces, secrets, database details, or private user data.
6. **Auditable administration:** sensitive administrative actions create immutable audit records.

## Minimum production controls

- HTTPS everywhere
- Secure, HttpOnly, SameSite cookies when cookie sessions are used
- Strong password hashing with Argon2id
- Short-lived access tokens and revocable refresh sessions
- Email verification and controlled account recovery
- Multi-factor authentication for privileged administrators
- Role- and resource-based authorization
- Rate limits for sign-in, enrollment, password reset, messaging, uploads, applications, and moderation
- File-type allowlists, size limits, generated storage names, and malware scanning
- Database encryption at rest where supported
- Encrypted backups
- Centralized logs with restricted access
- Dependency scanning and routine security updates
- Separate development, staging, and production environments

## Identity and number safeguards

- Unique handles and 333 numbers must be reserved through database uniqueness constraints.
- Number allocation must occur inside a transaction.
- Browser-generated numbers remain provisional until server confirmation.
- Existing telephone numbers must not be described as verified until a verification challenge succeeds.
- The four established service routes must be protected from member allocation.
- Identity changes, number reassignment, and recovery actions must be audited.

## KANSEE safeguards

- Meeting tokens must be short-lived and room-specific.
- Host and moderator permissions must be checked server-side.
- TURN credentials should be temporary.
- Camera, microphone, and screen capture require user action.
- Recording requires explicit notice and authorization.
- Meeting metadata retention should be minimized.
- Media streams should not be stored by default.

## Bazaar safeguards

- Provide block, mute, report, moderation, and appeal mechanisms.
- Restrict dangerous file types and executable uploads.
- Strip unnecessary image metadata where appropriate.
- Protect private profiles and restricted groups from unauthorized access.
- Require server-side ownership checks for all edits and deletions.
- Preserve moderation and audit records according to retention policy.

## SIte and Embed Studio safeguards

- Embedded code must run in a sandboxed frame.
- Project previews must not receive backend secrets.
- Publishing jobs must validate filenames and prevent path traversal.
- Uploaded archives must be inspected before extraction.
- Build workers should run with limited privileges and isolated storage.
- Provider deployment tokens remain server-side.

## Bunya safeguards

- Provider credentials belong in a secret manager.
- DNS, registrar, deployment, and backup operations require explicit authorization.
- Destructive actions require confirmation and audit logging.
- Secrets must be redacted from logs and API responses.
- Infrastructure administrators should use multi-factor authentication.

## Vulnerability reporting

Report suspected vulnerabilities privately to the project security contact. Include:

- A description of the issue
- Affected endpoint or component
- Reproduction steps
- Potential impact
- Suggested remediation when known

Do not include real user secrets or unnecessary personal data in reports.

## Response targets

Suggested initial targets:

- Critical: acknowledge within 24 hours
- High: acknowledge within 2 business days
- Medium: acknowledge within 5 business days
- Low: acknowledge within 10 business days

Actual remediation time depends on severity, exploitability, and operational risk.

## Prohibited repository content

Never commit:

- Real `.env` files
- Passwords or API tokens
- Database dumps containing personal data
- Private keys or certificates
- Production backup archives
- User-uploaded private media
- Incident evidence containing unredacted personal data
