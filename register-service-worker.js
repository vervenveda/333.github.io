/* Add this file to index.html with:
   <script src="./register-service-worker.js" defer></script> */

(() => {
  'use strict';

  if (!('serviceWorker' in navigator)) return;

  window.addEventListener('load', async () => {
    try {
      const registration = await navigator.serviceWorker.register('./service-worker.js', {
        scope: './'
      });

      window.PolyglotPWA = { registration };
      window.dispatchEvent(new CustomEvent('polyglot:pwa-ready', {
        detail: { registration }
      }));
    } catch (error) {
      console.warn('Polyglot service worker registration failed:', error);
      window.dispatchEvent(new CustomEvent('polyglot:pwa-error', {
        detail: { error }
      }));
    }
  });
})();
