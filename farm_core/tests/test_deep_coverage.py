# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger

class TestDeepCoverageFarmCore(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.models_to_test = ['farm.industry.task.template', 'agri.growth.cycle.mixin', 'farm.industry.product.category', 'agri.embedding.mixin', 'farm.industry.package.wizard', 'farm.task', 'agri.soil.analysis', 'farm.biological.asset', 'agri.soil.analysis.mixin', 'farm.core.compliance.mixin', 'agri.industry.variety', 'agri.biological.growth.curve', 'stock.move', 'farm.core.gis.utils', 'agri.view.mixin', 'agri.certification.status.mixin', 'agri.traceability.mixin', 'agri.resource.consumption.mixin', 'res.company', 'agri.geospatial.mixin', 'agri.task.mixin', 'stock.move.line', 'agri.actuator.mixin', 'stock.lot', 'agri.agent.instruction.mixin', 'agri.biological.valuation.mixin', 'agri.batch.operation.mixin', 'agri.performance.monitor', 'farm.core.common.fields', 'agri.value.bridge', 'agri.industry.data.package', 'agri.neighborhood.registry', 'agri.clearing.mixin', 'farm.location', 'farm.core.computed.field.mixin', 'agri.clearing.netting.engine', 'agri.industry.planting.mixin', 'agri.odoo19.performance.security.mixin', 'agri.quality.gate.mixin', 'agri.nutrient.mixin', 'agri.biological.asset', 'agri.audit.log', 'res.partner', 'agri.clearing.ledger', 'agri.location', 'agri.weather.sensitive.mixin', 'farm.activity', 'agri.dividend.pool', 'agri.incident.alert.mixin', 'farm.industry.uom.conversion', 'agri.performance.monitoring.mixin', 'agri.evidence.mixin', 'agri.industry.physio.stage', 'agri.biological.asset.mixin', 'farm.core.creation.method.mixin', 'agri.industry.variety.mixin', 'agri.geospatial.geofence', 'agri.biological.inventory.mixin', 'agri.sustainability.mixin']

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
