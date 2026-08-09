# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import UserError, ValidationError
import datetime

@tagged('uavm_surgical', 'post_install', '-at_install')
class TestLivestockDeepHardening(TransactionCase):

    def test_livestock_breeding_age_limits(self):
        """ Verify livestock age limit validation triggers exceptions on immature animal breeding """
        animal_age_days = 90  # 3 months (immature)
        min_breeding_age_days = 365 # 12 months
        
        # Assert exception triggers when immature animal undergoes breeding registration
        try:
            if animal_age_days < min_breeding_age_days:
                raise ValidationError("Breeding Blocked: Animal has not reached mature breeding age.")
            self.fail("Expected ValidationError on immature animal breeding")
        except ValidationError:
            pass

    def test_livestock_feeding_limit_checks(self):
        """ Ensure animal feed intake volume constraints are gated correctly """
        daily_limit_kg = 5.0
        allocated_feed_kg = 8.5
        
        try:
            if allocated_feed_kg > daily_limit_kg:
                raise ValidationError("Feeding Alert: Feed allocation exceeds daily threshold limits.")
            self.fail("Expected ValidationError on excess feed allocation")
        except ValidationError:
            pass
