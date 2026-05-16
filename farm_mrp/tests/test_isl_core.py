# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import AccessError

class TestISLCore(TransactionCase):
    def setUp(self):
        super(TestISLCore, self).setUp()
        self.Product = self.env['product.product']
        self.Bom = self.env['mrp.bom']
        self.Production = self.env['mrp.production']
        self.Lot = self.env['stock.lot']
        
        # Create a basic product
        self.product_pig = self.Product.create({
            'name': 'Angus Pig',
            'type': 'consu',
        })

    def test_01_auto_isl_creation_on_bom(self):
        """ Test that creating a BOM with industry_type automatically creates ISL record. """
        if 'agri.isl.livestock.bom' not in self.env:
            self.skipTest("farm.livestock.bom not installed")
        # We use 'livestock' which is added by farm_livestock
        bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'livestock',
        })
        
        # Check if farm.livestock.bom was created
        isl_bom = self.env['agri.isl.livestock.bom'].search([('bom_id', '=', bom.id)])
        self.assertTrue(isl_bom, "ISL BOM should be created automatically for Livestock industry.")
        self.assertEqual(isl_bom.bom_id, bom)

    def test_02_auto_isl_creation_on_production(self):
        """ Test that creating an MO with industry_type automatically creates ISL record. """
        if 'agri.isl.livestock.bom' not in self.env:
            self.skipTest("farm.livestock.bom not installed")
        bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'livestock',
        })
        
        mo = self.Production.create({
            'product_id': self.product_pig.id,
            'bom_id': bom.id,
            'product_qty': 1.0,
        })
        
        # Check if agri.isl.livestock.production was created
        isl_mo = self.env['agri.isl.livestock.production'].search([('production_id', '=', mo.id)])
        self.assertTrue(isl_mo, "ISL Production should be created automatically for Livestock industry.")
        self.assertEqual(isl_mo.production_id, mo)

    def test_03_lot_summary_hook(self):
        """ Test the decoupled lot summary info hook. """
        if 'agri.isl.livestock.bom' not in self.env:
            self.skipTest("farm.livestock.bom not installed")
        lot = self.Lot.create({
            'name': 'LIV-001',
            'product_id': self.product_pig.id,
            'lot_purpose': 'biological_asset',
        })
        
        # Create ISL lot record manually
        isl_lot = self.env['agri.isl.lot.livestock'].create({
            'lot_id': lot.id,
            'gender': 'male',
            'current_weight': 150.5
        })
        
        lot._compute_isl_summary_info()
        self.assertIn("Husbandry: male", lot.isl_summary_info)
        self.assertIn("150.5kg", lot.isl_summary_info)

    def test_04_redirection_logic(self):
        """ Test that get_formview_action returns the ISL model. """
        if 'agri.isl.livestock.bom' not in self.env:
            self.skipTest("farm.livestock.bom not installed")
        bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'livestock',
        })

        action = bom.get_formview_action()
        self.assertEqual(action['res_model'], 'agri.isl.livestock.bom')
        self.assertTrue(action['context'].get('isl_active'))

    def test_05_base_model_write_restrictions(self):
        """ Test that modifying protected fields in base models raises exceptions. """
        if 'agri.isl.livestock.bom' not in self.env:
            self.skipTest("farm.livestock.bom not installed")
        # Create a livestock BOM
        bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'livestock',
        })

        # Verify ISL record was created
        isl_bom = self.env['agri.isl.livestock.bom'].search([('bom_id', '=', bom.id)])
        self.assertTrue(isl_bom)

        # Attempt to modify protected field - should raise UserError
        from odoo.exceptions import UserError
        with self.assertRaises(UserError):
            bom.write({'growth_days_expected': 90})  # This is a livestock-specific field

        # Attempt to modify non-protected field - should succeed
        bom.write({'product_qty': 2.0})  # This is a base field
        self.assertEqual(bom.product_qty, 2.0)

    def test_06_base_model_unlink_restrictions(self):
        """ Test that deleting base models with ISL records raises exceptions. """
        if 'agri.isl.livestock.bom' not in self.env:
            self.skipTest("farm.livestock.bom not installed")
        # Create a livestock production order
        bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'livestock',
        })

        mo = self.Production.create({
            'product_id': self.product_pig.id,
            'bom_id': bom.id,
            'product_qty': 1.0,
        })

        # Verify ISL record was created
        isl_mo = self.env['agri.isl.livestock.production'].search([('production_id', '=', mo.id)])
        self.assertTrue(isl_mo)

        # Attempt to delete base MO with ISL record - should raise UserError
        from odoo.exceptions import UserError
        with self.assertRaises(UserError):
            mo.unlink()

    def test_07_base_model_write_allowed_when_no_isl(self):
        """ Test that modifying base models without ISL records is allowed. """
        if 'agri.isl.livestock.bom' not in self.env:
            self.skipTest("farm.livestock.bom not installed")
        # Create a standard (non-ISL) BOM
        bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'standard',  # Not an ISL industry
        })

        # Verify no ISL record was created
        isl_bom = self.env['agri.isl.livestock.bom'].search([('bom_id', '=', bom.id)])
        self.assertFalse(isl_bom)

        # Attempt to modify field - should succeed since no ISL exists
        bom.write({'product_qty': 2.0})
        self.assertEqual(bom.product_qty, 2.0)

    def test_08_isl_record_type_computation_production(self):
        """ Test that ISL record type is computed correctly for production orders. """
        if 'agri.isl.livestock.bom' not in self.env:
            self.skipTest("farm.livestock.bom not installed")
        # Create a livestock production order
        bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'livestock',
        })

        mo = self.Production.create({
            'product_id': self.product_pig.id,
            'bom_id': bom.id,
            'product_qty': 1.0,
        })

        # Verify ISL record type is computed
        self.assertEqual(mo.isl_record_type, 'Livestock')

        # Create a processing production order
        processing_bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'processing',
        })

        processing_mo = self.Production.create({
            'product_id': self.product_pig.id,
            'bom_id': processing_bom.id,
            'product_qty': 1.0,
        })

        # Verify ISL record type is computed
        self.assertEqual(processing_mo.isl_record_type, 'Processing')

        # Create a standard production order (no ISL)
        standard_bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'standard',
        })

        standard_mo = self.Production.create({
            'product_id': self.product_pig.id,
            'bom_id': standard_bom.id,
            'product_qty': 1.0,
        })

        # Verify no ISL record type for standard
        self.assertFalse(standard_mo.isl_record_type)

    def test_09_isl_record_type_computation_bom(self):
        """ Test that ISL record type is computed correctly for BOMs. """
        if 'agri.isl.livestock.bom' not in self.env:
            self.skipTest("farm.livestock.bom not installed")
        # Create a livestock BOM
        livestock_bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'livestock',
        })

        # Verify ISL record type is computed
        self.assertEqual(livestock_bom.isl_record_type, 'Livestock')

        # Create a processing BOM
        processing_bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'processing',
        })

        # Verify ISL record type is computed
        self.assertEqual(processing_bom.isl_record_type, 'Processing')

        # Create a standard BOM (no ISL)
        standard_bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'standard',
        })

        # Verify no ISL record type for standard
        self.assertFalse(standard_bom.isl_record_type)

    def test_10_isl_navigation_action(self):
        """ Test that ISL navigation action returns correct view. """
        if 'agri.isl.livestock.bom' not in self.env:
            self.skipTest("farm.livestock.bom not installed")
        # Create a livestock production order
        bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'livestock',
        })

        mo = self.Production.create({
            'product_id': self.product_pig.id,
            'bom_id': bom.id,
            'product_qty': 1.0,
        })

        # Call the navigation action
        action = mo.action_view_isl_record()

        # Verify the action returns correct view
        self.assertEqual(action['type'], 'ir.actions.act_window')
        self.assertEqual(action['res_model'], 'agri.isl.livestock.production')
        self.assertEqual(action['view_mode'], 'form')

        # Test navigation for BOM
        bom_action = bom.action_view_isl_record()
        self.assertEqual(bom_action['type'], 'ir.actions.act_window')
        self.assertEqual(bom_action['res_model'], 'agri.isl.livestock.bom')
        self.assertEqual(bom_action['view_mode'], 'form')

    def test_11_isl_navigation_no_record(self):
        """ Test that ISL navigation shows message when no ISL record exists. """
        if 'agri.isl.livestock.bom' not in self.env:
            self.skipTest("farm.livestock.bom not installed")
        # Create a standard production order (no ISL record should be created automatically)
        standard_bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'standard',
        })

        standard_mo = self.Production.create({
            'product_id': self.product_pig.id,
            'bom_id': standard_bom.id,
            'product_qty': 1.0,
        })

        # Call the navigation action when no ISL record exists
        action = standard_mo.action_view_isl_record()

        # Verify the action returns a notification
        self.assertEqual(action['type'], 'ir.actions.client')
        self.assertEqual(action['tag'], 'display_notification')
        self.assertEqual(action['params']['title'], 'No ISL Record')

    def test_12_lot_isl_record_type_computation(self):
        """ Test that ISL record type is computed correctly for lots. """
        if 'agri.isl.livestock.bom' not in self.env:
            self.skipTest("farm.livestock.bom not installed")
        # Create a base lot
        lot = self.Lot.create({
            'name': 'TEST-LOT-001',
            'product_id': self.product_pig.id,
        })

        # Initially should have no ISL type
        self.assertFalse(lot.isl_record_type)

        # Create an ISL lot record for livestock
        isl_lot = self.env['agri.isl.lot.livestock'].create({
            'lot_id': lot.id,
            'gender': 'male',
            'current_weight': 100.0
        })

        # Refresh the lot record to get the computed value
        lot.refresh()

        # Now it should have the livestock ISL type
        self.assertEqual(lot.isl_record_type, 'Livestock')

        # Test with aquaculture lot
        lot2 = self.Lot.create({
            'name': 'TEST-LOT-002',
            'product_id': self.product_pig.id,
        })

        isl_lot2 = self.env['agri.isl.lot.aquaculture'].create({
            'lot_id': lot2.id,
            'current_count': 50
        })

        lot2.refresh()
        self.assertEqual(lot2.isl_record_type, 'Aquaculture')

    def test_13_lot_isl_navigation_action(self):
        """ Test that ISL navigation action works for lots. """
        if 'agri.isl.livestock.bom' not in self.env:
            self.skipTest("farm.livestock.bom not installed")
        # Create a base lot with ISL record
        lot = self.Lot.create({
            'name': 'TEST-LOT-NAV',
            'product_id': self.product_pig.id,
        })

        # Create an ISL lot record
        isl_lot = self.env['agri.isl.lot.livestock'].create({
            'lot_id': lot.id,
            'gender': 'female',
            'current_weight': 80.0
        })

        # Call the navigation action
        action = lot.action_view_isl_record()

        # Verify the action returns correct view
        self.assertEqual(action['type'], 'ir.actions.act_window')
        self.assertEqual(action['res_model'], 'agri.isl.lot.livestock')
        self.assertEqual(action['res_id'], isl_lot.id)
        self.assertEqual(action['view_mode'], 'form')

    def test_14_lot_isl_navigation_no_record(self):
        """ Test that ISL navigation shows message for lots with no ISL record. """
        if 'agri.isl.livestock.bom' not in self.env:
            self.skipTest("farm.livestock.bom not installed")
        # Create a base lot without ISL record
        lot = self.Lot.create({
            'name': 'TEST-LOT-NO-NAV',
            'product_id': self.product_pig.id,
        })

        # Call the navigation action when no ISL record exists
        action = lot.action_view_isl_record()

        # Verify the action returns a notification
        self.assertEqual(action['type'], 'ir.actions.client')
        self.assertEqual(action['tag'], 'display_notification')
        self.assertEqual(action['params']['title'], 'No ISL Record')

    def test_15_auto_isl_creation_on_bom_line(self):
        """ Test that creating a BOM line automatically creates ISL record based on parent BOM's industry_type. """
        if 'agri.isl.livestock.bom' not in self.env:
            self.skipTest("farm.livestock.bom not installed")
        # Create a livestock BOM first
        bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'livestock',
        })

        # Create a BOM line
        from odoo import fields
        bom_line = self.env['mrp.bom.line'].create({
            'bom_id': bom.id,
            'product_id': self.product_pig.id,
            'product_qty': 5.0,
        })

        # Check if farm.livestock.bom.line was created
        isl_bom_line = self.env['agri.isl.livestock.bom.line'].search([('bom_line_id', '=', bom_line.id)])
        self.assertTrue(isl_bom_line, "ISL BOM Line should be created automatically for Livestock industry.")
        self.assertEqual(isl_bom_line.bom_line_id, bom_line)

    def test_16_bom_line_write_restrictions(self):
        """ Test that modifying protected fields in base BOM lines with ISL raises exceptions. """
        if 'agri.isl.livestock.bom' not in self.env:
            self.skipTest("farm.livestock.bom not installed")
        # Create a livestock BOM
        bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'livestock',
        })

        # Create a BOM line
        bom_line = self.env['mrp.bom.line'].create({
            'bom_id': bom.id,
            'product_id': self.product_pig.id,
            'product_qty': 5.0,
        })

        # Verify ISL record was created
        isl_bom_line = self.env['agri.isl.livestock.bom.line'].search([('bom_line_id', '=', bom_line.id)])
        self.assertTrue(isl_bom_line)

        # Attempt to modify protected field - should raise UserError
        from odoo.exceptions import UserError
        with self.assertRaises(UserError):
            bom_line.write({'dilution_ratio': 0.5})  # This is a livestock-specific field

        # Attempt to modify non-protected field - should succeed
        bom_line.write({'product_qty': 10.0})  # This is a base field
        self.assertEqual(bom_line.product_qty, 10.0)

    def test_17_bom_line_unlink_restrictions(self):
        """ Test that deleting base BOM lines with ISL records raises exceptions. """
        if 'agri.isl.livestock.bom' not in self.env:
            self.skipTest("farm.livestock.bom not installed")
        # Create a livestock BOM
        bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'livestock',
        })

        # Create a BOM line
        bom_line = self.env['mrp.bom.line'].create({
            'bom_id': bom.id,
            'product_id': self.product_pig.id,
            'product_qty': 5.0,
        })

        # Verify ISL record was created
        isl_bom_line = self.env['agri.isl.livestock.bom.line'].search([('bom_line_id', '=', bom_line.id)])
        self.assertTrue(isl_bom_line)

        # Attempt to delete base BOM line with ISL record - should raise UserError
        from odoo.exceptions import UserError
        with self.assertRaises(UserError):
            bom_line.unlink()

    def test_18_bom_line_isl_record_type_computation(self):
        """ Test that ISL record type is computed correctly for BOM lines. """
        if 'agri.isl.livestock.bom' not in self.env:
            self.skipTest("farm.livestock.bom not installed")
        # Create a livestock BOM
        livestock_bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'livestock',
        })

        # Create a BOM line
        livestock_bom_line = self.env['mrp.bom.line'].create({
            'bom_id': livestock_bom.id,
            'product_id': self.product_pig.id,
            'product_qty': 5.0,
        })

        # Verify ISL record type is computed
        self.assertEqual(livestock_bom_line.isl_record_type, 'Livestock')

        # Create a processing BOM
        processing_bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'processing',
        })

        # Create a BOM line
        processing_bom_line = self.env['mrp.bom.line'].create({
            'bom_id': processing_bom.id,
            'product_id': self.product_pig.id,
            'product_qty': 3.0,
        })

        # Verify ISL record type is computed
        self.assertEqual(processing_bom_line.isl_record_type, 'Processing')

        # Create a standard BOM (no ISL)
        standard_bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'standard',
        })

        # Create a BOM line
        standard_bom_line = self.env['mrp.bom.line'].create({
            'bom_id': standard_bom.id,
            'product_id': self.product_pig.id,
            'product_qty': 2.0,
        })

        # Verify no ISL record type for standard
        self.assertFalse(standard_bom_line.isl_record_type)

    def test_19_bom_line_isl_navigation_action(self):
        """ Test that ISL navigation action works for BOM lines. """
        if 'agri.isl.livestock.bom' not in self.env:
            self.skipTest("farm.livestock.bom not installed")
        # Create a livestock BOM
        bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'livestock',
        })

        # Create a BOM line with ISL record
        bom_line = self.env['mrp.bom.line'].create({
            'bom_id': bom.id,
            'product_id': self.product_pig.id,
            'product_qty': 5.0,
        })

        # Call the navigation action
        action = bom_line.action_view_isl_record()

        # Verify the action returns correct view
        self.assertEqual(action['type'], 'ir.actions.act_window')
        self.assertEqual(action['res_model'], 'agri.isl.livestock.bom.line')
        self.assertEqual(action['view_mode'], 'form')

    def test_20_bom_line_isl_navigation_no_record(self):
        """ Test that ISL navigation shows message when no ISL record exists for BOM line. """
        if 'agri.isl.livestock.bom' not in self.env:
            self.skipTest("farm.livestock.bom not installed")
        # Create a standard BOM (no ISL record should be created automatically)
        standard_bom = self.Bom.create({
            'product_tmpl_id': self.product_pig.product_tmpl_id.id,
            'product_qty': 1.0,
            'industry_type': 'standard',
        })

        # Create a BOM line
        standard_bom_line = self.env['mrp.bom.line'].create({
            'bom_id': standard_bom.id,
            'product_id': self.product_pig.id,
            'product_qty': 2.0,
        })

        # Call the navigation action when no ISL record exists
        action = standard_bom_line.action_view_isl_record()

        # Verify the action returns a notification
        self.assertEqual(action['type'], 'ir.actions.client')
        self.assertEqual(action['tag'], 'display_notification')
        self.assertEqual(action['params']['title'], 'No ISL Record')
