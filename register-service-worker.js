(() => {
  "use strict";

  if (!("serviceWorker" in navigator)) {
    document.dispatchEvent(
      new CustomEvent("333-service-worker-unsupported")
    );
    return;
  }

  const SERVICE_WORKER_URL = "./service-worker.js";
  const SERVICE_WORKER_SCOPE = "./";
  const UPDATE_CHECK_INTERVAL = 60 * 60 * 1000;

  let registration = null;
  let lastUpdateCheck = 0;
  let updateNotificationSentFor = null;

  function dispatch(name, detail = {}) {
    document.dispatchEvent(
      new CustomEvent(name, {
        detail: {
          registration,
          ...detail
        }
      })
    );
  }

  function workerIdentity(worker) {
    if (!worker) return null;

    return [
      worker.scriptURL || "",
      worker.state || "",
      worker === registration?.waiting ? "waiting" : "",
      worker === registration?.installing ? "installing" : "",
      worker === registration?.active ? "active" : ""
    ].join("|");
  }

  function announceWaitingWorker(worker = registration?.waiting) {
    if (!worker) return;

    const identity = workerIdentity(worker);
    if (identity && identity === updateNotificationSentFor) return;

    updateNotificationSentFor = identity;

    dispatch("333-app-update-ready", {
      worker
    });
  }

  function watchInstallingWorker(worker) {
    if (!worker) return;

    const onStateChange = () => {
      dispatch("333-service-worker-state-change", {
        worker,
        state: worker.state
      });

      if (
        worker.state === "installed" &&
        navigator.serviceWorker.controller
      ) {
        announceWaitingWorker(
          registration?.waiting || worker
        );
      }

      if (worker.state === "redundant") {
        dispatch("333-service-worker-update-failed", {
          worker,
          reason: "The installing worker became redundant."
        });
      }
    };

    worker.addEventListener("statechange", onStateChange);
    onStateChange();
  }

  async function checkForUpdate({ force = false } = {}) {
    if (!registration) return null;
    if (!navigator.onLine) return registration;

    const now = Date.now();

    if (
      !force &&
      now - lastUpdateCheck < UPDATE_CHECK_INTERVAL
    ) {
      return registration;
    }

    lastUpdateCheck = now;

    try {
      await registration.update();

      if (registration.waiting) {
        announceWaitingWorker(registration.waiting);
      }

      dispatch("333-service-worker-update-checked");
    } catch (error) {
      console.warn(
        "333 Network service worker update check failed:",
        error
      );

      dispatch("333-service-worker-update-check-failed", {
        error
      });
    }

    return registration;
  }

  async function registerServiceWorker() {
    try {
      registration = await navigator.serviceWorker.register(
        SERVICE_WORKER_URL,
        {
          scope: SERVICE_WORKER_SCOPE,
          updateViaCache: "none"
        }
      );

      dispatch("333-service-worker-registered");

      if (registration.waiting) {
        announceWaitingWorker(registration.waiting);
      }

      if (registration.installing) {
        watchInstallingWorker(registration.installing);
      }

      registration.addEventListener("updatefound", () => {
        const worker = registration.installing;

        dispatch("333-service-worker-update-found", {
          worker
        });

        watchInstallingWorker(worker);
      });

      await checkForUpdate({ force: true });

      return registration;
    } catch (error) {
      console.warn(
        "333 Network service worker registration failed:",
        error
      );

      dispatch("333-service-worker-registration-failed", {
        error
      });

      return null;
    }
  }

  navigator.serviceWorker.addEventListener(
    "controllerchange",
    () => {
      dispatch("333-service-worker-controller-changed", {
        controller: navigator.serviceWorker.controller
      });
    }
  );

  window.addEventListener("online", () => {
    checkForUpdate({ force: true });
  });

  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible") {
      checkForUpdate();
    }
  });

  window.addEventListener(
    "load",
    registerServiceWorker,
    { once: true }
  );
})();
