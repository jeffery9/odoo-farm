/** @odoo-module **/

import {KanbanController} from "@web/views/kanban/kanban_controller";
import {KanbanRenderer} from "@web/views/kanban/kanban_renderer";
import {KanbanModel} from "@web/views/kanban/kanban_model";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";

// Modern Execution Dashboard Renderer
class PrecisionExecutionDashboardRenderer extends KanbanRenderer {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        this.busService = useService("bus_service");
        this.channel = "precision_production/kpi_updates";

        // Subscribe to the bus channel
        this.busService.addChannel(this.channel);
        this.busService.on("notification", this, this.handleBusNotification);
    }

    // Handle bus notifications
    handleBusNotification(notifications) {
        for (const notification of notifications) {
            if (notification[0] === this.channel && notification[1].type === 'kpi_update') {
                this.updateKpiData(notification[1].data);
            }
        }
    }

    // Update KPI data from bus notifications
    updateKpiData(kpiData) {
        if (this.state.data && kpiData && Array.isArray(kpiData)) {
            // Update the records with new KPIs from the bus
            this.state.data.records.forEach(record => {
                const updatedRecord = kpiData.find(r => r.id === record.data.id);
                if (updatedRecord) {
                    // Update only the KPI fields that have changed
                    record.data.yield_confidence = updatedRecord.yield_confidence;
                    record.data.efficiency_index = updatedRecord.efficiency_index;
                    record.data.process_status = updatedRecord.process_status;
                    record.data.active_recipe_phase_id = updatedRecord.active_recipe_phase_id;
                    record.data.progress_percentage = updatedRecord.progress_percentage;
                }
            });

            // Trigger a re-render to show updated data
            this.render();
        }
    }
}

// Register the custom renderer
registry
    .category("ir.ui.view_widgets")
    .add("precision_execution_dashboard", PrecisionExecutionDashboardRenderer);

// Phase Timeline Widget with Bus Integration
import {Component, useState, onMounted, onWillUnmount} from "@odoo/hoot";

export class PrecisionPhaseTimeline extends Component {
    setup() {
        this.state = useState({
            phases: this.props.value || [],
            selectedPhase: null,
        });

        // Add bus service for real-time updates
        this.busService = useService("bus_service");
        this.channel = "precision_production/kpi_updates";

        // Subscribe to the bus channel
        this.busService.addChannel(this.channel);
        this.busService.on("notification", this, this.handleBusNotification);

        onMounted(() => {
            this.updateTimeline();
        });
    }

    // Handle bus notifications for phase updates
    handleBusNotification(notifications) {
        for (const notification of notifications) {
            if (notification[0] === this.channel && notification[1].type === 'kpi_update') {
                // Update timeline when KPI data changes
                this.updateTimeline();
            }
        }
    }

    updateTimeline() {
        // Process phases to create timeline visualization
        const phases = this.state.phases.sort((a, b) =>
            (a.sequence || 0) - (b.sequence || 0)
        );

        this.state.phases = phases.map((phase, index) => ({
            ...phase,
            position: index,
            isCompleted: phase.state === "done",
            isInProgress: phase.state === "progress",
            isUpcoming: phase.state === "pending",
        }));
    }

    selectPhase(phase) {
        this.state.selectedPhase = phase;
        // Trigger phase detail view
        this.props.onSelect && this.props.onSelect(phase);
    }
}

// Register the timeline component
registry
    .category("ir.ui.view_widgets")
    .add("precision_phase_timeline", PrecisionPhaseTimeline);

// Phase Kanban Widget with progress visualization and Bus Integration
export class PrecisionPhaseKanban extends Component {
    setup() {
        this.state = useState({
            phases: this.props.value || [],
        });

        // Add bus service for real-time updates
        this.busService = useService("bus_service");
        this.channel = "precision_production/kpi_updates";

        // Subscribe to the bus channel
        this.busService.addChannel(this.channel);
        this.busService.on("notification", this, this.handleBusNotification);
    }

    // Handle bus notifications for phase updates
    handleBusNotification(notifications) {
        for (const notification of notifications) {
            if (notification[0] === this.channel && notification[1].type === 'kpi_update') {
                // Force re-render when KPI data changes
                this.render();
            }
        }
    }
}

// Register the phase kanban component
registry
    .category("ir.ui.view_widgets")
    .add("precision_phase_kanban", PrecisionPhaseKanban);