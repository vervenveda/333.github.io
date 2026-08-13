# 333 Network — Phase 1 Integrity Patch

This package contains only the Phase 1 files that were blocked from direct connector writes or that benefit from being uploaded together.

## Replace at repository root

- `register-service-worker.js`
- `service-worker.js`
- `Dockerfile`
- `CHANGELOG.md`
- `PRIVACY.md`

## Add at repository root

- `.dockerignore`
- `requirements-runtime.txt`
- `.github/workflows/backend-ci.yml`

## Deliberate removals

Follow `DELETE_THESE_FILES.txt` after replacements are in place.

## Already updated on working branch

The working branch `agent/333-integrity-foundation-v1` already contains accepted updates for:

- `SECURITY.md`
- `ACCESSIBILITY.md`
- `ROADMAP.md`

`BUILD_LOG.md` was added to `main` as the sanitized architecture/change baseline before the working branch was created.

## PWA validation

The replacement registration script emits the events already consumed by the gateway:

- `333-app-update-ready`
- `333-service-worker-controller-changed`

The replacement service worker advances the cache generation to `v6` and retains the existing offline-first behavior.

## Docker validation intent

The replacement Dockerfile installs only runtime packages through `requirements-runtime.txt`. The existing `requirements.txt` may continue to serve development/testing environments.

## CI validation intent

`backend-ci.yml` checks repository hygiene first, then runs Ruff, MyPy, and the existing pytest coverage gate on Python 3.12. The first run is expected to tell us whether any pre-existing lint, typing, or coverage debt remains; we will repair real failures rather than weakening the checks.

## Do not include secrets

Do not add `.env`, credentials, database passwords, JWT/session secrets, provider tokens, private keys, or production account data to this repository.
