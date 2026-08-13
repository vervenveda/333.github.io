# 333 Network — Systematic Build Log

**Purpose:** Preserve implementation decisions and verified milestones while the 333 Network is completed systematically.

> This repository is public. This log records only non-sensitive implementation facts. Credentials, private server topology, security secrets, internal administrative routes, and other restricted architecture belong in the private Sovereign Build Codex and are intentionally excluded here.

## Operating discipline

1. Work in small, reviewable phases.
2. Verify each major change before beginning the next.
3. Update this log at regular checkpoints and after substantial public-repository milestones.
4. Preserve existing user-facing applications unless a migration is deliberate and reversible.
5. Do not expose secrets or administrative bearer credentials in browser code.
6. Keep local-first/offline behavior as a fallback where practical.
7. Keep 333 services specialized rather than duplicating the same system in multiple applications.

## Responsibility map

- **333 Network** — network experience and discovery.
- **HOLLO** — shared member identity and network identity.
- **E=Ven Mail** — network mail application/provisioning surface.
- **KANSEE** — meetings and video-conferencing experience.
- **Bazaar Art Live** — community/social/discovery feed.
- **SIte** — accessible website and application creation.
- **OHMIC Foundry** — build, deployment, hosting, releases, portable site publication, and future URL/domain hosting engine.
- **Bunya** — infrastructure control and operational visibility for deployment, domains, DNS, certificates, monitoring, backups, and provider operations.

## Verified audit baseline — 2026-08-13

The current repository already contains a substantial network foundation rather than an empty prototype.

### Implemented backend foundation

- FastAPI application entry point.
- Asynchronous SQLAlchemy/PostgreSQL foundation.
- Alembic migration environment.
- Redis-backed rate-limit foundation.
- Authentication, profiles, HOLLO, E=Ven application, and administration routers.
- Password hashing, token/session foundation, audit logging, and role checks.
- Docker deployment foundation.
- PWA/offline shell.

### Major frontend applications present

- HOLLO / 333 Direct Connect.
- KANSEE meeting rooms.
- E=Ven Mail.
- Bazaar Art Live.
- SIte website/application builder.
- Bunya infrastructure console.

### Confirmed service gaps

The FastAPI application declares future router families for KANSEE, Bazaar, SIte, Bunya, uploads, and notifications, but those router implementations are not yet present. The associated frontend applications therefore still depend heavily on local-first browser state.

### Confirmed integrity/maintenance findings

- PWA service-worker registration contains legacy Polyglot event naming that does not match the 333 gateway's update events.
- Several governance documents contain stale Polyglot project text and must be replaced with genuine 333 documents.
- Python bytecode/cache artifacts are present in the repository and should be removed.
- A duplicate root `env.py` exists alongside the Alembic migration environment and is an exact duplicate of `migrations/env.py`.
- No GitHub Actions CI workflow was found protecting the committed backend tests.
- Production and development Python dependencies should be separated in the Docker build.
- Some environment variables anticipated by `.env.example` are not yet represented by runtime settings and should be wired only when their services are implemented.

## Phase plan

### Phase 1 — Repository integrity and baseline protection

Status: **PREPARED — WORKING BRANCH + VERIFIED UPLOAD PATCH; NOT MERGED**

1. [x] Establish the build log.
2. [x] Audit and specify the PWA registration/update repair.
3. [x] Verify the duplicate root Alembic `env.py` and accidental bytecode artifacts.
4. [x] Replace stale `SECURITY.md`, `ACCESSIBILITY.md`, and `ROADMAP.md` on the working branch.
5. [x] Prepare 333-specific `PRIVACY.md` and `CHANGELOG.md` replacements.
6. [x] Prepare production dependency separation and `.dockerignore` hardening.
7. [x] Prepare initial CI for integrity, Ruff, MyPy, tests, and coverage.
8. [ ] Apply the blocked runtime/build files from the verified upload patch.
9. [ ] Remove the three deliberately identified stale/generated files.
10. [ ] Run and repair the first CI result if it reveals pre-existing quality debt.
11. [ ] Verify the complete Phase 1 diff before merge.

### Phase 2 — Shared identity circuit

Wire the public applications to one shared authenticated 333 client while retaining bounded offline/local fallback.

