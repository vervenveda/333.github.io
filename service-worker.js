
const CACHE_PREFIX = "333-333-network-pwa-";
const CACHE_VERSION = `${CACHE_PREFIX}v3`;

const STATIC_CACHE = `${CACHE_VERSION}-static`;
const RUNTIME_CACHE = `${CACHE_VERSION}-runtime`;
const MAX_RUNTIME_ENTRIES = 60;

const CORE_SHELL = [
  "./",
  "./index.html",
  "./offline.html",
  "./manifest.webmanifest",
  "./install-app.js",
  "./register-service-worker.js",
  "./assets/icons/icon-192.png",
  "./assets/icons/icon-512.png",
  "./assets/icons/icon-maskable-512.png",
];

const APP_PAGES = [
  "./apps/HOLLO_333_direct_connect_index.html",
  "./apps/KANSEE_333_meeting_rooms_index.html",
  "./apps/Bazaar_Art_Live_index.html",
  "./apps/SIte_builder_index.html",
  "./apps/Bunya_digital_infrastructure_index.html",
  "./apps/EVen_mail_index.html",
];

const PRECACHE_URLS = [...CORE_SHELL, ...APP_PAGES];

function isCacheable(response) {
  return Boolean(
    response &&
    response.ok &&
    (response.type === "basic" || response.type === "default")
  );
}

async function putInCache(cacheName, request, response) {
  if (!isCacheable(response)) return;

  const cache = await caches.open(cacheName);
  await cache.put(request, response.clone());
}

async function trimCache(cacheName, maxEntries) {
  const cache = await caches.open(cacheName);
  const keys = await cache.keys();

  if (keys.length <= maxEntries) return;

  const entriesToDelete = keys.slice(0, keys.length - maxEntries);
  await Promise.all(entriesToDelete.map(request => cache.delete(request)));
}

async function precacheFiles() {
  const cache = await caches.open(STATIC_CACHE);

  const results = await Promise.allSettled(
    PRECACHE_URLS.map(async url => {
      const request = new Request(url, { cache: "reload" });
      const response = await fetch(request);

      if (!isCacheable(response)) {
        throw new Error(`Unable to precache ${url}: HTTP ${response.status}`);
      }

      await cache.put(request, response);
    })
  );

  const failed = results
    .map((result, index) => ({ result, url: PRECACHE_URLS[index] }))
    .filter(({ result }) => result.status === "rejected");

  if (failed.length) {
    console.warn(
      "[333 Network] Some files were not precached:",
      failed.map(({ url, result }) => ({
        url,
        reason: String(result.reason),
      }))
    );
  }

  const requiredMissing = [];
  for (const url of ["./index.html", "./offline.html"]) {
    if (!(await cache.match(url))) requiredMissing.push(url);
  }

  if (requiredMissing.length) {
    throw new Error(
      `Required offline files were not cached: ${requiredMissing.join(", ")}`
    );
  }
}

async function handleNavigation(request) {
  try {
    const response = await fetch(request);

    if (isCacheable(response)) {
      await putInCache(RUNTIME_CACHE, request, response);
      await trimCache(RUNTIME_CACHE, MAX_RUNTIME_ENTRIES);
    }

    return response;
  } catch {
    const cachedPage = await caches.match(request);
    if (cachedPage) return cachedPage;

    const offlinePage = await caches.match("./offline.html");
    if (offlinePage) return offlinePage;

    return new Response(
      "333 Network is offline and the requested page is not cached.",
      {
        status: 503,
        statusText: "Offline",
        headers: { "Content-Type": "text/plain; charset=utf-8" },
      }
    );
  }
}

async function handleSameOriginAsset(request) {
  const cached = await caches.match(request);

  const networkUpdate = fetch(request)
    .then(async response => {
      if (isCacheable(response)) {
        await putInCache(RUNTIME_CACHE, request, response);
        await trimCache(RUNTIME_CACHE, MAX_RUNTIME_ENTRIES);
      }
      return response;
    });

  if (cached) {
    networkUpdate.catch(() => {
      // The cached response is already being returned.
    });
    return cached;
  }

  try {
    return await networkUpdate;
  } catch {
    return new Response("", {
      status: 504,
      statusText: "Asset unavailable while offline",
    });
  }
}

self.addEventListener("install", event => {
  event.waitUntil(
    precacheFiles().then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", event => {
  event.waitUntil(
    (async () => {
      const keys = await caches.keys();

      await Promise.all(
        keys
          .filter(
            key =>
              key.startsWith(CACHE_PREFIX) &&
              key !== STATIC_CACHE &&
              key !== RUNTIME_CACHE
          )
          .map(key => caches.delete(key))
      );

      await self.clients.claim();
    })()
  );
});

self.addEventListener("fetch", event => {
  const request = event.request;

  if (request.method !== "GET") return;
  if (request.headers.has("range")) return;

  const url = new URL(request.url);

  if (request.mode === "navigate") {
    event.respondWith(handleNavigation(request));
    return;
  }

  if (url.origin === self.location.origin) {
    event.respondWith(handleSameOriginAsset(request));
  }
});

self.addEventListener("message", event => {
  if (event.data?.type === "SKIP_WAITING") {
    self.skipWaiting();
  }

  if (event.data?.type === "CLEAR_333_RUNTIME_CACHE") {
    event.waitUntil(caches.delete(RUNTIME_CACHE));
  }
});
