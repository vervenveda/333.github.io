# 333 Network Accessibility Statement

**Last reviewed:** August 13, 2026

The 333 Network is being developed as an inclusive communication, community, creation, and infrastructure environment. The project aims toward WCAG 2.2 Level AA principles, but this statement does not claim formal certification or complete conformance.

## Scope

This statement applies to the public 333 gateway and its principal applications: HOLLO / 333 Direct Connect, KANSEE meeting rooms, E=Ven Mail, Bazaar Art Live, SIte website and application builder, and Bunya infrastructure console.

Some capabilities are local-first prototypes while shared backend services are completed. Accessibility requirements apply to both local and networked versions.

## Current design requirements

333 interfaces should provide semantic page structure and landmarks; keyboard-operable navigation and controls; visible keyboard focus; persistent labels; understandable validation and status messages; responsive reflow; reduced-motion support; text alternatives for meaningful images/icons; sufficient contrast; controls that do not depend on hover alone; readable fallbacks when optional media/browser APIs are unavailable; and understandable offline/error states.

## Application-specific requirements

### HOLLO

Identity, enrollment, contacts, and communication controls should remain usable by keyboard and assistive technology. Network numbers must be presented in text, not by visual styling alone.

### KANSEE

Meeting rooms must provide accessible labels for camera, microphone, participant, chat, invitation, presentation, and moderation controls. Live conferencing should include keyboard access, captions/transcripts where available, visible speaking/connection status that is not color-only, and alternatives to drag-only interactions.

### E=Ven Mail

Mail application and future mailbox interfaces should use programmatic field labels, clear error messages, keyboard navigation, readable message structure, and accessible status notifications.

### Bazaar Art Live

Posts, reactions, comments, groups, events, and media should expose meaningful accessible names and reading order. User-provided images should support alternative text or an equivalent descriptive workflow.

### SIte

The builder should help creators produce accessible sites, not merely make the editor itself accessible. Components should encourage semantic headings, labels, alternative text, focus order, contrast, responsive reflow, and keyboard-operable interactions. Drag-and-drop actions require a keyboard-accessible alternative.

### Bunya

Infrastructure status must not rely on color alone. Tables, health indicators, deployment controls, and warnings should have text equivalents and predictable keyboard order.

## Media and creator-hosted content

Future live audio/video features should support captions, transcripts, or equivalent communication accommodations where technically and operationally appropriate. OHMIC/SIte-hosted websites may contain creator-authored content; the platform should provide accessibility guidance and automated checks where practical, while making clear that automated checks cannot prove complete accessibility.

## Testing expectations

Before major releases, test representative flows with keyboard-only navigation, browser zoom and reflow, reduced-motion settings, high-contrast/forced-color settings where supported, representative screen readers, mobile touch input, validation/error states, and offline/degraded-network conditions.

## Current limitations

The network is under active development. Several services are not yet fully connected to their shared backend, and comprehensive assistive-technology testing has not yet been completed for every application state.
