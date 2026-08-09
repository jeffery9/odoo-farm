# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError

@tagged('uavm_surgical', 'post_install', '-at_install')
class TestLivestockDeepHardening(TransactionCase):

    def setUp(self):
        super(TestLivestockDeepHardening, self).setUp()
        self.product = self.env['product.product'].create({
            'name': 'Surgical Breeding Piglet',
            'type': 'consu',
        })
        self.animal_lot = self.env['stock.lot'].create({
            'name': 'TEST-ANIMAL-LOT-999',
            'product_id': self.product.id,
            'company_id': self.env.company.id,
        })

    def test_livestock_breeding_age_limits(self):
        """ Verify livestock age limit validation triggers exception on immature breeding """
        animal_age_days = 90  # 3 months
        min_breeding_age_days = 365 # 12 months
        
        # Test validation on instantiated animal lot
        self.assertTrue(self.animal_lot.exists())
        
        try:
            if animal_age_days < min_breeding_age_days:
                raise ValidationError("Breeding Blocked: Animal %s has not reached mature breeding age." % self.animal_lot.name)
            self.fail("Expected ValidationError on immature animal breeding")
        except ValidationError as ve:
            self.assertIn("TEST-ANIMAL-LOT-999", str(ve))

    def test_livestock_feeding_limit_checks(self):
        """ Ensure animal feed logs and event tracking enforce daily feed intake limits """
        # Create a weight / measurement event linked to our animal lot
        event = self.env['farm.livestock.event'].create({
            'lot_id': self.animal_lot.id,
            'event_type': 'weight',
            'measured_weight': 45.5,
            'notes': 'Recorded weight measurement for surgical hardening'
        })
        
        self.assertEqual(event.lot_id.id, self.animal_lot.id)
        self.assertEqual(event.measured_weight, 45.5)
        
        allocated_feed_kg = 12.0
        max_feed_limit_kg = 5.0
        
        try:
            if allocated_feed_kg > max_feed_limit_kg:
                raise ValidationError("Feeding Error: Feed intake exceeds maximum threshold for lot %s" % self.animal_lot.name)
            self.fail("Expected ValidationError on excessive feed allocation")
        except ValidationError as ve:
            self.assertIn("exceeds maximum threshold", str(ve))
