/** @odoo-module **/

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // 1. 注册 Service Worker
        navigator.serviceWorker.register('/farm_mobile/static/src/js/sw.js')
            .then(reg => console.log('PWA: Service Worker registered!', reg))
            .catch(err => console.log('PWA: Registration failed.', err));

        // 2. 动态注入 Manifest Link
        const link = document.createElement('link');
        link.rel = 'manifest';
        link.href = '/farm_mobile/static/manifest.json';
        document.head.appendChild(link);
    });
}
