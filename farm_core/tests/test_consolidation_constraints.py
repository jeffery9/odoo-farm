# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestConsolidationConstraints(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestConsolidationConstraints, cls).setUpClass()
        cls.Product = cls.env['product.product']
        cls.Category = cls.env['product.category']
        cls.Lot = cls.env['stock.lot']
        cls.Location = cls.env['stock.location']
        cls.Tracking = cls.env['stock.matter.tracking']
        cls.Quant = cls.env['stock.quant']

        # 1. Strict Isolation Category
        cls.strict_category = cls.Category.create({
            'name': 'Strict Seeds',
            'consolidation_strategy': 'strict_isolation',
            'allow_cross_quality_mix': False
        })

        # 2. Mix Allowed but Cross-Quality Blocked Category
        cls.mix_blocked_category = cls.Category.create({
            'name': 'Mixed No Cross Quality',
            'consolidation_strategy': 'weighted_average',
            'allow_cross_quality_mix': False
        })

        # Create Products
        cls.product_seed = cls.Product.create({
            'name': 'Seed Batch A',
            'categ_id': cls.strict_category.id,
            'type': 'consu',
            'is_storable': True
        })

        cls.product_juice = cls.Product.create({
            'name': 'Juice Batch B',
            'categ_id': cls.mix_blocked_category.id,
            'type': 'consu',
            'is_storable': True
        })

        # Create Lots
        cls.lot_seed_a = cls.Lot.create({
            'name': 'LOT-SEED-01',
            'product_id': cls.product_seed.id,
            'quality_grade': 'grade_a'
        })
        cls.lot_seed_b = cls.Lot.create({
            'name': 'LOT-SEED-02',
            'product_id': cls.product_seed.id,
            'quality_grade': 'grade_a'
        })

        cls.lot_juice_a = cls.Lot.create({
            'name': 'LOT-JUICE-01',
            'product_id': cls.product_juice.id,
            'quality_grade': 'grade_a'
        })
        cls.lot_juice_b = cls.Lot.create({
            'name': 'LOT-JUICE-02',
            'product_id': cls.product_juice.id,
            'quality_grade': 'grade_b'
        })

        # Create internal staging location
        cls.location_vessel = cls.Location.create({
            'name': 'Staging Bin C',
            'usage': 'internal'
        })

    def test_01_strict_isolation_prevents_multiple_lots(self):
        """ Test that containers using 'strict_isolation' strategy block different lot insertions """
        tracking = self.Tracking.create({
            'vessel_phase': 'idle'
        })

        # Insert first Lot
        self.Quant.create({
            'product_id': self.product_seed.id,
            'location_id': self.location_vessel.id,
            'lot_id': self.lot_seed_a.id,
            'quantity': 1.0,
            'package_id': tracking.package_id.id
        })

        # Putting the same lot is allowed
        self.Quant.create({
            'product_id': self.product_seed.id,
            'location_id': self.location_vessel.id,
            'lot_id': self.lot_seed_a.id,
            'quantity': 2.0,
            'package_id': tracking.package_id.id
        })

        # Adding a different lot should be blocked by strict isolation
        with self.assertRaisesRegex(ValidationError, "Strict Isolation"):
            self.Quant.create({
                'product_id': self.product_seed.id,
                'location_id': self.location_vessel.id,
                'lot_id': self.lot_seed_b.id,
                'quantity': 1.0,
                'package_id': tracking.package_id.id
            })

    def test_02_cross_quality_blocking(self):
        """ Test that containers using allow_cross_quality_mix=False block mixing different grades """
        tracking = self.Tracking.create({
            'vessel_phase': 'idle'
        })

        # Insert Grade A
        self.Quant.create({
            'product_id': self.product_juice.id,
            'location_id': self.location_vessel.id,
            'lot_id': self.lot_juice_a.id,
            'quantity': 10.0,
            'package_id': tracking.package_id.id
        })

        # Adding Grade B should be blocked because allow_cross_quality_mix is False
        with self.assertRaisesRegex(ValidationError, "Mixing Blocked"):
            self.Quant.create({
                'product_id': self.product_juice.id,
                'location_id': self.location_vessel.id,
                'lot_id': self.lot_juice_b.id,
                'quantity': 5.0,
                'package_id': tracking.package_id.id
            })
