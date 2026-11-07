# 333 Network — Topology and STOS Boundary Codex

**Checkpoint:** 2026-11-07  
**Scope:** Source topology and regression contracts only.  
**Production modifications:** None.  
**STOS terminal commissioning:** None.  
**Fallback policy:** Preserve previously validated 333 source and the Verve N Veda directory recovery ZIP; do not restore older backups over newer changes without a file-by-file reconciliation.

## Purpose

333 Network has six native browser applications (HOLLO, KANSEE, E=Ven Mail, Bazaar Art Live, SIte, Bunya), plus FleaPit, which also has an internal 333 media gate/hub and an alternative ProReSources implementation. The frontend is local-first; existing FastAPI routers are source implementations whose live deployment has not been established.

The founder is creating a **dedicated STOS (Sovereign Terminal Operating System) service-hosting terminal for each 333 subsidiary**. No terminal slot numbers, privileges, host names, signing keys, transport credentials, production deployments, or commissioning receipts are defined here. STOS internals remain outside the public GitHub contract. STOS terminal commissioning is strictly deferred until separately authorized.

## D01 — First baseline contracts

- Contract: `architecture/333-topology-contract.v1.json`
- Tests: `tests/test_topology_contract.py`
- Contract commit: `8a48e12dbd4e9370e27d1a8cb07abed7624935c6`
- Regression-tests commit: `99dd500cf9da4448301f670f2a2bd834e1fa11dc`
- Source cross-check: **PASS** for 7 frontend paths, 7 backend router paths, backend router registration strings, each application in 333 service-worker precache, 4 existing route numbers, current external FleaPit link, and planned-uncommissioned STOS states.
- Tests defined: 6. Python runner execution: **not yet independently verified**. Browser interactions: **not tested**.
- Preserved unchanged at this checkpoint: `index.html`, `service-worker.js`, `app/main.py`, all application HTML and routers, browser storage, stored identity and data.

## Identity authority

HOLLO's `333_identity_handoff_v1` is a browser-local descriptive handoff, **not verified member authentication**. A future STOS terminal must require server-verifiable identity and scoped capability authorization at its own trusted boundary. No public browser storage can grant permissions to a STOS terminal.

## Route authority

| Route | Destination |
|---|---|
| 333-111-7777 | 333 gateway |
| 333-222-7777 | HOLLO |
| 333-333-7777 | KANSEE |
| 333-444-7777 | Bazaar Art Live |

Do not invent routes for E=Ven Mail, SIte, Bunya or FleaPit.

## FleaPit reconciliation is deliberately deferred

- 333 owns `app/FleaPit™_media_gate_Index.html` and `app/FleaPit™ _media_hub_index.html`; the PWA precaches both.
- ProReSources Hub owns `Protools/FleaPit™_media_hub_Index.html` and `Protools/FleaPit™ Protected Media Hub_index.html`.
- The current 333 directory card deliberately still links to the ProReSources landing page.
- Do not silently change canonical routes or migrate browser data across origins. Compare features, versions, backup formats, and existing user expectations before making a decision.

## Planned hardening sequence

1. **D01 complete at source level:** Establish a read-only topology contract and six drift-detection tests.
2. **D02:** Add independent negative tests for cross-member access, unauthenticated requests, browser handoff misuse, token/session revocation, and access-control boundaries. No activation.
3. **D03:** Read-only FleaPit source parity audit across 333 and ProReSources; designate canonical ownership only after data compatibility evidence.
4. **D04:** Test offline-cache completeness, update behavior, imported JSON validation, backups, and untrusted preview content. Prevent sensitive API responses from entering public offline caches.
5. **D05:** Build a backend/readiness matrix that explicitly differentiates source existence, test success, deployed API, and independently commissioned STOS terminal.

## Acceptance and rollback

- A new contract or test must not change a current public application, the main VNV directory, local-storage keys, or any STOS component.
- Rerun `python3 -m unittest discover -s tests -p "test_topology_contract.py" -v` using a local checkout or an approved read-only CI runner before claiming test execution.
- Revert individual additive commits only after confirming no subsequent additions depend on them.
- Never expose STOS secrets, internal administration, runtime authority objects, host/port inventories or commissioning details in the public repository.

## D02 — Member authority boundary and negative-contract baseline (2026-11-07)

