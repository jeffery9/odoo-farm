# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestLivestockMatterBridge(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.livestock_asset = cls.env['farm.livestock.asset'].create({
            'ear_tag_code': 'TAG-LIVESTOCK-2026',
            'species': 'beef_cattle (肉牛)',
        })
        
    def test_field_injection_and_saving(self):
        matter = self.env['stock.matter.tracking'].create({
            'name': 'LPN-LIVESTOCK-TEST-001',
            'livestock_asset_id': self.livestock_asset.id,
        })
        self.assertEqual(matter.livestock_asset_id.id, self.livestock_asset.id)
