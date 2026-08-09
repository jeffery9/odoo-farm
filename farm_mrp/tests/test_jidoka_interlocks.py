# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestJidokaInterlocks(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestJidokaInterlocks, cls).setUpClass()
        cls.Product = cls.env['product.product']
        cls.Lot = cls.env['stock.lot']
        cls.Location = cls.env['stock.location']
        cls.Tracking = cls.env['stock.matter.tracking']
        cls.Quant = cls.env['stock.quant']

        cls.product_test = cls.Product.create({
            'name': 'Test Grain',
            'type': 'consu',
            'is_storable': True
        })

        cls.lot_grain = cls.Lot.create({
            'name': 'LOT-GRAIN-99',
            'product_id': cls.product_test.id
        })

        cls.location_silo = cls.Location.create({
            'name': 'Silo Sector Z',
            'usage': 'internal'
        })

    def test_locked_vessel_prevents_movements(self):
        tracking = self.Tracking.create({
            'vessel_phase': 'idle',
            'is_vessel_locked': False
        })

        # Add physical quantities inside the vessel when unlocked
        quant = self.Quant.create({
            'product_id': self.product_test.id,
            'location_id': self.location_silo.id,
            'lot_id': self.lot_grain.id,
            'quantity': 500.0,
            'package_id': tracking.package_id.id
        })

        # Lock the vessel physically
        tracking.write({'is_vessel_locked': True})

        # Attempting to change quantity or package should trigger a Jidoka lock raising ValidationError
        with self.assertRaisesRegex(ValidationError, "Jidoka Interlock Blocked"):
            quant.write({'quantity': 250.0})
