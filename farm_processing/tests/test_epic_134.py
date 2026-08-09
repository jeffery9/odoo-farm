# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestEpic134(TransactionCase):
    """ BDD Test for Epic 134 Dynamic Recipe Formulation """

    def setUp(self):
        super(TestEpic134, self).setUp()
        self.Product = self.env['product.product']
        self.Production = self.env['mrp.production']
        self.Bom = self.env['mrp.bom']
        
        # Setup Products
        self.concentrate = self.Product.create({'name': 'Fruit Concentrate', 'type': 'consu', 'is_storable': True})
        self.sugar_syrup = self.Product.create({'name': 'Sugar Syrup', 'type': 'consu', 'is_storable': True})
        self.final_juice = self.Product.create({'name': 'Adjusted Fruit Juice', 'type': 'consu', 'is_storable': True})

    def test_01_recipe_ast_define_formulation_formula_with_property_based_compensation(self):
        """
        US-134-01: Define formulation formula with property-based compensation
        Verify AST validation of formulas.
        """
        # Create a BOM with a dynamic formula
        bom = self.Bom.create({
            'product_tmpl_id': self.final_juice.product_tmpl_id.id,
            'product_qty': 1.0,
            'type': 'normal',
            'bom_line_ids': [
                (0, 0, {
                    'product_id': self.sugar_syrup.id,
                    'product_qty': 10.0,
                    'is_dynamic_formulation': True,
                    'dynamic_formula': 'base_qty + (12 - brix) * 2.5',
                    'min_qty': 5.0,
                    'max_qty': 20.0
                })
            ]
        })
        
        # Verify valid formula doesn't raise error
        bom.bom_line_ids._check_dynamic_formula_bounds()
        
        # Test Invalid Formula (Syntax Error)
        with self.assertRaises(ValidationError):
            bom.bom_line_ids.write({'dynamic_formula': 'base_qty + * brix'})
            bom.bom_line_ids._check_dynamic_formula_bounds()
            
        # Test Invalid Bounds (Min >= Max)
        with self.assertRaises(ValidationError):
            bom.bom_line_ids.write({
                'dynamic_formula': 'base_qty + brix',
                'min_qty': 50.0,
                'max_qty': 10.0
            })
            bom.bom_line_ids._check_dynamic_formula_bounds()

    def test_02_production_adjustment_dynamic_adjustment_of_material_consumption_during_picking(self):
        """
        US-134-02: Dynamic adjustment of material consumption during picking
        Verify recalculation of additives based on raw Brix.
        """
        # Setup BOM
        bom = self.Bom.create({
            'product_tmpl_id': self.final_juice.product_tmpl_id.id,
            'product_qty': 1.0,
            'type': 'normal',
            'bom_line_ids': [
                (0, 0, {
                    'product_id': self.sugar_syrup.id,
                    'product_qty': 10.0,
                    'is_dynamic_formulation': True,
                    'dynamic_formula': 'base_qty + (10 - brix) * 2.0', # If brix is 9, add (10-9)*2 = 2kg
                    'min_qty': 0.0,
                    'max_qty': 100.0
                })
            ]
        })
        
        # Create Production Order
        mo = self.Production.create({
            'product_id': self.final_juice.id,
            'product_qty': 1.0,
            'bom_id': bom.id
        })
        mo.action_confirm()
        
        # Trigger dynamic adjustment (Simulation uses mock_brix = 9.0 from advanced_processing_epics.py)
        # Expected: 10.0 + (10 - 9.0) * 2.0 = 12.0
        mo.action_apply_dynamic_formula()
        
        move = mo.move_raw_ids.filtered(lambda m: m.product_id == self.sugar_syrup)
        self.assertEqual(move.product_uom_qty, 12.0, "Dynamic adjustment failed to calculate correct quantity")

    def test_03_traceability_log_traceability_log_for_dynamic_formulation_adjustments(self):
        """
        US-134-03: Traceability log for dynamic formulation adjustments
        Verify audit trail for adjusted quantities.
        """
        bom = self.Bom.create({
            'product_tmpl_id': self.final_juice.product_tmpl_id.id,
            'product_qty': 1.0,
            'type': 'normal',
            'bom_line_ids': [(0, 0, {
                'product_id': self.sugar_syrup.id,
                'product_qty': 10.0,
                'is_dynamic_formulation': True,
                'dynamic_formula': 'base_qty * 1.1',
                'min_qty': 0, 'max_qty': 100
            })]
        })
        
        mo = self.Production.create({
            'product_id': self.final_juice.id,
            'product_qty': 1.0,
            'bom_id': bom.id
        })
        mo.action_confirm()
        mo.action_apply_dynamic_formula()
        
        # Check chatter for log message
        messages = mo.message_ids.mapped('body')
        has_log = any("Dynamic Formulation Applied" in m for m in messages)
        self.assertTrue(has_log, "Traceability log missing from production order chatter")
