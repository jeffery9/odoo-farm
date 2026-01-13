/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState } from "@odoo/owl";
import { OfflineStorage } from "./offline_storage";

export class FarmMobileCheckin extends Component {
    static template = "farm_mobile.CheckinButton";

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.state = useState({
            is_loading: false,
            gps_info: "",
        });
    }

    async _getGPS() {
        return new Promise((resolve, reject) => {
            if (!navigator.geolocation) {
                reject(new Error("GPS not supported"));
            }
            navigator.geolocation.getCurrentPosition(
                (pos) => resolve(pos.coords),
                (err) => reject(err),
                { enableHighAccuracy: true, timeout: 10000 }
            );
        });
    }

    async _capturePhoto() {
        return new Promise((resolve) => {
            const fileInput = document.getElementById('mobile_camera_input');
            fileInput.onchange = (e) => {
                const file = e.target.files[0];
                if (!file) {
                    resolve(null);
                    return;
                }
                const reader = new FileReader();
                reader.onload = () => resolve(reader.result.split(',')[1]);
                reader.readAsDataURL(file);
            };
            fileInput.click();
        });
    }

    async onSiteCheckin() {
        this.state.is_loading = true;
        try {
            const coords = await this._getGPS();
            const photo = await this._capturePhoto();
            if (!photo) {
                this.state.is_loading = false;
                return;
            }
            await this.orm.call("mrp.production", "action_mobile_check_in", [
                this.props.record.res_id, coords.latitude, coords.longitude, photo
            ]);
            this.notification.add("Site Check-in Successful!", { type: "success" });
            window.location.reload();
        } catch (err) {
            this.notification.add("Check-in Failed: " + err.message, { type: "danger" });
        } finally {
            this.state.is_loading = false;
        }
    }

    async onCaptureEvidence() {
        this.state.is_loading = true;
        try {
            const coords = await this._getGPS();
            const photo = await this._capturePhoto();
            if (!photo) {
                this.state.is_loading = false;
                return;
            }
            
            try {
                // 尝试在线上传
                await this.orm.call("mrp.production", "action_mobile_capture_evidence", [
                    this.props.record.res_id, coords.latitude, coords.longitude, photo
                ]);
                this.notification.add("Evidence Recorded!", { type: "success" });
            } catch (online_err) {
                // 在线失败，转存离线队列 [US-07-06]
                await OfflineStorage.saveToQueue({
                    res_id: this.props.record.res_id,
                    lat: coords.latitude,
                    lng: coords.longitude,
                    photo: photo
                });
                
                // 注册后台同步 (仅部分浏览器支持)
                if ('serviceWorker' in navigator && 'SyncManager' in window) {
                    const reg = await navigator.serviceWorker.ready;
                    await reg.sync.register('sync-field-evidence');
                }
                
                this.notification.add("Offline Mode: Evidence saved locally and will sync when network is restored.", { type: "warning", sticky: true });
            }
            window.location.reload();
        } catch (err) {
            this.notification.add("Evidence Failed: " + err.message, { type: "danger" });
        } finally {
            this.state.is_loading = false;
        }
    }
}

registry.category("view_widgets").add("farm_mobile_checkin", {
    component: FarmMobileCheckin,
});