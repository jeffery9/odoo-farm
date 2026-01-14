/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class AgriSpatialGauge extends Component {
    get strokeDasharray() {
        const rate = this.props.record.data.spatial_compliance_rate || 0;
        return `${rate}, 100`;
    }

    get gaugeColor() {
        const rate = this.props.record.data.spatial_compliance_rate || 0;
        if (rate >= 95) return "#27ae60"; // Green
        if (rate >= 80) return "#f39c12"; // Orange
        return "#e74c3c"; // Red
    }
}

export const agriSpatialGauge = {
    component: AgriSpatialGauge,
    additionalProps: (props) => {
        return {
            record: props.record,
        };
    },
};

registry.category("view_widgets").add("agri_spatial_gauge", agriSpatialGauge);
