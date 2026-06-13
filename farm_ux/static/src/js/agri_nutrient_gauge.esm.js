/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class AgriNutrientGauge extends Component {
    static template = "farm_ux.AgriNutrientGauge";

    get nutrients() {
        const data = this.props.record.data;
        return [
            { label: 'N', value: data.pure_n_qty || 0, color: '#27ae60' },
            { label: 'P', value: data.pure_p_qty || 0, color: '#2980b9' },
            { label: 'K', value: data.pure_k_qty || 0, color: '#f39c12' }
        ];
    }

    get maxValue() {
        // Find max value among N, P, K or default to 100
        const max = Math.max(...this.nutrients.map(n => n.value));
        return max > 100 ? max : 100;
    }

    getStrokeDash(value) {
        const percentage = (value / this.maxValue) * 100;
        return `${percentage}, 100`;
    }
}

export const agriNutrientGauge = {
    component: AgriNutrientGauge,
    additionalProps: (props) => {
        return {
            record: props.record,
        };
    },
};

registry.category("view_widgets").add("agri_nutrient_gauge", agriNutrientGauge);
