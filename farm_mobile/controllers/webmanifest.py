from odoo.addons.web.controllers.webmanifest import WebManifest
from odoo.http import request

class FarmWebManifest(WebManifest):

    def _get_service_worker_content(self):
        """ 
        通过继承原生控制器，向 Service Worker 追加自定义逻辑 [US-07-06]
        这样做既利用了 Odoo 19 的 PWA 框架，又实现了业务扩展。
        """
        body = super()._get_service_worker_content()
        
        # 追加后台同步和自定义缓存逻辑
        custom_logic = """
// --- Farm Mobile Custom Logic ---
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-field-evidence') {
    event.waitUntil(syncEvidenceData());
  }
});

async function syncEvidenceData() {
  console.log('PWA: Syncing offline evidence data...');
  / IndexedDB 数据并上传
}
"""
        return body + custom_logic