/** @odoo-module **/

import { Component, useState, onMounted, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

/**
 * AgriTraceabilityMap - Holographic DNA & Kinship Visualization
 * [US-TECH-DNA-06]
 */
export class AgriTraceabilityMap extends Component {
    setup() {
        super.setup();
        this.rpc = useService("rpc");
        this.notification = useService("notification");
        
        this.state = useState({
            nodes: [],
            edges: [],
            root_id: null,
            loading: true
        });

        onWillStart(async () => {
            await this.loadGraph();
        });
    }

    /**
     * Load recursive kinship and DNA data from the controller
     */
    async loadGraph() {
        this.state.loading = true;
        try {
            const lotId = this.props.record.data.id;
            if (!lotId) {
                this.state.loading = false;
                return;
            }

            const data = await this.rpc(`/agri/traceability/lot/${lotId}/graph`, {});
            
            if (data.error) {
                this.notification.add(data.error, { type: "danger" });
            } else {
                this.state.nodes = data.nodes || [];
                this.state.edges = data.edges || [];
                this.state.root_id = data.root_id;
            }
        } catch (error) {
            console.error("Traceability Map Error:", error);
        } finally {
            this.state.loading = false;
        }
    }

    static template = "AgriTraceabilityMap";
    static props = {
        ...standardFieldProps,
    };
}

// Register as a field widget
registry.category("fields").add("agri_traceability_map", {
    component: AgriTraceabilityMap,
});
