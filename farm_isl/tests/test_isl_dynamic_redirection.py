# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class TestISLDynamicRedirection(TransactionCase):
    """
    Test suite for refactored ISL Dynamic Redirection and Trait Mixins.
    Verifies that hardcoding removal didn't break functionality.
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Redirector = cls.env['agri.isl.model.redirector']
        
        # 1. Setup a basic intervention (mrp.production) for testing
        cls.product = cls.env['product.product'].create({
            'name': 'Organic Corn',
            'type': 'product',
        })
        
        cls.production = cls.env['mrp.production'].create({
            'product_id': cls.product.id,
            'product_qty': 1.0,
            'product_uom_id': cls.product.uom_id.id,
        })

    def test_01_dynamic_discovery_mrp(self):
        """ Verify that Redirector finds ISL record via _inherits metadata """
        # Create an ISL record linked to the base MO
        isl_mo = self.env['agri.isl.mrp.production'].create({
            'mrp_production_id': self.production.id,
            'industry_type': 'field_crop',
        })
        
        # Ask Redirector to find it
        found_isl = self.Redirector.get_isl_record('mrp.production', self.production.id)
        
        self.assertTrue(found_isl, "Redirector should find the ISL record dynamically")
        self.assertEqual(found_isl._name, 'agri.isl.mrp.production')
        self.assertEqual(found_isl.id, isl_mo.id)

    def test_02_industry_type_routing(self):
        """ Verify that Redirector respects industry_type during discovery """
        # 1. Create a generic ISL record
        self.env['agri.isl.mrp.production'].create({
            'mrp_production_id': self.production.id,
            'industry_type': 'general',
        })
        
        # 2. Simulate the base record having an industry type
        # We need to ensure the base record has the field if we want to test 'related' or specific logic,
        # but the Redirector checks the ISL record's industry_type.
        
        found_isl = self.Redirector.get_isl_record('mrp.production', self.production.id)
        self.assertEqual(found_isl.industry_type, 'general')

    def test_03_create_isl_record_dynamic(self):
        """ Verify automated ISL record creation via dynamic discovery """
        # Ensure no ISL record exists for this MO
        existing = self.env['agri.isl.mrp.production'].search([('mrp_production_id', '=', self.production.id)])
        existing.unlink()
        
        # Create via Redirector
        new_isl = self.Redirector.create_isl_record('mrp.production', self.production.id, industry_type='livestock')
        
        self.assertTrue(new_isl)
        self.assertEqual(new_isl._name, 'agri.isl.mrp.production')
        self.assertEqual(new_isl.industry_type, 'livestock')
        self.assertEqual(new_isl.mrp_production_id.id, self.production.id)

    def test_04_trait_mixins_availability(self):
        """ Ensure fields from specific Trait Mixins are available on concrete models """
        isl_mo = self.env['agri.isl.mrp.production'].new({
            'industry_type': 'field_crop'
        })
        
        # Check for Food Safety Trait fields
        self.assertTrue(hasattr(isl_mo, 'haccp_plan'), "ISL MO should have haccp_plan from Food Safety Trait")
        self.assertTrue(hasattr(isl_mo, 'gmp_compliance'), "ISL MO should have gmp_compliance from Livestock Trait")

    def test_05_compliance_validation_logic(self):
        """ Verify that industry-specific compliance methods still work """
        isl_mo = self.env['agri.isl.mrp.production'].create({
            'mrp_production_id': self.production.id,
            'industry_type': 'field_crop',
            'haccp_plan': False # Missing mandatory field for field_crop
        })
        
        # Should raise UserError based on inherited _check_industry_compliance logic
        with self.assertRaises(UserError) as e:
            isl_mo._check_industry_compliance()
        self.assertIn("requires HACCP plan", str(e.exception))
        
        # Fix and retry
        isl_mo.haccp_plan = "<p>Safe</p>"
        res = isl_mo._check_industry_compliance()
        self.assertTrue(res)

    def test_06_fallback_discovery(self):
        """ Verify fallback to generic map if no specific inherits match (Safety Net) """
        # This tests the generic_map in create_isl_record
        # We'll use a model that definitely has an ISL counterpart
        lot = self.env['stock.lot'].create({
            'name': 'TEST-LOT-ISL-01',
            'product_id': self.product.id,
            'company_id': self.env.company.id,
        })
        
        new_isl = self.Redirector.create_isl_record('stock.lot', lot.id)
        self.assertEqual(new_isl._name, 'agri.isl.stock.lot')

    def test_07_convention_based_discovery(self):
        """ Verify that ISL models are discovered via naming convention (agri.isl.suffix) """
        # Simulate a base model name
        base_model = 'stock.picking'
        
        # Ensure no ISL record exists for a test picking
        picking = self.env['stock.picking'].create({
            'picking_type_id': self.env.ref('stock.picking_type_in').id,
            'location_id': self.env.ref('stock.stock_location_suppliers').id,
            'location_dest_id': self.env.ref('stock.stock_location_stock').id,
        })
        
        # Try to create ISL record. The Redirector should find 'agri.isl.stock_picking' 
        # via the convention base_model.replace('.', '_')
        new_isl = self.Redirector.create_isl_record(base_model, picking.id)
        
        self.assertTrue(new_isl)
        self.assertEqual(new_isl._name, 'agri.isl.stock.picking')
        self.assertEqual(new_isl.picking_id.id, picking.id)
