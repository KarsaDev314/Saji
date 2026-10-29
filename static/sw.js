const CACHE_NAME = 'saji-cache-v2'; // Naikin versinya biar cache lama kehapus

self.addEventListener('install', (event) => {
  self.skipWaiting(); // Paksa SW baru langsung aktif
});

self.addEventListener('activate', (event) => {
  event.waitUntil(clients.claim()); // Ambil kendali halaman langsung
});

self.addEventListener('fetch', (event) => {
  // Biarin lewat aja dulu, nggak usah nge-cache apa-apa
  // biar nggak ada error file not found
  event.respondWith(fetch(event.request).catch(() => {
      return caches.match(event.request);
  }));
});