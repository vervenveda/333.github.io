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

## D08 — HOLLO Data Integrity, Identity, Media and Accessibility (2026-11-07)

### Scope / preservation
- Public file: `app/HOLLO_333_direct_connect_index.html` only, plus additive synthetic test and manual workflow entry.
- HOLLO's prior baseline Git blob: `05071daea488ee084f74d87ca4cee7306b4fc945`.
- Current hardened Git blob (post-D08): `fb4fe26598d252cb9c06592f5b00e68456e05f5d`.
- Future STOS service terminal remains **planned and uncommissioned**. No backend authority, database, identity service, live member records, browser storage, other subsidiary, or Verve N Veda master gateway touched.

### Source modifications
1. `91801b814f6f03464870103033cada89ee29f707`: Backup import stages/normalizes the candidate, requires available persistent browser storage, writes and verifies the stored bytes, restores the original workspace and handoff when commit fails, and reserves success messaging for a confirmed restore. Does not claim multi-key atomicity or guarantee recovery if browser storage itself becomes nonfunctional.
2. Same commit: Normalize imported invitation and activity fields, limit unsafe values, non-actionable unknown/missing-contact invitations, restrict mobile view and invitation-tab settings, and prevent locally imported profile/enrollment flags from becoming verified account authority. Historical completed profiles remain locally usable.
3. `2fd005cb1532b81b5ec9904a59efd62688ff65a5`: Media-permission request revision invalidation guards against delayed camera/microphone capture after cancellation, device switching, or page hiding. Stale tracks are stopped. Harden modal focus visibility checks, fallback focus, focus containment, and Escape handling.
4. `b57c6a38328f3a8b1a2d8f28097e7f3c59f1a752`: Link all four mobile tab controls to corresponding panels and maintain active tab focusability; enlarge enrollment, backup, and modal instructions to 16px while retaining existing form steps and actions.
5. `accfba8fe6e6af141c7dda78e1f08ba74dd68980`: Nine synthetic Node.js tests in `tests/hollo_hardening.test.mjs`.
6. `8701e7a8bb6023982065e23c4f65467b2767f469`: Manual, contents-read 333 audit workflow includes the HOLLO suite.

### Verification actually performed
- Source fetched from current main; all five inline `script` elements parsed, including the 69K-character main script.
- 134 unique HTML IDs; no duplicates and no missing direct `$('#id')` references.
- Balanced: 6 section, 2 details, 1 main, 3 nav, 2 style tags.
- In isolated JavaScript engine, executed actual extracted `importBackup()` with synthetic valid, quota-failure, handoff-failure, readback-failure, cancelled, and storage-unavailable cases. All six preserved the expected in-memory state and showed non-success status on failed/cancelled paths. A deliberately permanently corrupted readback mock does not prove storage rollback when the browser can no longer read accurate bytes.
- Actual extracted normalization functions rejected unknown/missing-contact actionable invitations and sanitized activity records.
- Actual extracted media-preview function refused a delayed stale permission result and stopped the returned test track.
- Source and isolated VM checks are **not** equivalent to running the full Node suite in GitHub Actions or testing a real browser.

### Remaining acceptance gates / hardening candidates
- Run manual GitHub Actions `333-topology-boundary-audit.yml` and save the actual Python and Node logs.
- In a browser test profile with synthetic data only: verify backup replacement, recovery from quota exhaustion, correct legacy backup loading, reset behavior, media permission denial, tab keyboard navigation, modal focus return, and viewport widths 390/768/1024/1440 px.
- Browser storage is not a durable multi-key transaction. If both the replacement write and attempted rollback fail, HOLLO warns rather than falsely reporting recovery; provide separate downloadable backup before migration.
- STOS integration requires independent authenticated member verification, consent, scoped capabilities, and controlled commissioning. Browser-local `333_identity_handoff_v1` never grants terminal authority.

### Rollback
Revert the isolated D08 HOLLO commits in reverse order only after checking later dependencies; preserve valid newer user data, the D07 visual work, other 333 pages and all STOS infrastructure. The prior HOLLO blob above is a documented source checkpoint, not authorization to overwrite unrelated changes.

## D09 — HOLLO Three More Preservation Bubbles (2026-11-07)

**Future STOS service terminal:** planned and uncommissioned. Terminal number deliberately not assigned. No runtime binding, privileged authority, port, secret, key, live database or administrator changes.

