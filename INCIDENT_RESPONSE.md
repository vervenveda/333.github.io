# Incident Response Plan

## Purpose

This plan provides a repeatable process for security, privacy, availability, integrity, and abuse incidents affecting the 333 Network.

## Incident examples

- Account takeover
- Exposed secret or signing key
- Unauthorized database access
- Personal-data disclosure
- Malicious upload
- E=Ven application data exposure
- KANSEE room intrusion
- Bazaar harassment or coordinated abuse
- SIte publishing compromise
- Bunya provider-token misuse
- Data loss or corrupted backups
- Service outage or denial-of-service event

## Severity levels

### Severity 1 — Critical
Active compromise, widespread sensitive-data exposure, destructive provider access, or severe safety risk.

### Severity 2 — High
Confirmed unauthorized access with limited scope, serious account compromise, or major outage.

### Severity 3 — Medium
Contained vulnerability, localized abuse, partial degradation, or suspicious activity requiring investigation.

### Severity 4 — Low
Minor issue with limited impact and no evidence of exploitation.

## Response roles

Assign people or service owners for:

- Incident commander
- Security investigation
- Infrastructure containment
- Application owner
- Privacy and legal review
- Member communication
- Evidence custodian
- Recovery verification

One person may hold multiple roles in a small organization, but responsibilities must be explicit.

## Response lifecycle

### 1. Detect and record

- Open an incident record.
- Record time, reporter, affected systems, and observed behavior.
- Preserve relevant logs.
- Avoid copying unnecessary personal data into chat or informal notes.
- Assign an initial severity.

### 2. Contain

Possible actions include:

- Revoke sessions
- Disable affected accounts
- Rotate exposed secrets
- Disable a vulnerable endpoint
- Isolate a worker or container
- Suspend uploads or publishing
- Restrict administrative access
- Place affected provider integrations in read-only mode

### 3. Investigate

Determine:

- Initial access method
- Time window
- Systems and records affected
- Whether data was viewed, changed, deleted, or exported
- Whether the incident remains active
- Whether member safety is implicated
- Whether legal notification duties may apply

Maintain a timestamped decision log.

### 4. Eradicate

- Patch vulnerabilities
- Remove malicious files or persistence
- Rotate credentials
- Correct permissions
- Rebuild compromised systems from trusted images
- Add tests or controls preventing recurrence

### 5. Recover

- Restore from verified backups when required
- Reapply records created after the backup
- Validate database integrity
- Confirm authentication, authorization, uploads, and administrative tools
- Monitor for recurrence
- Restore service gradually

### 6. Notify

Coordinate required notifications to:

- Affected members
- Service providers
- Insurers
- Legal counsel
- Regulators or authorities where required

Notices should be factual, timely, understandable, and limited to verified information.

### 7. Review

Within a reasonable period:

- Write a post-incident report
- Identify root causes and contributing conditions
- Record what worked and failed
- Assign remediation owners and deadlines
- Update policies, alerts, tests, and training
- Verify that remediation was completed

## Emergency secret rotation

Maintain a documented procedure for rotating:

- JWT and session secrets
- Database credentials
- SMTP credentials
- Object-storage credentials
- TURN secrets
- Deployment tokens
- DNS and registrar tokens
- Administrative bootstrap tokens

Rotation must account for invalidating existing sessions and updating all running services safely.

## Evidence handling

- Restrict evidence access.
- Record collection time and source.
- Preserve original logs where practical.
- Use redacted working copies.
- Store incident material separately from ordinary application logs.
- Delete evidence according to retention and legal requirements.
