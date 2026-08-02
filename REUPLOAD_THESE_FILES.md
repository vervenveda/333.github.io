# 333 Network Corrective Upload

Upload these five files to the **root** of `vervenveda/333.github.io`, replacing the files with the same names:

- `index.html`
- `manifest.webmanifest`
- `service-worker.js`
- `offline.html`
- `404.html`

Do not place them inside `app/`.

The current repository contains the correct six application files, but Polyglot versions of the manifest, service worker, and 404 page were uploaded accidentally. The current landing page also contains a contrast, typography, logo-size, and missing-brand-text regression.

This repair advances the 333 cache to **v5** and deletes both older 333 caches and the accidentally created `polyglot-*` caches during activation.

After upload, open the live page and refresh once. Select **Update Now** if the update banner appears. An installed copy may need to be closed and reopened once.
