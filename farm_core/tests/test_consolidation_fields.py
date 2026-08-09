# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestConsolidationFields(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestConsolidationFields, cls).setUpClass()
        cls.Category = cls.env['product.category']
        cls.Tracking = cls.env['stock.matter.tracking']

    def test_category_and_tracking_fields_exist(self):
        category = self.Category.create({
            'name': 'Test Consolidate',
            'consolidation_strategy': 'strict_isolation',
            'allow_cross_quality_mix': True
        })
        self.assertEqual(category.consolidation_strategy, 'strict_isolation')
        self.assertTrue(category.allow_cross_quality_mix)

        tracking = self.Tracking.create({
            'biological_stage': 'growing',
            'animal_count': 15,
            'water_volume_m3': 2.5
        })
        self.assertEqual(tracking.biological_stage, 'growing')
        self.assertEqual(tracking.animal_count, 15)
        self.assertEqual(tracking.water_volume_m3, 2.5)
