const CACHE_NAME = 'saji-cache-v3'; 
const ASSETS_TO_CACHE = [
    '/',
    '/static/style.css',
    '/static/app.js',
    '/static/icons/icon-192.png',
    '/static/icons/icon-512.png'
];

// 1. Simpan file ke cache saat pertama kali di-install
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
  self.skipWaiting(); 
});

// 2. Hapus cache versi lama kalau ada update baru
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            return caches.delete(cache);
          }
        })
      );
    })
  );
  self.clients.claim(); 
});

// 3. Ambil dari internet, kalau gagal (offline), ambil dari cache
self.addEventListener('fetch', (event) => {
  event.respondWith(
    fetch(event.request).catch(() => {
      return caches.match(event.request);
    })
  );
});