# 333 Network — Phase 1 v2 Reconciliation

This package is intentionally **root-ready**. Unlike the earlier package, the ZIP has no enclosing patch directory.

## Target branch

Apply only to:

`agent/333-integrity-foundation-v2`

Do not apply these files directly to `main` while Phase 1 remains under verification.

## Replace at repository root

- `SECURITY.md`
- `ACCESSIBILITY.md`
- `PRIVACY.md`
- `ROADMAP.md`
- `CHANGELOG.md`
- `BUILD_LOG.md`
- `register-service-worker.js`
- `service-worker.js`
- `Dockerfile`

## Add at repository root

- `.dockerignore`
- `requirements-runtime.txt`
- `.github/workflows/backend-ci.yml`

## Deliberate removals on v2 only

After the replacements are present, remove only:

1. `env.py`
2. `app/_pychache_/__init__.cpython-313.pyc`
3. `app/_pychache_/main.cpython-313.pyc`

Keep:

- `migrations/env.py`
- `app/__init__.py`
- `app/main.py`

## Misplaced folder on main

The current `main` contains a literal folder:

`agent/333-integrity-foundation-v1/`

That folder came from the first web upload. Do not delete it until the useful patch contents are confirmed in v2. Once v2 is fully validated, the literal folder can be removed from `main` as a cleanup-only change.

## Validation after application

1. Confirm `register-service-worker.js` contains 333-native events and no `PolyglotPWA`/`polyglot:pwa-*` names.
2. Confirm `service-worker.js` uses cache generation `v6` and no longer deletes `polyglot-*` caches.
3. Confirm `Dockerfile` installs `requirements-runtime.txt`.
4. Confirm the three deliberate cleanup targets are absent.
5. Allow `.github/workflows/backend-ci.yml` to run.
6. Inspect Ruff, MyPy, pytest, and coverage results; repair genuine failures rather than weakening the checks.
7. Compare v2 with `main` before merge.

## Security rule

Never add `.env`, credentials, database passwords, JWT/session secrets, deployment/provider tokens, private keys, or production account data to this repository.
