/**
 * Service Worker — Poultry India Expo 2026 Offline Cache
 * Caches all app assets using relative paths for GitHub Pages subpath compatibility.
 */

const CACHE_NAME = 'poultry-expo-offline-v2';

const CORE_ASSETS = [
  './',
  './index.html',
  './app.css',
  './app.js',
  './rules_engine.js',
  './manifest.json',
  './assets/app_icon.svg',
  './assets/shed_card_mock.svg',
  './assets/feed_mill_coa_mock.svg',
  './assets/oem_telemetry_mock.svg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(CORE_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME)
          .map((key) => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request, { ignoreSearch: true }).then((cached) => {
      if (cached) return cached;
      return fetch(event.request)
        .then((response) => {
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
          return response;
        })
        .catch(() => caches.match('./index.html'));
    })
  );
});
