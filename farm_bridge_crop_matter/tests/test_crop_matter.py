# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestCropMatterBridge(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.crop_cycle = cls.env['farm.crop.cycle'].create({
            'name': 'Autumn Wheat 2026 (2026秋小麦周期)',
        })
        
    def test_field_injection_and_saving(self):
        matter = self.env['stock.matter.tracking'].create({
            'name': 'LPN-CROP-TEST-001',
            'crop_cycle_id': self.crop_cycle.id,
        })
        self.assertEqual(matter.crop_cycle_id.id, self.crop_cycle.id)
