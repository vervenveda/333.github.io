# Phase 2B test targets

After installation and Bunya restart:

1. GET /health -> 200
2. GET /api/bunya/status -> member_authority = OHMIC Foundry
3. POST /api/auth/register -> creates account in OHMIC
4. POST /api/auth/login -> returns 333 access token + OHMIC refresh token
5. GET /api/auth/me with access token -> returns same account
6. POST /api/auth/refresh -> rotates refresh token through OHMIC
7. POST /api/auth/logout -> revokes refresh session through OHMIC
8. Existing /api/bunya/cloud member path still works

This phase does not yet remove the legacy database startup check from app/main.py.
