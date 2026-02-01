/** @odoo-module **/

import {KanbanController} from "@web/views/kanban/kanban_controller";
import {KanbanRenderer} from "@web/views/kanban/kanban_renderer";
import {KanbanModel} from "@web/views/kanban/kanban_model";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";

// Enhanced Phase Kanban Widget with IoT Integration and Bus
export class PrecisionIotPhaseKanban extends KanbanRenderer {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        this.busService = useService("bus_service");
        this.channel = "precision_production/kpi_updates";
        this.iotChannel = "precision_iot/device_updates";

        // Subscribe to the main precision production channel
        this.busService.addChannel(this.channel);
        this.busService.on("notification", this, this.handleBusNotification);

        // Also subscribe to IoT device updates
        this.busService.addChannel(this.iotChannel);
        this.busService.on("notification", this, this.handleIotNotification);
    }

    // Handle bus notifications for precision production
    handleBusNotification(notifications) {
        for (const notification of notifications) {
            if (notification[0] === this.channel && notification[1].type === 'kpi_update') {
                // Force re-render when KPI data changes
                this.render();
            }
        }
    }

    // Handle IoT device notifications
    handleIotNotification(notifications) {
        let shouldRender = false;

        for (const notification of notifications) {
            if (notification[0] === this.iotChannel) {
                const deviceUpdates = notification[1];
                if (deviceUpdates && deviceUpdates.type === 'device_status') {
                    // Update device status icons and indicators in the kanban view
                    shouldRender = true;
                } else if (deviceUpdates && deviceUpdates.type === 'reading_update') {
                    // Update real-time readings displayed in kanban cards
                    shouldRender = true;
                }
            }
        }

        if (shouldRender) {
            this.render();
        }
    }
}

// Register the IoT-enhanced phase kanban component
registry
    .category("ir.ui.view_widgets")
    .add("precision_iot_phase_kanban", PrecisionIotPhaseKanban);