# 333 Network Backend Foundation

This package supplies the root configuration and governance files for the shared backend serving:

- HOLLO enrollment, profiles, contacts, and direct communication
- KANSEE meeting rooms and invitations
- E=Ven Mail applications and future mailbox provisioning
- Bazaar Art Live profiles, posts, groups, events, and media
- SIte projects, builds, exports, and publishing requests
- Bunya infrastructure plans, DNS, deployment, monitoring, and backups

## What this package contains

This archive contains configuration and policy files only. It does **not** yet contain the application package, database models, API routers, migrations, or tests.

The following paths must be added before the API can run:

```text
app/
  main.py
  core/
  models/
  schemas/
  routers/
  services/
migrations/
  env.py
  script.py.mako
  versions/
tests/
```

The default Docker command expects:

```text
app.main:app
```

## Recommended first milestone

Build the shared identity layer before live meetings, social synchronization, mail delivery, or deployment automation:

1. Account creation and sign-in
2. HOLLO enrollment
3. Unique handle reservation
4. Existing-number verification status
5. Provisional 333-number reservation
6. E=Ven email applications
7. Administrator application review
8. Shared authenticated profile endpoint
9. Audit logging
10. Backup and restore procedures

## Local setup

Requirements:

- Python 3.12 or later
- Docker with Compose, or local PostgreSQL and Redis
- A copied and edited `.env` file

Create the environment file:

```bash
cp .env.example .env
```

Replace every placeholder secret in `.env`, especially:

```text
POSTGRES_PASSWORD
JWT_SECRET
SESSION_SECRET
ADMIN_BOOTSTRAP_TOKEN
```

Start the supporting services:

```bash
docker compose up -d db redis
```

Install Python dependencies locally:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

After `app/main.py` and the migration package exist:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

Or build the complete container:

```bash
docker compose up --build
```

## Frontend connection

The GitHub Pages applications should call one HTTPS API origin, such as:

```text
https://api.example.com
```

Do not put database credentials, SMTP passwords, provider tokens, TURN secrets, or signing keys in frontend JavaScript.

Configure exact allowed frontend origins through `FRONTEND_ORIGINS`. Avoid wildcard CORS when credentials or cookies are enabled.

## Environment rules

- `.env.example` is documentation and may be committed.
- `.env` contains secrets and must never be committed.
- Production secrets should be stored in the hosting provider’s secret manager.
- Use different secrets for development, staging, and production.
- Rotate credentials after suspected exposure or staff-access changes.
- Do not reuse the example values.

## Data boundaries

The initial backend should distinguish clearly between:

- A local browser profile and a verified backend account
- A provisional 333 number and a globally reserved network number
- An E=Ven address application and a provisioned mailbox
- A local KANSEE preview and a hosted meeting service
- A local Bazaar workspace and synchronized public community content
- A SIte export and a completed deployment
- A Bunya plan and an executed provider operation

## Required governance review

Before accepting real public registrations, review and adapt:

- `SECURITY.md`
- `PRIVACY.md`
- `DATA_RETENTION.md`
- `INCIDENT_RESPONSE.md`
- `DEPLOYMENT.md`

These files are operational starting points, not substitutes for legal advice or a jurisdiction-specific privacy review.
