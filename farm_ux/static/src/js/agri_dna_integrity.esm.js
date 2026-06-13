/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class AgriDnaIntegrity extends Component {
    static template = "farm_ux.AgriDnaIntegrity";
    
    get score() {
        return Math.round(this.props.record.data.dna_integrity_score || 0);
    }

    get scoreColor() {
        if (this.score >= 90) return '#27ae60'; // Green
        if (this.score >= 70) return '#f1c40f'; // Yellow
        return '#e74c3c'; // Red
    }

    get statusText() {
        if (this.score >= 90) return 'PRISTINE DNA';
        if (this.score >= 70) return 'VERIFIED';
        return 'TAINTED / AT RISK';
    }

    get dashArray() {
        const percentage = this.score;
        return `${percentage}, 100`;
    }
}

export const agriDnaIntegrity = {
    component: AgriDnaIntegrity,
    additionalProps: (props) => {
        return {
            record: props.record,
        };
    },
};

registry.category("view_widgets").add("agri_dna_integrity", agriDnaIntegrity);
