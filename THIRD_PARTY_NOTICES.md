# Third-Party Notices

Polyglot is designed to minimize dependencies. This file identifies external services, browser capabilities, and third-party materials currently referenced by the public landing page or anticipated by the repository foundation.

Third-party names and marks belong to their respective owners. Inclusion does not imply endorsement.

## 1. Google Fonts

The initial landing page requests these font families through Google Fonts:

- Cormorant Garamond
- Inter
- Noto Sans Arabic
- Noto Sans Devanagari
- Noto Sans Japanese
- Noto Sans Simplified Chinese

Google Fonts serves font stylesheets and font files from Google-controlled domains. Each font family is distributed under the license identified in its Google Fonts metadata or source repository. Those licenses may require preservation of copyright and license notices when font files are downloaded, modified, or redistributed.

Polyglot does not redistribute font files in the present repository packet.

Service information: https://fonts.google.com/

Before self-hosting fonts:

1. obtain the font files from an authorized source;
2. retain the exact license file supplied with each family;
3. do not rename reserved font names unless the license permits it;
4. document local modifications; and
5. update this notice with the bundled versions and licenses.

## 2. Browser Web APIs

Polyglot uses standard browser capabilities rather than bundled third-party JavaScript libraries.

### Web Speech API

The **Hear phrase** control uses `SpeechSynthesisUtterance` and `speechSynthesis` when supported. Voice data and processing are provided by the user's browser, operating system, installed voice packages, or an associated vendor service. Availability, pronunciation, and privacy behavior vary by platform.

Reference: https://developer.mozilla.org/docs/Web/API/Web_Speech_API

### Web Storage API

Appearance and **My Shelf** preferences use browser `localStorage`.

Reference: https://developer.mozilla.org/docs/Web/API/Window/localStorage

### Service Worker and Cache Storage

The optional offline shell uses the Service Worker and Cache Storage APIs. The code is original to this repository packet and does not bundle a third-party service-worker library.

References:

- https://developer.mozilla.org/docs/Web/API/Service_Worker_API
- https://developer.mozilla.org/docs/Web/API/CacheStorage

## 3. GitHub and GitHub Pages

The repository may be hosted through GitHub and published through GitHub Pages. GitHub's own terms, privacy notice, availability, and security controls govern that platform service.

Service information: https://pages.github.com/

## 4. Unicode characters and language samples

Polyglot displays ordinary Unicode text and symbols representing multiple writing systems. Unicode character encoding is an international technical standard; individual words, short greetings, and factual language names are not treated here as third-party software packages.

Longer translations, literary passages, dictionaries, recordings, illustrations, or curriculum materials must be reviewed separately for copyright, cultural permission, and attribution before inclusion.

## 5. Future third-party additions

A contributor adding any library, API, dataset, icon collection, audio recording, dictionary, translation, image, video, font, or embedded service must update this file with:

- the component or work name;
- creator or publisher;
- version or retrieval date;
- source location;
- applicable license or permission;
- required attribution;
- local modifications; and
- privacy or network behavior.

Do not add a third-party resource when its license, origin, or permission status is unclear.
