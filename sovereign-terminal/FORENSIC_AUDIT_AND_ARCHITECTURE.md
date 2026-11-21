# 333 Network Sovereign Mac Terminal · Forensic Audit & Architecture

## Current public state

The 333 Network applications are local-first browser workspaces. Their current public pages do not provide authenticated shared backend authority.

- Bazaar Art Live: localStorage for social state; IndexedDB for media; local moderation/report records; export/import support.
- HOLLO: browser-local identity/enrollment workspace and shared identity handoff; backend language exists but no commissioned shared service.
- KANSEE: browser-local meeting workspace; no commissioned realtime meeting backend.
- E=Ven Mail: browser-local application/workspace surface; no commissioned delivery backend.
- SIte: browser-local site/project builder.
- Bunya: browser-local infrastructure planning workspace.
- FleaPit: browser-local media hub/gate with IndexedDB media use.
- WEAL: placeholder route only.

The public gateway itself correctly distinguishes local application state from connected/authenticated services.

## Unified terminal decision

Use one owner-local process at 127.0.0.1:18733, but never one undifferentiated authority bucket.

Namespaces:
- gateway.*
- bazaar.*
- hollo.*
- kansee.*
- even.*
- site.*
- bunya.*
- fleapit.*
- fleapit-gate.*
- weal.*

Each namespace has its own encrypted snapshot, revision counter and audit events.

## Phase 1 authority

Allowed:
- owner pairing
- encrypted local snapshot read/write
- compare-and-swap revision protection
- source integrity verification
- local audit receipts
- namespace status

Denied:
- public publishing
- remote synchronization
- arbitrary file writes
- shell execution APIs
- arbitrary repository writes
- email delivery
- realtime meeting transport
- account verification
- global 333-number assignment
- STOS authority

## Security properties

- loopback only: 127.0.0.1:18733
- one-time owner pairing code printed only to Terminal
- maximum five pairing attempts
- memory-only session token
- 32-byte master key stored in macOS Keychain
- AES-256-GCM encrypted snapshots at rest
- 0700 data directories / 0600 snapshot and audit files
- expected-revision conflict protection
- immediate encrypted readback verification
- approved client manifest pins current Git blob identities
- fail closed if a pinned client differs
- no third-party Node packages
- no production secret in repository or CI

## Next commissioning gate

Do not wire public applications to the terminal until the owner-Mac preflight passes and each application receives a capability-specific bridge contract.
