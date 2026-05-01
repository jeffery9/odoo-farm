/** @odoo-module **/
import { registry } from "@web/core/registry";
registry.category("web_tour.tours").add('farm_crop_tour', {
    url: "/web",
    test: true,
    steps: () => [{ content: "Wait", trigger: '.o_main_navbar', run: () => {} }]
});
