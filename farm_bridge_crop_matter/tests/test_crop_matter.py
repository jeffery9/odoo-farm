# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestCropMatterBridge(TransactionCase):

    def setUp(self):
        super(TestCropMatterBridge, self).setUp()
        self.crop_cycle = self.env['farm.crop.cycle'].create({
            'name': 'Organic Corn 2026 (2026年有机玉米生长周期)'
        })
        self.tracking = self.env['stock.matter.tracking'].create({
            'name': 'CARRIER-C01 (物理载体 C01)'
        })

    def test_bridge_field_binding(self):
        """ Verify crop cycle can be late-bound to a physical tracking node """
        self.tracking.write({'crop_cycle_id': self.crop_cycle.id})
        self.assertEqual(self.tracking.crop_cycle_id.id, self.crop_cycle.id)

    def test_graceful_degradation_on_delete(self):
        """ Verify ondelete set null safety prevents cascading deletions """
        self.tracking.write({'crop_cycle_id': self.crop_cycle.id})
        self.crop_cycle.unlink()
        self.assertFalse(self.tracking.crop_cycle_id)
        self.assertTrue(self.tracking.exists(), "Physical carrier must survive crop cycle deletion")