### Upgrade 1 — Safe import structure and authority
Commit `d7dc0926682acf01657c158f4fd04ca04d70f67c`: Reject malformed import object/array shapes; validate contact IDs and block prototype-named contact/thread keys; use a null-prototype thread dictionary; constrain message metadata; preserve valid legacy orphaned threads; prevent imported sync metadata from granting remote authority. Original keys, routes and media/application features retained.

### Upgrade 2 — Verified reset with restoration attempt
Commits `8024708e4707439c48d65d31c43171017b79f295` and `f36cb958d8533d26350b3322d5ea61730fc829ae`: Reset now snapshots both existing workspace and handoff records, aborts if snapshot cannot be read, verifies the new workspace and handoff removal, and attempts to restore both prior records on failure. Success notification is reserved for a verified change. This is **not** a true transaction; recovery can fail when browser storage itself stops functioning.

### Upgrade 3 — Eliminate automatic background overwrites
Commit `c9113a4455dac75f1e815e923e895ac1b5146e24`: Preserve media cleanup during pagehide and visibility changes while removing redundant automatic saveState calls that could overwrite a newer tab's workspace. A storage event from another HOLLO tab reloads valid changed records and announces the change; a removed record prompts the user to reload. Concurrent deliberate edits can still conflict; complete multi-tab merging or revision CAS is not implemented.

### Tests and source verification
- `tests/hollo_three_bubbles.test.mjs` commit `2807a5bb004ca74827d934d49de04443133d4e5e`: Synthetic Node regressions for five reset scenarios, imported trust boundaries, automatic-save behavior, and STOS dormancy.
- Manual read-only workflow `.github/workflows/333-topology-boundary-audit.yml` extended in `ff6670f1295f5b13a987e4f913f2f43e21f493e7`.
- Independently executed in isolated JavaScript using the **actual extracted resetApp function** with synthetic records: success, quota failure, snapshot read failure, failed write/readback, and handoff removal failure. All five preserved the expected old state on failure; test records were not real user data.
- GitHub Actions / complete Node module suite **not yet executed or verified**. Full browser, viewport, keyboard, offline and multi-tab regression tests remain pending.
- 333 Network gateway, all other subsidiaries, master VNV directory, STOS and protected admin systems were not modified.

### Rollback
Pre-D09 hardened HOLLO Git blob: `fb4fe26598d252cb9c06592f5b00e68456e05f5d`. Roll back only isolated HOLLO source commits after checking for later edits; preserve actual user records and the D08 recovery improvements. Never overwrite the previously validated directory recovery ZIP.

## D10 — HOLLO entrance and status visual refinement (2026-11-07)

**Commit:** `3cbd8de01bf74abe9d4d9a60348c214bdc01e6a4` — scoped to `app/HOLLO_333_direct_connect_index.html`.

### Five agreed improvements
1. Keep official Verve N Veda global header/ticker and existing HOLLO application menu; refine HOLLO's local breadcrumb row and compact application selector rather than duplicate or replace the shared header.
2. Reorganize **My HOLLO Account** into clear introductory identity text, a stable local profile chip, and a symmetrical full-width three-action row (Enrollment & Profile, E=Ven Mail, Settings & Backup). Retain all original click targets.
3. Convert **Workspace Status** into a readable two-by-two local/connected service dashboard with expandable full privacy/architecture explanation. Status is descriptive, not proof of service deployment.
4. Tighten hero spacing and align the clear internal 333-222-7777 route card; do not misrepresent this as a public telephone number.
5. Increase scroll and footer clearance so the official fixed floating toolbar does not permanently hide bottom-of-page content. The shared toolbar itself remains unchanged. Actual overlay acceptance needs screenshots across desktop/tablet/mobile.

### Verified source invariants
- Git blob after commit: `08c6f1a6f07a075815d15c1dd84e89ad9edb820e`.
- 134 existing IDs preserved with zero duplicate IDs. Five inline JavaScript blocks parse. Inline application JavaScript remains byte-for-byte unchanged relative to pre-D10.
- Balanced 2 styles, 6 sections, 1 main, 3 details, 3 nav structures.
- Enrollment, identity, message form, contacts, studio, backup controls, shared ticker and ecosystem toolbar remain present.
- No contact data, local storage, route numbers, backend, donation link, 333 gateway, VNV master site, or STOS runtime touched.
- Dedicated HOLLO STOS terminal remains **planned/uncommissioned, number unassigned**.

### Remaining visual acceptance
Review in-browser desktop at 1440 and 1024 px, tablet 768 px and mobile 390 px; inspect dropdown keyboard operation, disclosure interaction, account button wrapping, status-label contrast, right-side toolbar overlay while scrolling, and the media studio controls. Source checks are not visual or behavioral confirmation.

