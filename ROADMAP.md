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

**Status: in progress**

- [x] Audit the current repository and backend structure.
- [x] Establish a public `BUILD_LOG.md` for sanitized technical milestones.
- [x] Replace stale Polyglot security and accessibility documents on the working branch.
- [ ] Replace the remaining stale Polyglot privacy, roadmap, and changelog text.
- [ ] Correct the service-worker registration event mismatch.
- [ ] Remove accidental Python bytecode and duplicate Alembic root file from version control.
- [ ] Add `.dockerignore` and separate runtime from development dependencies in production images.
- [ ] Add continuous integration for tests, linting, type checking, and configuration checks.

## Phase 2 — Shared identity circuit

**Status: backend foundation exists; frontend integration pending**

- [x] FastAPI authentication foundation.
- [x] Argon2 password hashing.
- [x] access/refresh token support and refresh rotation.
- [x] HOLLO profile and internal 333-number backend foundation.
- [x] E=Ven application and administrative review foundation.
- [ ] Create one shared 333 API/session client for all browser applications.
- [ ] Connect HOLLO to backend accounts while preserving local/offline fallback.
- [ ] Connect SIte, Bazaar, KANSEE, and E=Ven to the same authenticated identity.
- [ ] Define explicit session, logout, recovery, and cross-device synchronization behavior.

## Phase 3 — E=Ven application integration

- [ ] Connect the E=Ven frontend to the existing application API.
- [ ] Establish one canonical configured mail domain.
- [ ] Enforce unique mailbox/address reservation before provisioning.
- [ ] Add administrator review state to the frontend.
- [ ] Keep application approval distinct from live mailbox provisioning.

## Phase 4 — KANSEE live conferencing

- [ ] Add KANSEE room API and access-control model.
- [ ] Add signed invitations and presence.
- [ ] Add WebSocket signaling.
- [ ] Configure STUN/TURN services.
- [ ] Add WebRTC media transport.
- [ ] Add an SFU strategy for multi-party rooms.
- [ ] Synchronize chat, agendas, notes, polls, tasks, and meeting records.
- [ ] Preserve explicit microphone/camera consent and accessibility controls.

## Phase 5 — Bazaar Art Live synchronization

- [ ] Add Bazaar profiles and social graph services.
- [ ] Add posts, comments, reactions, groups, and events.
- [ ] Add moderated media upload/storage.
- [ ] Add notifications and saved content.
- [ ] Add opt-in discovery cards for sites published through OHMIC Foundry.

## Phase 6 — SIte + OHMIC Foundry hosting

- [ ] Treat SIte as the simple public website/application builder.
- [ ] Define a versioned portable project/publish payload.
- [ ] Implement OHMIC build jobs and release records.
- [ ] Add static site hosting and free 333-hosted URLs.
- [ ] Add custom-domain support, TLS, aliases, redirects, and rollback.
- [ ] Preserve complete export so published sites do not depend on the editor.
- [ ] Sandbox untrusted imported applications by default.

## Phase 7 — Bunya infrastructure control plane

- [ ] Connect Bunya to OHMIC deployment status and releases.
- [ ] Add domain and DNS management through narrow provider adapters.
- [ ] Add certificate/TLS status.
- [ ] Add object-storage, backup, monitoring, and restore status.
- [ ] Keep provider credentials and administrative secrets server-side only.

## Phase 8 — E=Ven mailbox service and communications bridges

- [ ] Add mailbox provisioning only after identity and operational controls are stable.
- [ ] Configure SMTP plus IMAP/JMAP or an equivalent supported mailbox interface.
- [ ] Add SPF, DKIM, DMARC, abuse handling, quotas, and recovery procedures.
- [ ] Evaluate optional PSTN/SIP bridging separately from native 333 identity numbers.

## Phase 9 — Operations, telemetry, and reporting

- [ ] Define privacy-minimized operational events.
- [ ] Feed approved 333 operational statistics into the protected Sovereign Admin reporting layer.
- [ ] Track health, deployment failures, conferencing failures, mail failures, backup age, and abuse controls.
- [ ] Keep private administrative topology and credentials out of public repositories and browser code.

## Release gates

A feature should not be described as live until the relevant service exists and has been verified. Major releases should pass:

- automated tests;
- lint and type checks;
- secret/configuration scanning;
- accessibility review;
- privacy/security review;
- backup and rollback checks where state changes are involved;
- frontend/backend contract validation;
- documentation and changelog updates.
