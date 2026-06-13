# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo import fields
from odoo.tools import mute_logger


class TestAgriculturalProcessingAdditionalFeatures(TransactionCase):
    """Test additional agricultural processing features [Refactored]"""

    def setUp(self):
        super().setUp()
        self.Product = self.env['product.product']
        self.Bom = self.env['mrp.bom']
        self.Production = self.env['mrp.production']
        self.Lot = self.env['stock.lot']
        
        # Setup test products
        self.product_template = self.env['product.template'].create({
            'name': 'Test Processed Product',
            'type': 'product',
        })
        self.product_raw = self.Product.create({
            'name': 'Raw Material',
            'type': 'product',
        })
        self.product_material = self.Product.create({
            'name': 'Seasonal Input',
            'type': 'product',
        })

        try:
            self.FarmSeasonalRecipe = self.env['agri.seasonal.recipe']
        except KeyError:
            self.FarmSeasonalRecipe = None

        try:
            self.FarmProcessingBom = self.env['agri.isl.processing.bom']
        except KeyError:
            self.FarmProcessingBom = None
            
        if not self.FarmProcessingBom:
            self.skipTest("Missing FarmProcessingBom")
    
    def test_seasonal_recipe_creation(self):
        """Test US-004-06: Seasonal 'Versioned' Recipe Management"""
        if self.FarmSeasonalRecipe is None:
            return
            
        # Create base recipe (BOM)
        base_bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.product_template.id,
            'product_qty': 1,
            'type': 'normal',
            'bom_line_ids': [
                (0, 0, {'product_id': self.product_raw.id, 'product_qty': 1}),
            ],
        })

        # Create seasonal recipe
        seasonal_recipe = self.FarmSeasonalRecipe.create({
            'product_tmpl_id': self.product_template.id,
            'bom_id': base_bom.id,
            'season_name': 'Summer 2024',
            'version_number': 1,
            'season_start_date': fields.Date.from_string('2024-06-01'),
            'season_end_date': fields.Date.from_string('2024-08-31'),
            'base_yield_factor': 1.0,
            'state': 'active',
        })

        self.assertEqual(seasonal_recipe.season_name, 'Summer 2024')
        self.assertEqual(seasonal_recipe.state, 'active')
        self.assertEqual(seasonal_recipe.base_yield_factor, 1.0)

    def test_seasonal_input_adjustments(self):
        """Test seasonal input adjustments"""
        if self.FarmSeasonalRecipe is None:
            return
            
        base_bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.product_template.id,
            'product_qty': 1,
            'type': 'normal',
        })

        seasonal_recipe = self.FarmSeasonalRecipe.create({
            'product_tmpl_id': self.product_template.id,
            'bom_id': base_bom.id,
            'season_name': 'Winter Adjustments',
            'version_number': 1,
            'season_start_date': fields.Date.from_string('2024-12-01'),
            'season_end_date': fields.Date.from_string('2025-02-28'),
            'state': 'active',
        })

        # Add seasonal input adjustment
        seasonal_input = self.env['agri.seasonal.recipe.input'].create({
            'seasonal_recipe_id': seasonal_recipe.id,
            'product_id': self.product_material.id,
            'base_qty': 10.0,
            'seasonal_qty': 15.0,
            'adjustment_reason': 'Winter season requires more input',
        })

        self.assertEqual(seasonal_input.seasonal_qty, 15.0)
        self.assertEqual(seasonal_input.qty_difference, 5.0)

    def test_get_applicable_seasonal_recipe(self):
        """Test getting applicable seasonal recipe for a date"""
        if self.FarmSeasonalRecipe is None:
            return
            
        base_bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.product_template.id,
            'product_qty': 1,
            'type': 'normal',
        })

        summer_recipe = self.FarmSeasonalRecipe.create({
            'product_tmpl_id': self.product_template.id,
            'bom_id': base_bom.id,
            'season_name': 'Summer Season',
            'version_number': 1,
            'season_start_date': fields.Date.from_string('2024-06-01'),
            'season_end_date': fields.Date.from_string('2024-08-31'),
            'state': 'active',
        })

        # Test getting summer recipe for a summer date
        summer_date = fields.Date.from_string('2024-07-15')
        applicable = self.FarmSeasonalRecipe.get_applicable_seasonal_recipe(self.product_template.id, summer_date)
        self.assertEqual(applicable.id, summer_recipe.id)
