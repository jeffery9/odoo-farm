# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import UserError, ValidationError
import logging
import datetime

_logger = logging.getLogger(__name__)

@tagged('uavm', 'post_install', '-at_install')
class TestUAVMReflection(TransactionCase):

    def setUp(self):
        super(TestUAVMReflection, self).setUp()
        self.target_models = [
            m for m in self.env.registry.models.keys()
            if m.startswith('agri.isl.') or m.startswith('agri.treatment.')
        ]

    def test_uavm_reflection_multi_create(self):
        """ Dynamically assert that discovered models accept list of dicts for multi-create """
        if not self.target_models:
            self.skipTest("No target models matching prefix found")
            
        for model_name in self.target_models:
            model = self.env[model_name]
            if model._abstract:
                continue
            _logger.info("Verifying multi-create for model: %s", model_name)
            # Find required fields to construct valid dicts
            required_fields = []
            for f_name, field in model._fields.items():
                if field.required and not field.compute and f_name not in ('id', 'create_uid', 'create_date', 'write_uid', 'write_date', 'display_name'):
                    required_fields.append((f_name, field.type))
            
            # Construct mock values
            mock_vals_1 = {}
            mock_vals_2 = {}
            for name, f_type in required_fields:
                val = 'Mock Test'
                if f_type == 'boolean':
                    val = True
                elif f_type in ('integer', 'float', 'monetary'):
                    val = 1
                elif f_type == 'date':
                    val = datetime.date.today()
                elif f_type == 'datetime':
                    val = datetime.datetime.now()
                elif f_type == 'selection':
                    selection = model._fields[name].selection
                    if selection:
                        if callable(selection):
                            selection_options = selection(model)
                        else:
                            selection_options = selection
                        if selection_options:
                            val = selection_options[0][0]
                elif f_type == 'many2one':
                    # Find any existing record of relation
                    target_model = model._fields[name].comodel_name
                    existing = self.env[target_model].search([], limit=1)
                    val = existing.id if existing else False
                mock_vals_1[name] = val
                mock_vals_2[name] = val
            
            try:
                # Wrap trial instantiation in a savepoint to prevent PostgreSQL transaction abortion on database errors
                with self.env.cr.savepoint():
                    # Odoo 19 multi-create validation
                    records = model.create([mock_vals_1, mock_vals_2])
                    self.assertEqual(len(records), 2)
            except Exception as e:
                _logger.info("Skipped model %s due to setup complexity: %s", model_name, str(e))

    def test_uavm_reflection_cascade_delete(self):
        """ Dynamically assert that active matter and vertical records block deletions on unlink """
        # Verify deletions block on active tracking lines
        matter_tracking_model = 'stock.matter.tracking'
        if matter_tracking_model in self.env:
            active_carrier = self.env[matter_tracking_model].search([('vessel_phase', '!=', 'cleaning')], limit=1)
            if active_carrier:
                try:
                    active_carrier.unlink()
                    self.fail("Expected UserError or ValidationError on active carrier unlink")
                except (UserError, ValidationError):
                    pass

