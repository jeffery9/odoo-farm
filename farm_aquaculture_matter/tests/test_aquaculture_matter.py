# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestAquacultureMatterBridge(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Product = cls.env['product.product']
        cls.fish_product = cls.Product.create({
            'name': 'Atlantic Salmon (三文鱼)',
            'type': 'consu'
        })
        cls.aqua_lot = cls.env['agri.isl.lot.aquaculture'].with_context(bypass_legacy_write_block=True).create({
            'name': 'POND-A1-2026',
            'product_id': cls.fish_product.id,
            'water_volume_m3': 2000.0,
            'total_biomass': 500.0,
            'gender': 'female',
        })
        cls.lss_unit = cls.env['farm.aquaculture.lss'].create({
            'name': 'LSS-BIOFILTER-001',
            'lss_type': 'biofilter',
        })

    def test_field_injection_and_saving(self):
        matter = self.env['stock.matter.tracking'].create({
            'name': 'LPN-AQUA-TEST-001',
            'aquaculture_asset_id': self.aqua_lot.id,
            'lss_unit_id': self.lss_unit.id,
        })
        self.assertEqual(matter.aquaculture_asset_id.id, self.aqua_lot.id)
        self.assertEqual(matter.lss_unit_id.id, self.lss_unit.id)