### Phase 3 — E=Ven application circuit

Connect the existing E=Ven frontend to the working backend application/review API and establish canonical mail-domain configuration. Mailbox delivery/provisioning remains a later infrastructure phase.

### Phase 4 — KANSEE live conferencing

Implement room API, ACLs, invitations, signaling, presence, STUN/TURN integration, WebRTC/SFU strategy, synchronized chat, and meeting event records.

### Phase 5 — Bazaar Art Live service

Implement profiles, posts, groups/events, media, notifications, moderation, and optional OHMIC-published-site discovery cards.

### Phase 6 — OHMIC Foundry deployment and hosting

Implement project/build/release/deployment contracts, static hosting, stable free 333 URLs, custom-domain routing, TLS, storage, version history, and rollback while preserving portable exports.

### Phase 7 — Bunya infrastructure control plane

Connect deployment state, domain/DNS operations, certificates, monitoring, backup status, and narrowly scoped provider operations without placing infrastructure secrets in frontend JavaScript.

### Phase 8 — Communications infrastructure

Complete mailbox provisioning/delivery and optional external telecom bridges after identity, deployment, and control-plane foundations are stable.

### Phase 9 — Operational reporting

Feed safe structured 333 operational events into the protected administrative reporting layer without storing private message contents as routine analytics.

---

## Change records

### 2026-08-13 — Log 001 — Baseline protection

**Decision:** All substantial 333 changes will be developed and verified in small, reviewable steps.

**Decision:** Public technical history and private architectural history are intentionally separated. This log is safe for the public repository; the Sovereign Build Codex remains the fuller private continuity record.

**Decision:** OHMIC Foundry will be developed as the deployment/hosting engine rather than duplicating a second hosting stack inside the 333 frontend repository.

**Decision:** Existing application roles are preserved: 333 = network, HOLLO = identity, SIte = creation, OHMIC = hosting/deployment, Bunya = infrastructure control, Bazaar = discovery/community, KANSEE = meetings, E=Ven = mail.

### 2026-08-13 — Log 002 — Phase 1 integrity preparation

**Working branch:** `agent/333-integrity-foundation-v1`.

**Verified direct branch changes:** 333-specific `SECURITY.md`, `ACCESSIBILITY.md`, and `ROADMAP.md` replacements.

**Verified PWA repair:** the existing gateway listens for `333-app-update-ready` and `333-service-worker-controller-changed`, while the old registration shim emitted copied Polyglot events. A replacement registration bridge was prepared to emit the exact 333 events and detect waiting/installing workers. The replacement JavaScript passed `node --check` before packaging.

**Verified cache cleanup:** a replacement service worker was prepared with the next 333 cache generation and without obsolete Polyglot cache-prefix cleanup. It also passed `node --check`.

**Verified repository cleanup targets:** root `env.py` is byte-for-byte identical to `migrations/env.py`; two committed `.pyc` files under the misspelled `app/_pychache_/` directory are generated artifacts. Removal remains deliberate and explicit; `migrations/env.py`, `app/__init__.py`, and `app/main.py` must remain.

**Prepared production hardening:** `.dockerignore`, `requirements-runtime.txt`, and a Dockerfile using runtime-only dependencies are packaged for application. The existing development/test dependency set remains available separately.

**Prepared CI:** `.github/workflows/backend-ci.yml` checks for the duplicate root `env.py` and committed `.pyc` artifacts before running Ruff, MyPy, and the repository's existing pytest coverage gate on Python 3.12. The first run is intentionally allowed to reveal real pre-existing quality debt; failures will be repaired rather than hidden by weakening the gate.

**Connector boundary:** executable/build-control writes and deletions were blocked by the connected GitHub safety layer. Those changes were not forced. They were packaged as a non-destructive upload patch instead.

**Patch checksum:** `333_Phase_1_Integrity_Patch.zip` SHA-256 `f8239b3cd2390f6522d923d21a4366339dd6c77c0e06b2d82fa13aee50caa30f`.

**Next verified target:** apply and verify the Phase 1 patch, remove the three explicit stale/generated files, inspect the first CI run, and close Phase 1 before beginning the shared identity circuit.
