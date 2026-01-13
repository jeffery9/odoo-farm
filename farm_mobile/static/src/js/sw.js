const CACHE_NAME = 'farm-mobile-v1';
const ASSETS_TO_CACHE = [
  '/web',
  '/farm_mobile/static/src/scss/farm_mobile.scss',
  '/farm_mobile/static/description/icon_192.png'
];

// 安装阶段：预缓存资源
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
});

// 激活阶段：清理旧缓存
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((name) => {
          if (name !== CACHE_NAME) return caches.delete(name);
        })
      );
    })
  );
});

// 拦截请求：优先从缓存读取 (Cache First)
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});

// 后台同步：网络恢复时触发 [US-07-06]
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-field-evidence') {
    event.waitUntil(syncEvidenceData());
  }
});

async function syncEvidenceData() {
  console.log('PWA: Syncing offline evidence data...');
  // 这里的逻辑通常涉及从 IndexedDB 读取离线数据并 fetch 到后端
  // 实际生产中需配合本地数据库如 idb 实现
}
