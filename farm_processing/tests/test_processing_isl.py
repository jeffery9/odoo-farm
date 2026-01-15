# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, Form
from odoo.exceptions import UserError

class TestProcessingISL(TransactionCase):
    def setUp(self):
        super(TestProcessingISL, self).setUp()
        self.Product = self.env['product.product']
        self.Bom = self.env['mrp.bom']
        self.Production = self.env['mrp.production']
        
        self.juice = self.Product.create({'name': 'Apple Juice', 'type': 'product'})
        self.apple = self.Product.create({'name': 'Apple', 'type': 'product'})

    def test_01_energy_cost_form_logic(self):
        """ Test energy cost calculation through Form UI simulation. """
        with Form(self.env['farm.processing.production']) as f:
            f.product_id = self.juice
            f.energy_reading_start = 5000.0
            f.energy_reading_end = 5150.0
            
        isl_mo = f.save()
        # Cost total should be 150.0 based on placeholder 1:1 logic
        self.assertEqual(isl_mo.energy_cost_total, 150.0, "Energy cost should be 150 (5150 - 5000)")

    def test_02_mass_balance_gate(self):
        """ Test mass balance logic in processing ISL using MO data. """
        bom = self.Bom.create({
            'product_tmpl_id': self.juice.product_tmpl_id.id,
            'product_qty': 100.0,
            'industry_type': 'food_processing',
        })
        isl_bom = self.env['farm.processing.bom'].search([('bom_id', '=', bom.id)])
        isl_bom.max_loss_rate = 5.0 
        
        # Simulate MO creation
        with Form(self.env['farm.processing.production']) as f:
            f.product_id = self.juice
            f.bom_id = bom
            f.product_qty = 100.0
        
        isl_mo = f.save()
        mo = isl_mo.production_id
        
        # 1. Simulate Consumption (100kg)
        self.env['stock.move'].create({
            'name': 'Apple Consumption',
            'product_id': self.apple.id,
            'product_uom_qty': 100.0,
            'quantity_done': 100.0,
            'production_id': mo.id,
            'location_id': self.env.ref('stock.stock_location_stock').id,
            'location_dest_id': self.juice.property_stock_production.id,
        })
        
        # 2. Case: High Loss (10kg loss -> 10% > 5%)
        # Create finished move lines (Odoo standard way)
        mo.move_finished_ids.write({'quantity_done': 90.0})
        
        isl_mo.isl_post_done()
        self.assertEqual(isl_mo.quality_gate_status, 'rejected', "Should be rejected due to 10% loss")
