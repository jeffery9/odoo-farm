/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class AgriGatingAudit extends Component {
    static template = "farm_ux.AgriGatingAudit";
    
    get weatherInfo() {
        const status = this.props.record.data.weather_gating_status;
        const config = {
            'safe': { icon: 'fa-sun-o', class: 'text-success', text: 'Safe' },
            'warning': { icon: 'fa-cloud', class: 'text-warning', text: 'Caution' },
            'blocked': { icon: 'fa-umbrella', class: 'text-danger', text: 'Blocked' },
            'none': { icon: 'fa-minus', class: 'text-muted', text: 'N/A' }
        };
        return config[status] || config['none'];
    }

    get complianceInfo() {
        const status = this.props.record.data.compliance_gating_status;
        const config = {
            'compliant': { icon: 'fa-shield', class: 'text-success', text: 'Compliant' },
            'warning': { icon: 'fa-exclamation-triangle', class: 'text-warning', text: 'Warning' },
            'blocked': { icon: 'fa-ban', class: 'text-danger', text: 'Violation' },
            'none': { icon: 'fa-circle-o-notch', class: 'text-muted', text: 'Pending' }
        };
        return config[status] || config['none'];
    }

    get iotInfo() {
        const status = this.props.record.data.iot_status;
        const config = {
            'connected': { icon: 'fa-wifi', class: 'text-success', text: 'Connected' },
            'offline': { icon: 'fa-times-circle', class: 'text-warning', text: 'Offline' },
            'critical': { icon: 'fa-bolt', class: 'text-danger', text: 'Alert' },
            'none': { icon: 'fa-power-off', class: 'text-muted', text: 'No Sensors' }
        };
        return config[status] || config['none'];
    }
}

export const agriGatingAudit = {
    component: AgriGatingAudit,
    additionalProps: (props) => {
        return {
            record: props.record,
        };
    },
};

registry.category("view_widgets").add("agri_gating_audit", agriGatingAudit);
