# Data Retention and Deletion

## Principles

- Keep personal data only as long as it serves a documented purpose.
- Use shorter retention periods for sensitive communication content.
- Separate active data, deleted-account grace periods, backups, and security evidence.
- Automate deletion where practical.
- Record legal holds and suspend deletion only for the affected records.

## Proposed baseline schedule

These periods are starting points and must be reviewed before production use.

| Data category | Proposed retention |
|---|---:|
| Active account and profile | While the account remains active |
| Deleted account grace period | 30 days |
| Expired email-verification tokens | Delete immediately after expiry |
| Expired password-reset tokens | Delete immediately after expiry |
| Refresh sessions | Until expiry or revocation |
| Authentication and audit logs | 365 days |
| High-value security logs | 730 days |
| E=Ven withdrawn or rejected application | 180 days, unless law or appeal requires longer |
| E=Ven approved application record | Life of account plus 1 year |
| KANSEE room metadata | 90 days by default |
| KANSEE room chat | User-controlled, with a default maximum of 90 days |
| KANSEE media | Not retained unless recording is explicitly enabled |
| Bazaar deleted post content | 30-day recovery window, then delete |
| Bazaar moderation evidence | 365 days or through appeal completion |
| Orphaned uploaded media | 7 days |
| SIte project versions | User-controlled; archive older versions after 1 year |
| Bunya audit records | 730 days |
| Routine backups | 30 days |
| Incident evidence | Duration of investigation plus 1 year |

## Account deletion workflow

1. Confirm the request through an authenticated session or verified recovery process.
2. Disable new sessions and revoke existing refresh tokens.
3. Mark the account for deletion.
4. Remove public visibility promptly.
5. Allow a documented grace period when appropriate.
6. Delete or anonymize active database records after the grace period.
7. Delete associated private media.
8. Allow encrypted backups to expire through the ordinary backup schedule.
9. Preserve only records required for legal, security, fraud-prevention, or financial obligations.
10. Record completion without retaining unnecessary deleted content.

## Backup deletion

Backups are immutable snapshots and may contain records deleted from the active database. Deleted information should disappear as backup generations expire. Backup restoration procedures must reapply deletion requests recorded after the restored snapshot.

## Legal holds

A legal hold must:

- Identify the exact records covered
- State the authorized reason
- Record who approved it
- Limit access
- Include a review date
- End promptly when no longer required

## Retention ownership

Assign a named operational owner for each data category. Review the schedule at least annually and after major product, legal, or infrastructure changes.
