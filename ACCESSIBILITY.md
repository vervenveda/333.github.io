# Accessibility Statement

**Polyglot — Khaemenes Academy Linguistics Hall**  
**Last reviewed:** August 2, 2026

Polyglot is being designed as an inclusive international learning space. The project aims toward the principles of WCAG 2.2 Level AA, but this statement does not claim formal certification or complete conformance.

## Current accessibility features

The present landing page includes:

- a **Skip to main content** link;
- semantic headings, sections, navigation, cards, buttons, and dialog markup;
- visible keyboard focus styling;
- keyboard-operable navigation and controls;
- descriptive labels for primary controls;
- responsive layouts for narrow and enlarged displays;
- light and dark appearance modes;
- support for the user's `prefers-reduced-motion` setting;
- readable text alternatives for the visual language compass;
- written translations alongside optional speech playback;
- `lang` attributes for multilingual sample phrases;
- right-to-left direction support for Arabic samples;
- status messages for shelf changes and unsupported speech playback; and
- an offline page that does not depend on external fonts.

## Known limitations

Current limitations include:

1. **Speech voices vary.** Pronunciation quality and language availability depend on the browser, operating system, and installed speech voices. Written text remains the authoritative fallback.
2. **No audio transcript library yet.** The current phrase feature uses short visible phrases rather than recorded lessons. Future audio must include transcripts and non-audio equivalents.
3. **External fonts may fail or be blocked.** The design falls back to common system fonts, but script rendering can vary by device.
4. **Future modules are placeholders.** Planned course collections, portals, and studios are announced in an accessible dialog but are not yet full learning destinations.
5. **Formal assistive-technology testing is ongoing.** Contributors should test with keyboard-only navigation, zoom, high-contrast settings, and representative screen readers before major releases.

## Language and script accessibility

Language education requires more than visual translation. New Polyglot material should:

- identify the language and, when relevant, dialect or regional variety;
- declare text direction correctly;
- avoid encoding information through color alone;
- provide text for images of writing systems;
- explain transliteration conventions;
- pair pronunciation audio with visible wording and meaning;
- allow users to pause or stop moving and spoken content;
- preserve zoom and reflow without horizontal scrolling; and
- avoid decorative fonts for long instructional passages.

## Contributor requirements

Before submitting a new interactive feature or learning module, contributors should verify:

- all functions can be reached and used by keyboard;
- focus order follows the visual and reading order;
- buttons and links have meaningful accessible names;
- form inputs have persistent labels and useful error messages;
- text contrast remains sufficient in all supported themes;
- images have appropriate alternative text or are marked decorative;
- media includes captions, transcripts, or equivalent instruction;
- motion respects reduced-motion preferences; and
- content remains understandable without sound, color, hover, or precise pointer movement.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full submission checklist.

## Reporting an accessibility barrier

Please report the page, device, browser, assistive technology, and a brief description of the barrier. Do not include private student information.

**Email:** KhaemenesAcademy@protonmail.com  
**Suggested subject:** `Polyglot Accessibility Report`

Accessibility reports may also be submitted through a public issue only when they contain no sensitive information.

## Continuing work

Accessibility is part of curriculum quality, not a final decoration. Planned priorities are listed in [ROADMAP.md](ROADMAP.md), and material changes should be recorded in [CHANGELOG.md](CHANGELOG.md).
