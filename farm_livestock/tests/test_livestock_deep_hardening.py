# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError, UserError
from odoo import fields
from datetime import date, timedelta

@tagged('uavm_surgical', 'post_install', '-at_install')
class TestLivestockDeepHardening(TransactionCase):

    def setUp(self):
        super(TestLivestockDeepHardening, self).setUp()
        self.product = self.env['product.product'].create({
            'name': 'Surgical Breeding Piglet',
            'type': 'consu',
            'is_storable': True,
        })
        self.animal_lot = self.env['stock.lot'].create({
            'name': 'TEST-ANIMAL-LOT-999',
            'product_id': self.product.id,
            'company_id': self.env.company.id,
        })

    def test_livestock_breeding_age_limits(self):
        """ Verify livestock age limit validation triggers exception on immature breeding """
        # Create an immature animal (90 days old)
        isl_lot = self.env['agri.isl.lot.livestock'].create({
            'name': 'TEST-ANIMAL-UNDERAGE',
            'product_id': self.product.id,
            'company_id': self.env.company.id,
            'birth_date': date.today() - timedelta(days=90),
            'breeding_status': 'immature',
        })
        
        # Changing breeding status should trigger a real ValidationError
        with self.assertRaisesRegex(ValidationError, "Breeding Blocked"):
            isl_lot.write({'breeding_status': 'pregnant'})

    def test_livestock_feeding_limit_checks(self):
        """ Ensure animal feed logs and event tracking enforce daily feed intake limits """
        # Creating a recipe with excessive daily feed intake should raise a real ValidationError
        with self.assertRaisesRegex(ValidationError, "exceeds maximum safe threshold"):
            self.env['agri.isl.livestock.recipe'].create({
                'product_id': self.product.id,
                'product_tmpl_id': self.product.product_tmpl_id.id,
                'product_qty': 1.0,
                'type': 'normal',
                'daily_feed_intake': 12.0, # Limit is 10.0
            })

    def test_livestock_quarantine_block(self):
        """ Ensure health block prevents starting manufacturing interventions on quarantined livestock """
        # Set property on stock.lot class dynamically for the duration of the test
        self.env['stock.lot'].__class__.health_state = property(lambda self: 'quarantine')
        try:
            # Create a BOM for livestock industry mapping
            bom = self.env['mrp.bom'].create({
                'product_id': self.product.id,
                'product_tmpl_id': self.product.product_tmpl_id.id,
                'product_qty': 1.0,
                'type': 'normal',
                'industry_type': 'livestock',
            })
            
            # Create an mrp.production record for livestock linking the BOM
            production = self.env['mrp.production'].create({
                'product_id': self.product.id,
                'product_qty': 1.0,
                'product_uom_id': self.product.uom_id.id,
                'bom_id': bom.id,
                'lot_producing_id': self.animal_lot.id,
            })
            
            # Triggering _hook_pre_start should raise UserError health block
            with self.assertRaisesRegex(UserError, "HEALTH BLOCK"):
                production._hook_pre_start()
        finally:
            # Clean up class property to prevent test side effects
            if hasattr(self.env['stock.lot'].__class__, 'health_state'):
                delattr(self.env['stock.lot'].__class__, 'health_state')

    def test_livestock_phi_block(self):
        """ Verify biosecurity PHI withdrawal end date blocks harvest safety check """
        # Create livestock asset lot with a future withdrawal end date
        isl_lot = self.env['agri.isl.lot.livestock'].create({
            'name': 'TEST-ANIMAL-PHI-LOT',
            'product_id': self.product.id,
            'company_id': self.env.company.id,
            'withdrawal_end_datetime': fields.Datetime.to_datetime(date.today() + timedelta(days=2)),
        })
        
        # Confirm that withdrawal_end_date is calculated as future
        self.assertTrue(isl_lot.withdrawal_end_date > date.today())
        
        # action_check_harvest_safety should raise UserError biosecurity block
        with self.assertRaisesRegex(UserError, "BIOSECURITY BLOCK"):
            isl_lot.action_check_harvest_safety()
