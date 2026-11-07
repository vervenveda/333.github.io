# FleaPit — Two-Repository Source Parity Checkpoint

**Audit date:** 2026-11-07  
**Mode:** Read-only. No route, account, data or STOS modifications.  
**Canonical owner:** Unresolved by design pending explicit approval.

## Files and recorded Git blob fingerprints

| Role | Repository path | Git blob SHA |
|---|---|---|
| 333 media gate | `vervenveda/333.github.io/app/FleaPit™_media_gate_Index.html` | `d521d584b6e172780bc274f9df588ab0388934f1` |
| 333 media hub | `vervenveda/333.github.io/app/FleaPit™ _media_hub_index.html` | `e51f6e4a9e6e9c1207c0e4c99b465d5299877025` |
| ProReSources landing | `vervenveda/proresource_hub.github.io/Protools/FleaPit™_media_hub_Index.html` | `e89e63cf6f60642ffec11f2d72fe038124635361` |
| ProReSources hub | `vervenveda/proresource_hub.github.io/Protools/FleaPit™ Protected Media Hub_index.html` | `d4f382e31c34756dba06540bc7ee32a9cbc28fea` |

The 333 and ProReSources media hubs differ in **two source lines** at the inspected commits, both presenting navigation/intro destinations. Their file lengths differ by two characters. The two gate/landing files differ on nine source lines, primarily branding and navigation, including one compressed JavaScript line. This is **not** a semantic-equivalence or runtime-behavior proof.

## Shared browser-local data contract

Both hub files contain `FleaPitProtectedDB`, `fleapit_protected_state_v3`, `fleapit_protected_snapshots_v3`, `fleapit_staged_import_v3`, `familyPin`, `indexedDB`, and `Connect to Watch`.

**Critical boundary:** Identical key strings DO NOT provide cross-origin continuity. `vervenveda.com` and `vervenveda.github.io` are distinct origins. The same holds for other origin variations. Never silently redirect a user to the other origin and assume that saved media or preferences follow.

## Identified navigation inconsistencies

- The 333 directory currently links externally to the ProReSources FleaPit landing page; both existing 333 FleaPit pages are precached by 333's service worker.
- 333 hub's `Introduction` link resolves to its **own hub file** rather than to the dedicated 333 media-gate landing. The ProReSources hub points to its separate landing file.
- No route number has been assigned to FleaPit. Do not invent one.
- Separate branch titles and navigation may be intentional. Retain until an owner decision.

## Recommended safe next steps

1. Audit backup export/import schema, including `schemaVersion`, IndexedDB records, snapshots, family controls, external media opt-in and malformed input handling.
2. Identify intended canonical navigation by user experience, but **do not** rewrite the existing card or merge versions until each existing origin's library persistence is accounted for.
3. Add source parity regression evidence through read-only comparisons. Avoid embedding sensitive media libraries in tests.
4. Plan future FleaPit STOS terminal separately and only through approved secure terminal commissioning. Public source must carry no privileged STOS endpoint or capability.
