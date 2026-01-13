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
}
