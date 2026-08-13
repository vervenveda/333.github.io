# 333 Network — Systematic Build Log

**Purpose:** Preserve implementation decisions and verified milestones while the 333 Network is completed systematically.

> This repository is public. This log records only non-sensitive implementation facts. Credentials, private server topology, security secrets, internal administrative routes, and other restricted architecture are intentionally excluded.

## Operating discipline

1. Work in small, reviewable phases.
2. Verify each major change before beginning the next.
3. Update this log at regular checkpoints and after substantial repository milestones.
4. Preserve existing user-facing applications unless a migration is deliberate and reversible.
5. Never expose infrastructure or administrative secrets in browser code.
6. Preserve local-first/offline fallback where practical.
7. Keep 333 services specialized instead of duplicating the same system in several applications.

## Responsibility map

- **333 Network** — network experience and discovery.
- **HOLLO** — shared member identity and network identity.
- **E=Ven Mail** — mail application/provisioning surface.
- **KANSEE** — meetings and video conferencing.
- **Bazaar Art Live** — community/social/discovery feed.
- **SIte** — accessible website/application creation.
- **OHMIC Foundry** — build, deployment, hosting, releases, portable publication, and future URL/domain hosting.
- **Bunya** — infrastructure control and operational visibility for deployment, domains, DNS, certificates, monitoring, backups, and provider operations.

## Verified audit baseline — 2026-08-13

The repository already contains a substantial network foundation:

- FastAPI entry point;
- async SQLAlchemy/PostgreSQL foundation;
- Alembic migration environment;
- Redis-backed rate-limit foundation;
- authentication, profiles, HOLLO, E=Ven application, and administration routers;
- password hashing, token/session foundation, audit logging, and role checks;
- Docker deployment foundation;
- PWA/offline shell;
- HOLLO, KANSEE, E=Ven Mail, Bazaar Art Live, SIte, and Bunya browser applications.

### Confirmed service gaps

The FastAPI application declares KANSEE, Bazaar, SIte, Bunya, uploads, and notifications as service families, but those router implementations are not all present yet. Their browser applications therefore remain substantially local-first.

### Confirmed integrity findings

- The service-worker registration shim contains copied Polyglot naming and does not emit the update events already expected by the 333 gateway.
- Several governance files contain stale Polyglot text.
- `env.py` at repository root is an exact duplicate of `migrations/env.py`.
- Two generated `.pyc` files are committed under `app/_pychache_/`.
- CI was not present to protect tests/lint/type/config checks.
- The production Docker image currently installs development/test dependencies from the combined requirements file.

## Phase plan

### Phase 1 — Repository integrity and baseline protection

**Status: RECONCILIATION PACKAGE PREPARED; NOT YET CLOSED**

- [x] Audit current repository/backend structure.
- [x] Establish sanitized build log.
- [x] Prepare genuine 333 governance documents.
- [x] Validate PWA event-contract repair and next cache generation.
- [x] Verify duplicate/generated cleanup targets.
- [x] Prepare runtime-only dependency file and Docker hardening.
- [x] Prepare first CI workflow.
- [x] Create protected branch `agent/333-integrity-foundation-v2` from current `main` after an upload-path mistake was detected.
- [x] Rebuild Phase 1 as a root-ready package with no enclosing patch directory.
- [ ] Apply root-ready package to v2.
- [ ] Remove the three verified stale/generated root artifacts on v2.
- [ ] Run and repair CI.
- [ ] Verify complete Phase 1 diff.
- [ ] Merge only after verification.

### Phase 2 — Shared identity circuit

Wire the public applications to one shared authenticated 333 client while retaining bounded local/offline fallback.

### Phase 3 — E=Ven application circuit

Connect the E=Ven frontend to the existing application/review API and establish canonical mail-domain configuration. Mail delivery/provisioning remains a later infrastructure phase.

### Phase 4 — KANSEE live conferencing

Implement room API, ACLs, invitations, signaling, presence, STUN/TURN integration, WebRTC/SFU strategy, synchronized collaboration data, and meeting records.

### Phase 5 — Bazaar Art Live service

Implement profiles, posts, groups/events, media, notifications, moderation, and optional OHMIC-published-site discovery cards.

### Phase 6 — OHMIC Foundry deployment and hosting

Implement project/build/release/deployment contracts, static hosting, stable free 333 URLs, custom-domain routing, TLS, storage, version history, and rollback while preserving portable exports.

### Phase 7 — Bunya infrastructure control plane

Connect deployment state, domains/DNS, certificates, monitoring, backup status, and narrowly scoped provider operations without placing provider secrets in frontend JavaScript.

### Phase 8 — Communications infrastructure

Complete mailbox provisioning/delivery and optional external telecom bridges after identity, deployment, and control-plane foundations are stable.

### Phase 9 — Operational reporting

Feed safe structured 333 operational events into the protected administrative reporting layer without storing private message contents as routine analytics.

---

## Change records

### Log 001 — Baseline protection — 2026-08-13

**Decision:** All substantial 333 work proceeds in small, verified phases.

**Decision:** OHMIC Foundry is the deployment/hosting engine rather than a duplicate hosting stack inside the 333 frontend repository.

**Decision:** Roles remain: 333 = network; HOLLO = identity; SIte = creation; OHMIC = hosting/deployment; Bunya = infrastructure control; Bazaar = discovery/community; KANSEE = meetings; E=Ven = mail.

### Log 002 — Phase 1 integrity preparation — 2026-08-13

Prepared and syntax-checked the corrected service-worker registration bridge and service worker. Verified that the gateway expects `333-app-update-ready` and `333-service-worker-controller-changed`. Prepared genuine 333 privacy/changelog/security/accessibility/roadmap documents, runtime-only Docker requirements, `.dockerignore`, and CI.

Verified deliberate cleanup targets:

- root `env.py` — exact duplicate of `migrations/env.py`;
- `app/_pychache_/__init__.cpython-313.pyc`;
- `app/_pychache_/main.cpython-313.pyc`.

`migrations/env.py`, `app/__init__.py`, and `app/main.py` must remain.

### Log 003 — Upload-path reconciliation — 2026-08-13

The first Phase 1 ZIP contained a top-level `333_Phase_1_Integrity_Patch/` directory. When uploaded through GitHub's web interface, its contents were preserved under a literal `agent/333-integrity-foundation-v1/` repository folder instead of replacing root files.

**Impact:** no intended root runtime file was overwritten. The mistake created additional files/folders only, so recovery is non-destructive.

**Recovery:** created fresh protected branch `agent/333-integrity-foundation-v2` from the latest `main`. Rebuilt the Phase 1 package so files exist directly at ZIP root, eliminating the enclosing-folder ambiguity.

**Scope guard:** this Phase 1 work does not modify the separate Admin security architecture.

**Next gate:** apply the root-ready package to v2, remove only the three verified stale/generated files, run CI, inspect every resulting diff, and close Phase 1 before beginning shared identity integration.