**Scope:** New read-only regression tests and manually dispatched CI; no backend, browser, member, STOS, or administrative changes.

- Added `tests/test_identity_boundaries.py`: **nine** source-level guard tests, including token presence, verified UUID identity match, absent OHMIC fail-closed logic, self-scoped member profiles, sovereign dependencies, administrator role guard, legacy identity tracking, FleaPit CSRF fail-closed adapter, and unchanged route/STOS declarations.
- Added `.github/workflows/333-topology-boundary-audit.yml`: manual-only, `contents: read`, two stdlib unittest suites. This workflow is **not yet executed**; do not claim full test success.
- Source cross-check: verified that HOLLO, Bazaar, FleaPit and Bunya have `Depends(get_current_sovereign_member)`; routes remain intact.
- **Readiness finding D02-A (migration):** `app/routers/even_mail.py` and `app/routers/admin.py` use SQL-backed `get_current_user` and legacy role checks rather than the newer OHMIC sovereign-member verifier. Do not merge authorities, infer privilege equivalence or alter production authentication until a migration specification and negative runtime tests exist.
- **Readiness finding D02-B (fail-closed dependency):** FleaPit write endpoints depend on `require_fleapit_csrf`; its adapter imports `app.dependencies.sovereign_csrf`, which is not present in the inspected repository. The adapter intentionally responds with HTTP 503 when no verifier can be resolved. Determine the canonical authority in the secure environment before enabling writes; do not add a permissive fallback.
- All future STOS subsidiary terminals remain *planned-uncommissioned*, with no assigned IDs, no activated connectors, no distributed secrets, and no admin changes.
- Test commit: `6b47f7b5aae061c2abc737bf3ed07c71090817e2`
- Manual CI commit: `8aec76740d93aaeed2dc0ab067d71694f4b3a940`
- Next proposed evidence: actual isolated negative runtime tests for unauthenticated requests, cross-member access, role denial, revoked sessions and unavailable OHMIC; do not run against real user records.

### Runbook

From a clean local checkout, run `python3 -m unittest discover -s tests -p 'test_topology_contract.py' -v` and `python3 -m unittest discover -s tests -p 'test_identity_boundaries.py' -v`; or manually dispatch the read-only GitHub Actions workflow. Record the actual test logs and commit SHA. A source-level test passing does **not** establish deployed backend authorization correctness.

## D03 — FleaPit near-parity evidence checkpoint (2026-11-07)

- Added `architecture/fleapit-source-parity-checkpoint.md` with the four source-file Git blob IDs, two-line hub difference, nine-line landing difference, shared local storage markers, and current split between the 333 precache and ProReSources directory destination.
- The two media hub versions are near-identical but **not bit-for-bit identical**. Do not assume cross-origin storage migration or identical runtime behavior.
- The 333 hub has an introduction self-link inconsistent with its dedicated 333 landing. No route or link modification made.
- Commit: `011ce29db122adebff8cd6b73393b625e7e25db1`.
- Next: isolated data-schema and browser acceptance tests; no STOS commissioning or browser-record mutation.

## D04 — Offline cache and backup safety (2026-11-07)

**Status:** Changes committed and source-verified; live browser activation, Python/Node executions, and GitHub Actions test logs are not yet verified. No STOS commissioning, member-data import, or service activation.

### Commits
- `38438f8e6ef77208811f4e4935a995f0cc8c08cb`: Service-worker v8 runtime cache now explicitly limits eligible requests to approved public static resources. Excludes Authorization-bearing, query-bearing, off-scope, unknown navigation and sensitive-namespace requests; excludes private/no-store/no-cache, Set-Cookie, JSON, and event-stream responses. Previous cache generation is eligible for cleanup upon activation.
- `5dda87a9f7cf2dcc97b7222792cb61bed4d8630c`: Offline page now includes FleaPit as a seventh directory destination; wording acknowledges that precache success is necessary.
- `1c06241c0d27633a13ec4ff8ca4f8df572c19c5e`: Eight source-level offline and backup integrity tests.
- `fb68cd55c162c1faff019503778c8d6a1ea0a677`: Six mocked JavaScript service-worker cache policy tests.
- `d0d1814d67f17e689a5ecbaf96eed73c6534970e` and `4733e34ec9dd74c3e2c8c95f8a6c870eddb2a2c0`: Included both D04 test suites in manually dispatched, read-only CI.

