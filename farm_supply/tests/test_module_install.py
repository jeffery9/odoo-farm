# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestFarmSupplyInstall(TransactionCase):
    def test_01_module_installed(self):
        """ Test that the farm_supply metadata module installs correctly """
        module = self.env['ir.module.module'].search([('name', '=', 'farm_supply')])
        self.assertTrue(module)
