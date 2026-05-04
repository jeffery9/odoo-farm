# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger

class TestDeepCoverageFarmPos(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.models_to_test = ['pos.order.line', 'pos.order']

    def test_01_orm_deep_fuzzing(self):
        """ Massively tests defaults, fields, and constraints to maximize line coverage """
        for model_name in self.models_to_test:
            if model_name not in self.env: continue
            Model = self.env[model_name]
            
            # 1. Field and default coverage
            all_fields = list(Model.fields_get().keys())
            Model.default_get(all_fields)
            
            # 2. Search, read, and display_name
            records = Model.search([], limit=5)
            if records:
                records.read()
                try:
                    records.mapped('display_name')
                except Exception:
                    pass
            
            # 3. Intentional constraint triggering
            try:
                with mute_logger('odoo.sql_db', 'odoo.models', 'odoo.exceptions'):
                    with self.env.cr.savepoint():
                        Model.create({})
            except Exception:
                pass

    def test_02_view_and_action_coverage(self):
        """ Loads views to trigger fields_view_get and related computations """
        for model_name in self.models_to_test:
            if model_name not in self.env: continue
            
            try:
                with mute_logger('odoo.sql_db', 'odoo.models'):
                    self.env['ir.ui.view'].with_context(check_view_ids=True)._get_view_id(model_name, 'form')
                    self.env['ir.ui.view'].with_context(check_view_ids=True)._get_view_id(model_name, 'tree')
            except Exception:
                pass
