# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError
from odoo import fields
from datetime import timedelta

class TestEpic094(TransactionCase):
    """ BDD Test Suite for Epic 094: Epic 094 Smart Livestock Management (Real Constraints Verification) """

    def setUp(self):
        super(TestEpic094, self).setUp()
        self.partner = self.env['res.partner'].create({'name': 'BDD Test Partner'})
        self.product = self.env['product.product'].create({
            'name': 'BDD Breeding Swine',
            'type': 'consu',
            'is_storable': True
        })
        self.lot = self.env['stock.lot'].create({
            'name': 'SWI-LOT-01',
            'product_id': self.product.id,
            'company_id': self.env.company.id
        })

    def test_01_swine_breeding_maturity_age_constraint(self):
        """
        Scenario: Individual animal profile management and breeding maturity constraints (US-094-04)
        Given a swine lot with a birth date less than 365 days ago (e.g. 100 days old)
        When an administrator attempts to set its breeding status to "open"
        Then the actual Odoo constrains '_check_breeding_maturity' on 'agri.isl.lot.livestock' must block the update
        And raise a ValidationError stating the animal has not reached mature breeding age (365 days).
        """
        # Create physical ISL lot layer
        isl_lot = self.env['agri.isl.lot.livestock'].create({
            'lot_id': self.lot.id,
            'birth_date': fields.Date.today() - timedelta(days=100),
            'breeding_status': 'immature'
        })

        # Actively write open status to trigger the actual Odoo backend constraint method
        with self.assertRaises(ValidationError) as context:
            isl_lot.write({'breeding_status': 'open'})

        # Verify the exception message came from the real livestock_isl.py model logic!
        self.assertIn("has not reached mature breeding age", str(context.exception))

    def test_02_breeding_recipe_safe_feed_intake_constraint(self):
        """
        Scenario: Feed intake limit validation (US-094-03)
        Given a breeding recipe configuration
        When an administrator attempts to set average daily feed intake to 12.5 kg (exceeding the 10.0 kg safety limit)
        Then the actual Odoo constrains '_check_daily_feed_intake' on 'agri.isl.livestock.recipe' must block the save
        And raise a ValidationError stating that the feed intake exceeds maximum safe threshold (10.0 kg).
        """
        # Create a base mrp.bom recipe
        base_recipe = self.env['mrp.bom'].create({
            'product_tmpl_id': self.product.product_tmpl_id.id,
            'product_qty': 1.0,
            'type': 'normal'
        })

        # Create physical ISL recipe and trigger the actual Odoo constrains
        with self.assertRaises(ValidationError) as context:
            self.env['agri.isl.livestock.recipe'].create({
                'recipe_id': base_recipe.id,
                'daily_feed_intake': 12.5 # Exceeds 10.0 kg safety limit!
            })

        self.assertIn("exceeds maximum safe threshold (10.0 kg)", str(context.exception))

    def test_03_veterinary_phi_withdrawal_period_biosecurity_block(self):
        """
        Scenario: Drug treatment, withdrawal, and biological safety check (US-094-05)
        Given a swine asset lot under withdrawal period (e.g. withdrawal end date set to tomorrow)
        When an operator calls 'action_check_harvest_safety' to verify delivery or slaughter suitability
        Then the actual Odoo method on 'agri.isl.lot.livestock' must identify the active PHI withdrawal period
        And raise a UserError blocking the harvest with message stating the lot is in PHI.
        """
        isl_lot = self.env['agri.isl.lot.livestock'].create({
            'lot_id': self.lot.id,
            'birth_date': fields.Date.today() - timedelta(days=400), # Mature
            'breeding_status': 'immature',
            'withdrawal_end_date': fields.Date.today() + timedelta(days=1) # Active PHI until tomorrow!
        })

        # Call the actual business logic method of the model
        with self.assertRaises(UserError) as context:
            isl_lot.action_check_harvest_safety()

        self.assertIn("is in PHI until", str(context.exception))