## D11 — HOLLO canonical blueprint and relic-chrome cleanup (2026-11-07)

**Reference:** Founder-supplied `Verve N Veda & Khaemenes Academy — Canonical Page Architecture & Design Blueprint, v1.0`, especially pages 1–3 (one canonical header, two distinct tickers, one official toolbar, typography), page 6 (shared menu and toolbar), page 7 (ticker contract), and page 8 (surgical acceptance protocol).

### Why
Founder screenshot showed two ecosystem navigations and top support/menu relic, while the official fixed 3×2 toolbar overlaid the lower-right HOLLO Workspace Status card. D10's added scroll padding did not prevent content from sitting beneath the fixed dock.

### Surgical source change
- `df1b4324b9ce6c560bfea55f595528d0851586c2`: removed hand-built `vnv-global-strip` and `vnv-global-ecosystem-shell` CSS and the older `vnv-support.js` loader (which could add another menu and support banner).
- Added one `vnv-header-autopopulate.js` mount, the canonical `vnv-333-ticker.js` and one `vnv-ticker-autopopulate.js`, and retained the one official `vnv-ecosystem-toolbar.js`.
- Preserved old handmade header's useful `Ecosystem Directory`, `Directory AGI`, `Public Cloud` routes by adding them to the existing HOLLO 333 applications dropdown. The original 333 donation destination remains accessible through the dropdown and footer.
- Added page-local status layout right-side dock-safe padding at laptop widths, and bottom clearance at narrow widths. The official toolbar source itself is untouched.
- Before blob `08c6f1a6f07a075815d15c1dd84e89ad9edb820e`; after blob `9cbb8059634f9801815e67a52782555aef99404b`.
- HOLLO's 72,636-character application JavaScript block is byte-for-byte unchanged, and its 133 remaining application element IDs have no duplicates. The one removed ID belonged to the retired header's CSS `<style>` element. Six sections, one main, two details, two navs and one style tag are balanced.
- `4fcca1c321c4295dd8ff77b5983f204e86fa57e1`: six stdlib Node test cases in `tests/hollo_blueprint_chrome.test.mjs` for the component contract, navigation preservation, account/control IDs, dock-safe rail and dormant STOS.
- `399ed9f79b24cce588d01a94bb8d225beed9bd2a`: registered the tests in manual-only GitHub Actions.

### Outstanding acceptance
Actual browser visual inspection is still required after publication at desktop/tablet/mobile widths. Confirm exactly one **rendered** canonical header and two distinct tickers, reliable enriched hamburger, no support/menu duplication, the toolbar not masking status cards at the screenshot viewport, and that footer support links function. Source presence is not runtime evidence. The old global support banner is intentionally retired on HOLLO; the existing donation destination remains available by intentional local links.

**No modifications:** Protected Verve N Veda homepage, HOLLO accounts, messages, enrollment, storage keys, backup format, service worker, backend, or STOS terminals. HOLLO's STOS slot remains unassigned/uncommissioned.

### Rollback protocol
If the new canonical header cannot render, revert only the D11 `index`-equivalent HOLLO source commit, not previous D07-D10 application hardening or global shared assets. Confirm no subsequent page edits first.

## D12 — HOLLO family integration and shared-component order (2026-11-07)

**Intent:** Help HOLLO belong visually and functionally to the Verve N Veda family while retaining its independent navy/cream identity, local 333 navigation, offline data, enrolled profiles, messaging and video features.

### Baseline verification
- Examined protected `vervenveda/vervenveda.github.io/index.html`: native 333 ticker, institutional site header, enriched branched hamburger and native shared toolbar entry. Did **not** change homepage.
- Examined canonical reusable sources: `assets/vnv-header-autopopulate.js`, `assets/vnv-333-ticker.js`, `assets/vnv-ticker-autopopulate.js`, `assets/vnv-ecosystem-toolbar.js`.
- Critical dependency detail: 333 ticker mounts on `DOMContentLoaded` while the header computes a sticky offset and attaches resize observers to tickers **when mounted**. Previous HOLLO source invoked header mount before ticker existence; this could leave an incorrect header offset.

