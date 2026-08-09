# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestStockLotBridge(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestStockLotBridge, cls).setUpClass()
        cls.Product = cls.env['product.product']
        cls.Lot = cls.env['stock.lot']
        cls.Location = cls.env['stock.location']
        cls.Tracking = cls.env['stock.matter.tracking']
        cls.Quant = cls.env['stock.quant']

        # Create test products
        cls.product_apple = cls.Product.create({
            'name': 'Organic Red Apple',
            'type': 'consu',
            'is_storable': True
        })

        # Create test lots
        cls.lot_a = cls.Lot.create({
            'name': 'LOT-APP-101',
            'product_id': cls.product_apple.id
        })

        # Create test location
        cls.location_vessel = cls.Location.create({
            'name': 'Staging Bin B',
            'usage': 'internal'
        })

    def test_decoupled_compatibility_bridge_and_write_locks(self):
        """ Verify Lot physical properties are computed from Matter Tracking, and legacy writes are blocked """
        # Create tracking vessel with physical profile
        tracking = self.Tracking.create({
            'vessel_phase': 'idle',
            'current_weight': 120.5,
            'life_stage': 'mature',
            'last_gps_lat': 41.25,
            'last_gps_lng': -73.98
        })

        # Put grapes lot into the tracking container
        self.Quant.create({
            'product_id': self.product_apple.id,
            'location_id': self.location_vessel.id,
            'lot_id': self.lot_a.id,
            'quantity': 1.0,
            'package_id': tracking.package_id.id
        })

        # Test read bridge
        self.assertEqual(self.lot_a.current_weight, 120.5)
        self.assertEqual(self.lot_a.life_stage, 'mature')
        self.assertEqual(self.lot_a.last_gps_lat, 41.25)

        # Test legacy write blocks
        with self.assertRaisesRegex(UserError, "Weight is now managed dynamically by Matter Tracking"):
            self.lot_a.write({'current_weight': 250.0})

        with self.assertRaisesRegex(UserError, "GPS positioning is now managed dynamically by Matter Tracking"):
            self.lot_a.write({'last_gps_lat': 42.0})
