const CACHE_PREFIX = "333-333-network-pwa-";
const CACHE_VERSION = `${CACHE_PREFIX}v8`;
const STATIC_CACHE = `${CACHE_VERSION}-static`;
const RUNTIME_CACHE = `${CACHE_VERSION}-runtime`;
const MAX_RUNTIME_ENTRIES = 60;

const CORE_SHELL = [
  "./",
  "./index.html",
  "./offline.html",
  "./404.html",
  "./manifest.webmanifest",
  "./install-app.js",
  "./register-service-worker.js",
  "./assets/icons/icon-192.png",
  "./assets/icons/icon-512.png",
  "./assets/icons/icon-maskable-512.png"
];

const APP_PAGES = [
  "./app/HOLLO_333_direct_connect_index.html",
  "./app/KANSEE_333_meeting_rooms_index.html",
  "./app/EVen_mail_index.html",
  "./app/Bazaar_Art_Live_index.html",
  "./app/FleaPit™_media_gate_Index.html",
  "./app/FleaPit™ _media_hub_index.html",
  "./app/SIte_builder_index.html",
  "./app/Bunya_digital_infrastructure_index.html"
];

const PRECACHE_URLS = [...CORE_SHELL, ...APP_PAGES];

/* Runtime cache is exclusively for public, origin-scoped static resources.
   Authenticated requests, APIs, query-bearing URLs and private responses bypass it. */
const STATIC_PATHS = new Set(PRECACHE_URLS.map(path => new URL(path, self.registration.scope).pathname));
const ASSET_EXTENSIONS = new Set([".css", ".js", ".mjs", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".ico", ".woff", ".woff2", ".webmanifest"]);

function approvedPublicCacheRequest(request) {
  if (request.method !== "GET" || request.headers.has("Authorization")) return false;
  const url = new URL(request.url);
  const scope = new URL(self.registration.scope);
  if (url.origin !== scope.origin || !url.pathname.startsWith(scope.pathname) ||
      url.search || url.hash) return false;
  if (STATIC_PATHS.has(url.pathname)) return true;
  if (request.mode === "navigate") return false;
  const extension = url.pathname.slice(url.pathname.lastIndexOf(".")).toLowerCase();
  if (!ASSET_EXTENSIONS.has(extension)) return false;
  const scoped = url.pathname.slice(scope.pathname.length).toLowerCase();
  if (scoped.split("/").some(part => ["api", "auth", "admin", "private", "account", "accounts", "member", "members", "token", "tokens", "session", "sessions", "vault", "backup", "backups"].includes(part))) return false;
  return true;
}

function approvedPublicCacheResponse(response) {
  if (!isCacheable(response)) return false;
  const policy = (response.headers.get("Cache-Control") || "").toLowerCase();
  if (/\b(?:private|no-store|no-cache)\b/.test(policy)) return false;
  if (response.headers.has("Set-Cookie")) return false;
  const type = (response.headers.get("Content-Type") || "").toLowerCase();
  if (type.includes("application/json") || type.includes("text/event-stream")) return false;
  return true;
}


function isCacheable(response) {
  return Boolean(response && response.ok && (response.type === "basic" || response.type === "default"));
}

async function putInCache(cacheName, request, response) {
  if (!approvedPublicCacheRequest(request) || !approvedPublicCacheResponse(response)) return;
  const cache = await caches.open(cacheName);
  await cache.put(request, response.clone());
}

async function trimCache(cacheName, maxEntries) {
  const cache = await caches.open(cacheName);
  const keys = await cache.keys();
  if (keys.length <= maxEntries) return;
  await Promise.all(keys.slice(0, keys.length - maxEntries).map(request => cache.delete(request)));
}

async function precacheFiles() {
  const cache = await caches.open(STATIC_CACHE);
  const results = await Promise.allSettled(PRECACHE_URLS.map(async url => {
    const request = new Request(url, { cache: "reload" });
    const response = await fetch(request);
    if (!isCacheable(response)) throw new Error(`Unable to precache ${url}: HTTP ${response.status}`);
    await cache.put(request, response);
  }));

  const failed = results
    .map((result, index) => ({ result, url: PRECACHE_URLS[index] }))
    .filter(({ result }) => result.status === "rejected");

  if (failed.length) {
    console.warn(
      "[333 Network] Some files were not precached:",
      failed.map(({ url, result }) => ({ url, reason: String(result.reason) }))
    );
  }

  const requiredMissing = [];
  for (const url of ["./index.html", "./offline.html"]) {
    if (!(await cache.match(url))) requiredMissing.push(url);
  }
  if (requiredMissing.length) {
    throw new Error(`Required offline files were not cached: ${requiredMissing.join(", ")}`);
  }
}

async function handleNavigation(request) {
  try {
    const response = await fetch(request);
    if (approvedPublicCacheRequest(request) && approvedPublicCacheResponse(response)) {
      await putInCache(RUNTIME_CACHE, request, response);
      await trimCache(RUNTIME_CACHE, MAX_RUNTIME_ENTRIES);
    }
    return response;
  } catch {
    const cachedPage = approvedPublicCacheRequest(request) ? await caches.match(request) : null;
    if (cachedPage) return cachedPage;
    const offlinePage = await caches.match("./offline.html");
    if (offlinePage) return offlinePage;
    return new Response(
      "333 Network is offline and the requested page is not cached.",
      {
        status: 503,
        statusText: "Offline",
        headers: { "Content-Type": "text/plain; charset=utf-8" }
      }
    );
  }
}

async function handleSameOriginAsset(request) {
  const cached = await caches.match(request);
  const networkUpdate = fetch(request).then(async response => {
    if (approvedPublicCacheRequest(request) && approvedPublicCacheResponse(response)) {
      await putInCache(RUNTIME_CACHE, request, response);
      await trimCache(RUNTIME_CACHE, MAX_RUNTIME_ENTRIES);
    }
    return response;
  });

  if (cached) {
    networkUpdate.catch(() => {});
    return cached;
  }

  try {
    return await networkUpdate;
  } catch {
    return new Response("", {
      status: 504,
      statusText: "Asset unavailable while offline"
    });
  }
}

self.addEventListener("install", event => {
  event.waitUntil(precacheFiles().then(() => self.skipWaiting()));
});

self.addEventListener("activate", event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(
      keys
        .filter(key => key.startsWith(CACHE_PREFIX) && key !== STATIC_CACHE && key !== RUNTIME_CACHE)
        .map(key => caches.delete(key))
    );
    await self.clients.claim();
  })());
});

self.addEventListener("fetch", event => {
  const request = event.request;
  if (request.method !== "GET" || request.headers.has("range")) return;

  const url = new URL(request.url);

  if (request.mode === "navigate") {
    event.respondWith(handleNavigation(request));
    return;
  }

  if (url.origin === self.location.origin && approvedPublicCacheRequest(request)) {
    event.respondWith(handleSameOriginAsset(request));
  }
});

self.addEventListener("message", event => {
  if (event.data?.type === "SKIP_WAITING") self.skipWaiting();
  if (event.data?.type === "CLEAR_333_RUNTIME_CACHE") {
    event.waitUntil(caches.delete(RUNTIME_CACHE));
  }
});