### Surgical changes
- `2548cee48632905ffa68bda6e77a88ab155c2366`: reorder ticker scripts and defer shared header mount until after 333 ticker `DOMContentLoaded` mount; AutoPopulate inserts one HOLLO ticker before the page's own breadcrumb. Preserve exactly one canonical header, the two specified tickers, and one official toolbar. Keep HOLLO-specific navy breadcrumb and application dropdown.
- Same commit: add understated familial header accent and breadcrumb border; reserve **up to 510px** beside Workspace Status at laptop widths because the official toolbar can be 480px wide (the previous 300px buffer was insufficient). Keep untouched toolbar source.
- `f11ba9e04db2adaccbd8b96b647adba73ac627bb`: explicit HOLLO ticker links to avoid relying on collapsed dropdown visibility.
- `3424cd0602e06005b3fd966fbd0dac8ff25e857f`: correct local ticker entry to validated `#holloWorkspace` rather than an unenforced `#enroll` anchor.

### Verification and constraints
- Original HOLLO inline application JavaScript (72,653 characters) **unchanged**; 133 source IDs preserved; all inline script blocks parsed before committing.
- Retired handwritten header and duplicate support loader remain absent. 333 application routes and contribution link remain unchanged.
- Protected homepage, other 333 apps, user data, STOS internals, administrator systems and terminal commissioning untouched.
- **Outstanding:** test actual rendered header offsets, ticker pause controls, 333 hamburger branching, layout-safe toolbar clearance at 1440/1160/1024/768/390 CSS px, and local HOLLO dropdown; source checks alone do not prove visual compatibility.
- HOLLO STOS terminal remains `planned-uncommissioned` and **number unassigned**.

## D13 — KANSEE conferencing integrity and family integration (2026-11-07)

**Scope:** Frontend-only KANSEE source changes, one additive test suite, and the existing manually triggered source-contract workflow. No changes to `app/routers/kansee.py`, other subsidiaries, the protected VNV homepage, live browser/member data, or STOS control surfaces. Future dedicated KANSEE STOS service terminal remains **planned-uncommissioned; number not assigned**.

### Baseline and commits
- Baseline KANSEE Git blob: `7f6597d06573115e73ca3eaad49316609463eebe`.
- `abb26dcbf56522c03756c67ee23c0d98e1a2ec44`: normalize imported profile, sync metadata, meeting participants/chat and collaborative local records; prevent local/HOLLO numberVerification flags from asserting backend identity; prevent prototype-key insertion into imported collaboration dictionaries.
- `ce393eed6d069a8b6c1bffcb350fe8ad36668796`: bound JSON backup import at 5MB; validate shape/schema; stage changes; verify persistent storage bytes and attempt previous-record rollback on failures; do not stop active media before backup commit is confirmed.
- `5e598b6d5f6c0de9eb973ea33c9ba0332f19fc1e`: add request-revision guards to camera/microphone and screen share and stop stale captures when a room changes or the page hides; media cleanup on hide/page exit.
- `2d6ce9fd31d0672774d734138e2382c73fa9bf27`: remove handwritten VNV global strip and legacy `vnv-support.js` loader; integrate approved shared header, 333 ticker, KANSEE Quick Links ticker and official toolbar. Preserve KANSEE teal/navy/gold styling, locally scoped dropdown, existing 333 app routes and original Stripe support destination.
- `f1d8d4915e4c86680026d3453f0598c49ecb39a1`: handle interruption of pending previews when screen sharing changes.
- `b347078cd0a681eb8cf48665ba5869d1883b95e2`: add `tests/kansee_hardening.test.mjs` with synthetic restore failures and source-boundary tests.
- `2aaff35b85afa13a23a292735841692d83e147cf`: include suite in `.github/workflows/333-topology-boundary-audit.yml`, manual-only with contents-read permission.

### Verified
- Executed actual extracted `importWorkspace()` in isolated JavaScript with synthetic records for successful write, quota denial, failed write readback, unreadable old storage and cancellation. **Five of five behaved as expected**: previous state and stored records preserved on failed/cancelled restores, successful backup only reported after readback, and media stopped only after confirmed commit.
- All in-page script blocks parse; KANSEE control IDs retained (only ID of discarded legacy stylesheet removed).
- No remote conferencing activation, network delivery, authentication change, public STOS routing, terminal number assignment, or privileged service assertion.
- Source tests and isolated harnesses are **not** a substitute for GitHub Actions logs or real-browser media/permission/layout acceptance.

### Outstanding acceptance
- Run the existing manual `333-topology-boundary-audit.yml` and preserve the actual Node test logs; not yet verified by the runner.
- Test camera/mic permission denial, audio-only/video-only fallback, late permission results after navigation, screen-share stop and browser hide in a synthetic browser profile.
- Test KANSEE identity handoff, older locally saved rooms, imported backup compatibility, all eight collaboration panels, room creation and joining, lobby demonstrations, chat, export and user-visible status.
- Validate the canonical header, enriched menu, two ticker stack and toolbar overlap at desktop/tablet/mobile sizes.
- The browser remains a local simulation. Real guest participants, authenticated remote delivery, WebRTC media server/SFU, TURN, secure session authority and the future sovereign STOS terminal are **not provisioned by these commits**.
- Browser localStorage has no atomic multi-key transaction; a permanently unusable browser storage subsystem can defeat rollback. Recommend independent backup export before restoring valuable data.

