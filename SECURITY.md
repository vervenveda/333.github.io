# Security Policy

Polyglot is presently a static GitHub Pages project. It has no public authentication system, central learner database, payment processor, or production API. Security reports are still important because unsafe links, script injection, dependency changes, and accidental disclosure can affect visitors.

## Supported versions

| Version | Security updates |
|---|---|
| Current `main` branch | Supported |
| Older copied or forked releases | Best effort only |
| Unofficial mirrors | Not controlled by Khaemenes Academy |

## Report a vulnerability privately

Please do not publish an unredacted vulnerability in a public issue.

Send reports to:

**KhaemenesAcademy@protonmail.com**  
**Suggested subject:** `Private Polyglot Security Report`

Include only the information needed to reproduce the problem:

- affected page or file;
- browser and operating system;
- clear reproduction steps;
- expected and observed behavior;
- potential impact;
- a minimal proof of concept, when safe; and
- whether the issue has already been disclosed elsewhere.

Do not send real student records, passwords, private keys, access tokens, or unnecessary personal information. Use fictional test data.

## In-scope concerns

Examples include:

- cross-site scripting or unsafe HTML injection;
- malicious or compromised external resources;
- service-worker cache poisoning or incorrect scope;
- open redirects or deceptive links;
- exposed secrets or private data committed to the repository;
- unsafe future form handling;
- dependency or build-pipeline compromise;
- content that impersonates an Academy portal; and
- a repository configuration that permits unauthorized modification.

## Usually out of scope

The following are generally not vulnerabilities in the current static release:

- missing features or planned modules;
- lack of an account system;
- browser speech voices that pronounce a language imperfectly;
- denial-of-service tests against GitHub Pages or third-party providers;
- reports that require social engineering, physical access, or compromised user devices; and
- scanner output without a reproducible security impact.

## Maintainer handling

The maintainers will aim to:

1. acknowledge a responsible report privately;
2. reproduce and evaluate the issue;
3. limit disclosure while a practical correction is prepared;
4. record public-facing fixes in [CHANGELOG.md](CHANGELOG.md); and
5. credit the reporter when requested and appropriate.

No bounty or payment program is promised.

## Repository safeguards

Contributors must:

- never commit `.env` files, private keys, tokens, passwords, student records, or unpublished answer keys;
- review every external script, font, API, iframe, and link before addition;
- use HTTPS resources;
- avoid inline collection of sensitive information;
- keep service-worker caches limited to public site resources;
- use dependency lockfiles if a build system is introduced; and
- document third-party components in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Coordinated disclosure

Please allow maintainers a reasonable opportunity to investigate and correct a confirmed issue before public disclosure. This request does not prevent good-faith reporting to an appropriate platform or authority when immediate harm requires it.
