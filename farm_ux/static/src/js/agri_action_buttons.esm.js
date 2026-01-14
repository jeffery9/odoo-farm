/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils";

export class AgriActionButtons extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            isHolding: false
        });
    }

    get canStart() {
        const data = this.props.record.data;
        return !data.is_working && data.state === 'confirmed' && data.simplified_state !== 'done';
    }

    get canStop() {
        return this.props.record.data.is_working;
    }

    get canFinish() {
        const data = this.props.record.data;
        return data.state === 'confirmed' || data.state === 'progress';
    }

    async onStartWork() {
        this.vibrate(50);
        await this.props.record.model.orm.call(
            this.props.record.resModel,
            'action_start_work',
            [this.props.record.resId]
        );
        await this.props.record.load();
    }

    async onStopWork() {
        this.vibrate([50, 100, 50]);
        await this.props.record.model.orm.call(
            this.props.record.resModel,
            'action_stop_work',
            [this.props.record.resId]
        );
        await this.props.record.load();
    }

    async onFinishWork() {
        this.vibrate(200);
        await this.props.record.model.orm.call(
            this.props.record.resModel,
            'button_mark_done',
            [this.props.record.resId]
        );
        await this.props.record.load();
    }

    vibrate(pattern) {
        if ("vibrate" in navigator) {
            navigator.vibrate(pattern);
        }
    }
}

export const agriActionButtons = {
    component: AgriActionButtons,
    additionalProps: (props) => {
        return {
            record: props.record,
        };
    },
};

registry.category("view_widgets").add("agri_action_buttons", agriActionButtons);
