# Contributing to Polyglot

Thank you for helping build **Polyglot — Khaemenes Academy Linguistics Hall**. Contributions may come from language teachers, native and heritage speakers, linguists, translators, accessibility reviewers, artists, students, families, and developers.

All participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Ways to contribute

You may propose:

- corrections to spelling, grammar, translation, transliteration, or pronunciation guidance;
- language-family, script, and cultural-context research;
- accessible lessons, quizzes, reading passages, and practice activities;
- keyboard, screen-reader, right-to-left, or reduced-motion improvements;
- privacy and security improvements;
- offline learning and performance enhancements;
- verified internal Academy links; and
- documentation, testing, and source attribution.

## Before opening a change

1. Search existing issues and pull requests to avoid duplicate work.
2. Keep one contribution focused on one clear purpose.
3. Do not include copyrighted textbooks, recordings, translations, images, or assessments without permission.
4. Do not include private student information, credentials, unpublished answer keys, or confidential Academy material.
5. Read [LICENSE.md](LICENSE.md), [PRIVACY.md](PRIVACY.md), [ACCESSIBILITY.md](ACCESSIBILITY.md), and [CULTURAL_RESPECT_GUIDELINES.md](docs/CULTURAL_RESPECT_GUIDELINES.md) when those files become available.

## Branch and commit guidance

Suggested branch names:

```text
feature/spanish-foundations
content/arabic-greetings
fix/mobile-navigation
accessibility/dialog-focus
security/service-worker-scope
```

Write commits that state what changed, for example:

```text
Add visible transliteration notes to Arabic phrases
Correct Japanese language tag in daily phrase card
Improve focus visibility in dark mode
```

## Language-content requirements

A language contribution should identify, when applicable:

- language name and native name;
- dialect, register, region, or historical period;
- writing system and text direction;
- source or reference used;
- literal translation and natural translation when they differ;
- transliteration system;
- pronunciation notation or audio source;
- cultural or situational context;
- intended learner level and age range;
- whether a fluent or native speaker reviewed it; and
- any uncertainty that still needs review.

Do not present one regional form as the only correct form when meaningful alternatives exist.

## AI-assisted contributions

AI tools may assist drafting, formatting, brainstorming, or code review, but they are not a substitute for subject-matter verification.

Disclose meaningful AI assistance in the pull request. Language content generated or translated with AI must be reviewed against reliable sources and, whenever practical, by a qualified human speaker or educator before publication.

Never use AI output to invent citations, cultural claims, sacred-text wording, or definitive pronunciation guidance.

## Cultural respect

Contributors must:

- avoid stereotypes, caricatures, exoticization, and national generalizations;
- name communities as they identify themselves;
- distinguish language, ethnicity, citizenship, religion, and geography;
- seek appropriate permission for protected Indigenous, sacred, ceremonial, or community-held material;
- credit community knowledge and original creators; and
- explain historical terms that may now be harmful or contested.

## Code standards

Polyglot currently favors accessible, dependency-light HTML, CSS, and JavaScript.

Code changes should:

- work on current major desktop and mobile browsers;
- preserve keyboard operation;
- avoid unnecessary frameworks and trackers;
- fail gracefully when an API is unavailable;
- use same-origin resources where practical;
- protect right-to-left and multilingual text behavior;
- avoid hidden network requests;
- update the service-worker cache version when cached core files change; and
- keep the static page usable without JavaScript whenever practical.

## Testing checklist

Before submission, test:

- [ ] keyboard-only navigation;
- [ ] visible focus in light and dark modes;
- [ ] browser zoom at 200%;
- [ ] narrow mobile layout;
- [ ] reduced-motion preference;
- [ ] language search and **My Shelf** behavior;
- [ ] right-to-left samples;
- [ ] planned-module dialog opening and closing;
- [ ] all modified links;
- [ ] offline fallback after service-worker installation; and
- [ ] browser console for unexpected errors.

## Pull-request description

Explain:

1. what changed;
2. why it improves Polyglot;
3. what sources or reviewers support language content;
4. what accessibility and device testing was completed;
5. whether AI tools were used; and
6. whether third-party licenses or notices changed.

## Review and acceptance

A contribution may be revised, postponed, or declined when it is inaccurate, inaccessible, culturally unsafe, legally unclear, duplicative, difficult to maintain, or outside the current roadmap. Publication is not guaranteed.

Accepted changes should be reflected in [CHANGELOG.md](CHANGELOG.md).
