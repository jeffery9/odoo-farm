# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, Form

class TestLivestockISL(TransactionCase):
    def setUp(self):
        super(TestLivestockISL, self).setUp()
        self.Product = self.env['product.product']
        self.Bom = self.env['mrp.bom']
        self.Production = self.env['mrp.production']
        self.Lot = self.env['stock.lot']
        
        self.pig = self.Product.create({'name': 'Pig', 'type': 'product', 'tracking': 'lot'})
        self.feed = self.Product.create({'name': 'Corn Feed', 'type': 'consu'})

    def test_01_fcr_logic_and_form(self):
        """ Test Feed Conversion Ratio calculation via Form interaction. """
        # Simulate creating an order from the ISL view
        with Form(self.env['farm.livestock.production']) as f:
            f.product_id = self.pig
            f.product_qty = 10.0
            f.initial_total_weight = 100.0
            f.final_total_weight = 200.0 # Gain = 100
            
        isl_mo = f.save()
        # Trigger recompute
        isl_mo._compute_fcr_isl()
        # Gain is 100, Qty is 10. FCR = 10 / 100 = 0.1
        self.assertEqual(isl_mo.fcr, 0.1, "FCR should be 0.1 (Qty/Gain)")

    def test_02_isl_post_done_form_integration(self):
        """ Test lot weight update after MO completion using Form context. """
        # 1. Setup Data
        lot = self.Lot.create({'name': 'PIG-BATCH-01', 'product_id': self.pig.id})
        isl_lot = self.env['farm.lot.livestock'].create({'lot_id': lot.id})
        
        # 2. Create MO via Form
        with Form(self.env['farm.livestock.production']) as f:
            f.product_id = self.pig
            f.product_qty = 1.0
            f.final_total_weight = 120.0
            # Link to the produced lot
            # Note: in real UI this happens during produce, we simulate it here
        
        isl_mo = f.save()
        isl_mo.production_id.lot_producing_id = lot
        
        # 3. Simulate completion hook
        isl_mo.isl_post_done()
        
        self.assertEqual(isl_lot.current_weight, 120.0, "Lot weight should be updated from ISL production data")
