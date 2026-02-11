self.addEventListener('install', (e) => {
  console.log('[Service Worker] Installing Service Worker ...', e);
  e.waitUntil(caches.open('pwa-cache').then(cache => cache.addAll(['/wireless_arming'])));
});

self.addEventListener('fetch', (e) => {
  console.log('[Service Worker] Fetching something ...', e);
  e.respondWith(caches.match(e.request).then(response => response || fetch(e.request)));
});
