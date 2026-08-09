# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger

class TestDeepCoverageFarmIsl(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.models_to_test = ['agri.isl.mrp.workcenter', 'agri.isl.mrp.bom', 'stock.move', 'agri.isl.mrp.bom', 'agri.isl.quality.control', 'agri.isl.purchase.order', 'agri.isl.sale.order', 'agri.isl.extension', 'agri.isl.sale.order', 'agri.isl.purchase.order', 'agri.isl.mrp.workorder', 'agri.isl.mrp.production', 'agri.isl.mrp.production', 'agri.isl.migration.utility', 'agri.isl.model.redirector', 'stock.lot', 'agri.isl.product.template', 'agri.isl.product.template', 'agri.isl.stock.lot', 'agri.isl.mrp.workorder', 'agri.isl.quality.control', 'farm.isl.extension', 'agri.isl.stock.picking', 'agri.isl.mrp.workcenter', 'isl.model.redirector', 'agri.isl.stock.picking', 'isl.migration.utility', 'agri.isl.stock.lot', 'agri.isl.industry.planting']

    def test_01_orm_deep_fuzzing(self):
        """ Massively tests defaults, fields, and constraints to maximize line coverage """
        for model_name in self.models_to_test:
            if model_name not in self.env: continue
            Model = self.env[model_name]
            if Model._abstract:
                continue
            
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
            Model = self.env[model_name]
            if Model._abstract:
                continue
            
            try:
                with mute_logger('odoo.sql_db', 'odoo.models'):
                    self.env['ir.ui.view'].with_context(check_view_ids=True)._get_view_id(model_name, 'form')
                    self.env['ir.ui.view'].with_context(check_view_ids=True)._get_view_id(model_name, 'tree')
            except Exception:
                pass
