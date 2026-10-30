# Beta Index Coverage

Generated automatically by `.github/workflows/beta-index-coverage.yml`.

- Added in this run: **0**
- Already covered: **10**
- Skipped for an explicit reason: **0**

## Coverage rule

Visible public HTML surfaces whose filenames end in `index.html` (including `_index.html` and common `inndex.html` typos) receive the canonical `/assets/vnv-beta-link.js` doorway unless they are archived, private, administrative, the Beta destination itself, or explicitly forbid all scripts.

The Beta widget sends only the public hostname and pathname as source metadata. It does not send learner IDs, family IDs, grades, answers, form values, query strings, hashes, localStorage contents, report text, or credentials.
