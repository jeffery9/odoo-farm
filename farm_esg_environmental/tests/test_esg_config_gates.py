# -*- coding: utf-8 -*-
# filepath: odoo-farm-dev/farm_esg_environmental/tests/test_esg_config_gates.py
from odoo.tests.common import TransactionCase

class TestEsgConfigGates(TransactionCase):

    def setUp(self):
        super(TestEsgConfigGates, self).setUp()
        self.settings = self.env['res.config.settings'].create({})

    def test_esg_environmental_config_defaults(self):
        """ Verify ESG configuration default parameters and dynamic boolean evaluation """
        self.assertFalse(self.settings.group_enable_carbon_tracking, "Carbon tracking should be disabled by default")
        self.settings.write({
            'group_enable_carbon_tracking': True,
            'group_enable_circular_tracking': True
        })
        self.assertTrue(self.settings.group_enable_carbon_tracking, "Should allow turning on carbon tracking manually")
        self.assertTrue(self.settings.group_enable_circular_tracking, "Should allow turning on circular tracking manually")