### Rollback
Revert these isolated KANSEE changes only after confirming no later dependent modifications. Preserve the HOLLO D07–D12 changes, 333 directory gateway, validated fallback ZIP, current browser data and future unassigned STOS terminal status.

### D13 final readiness addendum
- `afa956c2c42a6ae21cecb92701b017e425b6bbb1`: replace unverified browser-adapter "network connected" claim with explicitly **unverified adapter status**, and clarify that copied local room links are not authenticated live conferences.
- Final frontend Git blob: `e043fd41ca67b6ebbc95c429cb35f50d4f6ac5f1`.
- Final read-only source verification: 124 unique application IDs (no duplicates), 110 directly referenced ID targets found, 7 inline scripts parse, 14 sections/3 navs/1 main/1 style/1 header/1 footer/1 details balanced, exactly one canonical header / 333 ticker / KANSEE ticker / official toolbar, legacy header/support loader absent.
- Isolated actual-function media test: delayed camera and screen-share results were rejected after cancellation and both stale synthetic tracks were stopped. No real device was accessed.
- GitHub Actions still needs a manual run; future STOS terminal number remains unassigned.

## D14 — KANSEE conference gallery, breathing room and blueprint alignment (2026-11-07)

**Source standard:** Founder-provided `Verve N Veda & Khaemenes Academy — Canonical Page Architecture & Design Blueprint v1.0`: one canonical header, two tickers, one dock, centered hero, 16px minimum interactive typography, generous responsive spacing, no hidden content, and independent thematic character. Protected VNV gateway is unchanged.

### Implemented
- `85f776af037cdcc09f3c8ead479aab250c87c449`: visual-only refinement to `app/KANSEE_333_meeting_rooms_index.html`. Maximum application width increased from 1221px to 1700px, meeting stage promoted, desktop rail layout given more breathing room, and tablet/mobile layouts improved. Teal/navy/gold and cream/parchment retained.
- Stage is explicitly count-aware without changing participant records: one tile expands, two arrange side-by-side, three/four use two columns, five through nine use three columns where space permits, ten through sixteen use four columns on extra-wide screens and fewer columns at smaller breakpoints. Smaller viewports scroll rather than clip. Data count is set by `renderStage()` only.
- Strengthened typography for panel headings, controls, participant labels, chat, meeting metadata, and instructional text to 16px or more where overridden by the D14 scoped style; 7px corners and symmetric button spacing.
- Existing meeting controls, IDs, enrollment handoff, chat, media permissions, waiting room, collaborators, backup schema and STOS integrations remain unchanged.
- The existing local demo limit remains **16 participants**. Tiles for demonstration guests are avatars and labels; only the local user camera/screen stream can show local real media. No remote WebRTC media is commissioned by this change.
- `b04c2b27dea2943bb425a45e04a4cdef4cfd59a4`: five Node source-contract tests in `tests/kansee_gallery_layout.test.mjs` verify adaptive grid, 16-person simulation boundary, preserved controls, typography, and shared chrome.
- `45a1998cb4c7804e8a3cd890a809560493ce1525`: adds the gallery checks to the manual-only, contents-read `333-topology-boundary-audit.yml` workflow.

### Evidence and acceptance limits
- Source verification checked 124 existing IDs unchanged and all inline scripts parsed before the visual commit.
- This is a **visual layout enhancement**, not live video-conference infrastructure. Browser rendering at 390/768/1024/1440/1920px and 1/2/4/9/16 synthetic participants is still pending.
- Need manual keyboard, screen-reader, camera permission, grid overflow, screen share, toolbar clearance and real device testing. Test suite committed but not independently confirmed running through GitHub Actions.
- Future dedicated KANSEE STOS terminal remains **planned-uncommissioned and number unassigned**.

### Rollback
Revert only the D14 KANSEE display commit after checking later modifications. Do not roll back D13 data integrity or other 333 subsidiaries; preserve the founder's verified recovery ZIP.

## D15 — KANSEE meeting-first stage and Focus Mode (2026-11-07)

**Request:** Align KANSEE with VNV blueprint while preserving KANSEE's private, local-first conferencing character; expand the meeting stage, compact the entrance, refine controls, add Focus Mode, and improve responsive legibility.

