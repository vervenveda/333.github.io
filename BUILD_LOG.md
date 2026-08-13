# 333 Network — Systematic Build Log

**Purpose:** Preserve implementation decisions and verified milestones while the 333 Network is completed systematically.

> This repository is public. This log records only non-sensitive implementation facts. Credentials, private server topology, security secrets, internal administrative routes, and other restricted architecture belong in the private Sovereign Build Codex and are intentionally excluded here.

## Operating discipline

1. Work in small, reviewable phases.
2. Verify each major change before beginning the next.
3. Update this log after every major public-repository change.
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
- A duplicate root `env.py` exists alongside the Alembic migration environment and should be reviewed/removed if redundant.
- No GitHub Actions CI workflow was found protecting the committed backend tests.
- Production and development Python dependencies should be separated in the Docker build.
- Some environment variables anticipated by `.env.example` are not yet represented by runtime settings and should be wired only when their services are implemented.

## Phase plan

### Phase 1 — Repository integrity and baseline protection

Status: **IN PROGRESS**

Planned sequence:

1. Establish this build log.
2. Repair 333 PWA registration/update event contract.
3. Remove stale repository artifacts after verification.
4. Replace stale copied governance files with 333-specific versions.
5. Add CI for tests/lint/type/config validation.
6. Verify the complete Phase 1 diff before any broader architecture work.

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

**Next verified target:** repair the PWA registration/update event contract before touching broader backend behavior.
