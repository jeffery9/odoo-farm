# -*- coding: utf-8 -*-
# filepath: odoo-farm-dev/farm_core/tests/test_menu_reorganization_audit.py
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError

@tagged('standard', 'post_install')
class TestMenuReorganizationAudit(TransactionCase):

    def setUp(self):
        super(TestMenuReorganizationAudit, self).setUp()
        self.settings = self.env['res.config.settings'].create({})

    def test_01_verify_app_flatness_and_depth(self):
        """ Verify that the customized App tools have a maximum database menu depth of 3 levels (Root -> Category -> Leaf) """
        root_menus = self.env['ir.ui.menu'].search([('parent_id', '=', False)])
        
        # Target our refactored/specialized agricultural apps
        target_app_names = ['Agricultural Processing', 'Processing & Fermentation']
        active_apps = root_menus.filtered(lambda m: m.name in target_app_names)
        
        for app in active_apps:
            for sub_1 in app.child_id: # Level 1 (Category, e.g. Operations)
                for sub_2 in sub_1.child_id: # Level 2 (Leaf Action, e.g. Processing Tasks)
                    self.assertFalse(
                        sub_2.child_id, 
                        f"Menu depth exceeded! App '{app.name}' -> '{sub_1.name}' -> '{sub_2.name}' has nested child menu which violates Odoo's 3-level golden database standard!"
                    )
                    
        # Also verify that all menus in farm_esg_compliance have a maximum depth of 3 (Root -> Category -> Leaf)
        esg_compliance_xml_ids = self.env['ir.model.data'].search([
            ('module', '=', 'farm_esg_compliance'), 
            ('model', '=', 'ir.ui.menu')
        ])
        esg_compliance_menus = self.env['ir.ui.menu'].search([('id', 'in', esg_compliance_xml_ids.mapped('res_id'))])
        for menu in esg_compliance_menus:
            if menu.action: # Functional Leaf Action
                self.assertTrue(menu.parent_id, f"Compliance Menu '{menu.name}' has no parent category!")
                self.assertTrue(menu.parent_id.parent_id, f"Compliance Menu '{menu.name}' -> parent '{menu.parent_id.name}' has no root App!")
                # Support both standalone Root Apps (parent is NULL) and platform-wrapped Root Apps (parent of root is NULL)
                if menu.parent_id.parent_id.parent_id:
                    self.assertFalse(
                        menu.parent_id.parent_id.parent_id.parent_id, 
                        f"Compliance Menu '{menu.name}' exceeds the golden 3-level depth limit in the business App (parent of grandparent has parent: {menu.parent_id.parent_id.parent_id.parent_id.name})!"
                    )

    def test_02_no_circular_menus(self):
        """ Verify that the entire menu tree has no circular dependencies (DAG) """
        all_menus = self.env['ir.ui.menu'].search([])
        for menu in all_menus:
            current = menu
            path = []
            while current.parent_id:
                self.assertNotIn(
                    current.id, 
                    path, 
                    f"Circular reference detected in menu '{menu.name}' (ID: {menu.id})!"
                )
                path.append(current.id)
                current = current.parent_id

    def test_03_de_industrialization_terminology_check(self):
        """ Verify that no industrial terminologies exist in active menus """
        forbidden_words = ['work order', 'work center', '工单', '工作中心']
        all_menus = self.env['ir.ui.menu'].search([])
        for menu in all_menus:
            for word in forbidden_words:
                self.assertNotIn(
                    word, 
                    menu.name.lower(), 
                    f"Menu '{menu.name}' violates de-industrialization by using '{word}'!"
                )