### Source and commits
- `94d88465cf4ed4f1c07556f76ced6631768be615`: `app/KANSEE_333_meeting_rooms_index.html` only. Baseline Git blob `199608045cfb240dea36503f6507d3c42b80e530`; updated blob `01e3ab76aad690dfee7563cbb24d7034bf5664e9`.
- Desktop meeting-first stage uses proportional rails (approximately 18% Rooms / 62% Meeting Stage / 20% Meeting Console when wide enough); responsive breakpoints place the console below at intermediate widths and retain the pre-existing mobile tabs at narrow widths. Container maximum 1820px. Keep KANSEE navy/teal/gold/parchment theme.
- Hero explanatory sentence shortened but still states that live remote conferencing requires a verified service. Original number/route card, HOLLO profile and network status controls unchanged.
- Conversation Continuity / Connection & Privacy Status preserved intact under a keyboard-operable `<details>` disclosure. Local network status remains visible even when disclosure is closed.
- Six pre-existing media/stage controls preserved and refined for consistent 44px minimum height, 16px labels, charcoal/cream contrast and visibly distinct Leave.
- Added `stageFocusBtn` to existing Meeting Room panel. Native `requestFullscreen()` is used when available, with CSS-only local fallback; Escape and button toggle leave Focus Mode. Gallery, chat, participants, current room, media tracks and storage remain the same objects and handlers. Focus Mode never activates microphone/camera or remote connections.
- `565c37e8184ed77905ce8787672e7824b9dca64a`: added ten static and synthetic Focus Mode tests in `tests/kansee_focus_mode.test.mjs`.
- `a81a9025edc45e3e87ba5903d8cb203f97920472`: included tests in the manual-only, contents-read `333-topology-boundary-audit.yml`.

### Evidence and limitations
- Fetched new source from GitHub and verified 125 unique element IDs (124 existing + 1 new), no duplicates; all seven inline JavaScript blocks parse; 14 sections, 3 navs, 1 main, 1 style, 2 details, 1 header and 1 footer balanced.
- In isolated JavaScript with mocked fullscreen requests, actual extracted Focus Mode handlers successfully entered and exited native full screen, updating `aria-pressed` and the button label. No real camera, browser profile, network service, or STOS action involved.
- Source checks found all 16 regular-expression anchors required by the additive Focus Mode test file. **Complete Node suite and live visual/browser behavior have not been verified.**
- Outstanding acceptance: desktop widths 1440/1920, laptop 1024/1280, tablet 768, mobile 390, both supported native fullscreen and unsupported/denied fallback, Escape, permission and focus, 1/2/4/9/16 synthetic guests, scroll behavior and VNV floating toolbar overlay.
- This preserves **16 locally demonstrated participant tiles**; there is no claim of a live 16-feed WebRTC conference. Authenticated backends and STOS terminal remain **uncommissioned and unassigned**.

### Rollback
Revert only the D15 KANSEE source commit if layout/fullscreen browser acceptance fails, after checking subsequent changes. Keep earlier D13 security, D14 gallery adaptations, all HOLLO work, the protected gateway and the founder's verified fallback ZIP unchanged.

## D16 — E=Ven Mail readability and canonical family integration (2026-11-07)

**Request:** Give the E=Ven Mail local-first correspondence application visual TLC while preserving its distinct navy/parchment/rose/violet identity, existing mail controls, HOLLO handoff, applications, drafts and the legacy healthy fallback ZIP.

### Baseline and commits
- Baseline Git blob `f426a8d6ec7e1e9c1b86fe6ce16ee4f027193948`, `app/EVen_mail_index.html`.
- `bfd1b7f7eba207942d0fc149374b7d102082f843`: replace handwritten VNV global strip and duplicate `vnv-support.js` with one canonical header, 333 ticker, E=Ven Quick Links ticker, and official floating toolbar. Retain **E=Ven-specific mail search / identity / apply / settings header**, which is a separate application toolbar, not a duplicate ecosystem header.
- Same commit: override earlier 9–12px compressed labels with 16px readable text, 44–48px touch targets, 7px corners, updated 1760px maximum layout, generous three-pane inbox/folders/reader proportions, balanced mailbox and identity sections, and clearer contrast. All original mail application JS preserved byte-for-byte.
- `1380de7ede2f6838518e47fe7c2d096baa15f5a2`: preserve existing `reader.mobile-open` JavaScript behavior with matching mobile CSS, including overlay/close behavior at narrow screen widths.
- `720e8ebf0e87184838023bf9a1d7c747d0817741`: introduce six source contract tests in `tests/even_mail_blueprint.test.mjs`. `db7b28831030fbf5f89113b88a83889c09cd4076`: correct a test assertion that referenced a nonexistent static folder element ID (folders are dynamically rendered). `a10f6d040b154617ec0d5407185c696d8a1bc469`: register the suite in the manual-only, contents-read 333 source audit workflow.

