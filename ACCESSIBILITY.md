# 333 Network Accessibility Statement

**Last reviewed:** August 13, 2026

The 333 Network is being developed as an inclusive communication, community, creation, and infrastructure environment. The project aims toward WCAG 2.2 Level AA principles, but this statement does not claim formal certification or complete conformance.

## Scope

This statement applies to the public 333 gateway and its principal applications:

- HOLLO / 333 Direct Connect
- KANSEE meeting rooms
- E=Ven Mail
- Bazaar Art Live
- SIte website and application builder
- Bunya infrastructure console

Some capabilities are local-first prototypes while shared backend services are completed. Accessibility requirements apply to both local and networked versions.

## Current design requirements

333 interfaces should provide:

- semantic page structure and landmarks;
- keyboard-operable navigation and controls;
- visible keyboard focus;
- persistent labels for form controls;
- understandable validation and status messages;
- responsive layouts that reflow on narrow screens and at high zoom;
- reduced-motion support where animation is used;
- text alternatives for meaningful images and icons;
- sufficient contrast in supported themes;
- controls that do not depend on hover alone;
- readable fallbacks when optional media or browser APIs are unavailable;
- offline and error states that remain understandable and navigable.

## Application-specific requirements

### HOLLO

Identity, enrollment, contacts, and communication controls should remain usable by keyboard and assistive technology. Network numbers must be presented in text, not by visual styling alone.

### KANSEE

Meeting rooms must provide accessible labels for camera, microphone, participant, chat, invitation, presentation, and moderation controls. Live conferencing work should include keyboard access, captions/transcripts where available, visible speaking/connection status that is not color-only, and alternatives to drag-only interactions.

### E=Ven Mail

Mail application and future mailbox interfaces should use programmatic field labels, clear error messages, keyboard navigation, readable message structure, and accessible status notifications.

### Bazaar Art Live

Posts, reactions, comments, groups, events, and media should expose meaningful accessible names and reading order. User-provided images should support alternative text or an equivalent descriptive workflow.

### SIte

The builder should help creators produce accessible sites, not merely make the editor itself accessible. Components should encourage semantic headings, labels, alternative text, focus order, contrast, responsive reflow, and keyboard-operable interactions. Drag-and-drop actions require a keyboard-accessible alternative.

### Bunya

Infrastructure status must not rely on color alone. Tables, health indicators, deployment controls, and warnings should have text equivalents and predictable keyboard order.

## Media and conferencing

Future live audio/video features should support captions, transcripts, or equivalent communication accommodations where technically and operationally appropriate. Users must be able to understand media controls without sound, hover, or precise pointer movement.

## Creator-hosted content

OHMIC/SIte-hosted websites may contain creator-authored content. The platform should provide accessibility guidance and automated checks where practical, but creators remain responsible for reviewing their published content. Automated checks cannot prove complete accessibility.

## Testing expectations

Before major releases, test representative flows with:

- keyboard-only navigation;
- browser zoom and reflow;
- reduced-motion settings;
- high-contrast or forced-color settings where supported;
- representative screen readers;
- mobile touch input;
- validation and error states;
- offline and degraded-network conditions.

## Known limitations

The network is under active development. Several services are not yet fully connected to their shared backend, and comprehensive assistive-technology testing has not yet been completed for every application state.

A local prototype that appears usable is not considered complete until its networked states, errors, authentication flows, loading states, and recovery behavior have also been reviewed.

## Reporting an accessibility barrier

Accessibility reports should identify the application or page, browser/device, assistive technology if relevant, and a concise description of the barrier. Do not include passwords, private messages, sensitive account information, or other private user data in a public issue.

Accessibility improvements should be tracked alongside functional changes rather than postponed until the end of development.