### Preserved and unchanged
All seven application files, browser storage and profile data, the main gateway, backend routers, public routes, VNV master directory and STOS internals.

### Outstanding backup findings
- HOLLO and E=Ven Mail: 5 MB import caps and named schema checks.
- Bazaar Art Live: 150 MB maximum import; existing media store is cleared before all replacement media records are committed. Requires isolated failure/rollback testing before any change.
- Bunya: inspected JSON import has no explicit file-size cap before reading. Add a safe limit only after considering legacy backups and schema compatibility.
- FleaPit: 2 MB import cap and snapshot capabilities; identical storage identifiers do not permit cross-origin data sharing.

### Acceptance remaining
Run `python3 -m unittest discover -s tests -p 'test_offline_backup_boundaries.py' -v` and `node --test tests/service_worker_policy.test.mjs` using an approved read-only runner. Verify actual v7-to-v8 browser worker activation, public offline coverage, Cache Storage privacy exclusion, and synthetic backup rollback tests. No STOS slot is commissioned.

## D06 — Public-facing lower-page design refinement (2026-11-07)

**Commit:** `bb099ec42d5979ac157cb24293b1cd824947a561` — `index.html` only.

### Scope and preservation
- Refined Network Principles into three larger aligned cards, with 16 px supporting text and clear charcoal/navy/cream contrast.
- Refined the existing support panel to use the primary heading **Support Free Access**, paired with the established **Support the Network** Stripe action. The original contribution URL remains unchanged. The separately injected VNV support component was not edited.
- Replaced tiny current-build notice with **Network Service Status**, explicitly distinguishing available browser-local tools, capabilities requiring authenticated connected backends, and **planned/not-commissioned STOS hosting**.
- Refined footer typography, spacing, layout, and navigation; seven connected destinations now include FleaPit.
- Source structural checks: 11 balanced section tags; one canonical header mount; existing Stripe URL; one stylesheet pair; 3 principles and 3 status cards. Published-browser rendering, breakpoint behavior, click paths and PWA version interaction **not independently tested**.
- No changes to app HTML, registered routes, member storage, backend, service worker, shared VNV components, STOS terminals, administrative infrastructure or original directory fallback.

### Acceptance before extending this design
Review desktop/tablet/mobile screenshots, accessibility and contrast, location of globally injected Support Free Access component, footer-toolbar overlap, and donation link click-through. Keep the design scoped to 333 Network until validated.

## D07 — HOLLO workspace visual organization (2026-11-07)

**Visual change:** `0537e744d8e4254e072c3f9fd4f1d5c4c21a3e3a` in `app/HOLLO_333_direct_connect_index.html`. Baseline Git blob `70f8b27f4102e1cd98922e4197d95e5f231d0b2d`; updated blob `05071daea488ee084f74d87ca4cee7306b4fc945`.

- Original VNV ecosystem menu and ticker components retained. HOLLO-specific 333 navigation is now a compact expandable application selector containing its established links.
- My HOLLO Account clarifies local identity, provisional 333 numbers, and the existing enrollment/email/backup actions.
- Workspace Status condenses browser persistence, JSON backup, E=Ven handoff, and uncommissioned sync/signaling indicators without changing status values.
- Workspace CSS uses wider maximum layout, desktop proportions targeting 26/46/28 contacts/messages/studio, more readable 16 px text, balanced buttons, stronger charcoal/cream contrast, and tablet/mobile panel fallback.
- Contacts, direct dial, conversations, camera/mic preview, call controls, invitations, and activity use existing IDs and event handlers; descriptions and grouping are visual only.
- Explicit pre/post verification: 130 element IDs preserved, inline application script unchanged, six balanced section tags, two balanced details tags, one balanced main, and official support/ticker/toolbar scripts retained.
- No changes to message or invitation storage, credentials, member records, API endpoints, 333 numbers, modal event handlers, backup schema, STOS terminals or any other repository page.
- **Pending acceptance:** Browser rendering and behavior at wide desktop, 1024 px, 768 px and 390 px; account drop-down keyboard behavior, message controls, local camera preview, enrollment pop-up and backups. Source checks do not prove runtime success.
- Rollback: revert only the isolated HOLLO visual commit after checking for later source changes. Preserve user data and later approved commits.

