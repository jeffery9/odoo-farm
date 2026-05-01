/** @odoo-module **/
import { registry } from "@web/core/registry";

registry.category("web_tour.tours").add('agri_intervention_tour', {
    url: "/web",
    test: true,
    steps: () => [
        {
            content: "Wait for the web client to load",
            trigger: '.o_main_navbar',
            run: () => {},
        },
        {
            content: "Open Manufacturing / Operations App",
            trigger: '.o_app[data-menu-xmlid="mrp.menu_mrp_root"]',
            run: "click",
        },
        {
            content: "Wait for list view to load",
            trigger: '.o_list_view',
            run: () => {},
        },
        {
            content: "Click Create button",
            trigger: 'button.o_list_button_add',
            run: "click",
        },
        {
            content: "Wait for form view",
            trigger: '.o_form_view',
            run: () => {},
        }
    ]
});
