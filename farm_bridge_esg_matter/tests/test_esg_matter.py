# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestEsgMatterBridge(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        uom = cls.env['uom.uom'].search([], limit=1)
        factor = cls.env['agri.carbon.factor'].create({
            'name': 'Test Factor',
            'category': 'energy',
            'emission_factor': 1.5,
            'uom_id': uom.id,
        })
        cls.ledger = cls.env['agri.carbon.ledger'].create({
            'factor_id': factor.id,
            'quantity': 10.0,
        })
        
    def test_field_injection_and_saving(self):
        matter = self.env['stock.matter.tracking'].create({
            'name': 'LPN-ESG-TEST-001',
            'carbon_ledger_id': self.ledger.id,
        })
        self.assertEqual(matter.carbon_ledger_id.id, self.ledger.id)
