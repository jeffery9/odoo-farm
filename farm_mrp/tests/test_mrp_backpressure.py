# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestMrpBackpressure(TransactionCase):
    def setUp(self):
        super(TestMrpBackpressure, self).setUp()
        self.Location = self.env['farm.location']
        self.Product = self.env['product.product']
        self.Bom = self.env['mrp.bom']
        self.Production = self.env['mrp.production']

        # 1. Create product and destination
        self.p_cow = self.Product.create({'name': 'Dairy Cow', 'is_storable': True})
        self.dest_location = self.Location.create({
            'name': 'Holding Pen C',
            'gps_lat': 12.0,
            'gps_lng': 34.0,
            'land_area': 100.0,
            'max_stocking_density': 0.1  # Max 10 animals
        })

        # 2. Create base BOM
        self.bom = self.Bom.create({
            'product_id': self.p_cow.id,
            'product_tmpl_id': self.p_cow.product_tmpl_id.id,
            'product_qty': 1.0,
            'type': 'normal'
        })

    def test_mrp_confirmation_backpressure_block(self):
        # Attempt to plan and confirm an order of 15 animals (violating max 10 density limit)
        mo = self.Production.create({
            'product_id': self.p_cow.id,
            'bom_id': self.bom.id,
            'product_qty': 15.0,
            'location_dest_id': self.dest_location.agri_location_id.id
        })
        
        with self.assertRaises(ValidationError):
            mo.action_confirm()
