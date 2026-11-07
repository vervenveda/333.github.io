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
