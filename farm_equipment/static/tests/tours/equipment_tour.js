/** @odoo-module **/
import { registry } from "@web/core/registry";

registry.category("web_tour.tours").add('farm_equipment_tour', {
    url: "/web",
    test: true,
    steps: () => [
        {
            content: "Wait for the web client to load",
            trigger: '.o_main_navbar',
            run: () => {},
        }
    ]
});