### Preservation checks
- Current mail frontend blob `5eb8ba2d6544953e31e93826c97e1c3d03ac3f28`.
- 74 surviving application and modal IDs; **no duplicates**, no missing direct selector targets. The sole removed ID belonged to the retired header CSS `<style>`.
- Seven inline JavaScript blocks pass source syntax checks; 4 sections, 1 main, 3 nav, 4 header, 3 footer and 1 style structures balanced in source.
- Exactly one canonical shared header script, one 333 ticker, one E=Ven Quick Links ticker, and one official toolbar; legacy duplicate support/global header absent.
- Canonical VNV homepage, other 333 apps, HOLLO identity files, messages, browser storage, backend/router and STOS not modified. Future E=Ven terminal remains **planned/uncommissioned, slot unassigned**.

### Important operational boundaries and acceptance
- Current app is still **local applications and drafts**. No real SMTP mail service, provisioning, mailbox account approval, multi-device communication or verified network service has been activated.
- CSS/readability checks are source-level, **not a live browser screenshot test**. Browser widths 390/768/1024/1440/1920, keyboard menu/search/draft/reader toggle, mail reader focus/close, legacy demo messages, identity handoff, floating toolbar clearance and zoom should be tested with synthetic records.
- Chrome screenshot appears to use a substantially reduced effective page scale; verify browser zoom at 100% independently. Never claim CSS alone addresses browser zoom.
- Run manual `333-topology-boundary-audit.yml` and examine actual Node logs. Tests are committed, but the full runner has not been observed here.

### Rollback
If visual acceptance fails, revert the two D16 E=Ven Mail page commits after checking intervening edits; do not revert previously validated HOLLO/KANSEE hardening, global VNV assets or historical fallback archives.

## D17 — E=Ven Mail centered charcoal-and-cream refinement (2026-11-07)

**Founder's acceptance direction:** Reduce gold to a restrained accent; emphasize light cream, ivory and charcoal; center the E=Ven-specific second application header, balance search/actions, calm the HOLLO identity ribbon, unify sidebar controls and make the three-pane mailbox more symmetrical. Keep independent E=Ven Mail identity; official VNV header, two tickers, enriched hamburger and toolbar unchanged.

### Changes and checkpoints
- `6649e6d18f294a2c7aa778019813c14c6735af7e`: isolated CSS-only D17 enhancement to `app/EVen_mail_index.html`. Baseline blob `5eb8ba2d6544953e31e93826c97e1c3d03ac3f28`; new blob `40e65732efa5fa5a56733cc53093fbc312f76e55`.
- The secondary application header has balanced desktop grid columns and centrally anchored search, restrained charcoal background, cream action buttons and 7px radii. The local mail-specific toolbar stays distinct from the shared institutional header.
- HOLLO identity strip becomes a neutral centered cream/charcoal ribbon with readable 16px text and a single elegant enrollment button.
- Mailbox: cream sidebar, unified charcoal/ivory compose and application controls, charcoal active folder, regular 16px label text, subtle muted-violet selected-message edge, clearer left/center/right pane proportions and generous spacing. Gold limited to minor accent details, no large gold blocks.
- E=Ven mail application's existing JavaScript was verified **byte-for-byte unchanged**; all 74 IDs preserved, no duplicates. Data records, identity handoff, local drafts, application workflows, reader open/close, and backup logic not modified.
- `f24f91203affd6a2e4fe1dc97951015dda39cbb9`: six new synthetic source-contract tests in `tests/even_mail_palette.test.mjs`.
- `8234f26a9e79c4a753dc1eb72574e428bbb66bcf`: add D17 checks to existing manual-only, contents-read 333 topology audit workflow.

### Validation boundary
- The 74 existing application element IDs and seven inline script blocks remain intact. New tests are committed, but the full GitHub Actions execution and actual visual rendering have not yet been independently observed.
- Check 100%-zoom desktop, 1280px laptop, 768px tablet and 390px mobile. Confirm centered second header, single official VNV hamburger, both tickers, no toolbar overlap, soft active-row contrasts, mobile folder drawer and reader close, and readable labels.
- Dedicated STOS email terminal stays planned/uncommissioned and **number unassigned**. Nothing here provisions live SMTP service, authenticated mailbox access, account verification, live delivery or remote synchronization.

