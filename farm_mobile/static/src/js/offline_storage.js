/** @odoo-module **/

export class OfflineStorage {
    static async openDB() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open("FarmOfflineDB", 1);
            request.onupgradeneeded = (e) => {
                const db = e.target.result;
                if (!db.objectStoreNames.contains("evidence_queue")) {
                    db.createObjectStore("evidence_queue", { keyPath: "id", autoIncrement: true });
                }
            };
            request.onsuccess = (e) => resolve(e.target.result);
            request.onerror = (e) => reject(e.target.error);
        });
    }

    static async saveToQueue(data) {
        const db = await this.openDB();
        return new Promise((resolve, reject) => {
            const tx = db.transaction("evidence_queue", "readwrite");
            tx.objectStore("evidence_queue").add(data);
            tx.oncomplete = () => resolve();
            tx.onerror = () => reject();
        });
    }

    static async syncAll(orm) {
        const db = await this.openDB();
        const tx = db.transaction("evidence_queue", "readonly");
        const store = tx.objectStore("evidence_queue");
        const allItems = await new Promise(resolve => {
            store.getAll().onsuccess = (e) => resolve(e.target.result);
        });

        for (const item of allItems) {
            try {
                await orm.call("mrp.production", "action_mobile_capture_evidence", [
                    item.res_id, item.lat, item.lng, item.photo
                ]);
                // 成功后删除
                const delTx = db.transaction("evidence_queue", "readwrite");
                delTx.objectStore("evidence_queue").delete(item.id);
            } catch (err) {
                console.error("PWA: Failed to sync item", item.id, err);
            }
        }
    }
}
