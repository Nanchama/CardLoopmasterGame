const CACHE_NAME = "chronoloop-pwa-v6";
const OFFLINE_URL = "./index.html";
const ASSETS = ["./","./index.html","./manifest.webmanifest","./icon-192.png","./icon-512.png","./robots.txt"];

self.addEventListener("install", event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener("activate", event => {
  event.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key)))
  ));
  self.clients.claim();
});

self.addEventListener("fetch", event => {
  const req = event.request;
  if (req.method !== "GET") return;
  if (req.mode === "navigate") {
    event.respondWith(caches.match(OFFLINE_URL).then(cached => {
      if (cached) return cached;
      return fetch(req).catch(() => caches.match(OFFLINE_URL));
    }));
    return;
  }
  event.respondWith(caches.match(req).then(cached => {
    if (cached) return cached;
    return fetch(req).then(response => {
      const copy = response.clone();
      caches.open(CACHE_NAME).then(cache => cache.put(req, copy));
      return response;
    });
  }));
});
