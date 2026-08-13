# 333 Network Roadmap

This roadmap tracks the staged development of the 333 Network and its connected applications. It is a planning document, not a promise of release dates. Each phase must preserve local-first operation, clear trust boundaries, portability, accessibility, and honest labeling of features that are still planned.

## Architectural roles

- **HOLLO** — shared member identity, profiles, internal 333 numbers, contacts, and direct communication.
- **KANSEE** — meeting rooms, invitations, conferencing, collaboration, and meeting records.
- **E=Ven Mail** — email applications, account approval, and future mailbox services.
- **Bazaar Art Live** — social feed, profiles, groups, events, media, and discovery.
- **SIte** — accessible website and application creation.
- **OHMIC Foundry** — build, deployment, hosting, releases, rollback, and portable project publishing.
- **Bunya** — infrastructure control plane for deployment, domains, DNS, TLS, monitoring, and backups.
- **333 Network** — shared identity, navigation, communication, community, and discovery layer connecting those services.

## Phase 1 — Repository integrity and baseline protection

**Status: reconciliation in progress**

- [x] Audit the current repository and backend structure.
- [x] Establish a public `BUILD_LOG.md` for sanitized technical milestones.
- [x] Prepare genuine 333 security, accessibility, privacy, roadmap, and changelog documents.
- [x] Specify and validate the service-worker registration event repair.
- [x] Identify accidental Python bytecode and duplicate root Alembic environment file.
- [x] Prepare `.dockerignore` and runtime-only production dependency set.
- [x] Prepare CI for repository hygiene, linting, typing, tests, and coverage.
- [ ] Apply the root-ready reconciliation package to the protected v2 branch.
- [ ] Remove the accidental literal `agent/333-integrity-foundation-v1/` folder from `main` only after its useful contents are reconciled.
- [ ] Run CI and repair real failures.
- [ ] Verify Phase 1 before merge.

## Phase 2 — Shared identity circuit

- [x] FastAPI authentication foundation.
- [x] Argon2 password hashing.
- [x] Access/refresh token support and refresh rotation.
- [x] HOLLO profile and internal 333-number backend foundation.
- [x] E=Ven application and administrative review foundation.
- [ ] Create one shared 333 API/session client for browser applications.
- [ ] Connect HOLLO to backend accounts while preserving local/offline fallback.
- [ ] Connect SIte, Bazaar, KANSEE, and E=Ven to the same authenticated identity.
- [ ] Define explicit session, logout, recovery, and cross-device synchronization behavior.

## Phase 3 — E=Ven application integration

Connect the E=Ven frontend to the existing application API, establish one canonical configured mail domain, enforce address reservation, expose administrator review state, and keep application approval distinct from mailbox provisioning.

## Phase 4 — KANSEE live conferencing

Add room API/access control, signed invitations, presence, WebSocket signaling, STUN/TURN, WebRTC media, an SFU strategy for multi-party rooms, synchronized collaboration state, and preserved microphone/camera consent/accessibility controls.

## Phase 5 — Bazaar Art Live synchronization

Add Bazaar profiles/social graph, posts/comments/reactions, groups/events, moderated media storage, notifications, saved content, and opt-in discovery cards for OHMIC-published sites.

## Phase 6 — SIte + OHMIC Foundry hosting

Treat SIte as the simple creator, define a versioned portable publish payload, implement OHMIC build jobs/releases, static hosting, free 333-hosted URLs, custom-domain support, TLS, aliases/redirects, rollback, exportability, and isolation of untrusted imported applications.

## Phase 7 — Bunya infrastructure control plane

Connect Bunya to OHMIC deployment status/releases, domain/DNS management, certificate status, object storage, backups, monitoring, and narrowly scoped provider adapters while keeping provider credentials server-side.

## Phase 8 — Communications infrastructure

Complete mailbox provisioning/delivery and optional external telecom bridges after identity, deployment, and control-plane foundations are stable.

## Phase 9 — Operations, telemetry, and reporting

Define privacy-minimized operational events and feed approved 333 operational statistics into the protected administrative reporting layer without exposing private administrative topology or credentials.

## Release gates

A feature should not be described as live until the relevant service exists and has been verified. Major releases should pass automated tests, lint/type checks, secret/configuration scanning, accessibility review, privacy/security review, backup/rollback checks where state changes are involved, frontend/backend contract validation, and documentation/changelog updates.