### Rollback
Revert only the D17 E=Ven CSS commit after checking later edits; preserve prior D16 correction, HOLLO/KANSEE improvements, VNV protected gateway, browser data and validated fallback archive.

## D18 — E=Ven Mail five-stage local data and service hardening (2026-11-07)

**Intent:** Advance E=Ven Mail's local-first privacy and safe future STOS readiness while preserving the founder-approved cream/charcoal D17 visual blueprint, canonical shared VNV header, two tickers, toolbar, HOLLO handoff, application forms, drafts, inbox and eight surrounding 333 subsidiaries.

### Baseline and commits
- Before D18 blob: `40e65732efa5fa5a56733cc53093fbc312f76e55` (E=Ven Mail source).
- `ab92eec85dde55d8e0c4426850a7c1c7de5b3a31`: cap and deduplicate imported applications, mailboxes and messages, reject malformed records, constrain remote synchronization metadata, and downgrade imported `provisioned` local mailbox records to nonauthoritative pending status. Guard guarded local browser writes with storage readback and optimistic old-value checks.
- `3f8a458816b5e69649d778d8125c88727529f437`: stage and verify import and reset replacement before changing active workspace, attempt prior-record rollback on storage failures, and refuse silently overwriting content from another tab. Preserve older tab's draft state in memory for a deliberate backup export.
- `cf96a088f8292dd7f421e1445c40e0290fb1b40d`: require saved data before claiming success for local drafts, Sent Local messages or E=Ven applications. Display honest local-only identity, provisioning, SMTP delivery and future STOS status in Settings.
- `9fe26fe3c8db235bdfe353c21914f03d3bd692d8`: detect first-write races even when the current tab began with no stored workspace.
- Final Git blob: `942b0236a6f8505d8eeb0ac11a6f2b20d7d67956`.
- `120508060a77039cd7253ef69723ef291482aeb0`: `tests/even_mail_integrity.test.mjs` adds synthetic restore and boundary checks.
- `dc9b71a7ef706012805efc067a01161c64e24229`: registers the test suite in manually triggered read-only `.github/workflows/333-topology-boundary-audit.yml`.

### Verification
- Executed actual extracted `importWorkspace()` and `commitWorkspaceReplacement()` in isolated JavaScript with synthetic storage for success, quota failure, readback failure, unreadable previous storage, cancelled import. Five of five retained the correct old or new state and recorded bytes; successful import notified only after verification. Actual extracted `saveState()` rejected an attempted first-write overwrite from a second tab.
- Verified on latest GitHub file: 74 unique HTML element IDs, zero duplicates, zero missing `$('#id')` selector targets; seven inline JS blocks parse, existing shared header / 333 ticker / E=Ven ticker / toolbar references preserved. Existing presentation stylesheet not modified.
- New test suite committed and wired into manual GitHub Actions; **complete runner execution not independently observed**. Source checks and mocks are not a full browser acceptance test.
- No real account, private message, browser storage, production mail server, authenticated backend route, or STOS terminal modified.

### Known limits and remaining acceptance
- Browser localStorage is not an atomic database and is not a secure vault; recovery after persistent storage corruption cannot be guaranteed. Export a local backup before substantial migrations. Backup exports are unencrypted JSON and must be safeguarded by the user.
- Cross-tab safeguard is fail-closed and protective of the current tab's in-memory content; it does not yet offer automatic conflict merging. The user should export the current tab, reload the authoritative stored workspace and manually reconcile if there is a collision.
- The import cap is 5MB; application and mailbox caps are 250 each, messages remain capped at 500. Imported remote-looking mailbox statuses are downgraded because the existing local-only application has no verified provisioning service. Future provisioned status requires independently authenticated backend evidence.
- Live browser acceptance pending: legacy backup shape, reset with quota denial, two-tab concurrent editing, drafting with a blocked write, local application status, keyboard/dialog focus, and desktop/tablet/mobile usability at 100% zoom.
- Existing `app/routers/even_mail.py` supports authenticated application submission/withdrawal; none of those endpoints was activated or modified here. SMTP, mail delivery, provisioning and remote synchronization remain unconfigured. Dedicated E=Ven Mail STOS terminal remains **planned, uncommissioned, number unassigned**.

### Rollback
Revert only the four D18 E=Ven Mail source commits (in reverse order) after checking newer dependencies. Keep D16-D17 visual refinements, HOLLO/KANSEE hardening, 333 directory, protected VNV homepage, STOS infrastructure and founder's verified fallback ZIP untouched.
