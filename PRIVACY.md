# 333 Network Privacy Notice — Development Foundation

**Last reviewed:** August 13, 2026

The 333 Network is under active development. This notice describes the repository's current architecture at a high level and does not claim that every planned network service is publicly operational. Before broad public registration or production hosting, the final production deployment must receive a jurisdiction-specific privacy and legal review.

## Current data boundaries

The project intentionally distinguishes between:

- information stored only in a browser for local-first/offline use;
- information submitted to the shared backend when a backend feature is enabled;
- public community content a member deliberately publishes;
- administrative/audit information used to protect the service; and
- future services that are planned but not yet operational.

Local browser data is not automatically the same thing as a verified server account. Clearing browser storage or changing devices may remove local-only state unless a feature has been synchronized through an enabled backend service.

## Shared backend foundation

The current backend foundation can support account authentication, member/profile records, HOLLO enrollment and internal 333-number records, E=Ven Mail applications, refresh/session security records, and audit records. The exact production collection and retention behavior must follow the repository's data-retention policy and the configuration of the deployed service.

The project should collect only information needed for the requested service and should avoid placing credentials, provider secrets, private administrative topology, or sensitive user content in public repository files or browser source code.

## Application-specific status

### HOLLO

HOLLO is intended to provide shared identity, profiles, contacts, and direct communication. Browser-local identity and a verified backend identity must remain clearly distinguishable until synchronization is enabled and verified.

### KANSEE

KANSEE currently contains substantial local meeting and collaboration functionality. Live network conferencing, signaling, and hosted meeting synchronization must not be described as operational until those services are deployed and verified. Camera and microphone access should remain permission-based and user initiated.

### E=Ven Mail

An E=Ven Mail application is not the same as a provisioned mailbox. Mailbox provisioning, mail transport, mailbox storage, spam/abuse controls, and related retention rules require separate production services and policies.

### Bazaar Art Live

Bazaar Art Live is intended for community and public/discoverable content. Publishing to a public feed or sharing a hosted SIte should remain an explicit user action rather than an automatic consequence of creating local content.

### SIte and OHMIC Foundry

SIte projects should remain portable and exportable. OHMIC Foundry hosting must clearly distinguish draft/private project material from files included in a public build. Private data must never be silently included in a public release.

### Bunya

Bunya is an infrastructure control surface. DNS, registrar, hosting-provider, storage, deployment, TLS, mail, and other provider credentials must remain server-side and must never be exposed to public browser code.

## Security and operational records

The backend may maintain security and audit records needed for account protection, abuse prevention, rate limiting, incident investigation, and system reliability. Logs should avoid recording secrets or unnecessary message/content bodies. Where practical, identifiers used for security telemetry should be minimized or pseudonymized.

## Children and families

Some Verve N Veda and Khaemenes experiences serve children and families. The 333 Network should not assume that a general network account design is automatically suitable for minors. Age-appropriate experiences, guardian controls, consent requirements, educational records, communication safety, and applicable child-privacy rules require separate review before a child-facing hosted account system is enabled.

## External infrastructure

A production deployment may require infrastructure providers for hosting, databases, object storage, mail delivery, DNS, TURN/STUN, monitoring, backups, or other operations. Provider use and data processing must be documented before production deployment. Frontend applications must never receive provider administrative secrets.

## User control and portability

The project should preserve practical paths for users to export their work, remove local browser data, request account/data actions supported by the deployed service, and move published websites away from OHMIC Foundry without losing the site they created.

## Retention and deletion

See `DATA_RETENTION.md` for the repository's current retention framework. Final retention periods must match the deployed service, legal obligations, backup model, abuse-prevention requirements, and published user notice.

## Changes

Material privacy changes should be recorded in `CHANGELOG.md`. A data-collecting feature should not be publicly launched with documentation that still describes an earlier or unrelated application.

## Security reports

Use the process in `SECURITY.md` for security concerns. Do not post credentials, private account data, security tokens, or sensitive personal information in public issues.
