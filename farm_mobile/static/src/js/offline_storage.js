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
                // 新增：任务缓存表 [US-07-07]
                if (!db.objectStoreNames.contains("tasks_cache")) {
                    db.createObjectStore("tasks_cache", { keyPath: "id" });
                }
                // 新增：离线数据变更队列 [US-07-08]
                if (!db.objectStoreNames.contains("input_changes")) {
                    db.createObjectStore("input_changes", { keyPath: "id", autoIncrement: true });
                }
                // 新增：知识库离线缓存 [US-07-07]
                if (!db.objectStoreNames.contains("knowledge_cache")) {
                    db.createObjectStore("knowledge_cache", { keyPath: "id" });
                }
                // 新增：离线地图瓦片缓存 [US-26-04]
                if (!db.objectStoreNames.contains("map_tiles")) {
                    db.createObjectStore("map_tiles", { keyPath: "url" });
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

    static async cacheTasks(tasks) {
        const db = await this.openDB();
        const tx = db.transaction("tasks_cache", "readwrite");
        const store = tx.objectStore("tasks_cache");
        tasks.forEach(task => store.put(task));
    }

    static async saveInputChange(change) {
        const db = await this.openDB();
        const tx = db.transaction("input_changes", "readwrite");
        tx.objectStore("input_changes").add(change);
    }

    static async cacheKnowledge(articles) {
        const db = await this.openDB();
        const tx = db.transaction("knowledge_cache", "readwrite");
        const store = tx.objectStore("knowledge_cache");
        articles.forEach(art => store.put(art));
    }

    static async getOfflineKnowledge() {
        const db = await this.openDB();
        const tx = db.transaction("knowledge_cache", "readonly");
        return new Promise(resolve => {
            tx.objectStore("knowledge_cache").getAll().onsuccess = (e) => resolve(e.target.result);
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
