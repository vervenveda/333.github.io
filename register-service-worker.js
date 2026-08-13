/* 333 Network service-worker registration and update bridge. */
(() => {
  'use strict';

  if (!('serviceWorker' in navigator)) return;

  let controllerChangeHandled = false;

  function dispatch(name, detail = {}) {
    document.dispatchEvent(new CustomEvent(name, { detail }));
  }

  function announceWaiting(registration) {
    if (!registration?.waiting) return;
    dispatch('333-app-update-ready', {
      registration,
      worker: registration.waiting
    });
  }

  function watchInstallingWorker(registration) {
    const worker = registration?.installing;
    if (!worker) return;

    worker.addEventListener('statechange', () => {
      if (
        worker.state === 'installed' &&
        navigator.serviceWorker.controller
      ) {
        announceWaiting(registration);
      }
    });
  }

  window.addEventListener('load', async () => {
    try {
      const registration = await navigator.serviceWorker.register(
        './service-worker.js',
        { scope: './' }
      );

      window.Network333PWA = { registration };
      dispatch('333-pwa-ready', { registration });

      announceWaiting(registration);

      registration.addEventListener('updatefound', () => {
        watchInstallingWorker(registration);
      });

      navigator.serviceWorker.addEventListener('controllerchange', () => {
        if (controllerChangeHandled) return;
        controllerChangeHandled = true;
        dispatch('333-service-worker-controller-changed', { registration });
      });

      // Check for an updated worker after registration without blocking startup.
      registration.update().catch(() => {});
    } catch (error) {
      console.warn('333 Network service worker registration failed:', error);
      dispatch('333-pwa-error', { error });
    }
  });
})();
