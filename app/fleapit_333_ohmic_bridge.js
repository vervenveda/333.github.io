(() => {
  "use strict";

  const DB_NAME = "FleaPitProtectedDB";
  const DB_VERSION = 1;
  const STORE = "records";
  const FALLBACK_KEY = "fleapit_protected_state_v3";
  const API_CANDIDATES = ["/api/fleapit", "/api/v1/fleapit"];
  const CSRF_CANDIDATES = ["/api/auth/csrf", "/api/v1/auth/csrf"];

  let apiBase = null;
  let remoteRevision = 0;
  let badge = null;

  const meaningful = state => Boolean(
    state && (
      state.media?.length ||
      state.customResources?.length ||
      state.favorites?.length ||
      state.queue?.length ||
      Object.keys(state.resume || {}).length
    )
  );

  function setStatus(text, mode = "") {
    if (!badge) return;
    badge.textContent = text;
    badge.dataset.mode = mode;
    badge.title = "FleaPit sovereign member-library synchronization";
  }

  function openDB() {
    return new Promise((resolve, reject) => {
      if (!("indexedDB" in window)) return reject(new Error("IndexedDB unavailable"));
      const request = indexedDB.open(DB_NAME, DB_VERSION);
      request.onupgradeneeded = () => {
        if (!request.result.objectStoreNames.contains(STORE)) {
          request.result.createObjectStore(STORE);
        }
      };
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async function readLocal() {
    try {
      const db = await openDB();
      return await new Promise((resolve, reject) => {
        const req = db.transaction(STORE, "readonly").objectStore(STORE).get("state");
        req.onsuccess = () => resolve(req.result || null);
        req.onerror = () => reject(req.error);
      });
    } catch {
      try {
        return JSON.parse(localStorage.getItem(FALLBACK_KEY) || "null");
      } catch {
        return null;
      }
    }
  }

  async function writeLocal(value) {
    try {
      const db = await openDB();
      await new Promise((resolve, reject) => {
        const tx = db.transaction(STORE, "readwrite");
        tx.objectStore(STORE).put(value, "state");
        tx.oncomplete = resolve;
        tx.onerror = () => reject(tx.error);
      });
      return;
    } catch {
      localStorage.setItem(FALLBACK_KEY, JSON.stringify(value));
    }
  }

  async function request(url, options = {}) {
    return fetch(url, {
      credentials: "include",
      cache: "no-store",
      ...options,
      headers: {
        Accept: "application/json",
        ...(options.headers || {})
      }
    });
  }

  async function discoverApi() {
    if (window.FLEAPIT_API_BASE) {
      apiBase = String(window.FLEAPIT_API_BASE).replace(/\/$/, "");
      return true;
    }
    for (const candidate of API_CANDIDATES) {
      try {
        const response = await request(`${candidate}/status`);
        if (response.ok) {
          apiBase = candidate;
          return true;
        }
      } catch {}
    }
    return false;
  }

  async function csrfToken() {
    for (const candidate of CSRF_CANDIDATES) {
      try {
        const response = await request(candidate);
        if (!response.ok) continue;
        const body = await response.json();
        const token =
          body.csrfToken ||
          body.csrf_token ||
          body.token ||
          body.csrf ||
          body.data?.csrfToken ||
          "";
        if (token) return String(token);
      } catch {}
    }
    throw new Error("CSRF token is unavailable.");
  }

  async function readRemote() {
    const response = await request(`${apiBase}/state`);
    if (response.status === 401 || response.status === 403) {
      setStatus("OHMIC · Sign in", "guest");
      return null;
    }
    if (!response.ok) throw new Error(`Remote state failed: ${response.status}`);
    const body = await response.json();
    remoteRevision = Number(body.revision) || 0;
    return body;
  }

  async function pushLocal(local) {
    const token = await csrfToken();
    const response = await request(`${apiBase}/state`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-Token": token
      },
      body: JSON.stringify({
        state: local,
        baseRevision: remoteRevision,
        reason: "fleapit-hub-sync"
      })
    });
    if (response.status === 409) {
      await readRemote();
      throw new Error("OHMIC has a newer FleaPit revision. Reload or sync again.");
    }
    if (!response.ok) throw new Error(`OHMIC save failed: ${response.status}`);
    const body = await response.json();
    remoteRevision = Number(body.revision) || remoteRevision + 1;
    setStatus(`OHMIC · Synced r${remoteRevision}`, "ready");
  }

  async function pullRemote(record) {
    if (!record?.state) return;
    await writeLocal(record.state);
    setStatus(`OHMIC · Restored r${record.revision || 0}`, "ready");
    window.setTimeout(() => window.location.reload(), 350);
  }

  async function synchronize() {
    if (!apiBase && !(await discoverApi())) {
      setStatus("OHMIC · Local only", "local");
      return;
    }

    setStatus("OHMIC · Checking…", "working");
    const local = await readLocal();
    const remote = await readRemote();
    if (!remote) return;

    const localTime = Number(local?.updatedAt) || 0;
    const remoteTime = Number(remote?.state?.updatedAt) || 0;

    if (!remote.revision && meaningful(local)) {
      await pushLocal(local);
      return;
    }
    if (remote.revision && !meaningful(local)) {
      await pullRemote(remote);
      return;
    }
    if (remoteTime > localTime && remote.revision) {
      if (window.confirm("OHMIC has a newer FleaPit library. Restore it to this browser?")) {
        await pullRemote(remote);
      } else {
        setStatus(`OHMIC · Remote r${remote.revision}`, "pending");
      }
      return;
    }
    if (localTime > remoteTime && meaningful(local)) {
      await pushLocal(local);
      return;
    }

    setStatus(`OHMIC · Synced r${remote.revision || 0}`, "ready");
  }

  function installBadge() {
    const actions = document.querySelector(".topbar .actions, .actions");
    if (!actions) return;
    badge = document.createElement("button");
    badge.type = "button";
    badge.className = "btn small";
    badge.id = "ohmicFleaPitSync";
    badge.textContent = "OHMIC · Local";
    badge.addEventListener("click", () => {
      synchronize().catch(error => {
        console.warn("[FleaPit/OHMIC]", error);
        setStatus("OHMIC · Retry", "error");
      });
    });
    actions.appendChild(badge);
  }

  window.FleaPitSovereignSync = {
    sync: synchronize,
    readLocal,
    readRemote: () => apiBase ? readRemote() : null
  };

  window.addEventListener("load", () => {
    installBadge();
    discoverApi()
      .then(found => {
        if (!found) {
          setStatus("OHMIC · Local only", "local");
          return;
        }
        return readRemote().then(remote => {
          if (remote) setStatus(`OHMIC · Ready r${remote.revision || 0}`, "ready");
        });
      })
      .catch(() => setStatus("OHMIC · Local only", "local"));
  });
})();
