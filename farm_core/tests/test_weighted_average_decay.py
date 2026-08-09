# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged

@tagged('post_install', '-at_install')
class TestWeightedAverageDecay(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestWeightedAverageDecay, cls).setUpClass()
        cls.Product = cls.env['product.product']
        cls.Category = cls.env['product.category']
        cls.Lot = cls.env['stock.lot']
        cls.Location = cls.env['stock.location']
        cls.Tracking = cls.env['stock.matter.tracking']
        cls.Quant = cls.env['stock.quant']

        cls.bulk_category = cls.Category.create({
            'name': 'Bulk Liquids',
            'consolidation_strategy': 'weighted_average',
            'allow_cross_quality_mix': True
        })

        cls.product_juice = cls.Product.create({
            'name': 'Raw Apple Juice',
            'categ_id': cls.bulk_category.id,
            'type': 'consu',
            'is_storable': True
        })

        cls.lot_apple_1 = cls.Lot.create({
            'name': 'LOT-APP-01',
            'product_id': cls.product_juice.id,
            'certification_type': 'organic'
        })
        cls.lot_apple_2 = cls.Lot.create({
            'name': 'LOT-APP-02',
            'product_id': cls.product_juice.id,
            'certification_type': 'non_certified'
        })

        cls.location_vat = cls.Location.create({
            'name': 'Vat Tank 10',
            'usage': 'internal'
        })

    def test_weighted_average_accumulates_and_decays_dna(self):
        tracking = self.Tracking.create({
            'vessel_phase': 'idle',
            'current_weight': 0.0,
            'is_consolidated': False
        })

        # 1. Load Lot 1 (100kg, DNA 100.0)
        self.Quant.create({
            'product_id': self.product_juice.id,
            'location_id': self.location_vat.id,
            'lot_id': self.lot_apple_1.id,
            'quantity': 100.0,
            'package_id': tracking.package_id.id
        })

        # 2. Load Lot 2 (200kg, DNA 80.0)
        self.Quant.create({
            'product_id': self.product_juice.id,
            'location_id': self.location_vat.id,
            'lot_id': self.lot_apple_2.id,
            'quantity': 200.0,
            'package_id': tracking.package_id.id
        })

        # Expected weight = 100 + 200 = 300
        self.assertEqual(tracking.current_weight, 300.0)
        self.assertTrue(tracking.is_consolidated)

        # Expected DNA = ((100 * 100.0 + 200 * 80.0) / 300) * 0.90 = (26000 / 300) * 0.90 = 86.666 * 0.90 = 78.0
        # DNA decay calculation should execute automatically on write.
        self.assertAlmostEqual(tracking.dna_integrity_score, 78.0, places=1)
