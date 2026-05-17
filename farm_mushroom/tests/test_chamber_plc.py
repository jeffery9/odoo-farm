# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestChamberPlc(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.enoki = cls.env['product.product'].create({'name': 'Enoki Mushroom', 'type': 'product'})

    def test_01_plc_orchestration(self):
        """ Scenario 34: Edible Fungi Chamber Orchestration """
        mo = self.env['farm.mushroom.production'].create({
            'product_id': self.enoki.id,
            'product_qty': 500,
            'growth_phase': 'incubation'
        })
        
        mo.action_next_phase()
        self.assertEqual(mo.growth_phase, 'pinning')
        self.assertIn("Drop temp to 12C", mo.plc_status)
        
        mo.action_next_phase()
        self.assertEqual(mo.growth_phase, 'fruiting')
        self.assertIn("Raise temp to 18C", mo.plc_status)

