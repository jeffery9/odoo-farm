# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, Form

class TestISLViews(TransactionCase):
    def setUp(self):
        super(TestISLViews, self).setUp()
        self.Product = self.env['product.product']
        self.uom_unit = self.env.ref('uom.product_uom_unit')
        
        self.product_apple = self.Product.create({
            'name': 'Apple',
            'type': 'product',
        })

    def test_specialized_views_existence(self):
        """ Verify that ISL specialized views are correctly registered. """
        # Livestock
        view_livestock = self.env.ref('farm_livestock.view_farm_livestock_bom_form', raise_if_not_found=False)
        self.assertTrue(view_livestock and view_livestock.model == 'farm.livestock.bom')
        
        # Aquaculture
        view_aqua = self.env.ref('farm_aquaculture.view_farm_aquaculture_bom_form', raise_if_not_found=False)
        self.assertTrue(view_aqua and view_aqua.model == 'farm.aquaculture.bom')
        
        # Processing
        view_proc = self.env.ref('farm_processing.view_farm_processing_bom_form', raise_if_not_found=False)
        self.assertTrue(view_proc and view_proc.model == 'farm.processing.bom')
        
        # Crop
        view_crop = self.env.ref('farm_field_crops.view_farm_crop_bom_form', raise_if_not_found=False)
        self.assertTrue(view_crop and view_crop.model == 'farm.crop.bom')

    def test_livestock_bom_form_simulation(self):
        """ Simulate user interaction with Livestock ISL BOM Form. """
        with Form(self.env['farm.livestock.bom']) as f:
            f.product_tmpl_id = self.product_apple.product_tmpl_id
            f.product_qty = 1.0
            f.product_uom_id = self.uom_unit
            f.growth_days_expected = 180
            f.daily_feed_intake = 2.5
            
            # Verify that base fields are accessible through delegation
            self.assertEqual(f.product_tmpl_id.name, 'Apple')
            
        bom_isl = f.save()
        self.assertEqual(bom_isl.growth_days_expected, 180)
        self.assertTrue(bom_isl.bom_id, "Base BOM should have been created via delegation")

    def test_processing_production_form_simulation(self):
        """ Simulate user interaction with Processing ISL Production Form. """
        with Form(self.env['farm.processing.production']) as f:
            f.product_id = self.product_apple
            f.product_qty = 100.0
            f.energy_reading_start = 1200.0
            f.energy_reading_end = 1250.0
            
            # Check if delegated fields are correctly set
            self.assertEqual(f.state, 'draft')
            
        mo_isl = f.save()
        self.assertEqual(mo_isl.energy_cost_total, 50.0)
        self.assertEqual(mo_isl.production_id.product_qty, 100.0)

    def test_crop_production_form_simulation(self):
        """ Simulate user interaction with Crop ISL Production Form. """
        with Form(self.env['farm.crop.production']) as f:
            f.product_id = self.product_apple
            f.area_to_treat = 5.5
            
        crop_mo = f.save()
        self.assertEqual(crop_mo.area_to_treat, 5.5)
        self.assertEqual(crop_mo.production_id.product_id, self.product_apple)

    def test_menu_actions(self):
        """ Verify that menu actions point to ISL models. """
        action_livestock = self.env.ref('farm_livestock.action_farm_livestock_mo_isl')
        self.assertEqual(action_livestock.res_model, 'farm.livestock.production')
        
        action_aqua = self.env.ref('farm_aquaculture.action_farm_aquaculture_mo_isl')
        self.assertEqual(action_aqua.res_model, 'farm.aquaculture.production')
        
        action_crop = self.env.ref('farm_field_crops.action_farm_crop_mo_isl')
        self.assertEqual(action_crop.res_model, 'farm.crop.production')