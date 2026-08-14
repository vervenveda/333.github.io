# OHMIC / 333 Sovereign Account Authority — Phase 2B

This package migrates the 333 account endpoints from SQL-backed persistence to
the encrypted OHMIC Account Authority already running behind the Secure Server.

Files replaced:
- app/routers/auth.py
- app/core/rate_limits.py

File added:
- app/services/ohmic_account_service.py

What changes:
- /api/auth/register -> OHMIC Account Authority
- /api/auth/login -> OHMIC Account Authority
- /api/auth/refresh -> OHMIC Account Authority
- /api/auth/logout -> OHMIC Account Authority
- /api/auth/me -> OHMIC member/account authority
- rate-limit counters become process-local ephemeral state instead of Redis

What does NOT change in this phase:
- profiles
- other application routers
- app/main.py database startup/readiness plumbing
- legacy SQL modules remain present temporarily
- OHMIC encrypted data files are not touched

No secrets are included in this ZIP.
